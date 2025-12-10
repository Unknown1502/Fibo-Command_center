"""
API router for professional image processing.
Handles HDR tone mapping, color space conversion, and format export.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from image_processor import image_processor

logger = logging.getLogger(__name__)

router = APIRouter()


class ProcessImageRequest(BaseModel):
    """Request model for image processing."""
    output_format: Literal['tiff', 'exr', 'png', 'webp'] = Field(
        default='png',
        description="Output image format"
    )
    bit_depth: int = Field(
        default=16,
        description="Color bit depth (8, 16, or 32)",
        ge=8,
        le=32
    )
    color_space: Literal['srgb', 'rec2020', 'dci_p3', 'adobe_rgb'] = Field(
        default='srgb',
        description="Target color space"
    )
    tone_mapping: Literal['reinhard', 'filmic', 'aces', 'uncharted2', 'none'] = Field(
        default='none',
        description="HDR tone mapping algorithm"
    )
    preset: Optional[str] = Field(
        default=None,
        description="Quick preset (overrides other settings): web, print, film_tv, cinema, games"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "output_format": "tiff",
                "bit_depth": 16,
                "color_space": "adobe_rgb",
                "tone_mapping": "aces",
                "preset": None
            }
        }


class ProcessImageResponse(BaseModel):
    """Response model for image processing."""
    success: bool
    message: str
    metadata: Dict[str, Any]
    download_filename: str


@router.post("/process", response_model=ProcessImageResponse)
async def process_image(
    file: UploadFile = File(..., description="Image file to process"),
    output_format: str = Query(default='png', description="Output format"),
    bit_depth: int = Query(default=16, description="Bit depth"),
    color_space: str = Query(default='srgb', description="Color space"),
    tone_mapping: str = Query(default='none', description="Tone mapping"),
    preset: Optional[str] = Query(default=None, description="Quick preset"),
    quality: Optional[int] = Query(default=90, description="Quality for WebP (0-100)"),
    compression: Optional[str] = Query(default='lzw', description="Compression for TIFF")
):
    """
    Process an uploaded image with HDR tone mapping and export to professional format.
    
    **Use Cases:**
    - Convert to 16-bit for print production
    - Apply HDR tone mapping for cinematic look
    - Export to wide gamut color spaces (Rec.2020, DCI-P3)
    - Create game-ready assets with proper tone mapping
    
    **Presets:**
    - `web`: WebP, 8-bit, sRGB (optimized for web)
    - `print`: TIFF, 16-bit, Adobe RGB (magazine/poster quality)
    - `film_tv`: TIFF, 16-bit, Rec.2020, ACES (broadcast quality)
    - `cinema`: EXR, 32-bit, DCI-P3 (theater projection)
    - `games`: PNG, 8-bit, sRGB, Uncharted2 (game engine ready)
    
    **Returns:**
    - Processed image file with metadata
    """
    try:
        # Read uploaded file
        image_data = await file.read()
        
        # Process image
        processed_data, metadata = image_processor.process_image(
            image_data=image_data,
            output_format=output_format,
            bit_depth=bit_depth,
            color_space=color_space,
            tone_mapping=tone_mapping,
            preset=preset,
            quality=quality,
            compression=compression
        )
        
        # Determine MIME type
        mime_types = {
            'tiff': 'image/tiff',
            'exr': 'image/x-exr',
            'png': 'image/png',
            'webp': 'image/webp'
        }
        
        # Generate filename
        original_name = file.filename.rsplit('.', 1)[0] if file.filename else 'image'
        download_filename = f"{original_name}_processed.{output_format}"
        
        # Return processed image
        return Response(
            content=processed_data,
            media_type=mime_types.get(output_format, 'application/octet-stream'),
            headers={
                'Content-Disposition': f'attachment; filename="{download_filename}"',
                'X-Processing-Metadata': str(metadata)
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Image processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/presets")
async def get_presets():
    """
    Get available quick presets for image processing.
    
    **Returns:**
    - Dictionary of presets with descriptions and use cases
    """
    return {
        "presets": image_processor.get_available_presets(),
        "total": len(image_processor.get_available_presets())
    }


@router.get("/formats")
async def get_supported_formats():
    """
    Get supported output formats and their capabilities.
    
    **Returns:**
    - Dictionary of formats with supported bit depths and options
    """
    return {
        "formats": image_processor.supported_formats,
        "color_spaces": list(image_processor.COLOR_SPACES.keys()),
        "tone_mapping": image_processor.TONE_MAPPING_ALGORITHMS
    }


@router.get("/color-spaces")
async def get_color_spaces():
    """
    Get detailed information about supported color spaces.
    
    **Returns:**
    - Color space descriptions and use cases
    """
    return {
        "color_spaces": {
            "srgb": {
                "name": "sRGB",
                "description": "Standard RGB - most common color space for web and displays",
                "use_case": "Web graphics, social media, general digital use",
                "gamut": "Standard"
            },
            "rec2020": {
                "name": "Rec. 2020",
                "description": "Wide color gamut for HDR displays and broadcast",
                "use_case": "HDR video, 4K/8K television, streaming platforms",
                "gamut": "Wide"
            },
            "dci_p3": {
                "name": "DCI-P3",
                "description": "Digital cinema standard with wide gamut",
                "use_case": "Cinema projection, Apple displays, professional video",
                "gamut": "Wide"
            },
            "adobe_rgb": {
                "name": "Adobe RGB",
                "description": "Professional photography and print color space",
                "use_case": "Print production, photography, professional editing",
                "gamut": "Wide"
            }
        }
    }


@router.get("/tone-mapping")
async def get_tone_mapping_info():
    """
    Get detailed information about tone mapping algorithms.
    
    **Returns:**
    - Tone mapping algorithm descriptions and characteristics
    """
    return {
        "algorithms": {
            "none": {
                "name": "None",
                "description": "No tone mapping applied",
                "use_case": "Standard images, no HDR content"
            },
            "reinhard": {
                "name": "Reinhard",
                "description": "Simple global tone mapping, preserves local contrast",
                "use_case": "General HDR images, photography",
                "characteristics": "Natural, gentle compression"
            },
            "filmic": {
                "name": "Filmic",
                "description": "ACES-like curve for cinematic look",
                "use_case": "Professional video, film production",
                "characteristics": "Cinematic, smooth highlights"
            },
            "aces": {
                "name": "ACES",
                "description": "Academy Color Encoding System standard",
                "use_case": "Film/TV production, VFX workflows",
                "characteristics": "Industry standard, predictable"
            },
            "uncharted2": {
                "name": "Uncharted 2",
                "description": "Game-proven tone mapping from Uncharted 2",
                "use_case": "Game development, real-time rendering",
                "characteristics": "Stylized, vibrant, game-friendly"
            }
        }
    }
