"""
Generation API Router
Handles image generation requests
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
import hashlib
import json
import asyncio

from fibo_integration import fibo_integration
from fibo_agent import fibo_agent
from database import get_db, Generation
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple in-memory cache for generation results (TTL: 1 hour)
generation_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = timedelta(hours=1)


def _generate_cache_key(request: "GenerationRequest") -> str:
    """Generate a unique cache key for a generation request"""
    key_data = {
        "prompt": request.prompt,
        "mode": request.mode,
        "camera_angle": request.camera_angle,
        "fov": request.fov,
        "lighting": request.lighting,
        "color_palette": request.color_palette,
        "composition": request.composition,
        "style": request.style
    }
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_str.encode()).hexdigest()


def _get_cached_result(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached result if it exists and hasn't expired"""
    if cache_key in generation_cache:
        cached = generation_cache[cache_key]
        if datetime.utcnow() - cached['timestamp'] < CACHE_TTL:
            logger.info(f"Cache hit for key: {cache_key}")
            return cached['data']
        else:
            # Expired, remove from cache
            del generation_cache[cache_key]
            logger.info(f"Cache expired for key: {cache_key}")
    return None


def _cache_result(cache_key: str, data: Dict[str, Any]):
    """Cache a generation result"""
    generation_cache[cache_key] = {
        'data': data,
        'timestamp': datetime.utcnow()
    }
    logger.info(f"Cached result for key: {cache_key}")


def _calculate_quality_score(parameters: Dict[str, Any], result: Dict[str, Any]) -> float:
    """Calculate quality score based on parameter completeness and generation success"""
    score = 0.5  # Base score
    
    # Bonus for complete parameters
    param_count = sum(1 for v in parameters.values() if v is not None)
    score += min(param_count * 0.05, 0.3)
    
    # Bonus if image was successfully generated
    if result.get('image_url'):
        score += 0.2
    
    # Cap at 1.0
    return min(score, 1.0)


class GenerationRequest(BaseModel):
    """Request model for image generation"""
    prompt: str = Field(..., description="Description of desired image", min_length=3, max_length=2000)
    mode: str = Field(default="ai", description="Generation mode: 'ai' or 'manual'")
    camera_angle: Optional[str] = Field(None, description="Camera angle")
    fov: Optional[str] = Field(None, description="Field of view")
    lighting: Optional[str] = Field(None, description="Lighting type")
    color_palette: Optional[str] = Field(None, description="Color palette")
    composition: Optional[str] = Field(None, description="Composition style")
    style: Optional[str] = Field(None, description="Visual style")
    project_id: Optional[int] = Field(None, description="Associated project ID")
    user_id: int = Field(default=1, description="User ID")
    use_cache: bool = Field(default=True, description="Use cached results if available")
    max_retries: int = Field(default=3, description="Maximum retry attempts", ge=0, le=5)
    
    @validator('mode')
    def validate_mode(cls, v):
        if v not in ['ai', 'manual']:
            raise ValueError('mode must be "ai" or "manual"')
        return v
    
    @validator('camera_angle')
    def validate_camera_angle(cls, v):
        if v and v not in ['eye-level', 'low-angle', 'high-angle', 'dutch-tilt', 'bird\'s-eye']:
            raise ValueError(f'Invalid camera_angle: {v}')
        return v
    
    @validator('fov')
    def validate_fov(cls, v):
        if v and v not in ['wide', 'standard', 'telephoto']:
            raise ValueError(f'Invalid fov: {v}')
        return v
    
    @validator('lighting')
    def validate_lighting(cls, v):
        if v and v not in ['natural', 'studio', 'dramatic', 'golden-hour', 'soft', 'hard']:
            raise ValueError(f'Invalid lighting: {v}')
        return v
    
    @validator('color_palette')
    def validate_color_palette(cls, v):
        if v and v not in ['vibrant', 'pastel', 'monochrome', 'warm', 'cool', 'neon']:
            raise ValueError(f'Invalid color_palette: {v}')
        return v
    
    @validator('composition')
    def validate_composition(cls, v):
        if v and v not in ['rule-of-thirds', 'centered', 'dynamic', 'minimal']:
            raise ValueError(f'Invalid composition: {v}')
        return v
    
    @validator('style')
    def validate_style(cls, v):
        if v and v not in ['photorealistic', 'cinematic', 'editorial', 'commercial']:
            raise ValueError(f'Invalid style: {v}')
        return v


class GenerationResponse(BaseModel):
    """Response model for image generation"""
    id: int
    status: str
    image_url: Optional[str]
    parameters: Dict[str, Any]
    quality_score: Optional[float]
    generation_time: Optional[float]
    reasoning: Optional[Dict[str, Any]]
    cached: bool = False
    retry_count: int = 0


