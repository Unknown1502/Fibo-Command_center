"""
Mock FIBO Service for Frontend Testing
This mock service simulates FIBO API responses for development and testing
"""
import asyncio
import random
from typing import Dict, Any, Optional, List
import logging
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class MockFIBOIntegration:
    """
    Mock FIBO integration for testing when API is unavailable
    Generates placeholder images with parameter overlays
    """
    
    def __init__(self):
        self.mock_mode = True
        logger.info("MockFIBOIntegration initialized - Using placeholder images")
    
    async def generate(
        self,
        prompt: str,
        camera_angle: Optional[str] = None,
        fov: Optional[str] = None,
        lighting: Optional[str] = None,
        color_palette: Optional[str] = None,
        composition: Optional[str] = None,
        style: Optional[str] = None,
        additional_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate mock image with parameter visualization
        """
        try:
            logger.info(f"Mock generating image: {prompt}")
            
            # Simulate API delay
            await asyncio.sleep(1)
            
            # Create a simple placeholder image
            width = 1024
            height = 1024
            
            # Choose color based on color_palette
            colors = {
                "vibrant": [(255, 0, 100), (0, 255, 200)],
                "pastel": [(255, 200, 200), (200, 200, 255)],
                "monochrome": [(100, 100, 100), (200, 200, 200)],
                "warm": [(255, 150, 100), (255, 200, 150)],
                "cool": [(100, 150, 255), (150, 200, 255)],
                "neon": [(255, 0, 255), (0, 255, 255)],
                "earth-tones": [(160, 120, 80), (200, 180, 140)],
                "jewel-tones": [(150, 50, 150), (50, 150, 150)]
            }
            
            color_set = colors.get(color_palette or "vibrant", [(100, 150, 200), (200, 150, 100)])
            
            # Create gradient image
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            # Draw gradient
            for y in range(height):
                ratio = y / height
                r = int(color_set[0][0] * (1 - ratio) + color_set[1][0] * ratio)
                g = int(color_set[0][1] * (1 - ratio) + color_set[1][1] * ratio)
                b = int(color_set[0][2] * (1 - ratio) + color_set[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add text overlay with parameters
            try:
                # Try to load a font, fallback to default if not available
                font_large = ImageFont.truetype("arial.ttf", 40)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Add title
            title_text = "MOCK FIBO GENERATION"
            draw.text((50, 50), title_text, fill=(255, 255, 255), font=font_large)
            
            # Add prompt
            prompt_lines = [prompt[i:i+40] for i in range(0, len(prompt), 40)]
            y_offset = 120
            for line in prompt_lines[:3]:  # Max 3 lines
                draw.text((50, y_offset), line, fill=(255, 255, 255), font=font_small)
                y_offset += 35
            
            # Add parameters
            param_text = []
            if camera_angle:
                param_text.append(f"Camera: {camera_angle}")
            if fov:
                param_text.append(f"FOV: {fov}")
            if lighting:
                param_text.append(f"Lighting: {lighting}")
            if composition:
                param_text.append(f"Composition: {composition}")
            if style:
                param_text.append(f"Style: {style}")
            
            y_offset = height - 200
            for param in param_text:
                draw.text((50, y_offset), param, fill=(255, 255, 255), font=font_small)
                y_offset += 30
            
            # Add watermark
            draw.text((50, height - 50), "Development Mode - Replace with real FIBO API", 
                     fill=(255, 255, 255), font=font_small)
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Return mock response
            return {
                "status": "success",
                "image_url": f"data:image/png;base64,{image_base64}",
                "parameters": {
                    "prompt": prompt,
                    "camera_angle": camera_angle,
                    "fov": fov,
                    "lighting": lighting,
                    "color_palette": color_palette,
                    "composition": composition,
                    "style": style
                },
                "mock": True,
                "message": "This is a mock response. Configure FIBO_API_KEY for real generation."
            }
            
        except Exception as e:
            logger.error(f"Error in mock generation: {str(e)}")
            raise
    
    async def batch_generate(
        self,
        requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch (mock)
        """
        results = []
        for req in requests:
            result = await self.generate(**req)
            results.append(result)
        return results
    
    async def refine(
        self,
        image_id: str,
        refinement_prompt: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Refine existing generation (mock)
        """
        logger.info(f"Mock refining image {image_id}: {refinement_prompt}")
        
        # Just generate a new image with the refinement prompt
        return await self.generate(
            prompt=refinement_prompt,
            **(parameters or {})
        )
