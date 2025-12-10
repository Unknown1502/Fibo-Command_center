"""
AI Prompt Translation API Router
Natural language to FIBO JSON conversion
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging

from prompt_translator import prompt_translator

logger = logging.getLogger(__name__)

router = APIRouter()


class TranslationRequest(BaseModel):
    """Request model for prompt translation"""
    prompt: str = Field(
        ...,
        description="Natural language description of desired image",
        min_length=5,
        max_length=1000,
        example="I need dramatic product photos of a watch that look expensive and cinematic"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional context (product type, brand, industry)",
        example={"product_type": "watch", "brand": "luxury", "use_case": "e-commerce"}
    )


class TranslationResponse(BaseModel):
    """Response model for translation"""
    intent: str = Field(..., description="Identified user intent")
    mood: str = Field(..., description="Emotional/aesthetic goal")
    parameters: Dict[str, Any] = Field(..., description="FIBO parameters")
    reasoning: Dict[str, str] = Field(..., description="Parameter reasoning")
    confidence: float = Field(..., description="Confidence score (0-1)")
    suggestions: list = Field(..., description="Alternative suggestions")
    fallback: Optional[bool] = Field(None, description="Whether fallback was used")


@router.post("/translate", response_model=TranslationResponse)
async def translate_prompt(request: TranslationRequest):
    """
    Translate natural language to FIBO parameters
    
    This endpoint uses GPT-4 to intelligently convert conversational descriptions
    into optimized FIBO JSON parameters. Perfect for:
    
    - **Non-technical users**: Describe what you want in plain English
    - **Learning FIBO**: See how pros structure parameters
    - **Optimization**: Get expert-level parameter selections
    - **Exploration**: Receive alternative suggestions to try
    
    Example transformations:
    - "Make it look like a magazine cover" → high-angle, editorial, vibrant
    - "Dark and moody fantasy scene" → low-angle, dramatic, cool palette
    - "Bright e-commerce shot" → eye-level, studio, vibrant
    
    Returns detailed reasoning for each parameter choice and alternative suggestions.
    """
    try:
        logger.info(f"Translating prompt: {request.prompt[:100]}...")
        
        result = await prompt_translator.translate(
            user_prompt=request.prompt,
            context=request.context
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


@router.get("/examples")
async def get_translation_examples():
    """
    Get example translations to demonstrate capability
    """
    return {
        "examples": [
            {
                "input": "dramatic luxury watch commercial",
                "output": {
                    "camera_angle": "low-angle",
                    "fov": "telephoto",
                    "lighting": "dramatic",
                    "color_palette": "monochrome",
                    "composition": "centered",
                    "style": "cinematic"
                },
                "reasoning": "Low angle for prestige, telephoto for compression, dramatic lighting for depth, monochrome for timeless elegance"
            },
            {
                "input": "bright cheerful summer beach collection",
                "output": {
                    "camera_angle": "eye-level",
                    "fov": "wide",
                    "lighting": "golden-hour",
                    "color_palette": "vibrant",
                    "composition": "dynamic",
                    "style": "editorial"
                },
                "reasoning": "Eye-level for relatability, wide for environment, golden-hour for warmth, vibrant for energy"
            },
            {
                "input": "professional clean product photography",
                "output": {
                    "camera_angle": "eye-level",
                    "fov": "standard",
                    "lighting": "studio",
                    "color_palette": "vibrant",
                    "composition": "centered",
                    "style": "commercial"
                },
                "reasoning": "Eye-level neutral view, studio lighting for clarity, centered for product focus"
            },
            {
                "input": "epic fantasy game character art",
                "output": {
                    "camera_angle": "low-angle",
                    "fov": "wide",
                    "lighting": "dramatic",
                    "color_palette": "cool",
                    "composition": "dynamic",
                    "style": "artistic"
                },
                "reasoning": "Low angle for hero shot, wide for epic scale, dramatic for atmosphere, cool for fantasy mood"
            },
            {
                "input": "minimalist modern architecture magazine",
                "output": {
                    "camera_angle": "eye-level",
                    "fov": "wide",
                    "lighting": "soft",
                    "color_palette": "monochrome",
                    "composition": "minimal",
                    "style": "editorial"
                },
                "reasoning": "Eye-level for clean lines, wide for space, soft for even tones, monochrome for sophistication"
            }
        ]
    }


@router.get("/parameter-guide")
async def get_parameter_guide():
    """
    Get comprehensive FIBO parameter guide
    Educational resource for understanding each parameter's impact
    """
    return {
        "camera_angle": {
            "description": "Camera perspective relative to subject",
            "options": {
                "eye-level": {
                    "description": "Camera at subject's height",
                    "effect": "Neutral, natural perspective",
                    "best_for": "Documentary, realism, balanced shots",
                    "psychology": "Equality, relatability, honesty"
                },
                "low-angle": {
                    "description": "Camera looking up at subject",
                    "effect": "Subject appears larger, more powerful",
                    "best_for": "Hero shots, authority, grandeur",
                    "psychology": "Power, dominance, respect"
                },
                "high-angle": {
                    "description": "Camera looking down at subject",
                    "effect": "Subject appears smaller, vulnerable",
                    "best_for": "Overview, context, intimacy",
                    "psychology": "Vulnerability, submission, overview"
                },
                "dutch-tilt": {
                    "description": "Tilted horizon line",
                    "effect": "Creates tension and energy",
                    "best_for": "Action, unease, dynamic shots",
                    "psychology": "Instability, chaos, energy"
                },
                "bird's-eye": {
                    "description": "Directly from above",
                    "effect": "Flattens perspective, shows patterns",
                    "best_for": "Maps, layouts, overhead views",
                    "psychology": "God's eye, detachment, planning"
                }
            }
        },
        "fov": {
            "description": "Field of view - how much of the scene is captured",
            "options": {
                "wide": {
                    "description": "Broad view (24-35mm equivalent)",
                    "effect": "Environmental context, perspective distortion",
                    "best_for": "Architecture, landscapes, interiors",
                    "characteristics": "Dramatic depth, spatial awareness"
                },
                "standard": {
                    "description": "Natural vision (40-60mm equivalent)",
                    "effect": "Balanced, realistic perspective",
                    "best_for": "Portraits, products, general purpose",
                    "characteristics": "Natural, comfortable, versatile"
                },
                "telephoto": {
                    "description": "Narrow view (85mm+ equivalent)",
                    "effect": "Compressed perspective, isolates subject",
                    "best_for": "Portraits, details, cinematic shots",
                    "characteristics": "Shallow depth, compression, intimacy"
                }
            }
        },
        "lighting": {
            "description": "Light quality and direction",
            "options": {
                "natural": {
                    "description": "Realistic daylight",
                    "mood": "Authentic, documentary",
                    "best_for": "Realism, outdoor scenes",
                    "quality": "Variable, realistic shadows"
                },
                "studio": {
                    "description": "Controlled, even lighting",
                    "mood": "Professional, clean",
                    "best_for": "Product photography, controlled environments",
                    "quality": "Even, minimal shadows"
                },
                "dramatic": {
                    "description": "High contrast, defined shadows",
                    "mood": "Moody, cinematic, intense",
                    "best_for": "Film noir, atmosphere, emotion",
                    "quality": "High contrast, deep shadows"
                },
                "golden-hour": {
                    "description": "Warm sunset/sunrise light",
                    "mood": "Romantic, beautiful, nostalgic",
                    "best_for": "Lifestyle, portraits, dreamy scenes",
                    "quality": "Warm tones, soft shadows"
                },
                "soft": {
                    "description": "Diffused, gentle light",
                    "mood": "Gentle, flattering, peaceful",
                    "best_for": "Beauty, portraits, delicate subjects",
                    "quality": "Minimal shadows, even tones"
                },
                "hard": {
                    "description": "Direct, sharp shadows",
                    "mood": "Edgy, graphic, bold",
                    "best_for": "Fashion, graphic design, contrast",
                    "quality": "Sharp shadows, high definition"
                }
            }
        }
    }
