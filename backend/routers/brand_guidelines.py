"""
API router for Brand Guidelines system.
Create, manage, and enforce brand identity across image generations.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from brand_guidelines import brand_manager

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateGuidelineRequest(BaseModel):
    """Request model for creating a brand guideline."""
    brand_id: str = Field(..., description="Unique brand identifier")
    name: str = Field(..., description="Brand name")
    colors: Optional[List[str]] = Field(default=None, description="Brand colors (hex codes)")
    fonts: Optional[List[str]] = Field(default=None, description="Brand fonts")
    styles: Optional[List[str]] = Field(default=None, description="Allowed visual styles")
    rules: Optional[Dict[str, Any]] = Field(default=None, description="Custom brand rules")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "brand_id": "acme_corp",
                "name": "ACME Corporation",
                "colors": ["#FF6B35", "#004E89", "#F7F7F7"],
                "fonts": ["Montserrat", "Open Sans"],
                "styles": ["minimalist", "realistic"],
                "rules": {
                    "allowed_color_palettes": ["neutral", "muted"],
                    "lighting": {"forbidden": ["hard"]},
                    "composition": {"required": "rule_of_thirds"}
                }
            }
        }


class UpdateGuidelineRequest(BaseModel):
    """Request model for updating a brand guideline."""
    name: Optional[str] = None
    colors: Optional[List[str]] = None
    fonts: Optional[List[str]] = None
    styles: Optional[List[str]] = None
    rules: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class ValidateGenerationRequest(BaseModel):
    """Request model for validating generation against brand guidelines."""
    brand_id: str
    parameters: Dict[str, Any]
    image_analysis: Optional[Dict[str, Any]] = None


@router.post("/guidelines")
async def create_guideline(request: CreateGuidelineRequest):
    """
    Create a new brand guideline profile.
    
    **Use Cases:**
    - Define brand colors, fonts, and visual styles
    - Set approval rules for automated validation
    - Ensure consistency across all brand content
    - Store per-project visual identity
    
    **Returns:**
    - Created brand guideline with unique ID
    """
    try:
        guideline = brand_manager.create_guideline(
            brand_id=request.brand_id,
            name=request.name,
            colors=request.colors,
            fonts=request.fonts,
            styles=request.styles,
            rules=request.rules,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "guideline": guideline.to_dict(),
            "message": f"Brand guideline '{request.name}' created successfully"
        }
    except Exception as e:
        logger.error(f"Failed to create guideline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/guidelines")
async def list_guidelines():
    """
    List all stored brand guidelines.
    
    **Returns:**
    - List of all brand guidelines with summary information
    """
    return {
        "guidelines": brand_manager.list_guidelines(),
        "total": len(brand_manager.guidelines)
    }


@router.get("/guidelines/{brand_id}")
async def get_guideline(brand_id: str):
    """
    Get a specific brand guideline by ID.
    
    **Returns:**
    - Complete brand guideline details
    """
    guideline = brand_manager.get_guideline(brand_id)
    if not guideline:
        raise HTTPException(status_code=404, detail=f"Brand guideline not found: {brand_id}")
    
    return {
        "guideline": guideline.to_dict()
    }


@router.patch("/guidelines/{brand_id}")
async def update_guideline(brand_id: str, request: UpdateGuidelineRequest):
    """
    Update an existing brand guideline.
    
    **Returns:**
    - Updated brand guideline
    """
    updates = request.model_dump(exclude_unset=True)
    guideline = brand_manager.update_guideline(brand_id, **updates)
    
    if not guideline:
        raise HTTPException(status_code=404, detail=f"Brand guideline not found: {brand_id}")
    
    return {
        "success": True,
        "guideline": guideline.to_dict(),
        "message": f"Brand guideline updated successfully"
    }


@router.delete("/guidelines/{brand_id}")
async def delete_guideline(brand_id: str):
    """
    Delete a brand guideline.
    
    **Returns:**
    - Success confirmation
    """
    success = brand_manager.delete_guideline(brand_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Brand guideline not found: {brand_id}")
    
    return {
        "success": True,
        "message": f"Brand guideline deleted successfully"
    }


@router.post("/validate")
async def validate_generation(request: ValidateGenerationRequest):
    """
    Validate generation parameters against brand guidelines.
    
    **Use Cases:**
    - Pre-flight check before generating images
    - Automated brand compliance scoring
    - Rejection/approval workflow
    - Quality assurance for brand consistency
    
    **Returns:**
    - Compliance score (0-100)
    - List of violations and warnings
    - Suggestions for compliance
    - Pass/fail status
    """
    try:
        result = brand_manager.validate_generation(
            brand_id=request.brand_id,
            parameters=request.parameters,
            image_analysis=request.image_analysis
        )
        
        return result
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/parse-document")
async def parse_document(file: UploadFile = File(..., description="Brand guideline document")):
    """
    Parse a brand guideline document to extract rules.
    
    **Supported Formats:**
    - Text files (.txt)
    - (Future: PDF, DOCX with proper parsers)
    
    **Returns:**
    - Extracted colors, fonts, styles, and rules
    """
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        parsed = brand_manager.parse_document(text)
        
        return {
            "success": True,
            "parsed": parsed,
            "message": "Document parsed successfully",
            "note": "Review and adjust parsed values before creating guideline"
        }
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be text format (UTF-8)")
    except Exception as e:
        logger.error(f"Document parsing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_examples():
    """
    Get example brand guidelines for common use cases.
    
    **Returns:**
    - Example guidelines for different industries
    """
    return {
        "examples": [
            {
                "name": "Tech Startup",
                "brand_id": "tech_startup_example",
                "colors": ["#00D9FF", "#0A0E27", "#F8F9FA"],
                "styles": ["minimalist", "realistic"],
                "rules": {
                    "allowed_color_palettes": ["vibrant", "neutral"],
                    "composition": {"required": "rule_of_thirds"}
                }
            },
            {
                "name": "Luxury Fashion",
                "brand_id": "luxury_fashion_example",
                "colors": ["#000000", "#FFFFFF", "#C9B037"],
                "styles": ["cinematic", "artistic"],
                "rules": {
                    "allowed_color_palettes": ["monochrome", "muted"],
                    "lighting": {"forbidden": ["hard"]},
                    "composition": {"required": "symmetrical"}
                }
            },
            {
                "name": "Eco-Friendly Brand",
                "brand_id": "eco_brand_example",
                "colors": ["#2D5016", "#88AB75", "#E8DDB5"],
                "styles": ["realistic", "vintage"],
                "rules": {
                    "allowed_color_palettes": ["neutral", "pastel"],
                    "lighting": {"preferred": ["soft", "golden_hour"]}
                }
            }
        ]
    }
