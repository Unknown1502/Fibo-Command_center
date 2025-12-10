"""
API router for ControlNet integration.
Advanced composition control with edge detection, depth maps, and pose estimation.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from controlnet import controlnet_processor

logger = logging.getLogger(__name__)

router = APIRouter()


class ProcessControlRequest(BaseModel):
    """Request model for control image processing."""
    control_type: Literal['canny_edge', 'depth_map', 'normal_map', 'hed_edge', 'scribble', 'pose'] = Field(
        ...,
        description="Type of control processing to apply"
    )
    strength: float = Field(
        default=1.0,
        description="Control strength (0-1), higher = stronger influence",
        ge=0.0,
        le=1.0
    )
    sensitivity: Optional[Literal['low', 'medium', 'high']] = Field(
        default='medium',
        description="Edge detection sensitivity (for canny_edge)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "control_type": "canny_edge",
                "strength": 0.8,
                "sensitivity": "medium"
            }
        }


@router.post("/process")
async def process_control_image(
    file: UploadFile = File(..., description="Reference image to process"),
    control_type: str = Query(..., description="Control type"),
    strength: float = Query(default=1.0, description="Control strength (0-1)"),
    sensitivity: Optional[str] = Query(default='medium', description="Edge sensitivity")
):
    """
    Process a reference image to create a ControlNet control image.
    
    **Control Types:**
    - `canny_edge`: Precise edge detection for architecture, products
    - `depth_map`: Depth estimation for spatial control
    - `normal_map`: Surface normals for texture/lighting
    - `hed_edge`: Soft edges for natural scenes
    - `scribble`: Sketch-style control for conceptual designs
    - `pose`: Human pose detection for character control
    
    **Workflow:**
    1. Upload reference image
    2. Select control type based on use case
    3. Adjust strength (0-1) for influence level
    4. Download processed control image
    5. Use with FIBO generation + control parameters
    
    **Use Cases:**
    - Maintain specific composition from reference
    - Control spatial depth in generated images
    - Guide character poses from reference photos
    - Preserve architectural structures
    - Sketch-to-image workflows
    
    **Returns:**
    - Processed control image (PNG format)
    - Metadata with processing details
    """
    try:
        # Validate control type
        if control_type not in controlnet_processor.CONTROL_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid control type. Must be one of: {controlnet_processor.CONTROL_TYPES}"
            )
        
        # Read uploaded file
        image_data = await file.read()
        
        # Process control image
        processed_data, metadata = controlnet_processor.process_control_image(
            image_data=image_data,
            control_type=control_type,
            strength=strength,
            sensitivity=sensitivity
        )
        
        # Generate filename
        original_name = file.filename.rsplit('.', 1)[0] if file.filename else 'control'
        download_filename = f"{original_name}_{control_type}.png"
        
        # Return processed control image
        return Response(
            content=processed_data,
            media_type='image/png',
            headers={
                'Content-Disposition': f'attachment; filename="{download_filename}"',
                'X-Control-Metadata': str(metadata)
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Control image processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/types")
async def get_control_types():
    """
    Get available ControlNet control types with descriptions.
    
    **Returns:**
    - Dictionary of control types with use cases and parameters
    """
    return {
        "control_types": controlnet_processor.get_control_info(),
        "total": len(controlnet_processor.CONTROL_TYPES)
    }


@router.get("/examples")
async def get_examples():
    """
    Get example use cases for ControlNet integration.
    
    **Returns:**
    - Example workflows and recommended settings
    """
    return {
        "examples": [
            {
                "name": "Product Photography Consistency",
                "control_type": "canny_edge",
                "strength": 0.9,
                "sensitivity": "high",
                "use_case": "Maintain exact product shape across different backgrounds/lighting",
                "workflow": "1. Upload product photo, 2. Use canny_edge with high sensitivity, 3. Generate with different parameters"
            },
            {
                "name": "Portrait Pose Control",
                "control_type": "pose",
                "strength": 0.8,
                "use_case": "Generate portraits with specific pose from reference",
                "workflow": "1. Upload reference pose photo, 2. Use pose detection, 3. Generate with desired style"
            },
            {
                "name": "Architectural Preservation",
                "control_type": "canny_edge",
                "strength": 1.0,
                "sensitivity": "medium",
                "use_case": "Keep building structure while changing style/lighting",
                "workflow": "1. Upload building photo, 2. Canny edge detection, 3. Generate with different styles"
            },
            {
                "name": "Landscape Depth Control",
                "control_type": "depth_map",
                "strength": 0.7,
                "use_case": "Control spatial depth in landscape generation",
                "workflow": "1. Upload landscape reference, 2. Generate depth map, 3. Use for spatial consistency"
            },
            {
                "name": "Sketch to Image",
                "control_type": "scribble",
                "strength": 0.6,
                "use_case": "Convert rough sketches to finished images",
                "workflow": "1. Upload hand-drawn sketch, 2. Process as scribble, 3. Generate realistic image"
            },
            {
                "name": "Natural Scene Composition",
                "control_type": "hed_edge",
                "strength": 0.7,
                "use_case": "Preserve organic shapes and natural composition",
                "workflow": "1. Upload nature photo, 2. HED edge detection, 3. Generate with different seasons/times"
            }
        ]
    }


@router.get("/use-cases")
async def get_use_cases():
    """
    Get detailed use cases organized by industry/application.
    
    **Returns:**
    - Use cases categorized by industry with recommended settings
    """
    return {
        "use_cases": {
            "e_commerce": {
                "name": "E-Commerce Product Shots",
                "recommended_control": "canny_edge",
                "strength": 0.9,
                "description": "Maintain consistent product shape across lifestyle images",
                "benefits": ["Consistent branding", "Fast variant generation", "Cost savings"]
            },
            "fashion": {
                "name": "Fashion Photography",
                "recommended_control": "pose",
                "strength": 0.8,
                "description": "Control model poses while changing clothing/backgrounds",
                "benefits": ["Pose consistency", "Quick outfit variants", "Reduced photoshoot costs"]
            },
            "architecture": {
                "name": "Architectural Visualization",
                "recommended_control": "canny_edge",
                "strength": 1.0,
                "description": "Preserve building structure across different styles/seasons",
                "benefits": ["Design exploration", "Client presentations", "Seasonal variations"]
            },
            "game_development": {
                "name": "Game Asset Creation",
                "recommended_control": "normal_map",
                "strength": 0.8,
                "description": "Generate consistent 3D-aware textures and assets",
                "benefits": ["Asset variations", "PBR workflows", "Rapid prototyping"]
            },
            "concept_art": {
                "name": "Concept Art Development",
                "recommended_control": "scribble",
                "strength": 0.6,
                "description": "Transform rough sketches into detailed concept art",
                "benefits": ["Faster iteration", "Explore ideas", "Client presentations"]
            },
            "marketing": {
                "name": "Marketing Campaigns",
                "recommended_control": "depth_map",
                "strength": 0.7,
                "description": "Create depth-consistent marketing imagery across channels",
                "benefits": ["Brand consistency", "Multi-channel content", "A/B testing"]
            }
        }
    }


@router.get("/workflow-guide")
async def get_workflow_guide():
    """
    Get step-by-step workflow guide for ControlNet integration.
    
    **Returns:**
    - Detailed workflow instructions for beginners
    """
    return {
        "workflow": {
            "step_1": {
                "title": "Prepare Reference Image",
                "description": "Select or create a reference image that has the composition/structure you want",
                "tips": [
                    "High-resolution images work best (1024x1024+)",
                    "Clear, well-lit reference images produce better results",
                    "Consider cropping to focus on main subject"
                ]
            },
            "step_2": {
                "title": "Choose Control Type",
                "description": "Select the appropriate control type for your use case",
                "decision_tree": {
                    "precise_shapes": "canny_edge",
                    "human_figures": "pose",
                    "spatial_depth": "depth_map",
                    "rough_sketches": "scribble",
                    "natural_scenes": "hed_edge",
                    "3d_surfaces": "normal_map"
                }
            },
            "step_3": {
                "title": "Upload and Process",
                "description": "Upload your reference image and process it with selected control type",
                "parameters": {
                    "strength": "0.6-1.0 (higher = stronger control)",
                    "sensitivity": "low/medium/high (for edge detection)"
                }
            },
            "step_4": {
                "title": "Download Control Image",
                "description": "Save the processed control image for use with generation",
                "note": "Control image is a black/white or colored guide showing structure"
            },
            "step_5": {
                "title": "Generate with Control",
                "description": "Use the control image alongside your FIBO parameters",
                "workflow": [
                    "Set your desired FIBO parameters (lighting, style, etc.)",
                    "Reference the control image for composition guidance",
                    "Generate images that follow the control structure",
                    "Adjust strength if control is too strong/weak"
                ]
            },
            "step_6": {
                "title": "Iterate and Refine",
                "description": "Fine-tune strength and parameters for optimal results",
                "tips": [
                    "Lower strength for more creative freedom",
                    "Higher strength for precise reproduction",
                    "Try different FIBO parameters with same control",
                    "Use A/B testing to find best combination"
                ]
            }
        }
    }
