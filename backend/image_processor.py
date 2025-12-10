"""
Professional image processing module for HDR and 16-bit export capabilities.
Supports multiple color spaces, tone mapping algorithms, and export formats.
"""

import io
import numpy as np
from PIL import Image
import cv2
from typing import Optional, Dict, Any, Literal
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Advanced image processing for professional workflows.
    Handles HDR tone mapping, color space conversion, and high-bit-depth export.
    """
    
    # Color space conversion matrices (RGB to XYZ, then XYZ to target)
    COLOR_SPACES = {
        'srgb': 'default',  # Standard RGB (most common)
        'rec2020': 'bt2020',  # Wide gamut for HDR displays
        'dci_p3': 'p3',  # Digital cinema standard
        'adobe_rgb': 'adobe'  # Photography/print standard
    }
    
    TONE_MAPPING_ALGORITHMS = ['reinhard', 'filmic', 'aces', 'uncharted2', 'none']
    
    def __init__(self):
        self.supported_formats = {
            'tiff': {'bit_depth': [8, 16, 32], 'compression': ['none', 'lzw', 'jpeg']},
            'exr': {'bit_depth': [16, 32], 'compression': ['none', 'zip', 'piz']},
            'png': {'bit_depth': [8, 16], 'compression': ['default']},
            'webp': {'bit_depth': [8], 'quality': [0, 100]}
        }
    
    def process_image(
        self,
        image_data: bytes,
        output_format: Literal['tiff', 'exr', 'png', 'webp'] = 'png',
        bit_depth: int = 16,
        color_space: Literal['srgb', 'rec2020', 'dci_p3', 'adobe_rgb'] = 'srgb',
        tone_mapping: Literal['reinhard', 'filmic', 'aces', 'uncharted2', 'none'] = 'none',
        preset: Optional[str] = None,
        **kwargs
    ) -> tuple[bytes, Dict[str, Any]]:
        """
        Process image with HDR tone mapping and export to specified format.
        
        Args:
            image_data: Input image as bytes
            output_format: Output format (tiff, exr, png, webp)
            bit_depth: Color depth (8, 16, or 32 bits)
            color_space: Target color space
            tone_mapping: HDR tone mapping algorithm
            preset: Quick preset (web, print, film_tv, cinema, games)
            **kwargs: Additional format-specific options
        
        Returns:
            Tuple of (processed_image_bytes, metadata_dict)
        """
        try:
            # Apply preset if specified
            if preset:
                params = self._get_preset_params(preset)
                output_format = params.get('format', output_format)
                bit_depth = params.get('bit_depth', bit_depth)
                color_space = params.get('color_space', color_space)
                tone_mapping = params.get('tone_mapping', tone_mapping)
            
            # Validate parameters
            self._validate_parameters(output_format, bit_depth, color_space, tone_mapping)
            
            # Load image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to numpy array for processing
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            # Apply tone mapping if specified
            if tone_mapping != 'none':
                img_array = self._apply_tone_mapping(img_array, tone_mapping)
            
            # Convert color space if needed
            if color_space != 'srgb':
                img_array = self._convert_color_space(img_array, 'srgb', color_space)
            
            # Convert to target bit depth
            if bit_depth == 8:
                img_array = (np.clip(img_array, 0, 1) * 255).astype(np.uint8)
            elif bit_depth == 16:
                img_array = (np.clip(img_array, 0, 1) * 65535).astype(np.uint16)
            else:  # 32-bit
                img_array = img_array.astype(np.float32)
            
            # Convert back to PIL Image
            if bit_depth == 32:
                # For 32-bit, we need to use a different mode
                processed_img = Image.fromarray(img_array, mode='F')
            else:
                processed_img = Image.fromarray(img_array)
            
            # Export to specified format
            output_bytes, metadata = self._export_image(
                processed_img, output_format, bit_depth, **kwargs
            )
            
            # Add processing metadata
            metadata.update({
                'bit_depth': bit_depth,
                'color_space': color_space,
                'tone_mapping': tone_mapping,
                'output_format': output_format,
                'preset': preset or 'custom'
            })
            
            return output_bytes, metadata
            
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise
    
    def _validate_parameters(self, output_format: str, bit_depth: int, color_space: str, tone_mapping: str):
        """Validate processing parameters."""
        if output_format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {output_format}")
        
        if bit_depth not in self.supported_formats[output_format]['bit_depth']:
            raise ValueError(f"{output_format} does not support {bit_depth}-bit depth")
        
        if color_space not in self.COLOR_SPACES:
            raise ValueError(f"Unsupported color space: {color_space}")
        
        if tone_mapping not in self.TONE_MAPPING_ALGORITHMS:
            raise ValueError(f"Unsupported tone mapping: {tone_mapping}")
    
    def _apply_tone_mapping(self, img_array: np.ndarray, algorithm: str) -> np.ndarray:
        """Apply HDR tone mapping algorithm."""
        if algorithm == 'reinhard':
            # Reinhard tone mapping: I_out = I_in / (1 + I_in)
            return img_array / (1 + img_array)
        
        elif algorithm == 'filmic':
            # Filmic tone mapping (ACES-like curve)
            a = 2.51
            b = 0.03
            c = 2.43
            d = 0.59
            e = 0.14
            return np.clip((img_array * (a * img_array + b)) / (img_array * (c * img_array + d) + e), 0, 1)
        
        elif algorithm == 'aces':
            # ACES filmic tone mapping
            a = 2.51
            b = 0.03
            c = 2.43
            d = 0.59
            e = 0.14
            img_array = img_array * 0.6  # Exposure adjustment
            return np.clip((img_array * (a * img_array + b)) / (img_array * (c * img_array + d) + e), 0, 1)
        
        elif algorithm == 'uncharted2':
            # Uncharted 2 tone mapping
            def uncharted2_tonemap_partial(x):
                A = 0.15
                B = 0.50
                C = 0.10
                D = 0.20
                E = 0.02
                F = 0.30
                return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F
            
            exposure_bias = 2.0
            curr = uncharted2_tonemap_partial(img_array * exposure_bias)
            W = 11.2
            white_scale = 1.0 / uncharted2_tonemap_partial(W)
            return curr * white_scale
        
        return img_array
    
    def _convert_color_space(self, img_array: np.ndarray, src: str, dst: str) -> np.ndarray:
        """Convert between color spaces."""
        # For simplicity, using OpenCV color conversion
        # In production, you'd use proper color management with ICC profiles
        
        if src == 'srgb' and dst == 'rec2020':
            # Convert sRGB to Rec.2020 (wide gamut)
            # This is a simplified conversion; proper implementation needs color matrices
            img_array = np.clip(img_array * 1.1, 0, 1)  # Expand gamut slightly
        
        elif src == 'srgb' and dst == 'dci_p3':
            # Convert sRGB to DCI-P3
            img_array = np.clip(img_array * 1.05, 0, 1)
        
        elif src == 'srgb' and dst == 'adobe_rgb':
            # Convert sRGB to Adobe RGB
            img_array = np.clip(img_array * 1.08, 0, 1)
        
        return img_array
    
    def _export_image(
        self, img: Image.Image, output_format: str, bit_depth: int, **kwargs
    ) -> tuple[bytes, Dict[str, Any]]:
        """Export image to specified format."""
        output = io.BytesIO()
        metadata = {}
        
        if output_format == 'tiff':
            compression = kwargs.get('compression', 'lzw')
            img.save(output, format='TIFF', compression=compression)
            metadata['compression'] = compression
        
        elif output_format == 'exr':
            # EXR requires OpenEXR library, fallback to TIFF for now
            # In production, use: import OpenEXR, Imath
            logger.warning("EXR export not fully implemented, using TIFF instead")
            img.save(output, format='TIFF', compression='none')
            metadata['note'] = 'EXR requested but exported as TIFF (OpenEXR required)'
        
        elif output_format == 'png':
            if bit_depth == 16:
                img.save(output, format='PNG', compress_level=kwargs.get('compress_level', 6))
            else:
                img.save(output, format='PNG')
        
        elif output_format == 'webp':
            quality = kwargs.get('quality', 90)
            img.save(output, format='WEBP', quality=quality)
            metadata['quality'] = quality
        
        output.seek(0)
        return output.read(), metadata
    
    def _get_preset_params(self, preset: str) -> Dict[str, Any]:
        """Get parameters for quick presets."""
        presets = {
            'web': {
                'format': 'webp',
                'bit_depth': 8,
                'color_space': 'srgb',
                'tone_mapping': 'none',
                'quality': 85
            },
            'print': {
                'format': 'tiff',
                'bit_depth': 16,
                'color_space': 'adobe_rgb',
                'tone_mapping': 'none',
                'compression': 'lzw'
            },
            'film_tv': {
                'format': 'tiff',
                'bit_depth': 16,
                'color_space': 'rec2020',
                'tone_mapping': 'aces',
                'compression': 'none'
            },
            'cinema': {
                'format': 'exr',
                'bit_depth': 32,
                'color_space': 'dci_p3',
                'tone_mapping': 'filmic',
                'compression': 'zip'
            },
            'games': {
                'format': 'png',
                'bit_depth': 8,
                'color_space': 'srgb',
                'tone_mapping': 'uncharted2',
                'compress_level': 9
            }
        }
        
        if preset not in presets:
            raise ValueError(f"Unknown preset: {preset}. Available: {list(presets.keys())}")
        
        return presets[preset]
    
    def get_available_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get all available presets with descriptions."""
        return {
            'web': {
                'name': 'Web Optimized',
                'description': 'Optimized for web (WebP, 8-bit, sRGB)',
                'use_case': 'Websites, social media, online galleries'
            },
            'print': {
                'name': 'Print Production',
                'description': 'High quality for print (TIFF, 16-bit, Adobe RGB)',
                'use_case': 'Magazines, posters, professional printing'
            },
            'film_tv': {
                'name': 'Film & TV',
                'description': 'Broadcast quality (TIFF, 16-bit, Rec.2020, ACES)',
                'use_case': 'Television production, streaming, HDR content'
            },
            'cinema': {
                'name': 'Digital Cinema',
                'description': 'Cinema grade (EXR, 32-bit, DCI-P3)',
                'use_case': 'Feature films, theater projection, VFX'
            },
            'games': {
                'name': 'Game Assets',
                'description': 'Game engine ready (PNG, 8-bit, Uncharted2)',
                'use_case': 'Video games, real-time rendering, Unity/Unreal'
            }
        }


# Global instance
image_processor = ImageProcessor()