class BatchGenerationRequest(BaseModel):
    """Request model for batch image generation"""
    requests: List[GenerationRequest] = Field(..., description="List of generation requests", min_items=1, max_items=50)
    parallel: bool = Field(default=True, description="Generate in parallel or sequential")
    continue_on_error: bool = Field(default=True, description="Continue processing if one generation fails")


class BatchGenerationResponse(BaseModel):
    """Response model for batch generation"""
    total: int
    successful: int
    failed: int
    results: List[Optional[GenerationResponse]]
    errors: List[Optional[str]]


@router.post("/", response_model=GenerationResponse)
async def generate_image(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate an image using FIBO
    
    - **prompt**: Description of what you want to generate
    - **mode**: 'ai' for automatic parameter selection, 'manual' for explicit control
    - **camera_angle**: Camera angle (if mode='manual')
    - **fov**: Field of view (if mode='manual')
    - **lighting**: Lighting type (if mode='manual')
    - **color_palette**: Color palette (if mode='manual')
    - **composition**: Composition style (if mode='manual')
    - **style**: Visual style (if mode='manual')
    """
    try:
        start_time = datetime.utcnow()
        logger.info(f"Generation request: {request.prompt} (mode: {request.mode})")
        
        # Check cache first
        cache_key = _generate_cache_key(request)
        cached_result = None
        if request.use_cache:
            cached_result = _get_cached_result(cache_key)
        
        if cached_result:
            # Return cached result
            logger.info("Returning cached generation result")
            return GenerationResponse(
                **cached_result,
                cached=True
            )
        
        # Create database record
        generation = Generation(
            user_id=request.user_id,
            project_id=request.project_id,
            prompt=request.prompt,
            mode=request.mode,
            status="processing"
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        
        # Determine parameters based on mode
        if request.mode == "ai":
            # Use AI agent to analyze intent and suggest parameters
            logger.info("Using AI mode - analyzing intent...")
            try:
                intent_analysis = await fibo_agent.analyze_intent(request.prompt)
                params = intent_analysis.get("parameters", {})
                reasoning = intent_analysis.get("reasoning", {})
            except Exception as e:
                # Fallback to smart defaults if OpenAI fails (quota exceeded, etc.)
                logger.warning(f"AI analysis failed, using smart defaults: {str(e)}")
                params = {
                    "prompt": request.prompt,
                    "camera_angle": "eye-level",
                    "fov": "standard",
                    "lighting": "studio",
                    "color_palette": "vibrant",
                    "composition": "rule-of-thirds",
                    "style": "photorealistic"
                }
                reasoning = {"note": "Using optimized defaults (AI unavailable)"}
            
            # Generate with AI-suggested parameters (with retry logic)
            retry_count = 0
            last_error = None
            result = None
            
            for attempt in range(request.max_retries + 1):
                try:
                    result = await fibo_integration.generate(
                        prompt=params.get("prompt", request.prompt),
                        camera_angle=params.get("camera_angle"),
                        fov=params.get("fov"),
                        lighting=params.get("lighting"),
                        color_palette=params.get("color_palette"),
                        composition=params.get("composition"),
                        style=params.get("style")
                    )
                    break  # Success!
                except Exception as e:
                    last_error = e
                    retry_count = attempt + 1
                    if attempt < request.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Generation attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"All {request.max_retries + 1} generation attempts failed")
                        raise last_error
        else:
            # Manual mode - use provided parameters (with retry logic)
            logger.info("Using manual mode - explicit parameters")
            retry_count = 0
            last_error = None
            result = None
            
            for attempt in range(request.max_retries + 1):
                try:
                    result = await fibo_integration.generate(
                        prompt=request.prompt,
                        camera_angle=request.camera_angle,
                        fov=request.fov,
                        lighting=request.lighting,
                        color_palette=request.color_palette,
                        composition=request.composition,
                        style=request.style
                    )
                    break  # Success!
                except Exception as e:
                    last_error = e
                    retry_count = attempt + 1
                    if attempt < request.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Generation attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"All {request.max_retries + 1} generation attempts failed")
                        raise last_error
            
            reasoning = None
        
        # Calculate generation time
        end_time = datetime.utcnow()
        generation_time = (end_time - start_time).total_seconds()
        
        # Calculate quality score
        quality_score = _calculate_quality_score(result.get("parameters", {}), result)
        
        # Update database record
        generation.status = "completed"
        generation.result_url = result.get("image_url")
        generation.parameters = result.get("parameters")
        generation.generation_time = generation_time
        generation.quality_score = quality_score
        generation.completed_at = end_time
        db.commit()
        
        logger.info(f"Generation completed in {generation_time:.2f}s (quality: {quality_score:.2f}, retries: {retry_count})")
        
        # Create response
        response_data = {
            "id": generation.id,
            "status": "completed",
            "image_url": result.get("image_url"),
            "parameters": result.get("parameters"),
            "quality_score": quality_score,
            "generation_time": generation_time,
            "reasoning": reasoning,
            "retry_count": retry_count
        }
        
        # Cache the result
        if request.use_cache:
            _cache_result(cache_key, response_data)
        
        return GenerationResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        
        # Update database with error
        if 'generation' in locals():
            generation.status = "failed"
            generation.error_message = str(e)
            db.commit()
        
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/parameters")
async def get_parameters():
    """
    Get all available FIBO parameters and their options
    """
    return {
        "parameters": fibo_integration.get_parameter_options(),
        "modes": ["ai", "manual"],
        "description": "Use 'ai' mode for automatic parameter selection or 'manual' for explicit control"
    }


@router.get("/{generation_id}")
async def get_generation(
    generation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific generation
    """
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return {
        "id": generation.id,
        "prompt": generation.prompt,
        "mode": generation.mode,
        "status": generation.status,
        "result_url": generation.result_url,
        "parameters": generation.parameters,
        "quality_score": generation.quality_score,
        "generation_time": generation.generation_time,
        "created_at": generation.created_at,
        "completed_at": generation.completed_at,
        "error_message": generation.error_message
    }


@router.post("/{generation_id}/refine")
async def refine_generation(
    generation_id: int,
    refinement_prompt: str,
    db: Session = Depends(get_db)
):
    """
    Refine an existing generation with modifications
    """
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    if not generation.result_url:
        raise HTTPException(status_code=400, detail="No image to refine")
    
    try:
        # Use agent to determine refinement parameters
        optimization = await fibo_agent.optimize_parameters(
            generation.parameters,
            refinement_prompt,
            generation.quality_score
        )
        
        # Refine the image
        result = await fibo_integration.refine(
            generation.result_url,
            optimization.get("parameters", {})
        )
        
        # Create new generation record for refined version
        refined_generation = Generation(
            user_id=generation.user_id,
            project_id=generation.project_id,
            prompt=f"{generation.prompt} (refined: {refinement_prompt})",
            mode="ai",
            status="completed",
            result_url=result.get("image_url"),
            parameters=result.get("parameters"),
            completed_at=datetime.utcnow()
        )
        db.add(refined_generation)
        db.commit()
        db.refresh(refined_generation)
        
        return {
            "id": refined_generation.id,
            "status": "completed",
            "image_url": result.get("image_url"),
            "parameters": result.get("parameters")
        }
        
    except Exception as e:
        logger.error(f"Refinement failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")


@router.post("/batch", response_model=BatchGenerationResponse)
async def batch_generate_images(
    request: BatchGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate multiple images in batch
    
    - **requests**: List of generation requests (max 50)
    - **parallel**: Generate in parallel (faster) or sequential (safer)
    - **continue_on_error**: Continue processing if one generation fails
    """
    logger.info(f"Batch generation request: {len(request.requests)} images")
    
    results = []
    errors = []
    successful = 0
    failed = 0
    
    async def process_single_generation(gen_request: GenerationRequest, index: int):
        """Process a single generation request"""
        try:
            result = await generate_image(gen_request, background_tasks, db)
            return (index, result, None)
        except Exception as e:
            error_msg = f"Generation {index + 1} failed: {str(e)}"
            logger.error(error_msg)
            if not request.continue_on_error:
                raise
            return (index, None, error_msg)
    
    try:
        if request.parallel:
            # Generate all images in parallel
            tasks = [
                process_single_generation(gen_request, i)
                for i, gen_request in enumerate(request.requests)
            ]
            completed = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for item in completed:
                if isinstance(item, Exception):
                    failed += 1
                    errors.append(str(item))
                    results.append(None)
                else:
                    index, result, error = item
                    if result:
                        successful += 1
                        results.append(result)
                        errors.append(None)
                    else:
                        failed += 1
                        results.append(None)
                        errors.append(error)
        else:
            # Generate sequentially
            for i, gen_request in enumerate(request.requests):
                try:
                    result = await generate_image(gen_request, background_tasks, db)
                    successful += 1
                    results.append(result)
                    errors.append(None)
                except Exception as e:
                    error_msg = f"Generation {i + 1} failed: {str(e)}"
                    logger.error(error_msg)
                    failed += 1
                    results.append(None)
                    errors.append(error_msg)
                    
                    if not request.continue_on_error:
                        raise HTTPException(status_code=500, detail=error_msg)
        
        logger.info(f"Batch generation completed: {successful} successful, {failed} failed")
        
        return BatchGenerationResponse(
            total=len(request.requests),
            successful=successful,
            failed=failed,
            results=results,
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch generation failed: {str(e)}")


@router.get("/history")
async def get_generation_history(
    user_id: int = 1,
    project_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get generation history for a user
    
    - **user_id**: User ID to fetch history for
    - **project_id**: Optional project ID to filter by
    - **limit**: Maximum number of results (default 50, max 200)
    - **offset**: Number of results to skip
    - **status**: Filter by status (pending, processing, completed, failed)
    """
    limit = min(limit, 200)  # Cap at 200
    
    query = db.query(Generation).filter(Generation.user_id == user_id)
    
    if project_id:
        query = query.filter(Generation.project_id == project_id)
    
    if status:
        query = query.filter(Generation.status == status)
    
    # Order by most recent first
    query = query.order_by(Generation.created_at.desc())
    
    total = query.count()
    generations = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": [
            {
                "id": gen.id,
                "prompt": gen.prompt,
                "mode": gen.mode,
                "status": gen.status,
                "result_url": gen.result_url,
                "parameters": gen.parameters,
                "quality_score": gen.quality_score,
                "generation_time": gen.generation_time,
                "created_at": gen.created_at,
                "completed_at": gen.completed_at,
                "error_message": gen.error_message
            }
            for gen in generations
        ]
    }


@router.get("/statistics")
async def get_generation_statistics(
    user_id: int = 1,
    project_id: Optional[int] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get generation statistics for a user
    
    - **user_id**: User ID to get statistics for
    - **project_id**: Optional project ID to filter by
    - **days**: Number of days to include (default 30)
    """
    from sqlalchemy import func
    
    # Calculate date threshold
    since_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(Generation).filter(
        Generation.user_id == user_id,
        Generation.created_at >= since_date
    )
    
    if project_id:
        query = query.filter(Generation.project_id == project_id)
    
    total_generations = query.count()
    
    # Status breakdown
    status_counts = db.query(
        Generation.status,
        func.count(Generation.id)
    ).filter(
        Generation.user_id == user_id,
        Generation.created_at >= since_date
    )
    
    if project_id:
        status_counts = status_counts.filter(Generation.project_id == project_id)
    
    status_counts = status_counts.group_by(Generation.status).all()
    
    # Mode breakdown
    mode_counts = db.query(
        Generation.mode,
        func.count(Generation.id)
    ).filter(
        Generation.user_id == user_id,
        Generation.created_at >= since_date
    )
    
    if project_id:
        mode_counts = mode_counts.filter(Generation.project_id == project_id)
    
    mode_counts = mode_counts.group_by(Generation.mode).all()
    
    # Average metrics
    completed_query = query.filter(Generation.status == "completed")
    
    avg_generation_time = db.query(
        func.avg(Generation.generation_time)
    ).filter(
        Generation.user_id == user_id,
        Generation.status == "completed",
        Generation.created_at >= since_date
    )
    
    if project_id:
        avg_generation_time = avg_generation_time.filter(Generation.project_id == project_id)
    
    avg_generation_time = avg_generation_time.scalar() or 0
    
    avg_quality_score = db.query(
        func.avg(Generation.quality_score)
    ).filter(
        Generation.user_id == user_id,
        Generation.status == "completed",
        Generation.created_at >= since_date
    )
    
    if project_id:
        avg_quality_score = avg_quality_score.filter(Generation.project_id == project_id)
    
    avg_quality_score = avg_quality_score.scalar() or 0
    
    return {
        "period_days": days,
        "total_generations": total_generations,
        "status_breakdown": {status: count for status, count in status_counts},
        "mode_breakdown": {mode: count for mode, count in mode_counts},
        "average_generation_time": round(avg_generation_time, 2),
        "average_quality_score": round(avg_quality_score, 2),
        "success_rate": round(
            (dict(status_counts).get("completed", 0) / total_generations * 100) if total_generations > 0 else 0,
            2
        )
    }


@router.delete("/cache")
async def clear_cache():
    """
    Clear the generation cache
    """
    cache_size = len(generation_cache)
    generation_cache.clear()
    logger.info(f"Cleared {cache_size} cached generations")
    
    return {
        "status": "success",
        "cleared": cache_size,
        "message": f"Cleared {cache_size} cached generation(s)"
    }


@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics
    """
    total_cached = len(generation_cache)
    
    # Count expired vs valid
    now = datetime.utcnow()
    expired = sum(1 for cached in generation_cache.values() if now - cached['timestamp'] >= CACHE_TTL)
    valid = total_cached - expired
    
    return {
        "total_cached": total_cached,
        "valid": valid,
        "expired": expired,
        "ttl_hours": CACHE_TTL.total_seconds() / 3600
    }
