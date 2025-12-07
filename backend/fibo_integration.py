"""
FIBO Integration Layer
Handles all communication with Bria FIBO API
"""
import httpx
import logging
from typing import Dict, Any, Optional, List
from config import settings
import base64
import io
from PIL import Image

logger = logging.getLogger(__name__)


class FIBOIntegration:
    """
    Integration layer for Bria FIBO API
    Handles image generation with full parameter control
    """
    
    def __init__(self):
        self.api_key = settings.FIBO_API_KEY or settings.FAL_API_KEY
        self.api_url = settings.FIBO_API_URL if settings.FIBO_API_KEY else settings.FAL_API_URL
        self.use_fal = not settings.FIBO_API_KEY
        
        if not self.api_key:
            raise ValueError("FIBO_API_KEY or FAL_API_KEY must be configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers for Bria V2 API"""
        if self.use_fal:
            return {
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            # Bria V2 API uses api_token header
            return {
                "api_token": self.api_key,
                "Content-Type": "application/json"
            }
    
    def _enhance_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance parameters with professional settings
        """
        enhanced = params.copy()
        
        # Add HDR and 16-bit support if enabled
        if settings.HDR_ENABLED:
            enhanced['hdr'] = True
            enhanced['color_depth'] = settings.DEFAULT_COLOR_DEPTH
            enhanced['color_space'] = settings.DEFAULT_COLOR_SPACE
        
        # Set quality to maximum
        enhanced['quality'] = settings.DEFAULT_QUALITY
        
        # Set default dimensions if not provided
        if 'width' not in enhanced:
            enhanced['width'] = settings.DEFAULT_IMAGE_WIDTH
        if 'height' not in enhanced:
            enhanced['height'] = settings.DEFAULT_IMAGE_HEIGHT
        
        return enhanced
    
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
        Generate image using FIBO API
        
        Args:
            prompt: Description of desired image
            camera_angle: Camera angle (eye-level, low-angle, high-angle, dutch-tilt, bird's-eye)
            fov: Field of view (wide, standard, telephoto)
            lighting: Lighting type (natural, studio, dramatic, golden-hour, soft, hard)
            color_palette: Color palette (vibrant, pastel, monochrome, warm, cool, neon)
            composition: Composition style (rule-of-thirds, centered, dynamic, minimal)
            style: Visual style (photorealistic, cinematic, editorial, commercial)
            additional_params: Any additional parameters
        
        Returns:
            Dictionary containing generation results
        """
        try:
            # Build prompt with FIBO parameters embedded
            full_prompt = prompt
            
            # Add FIBO-specific parameters to prompt for V2 API
            if camera_angle or fov or lighting or color_palette or composition or style:
                param_descriptions = []
                if camera_angle:
                    param_descriptions.append(f"camera angle: {camera_angle}")
                if fov:
                    param_descriptions.append(f"field of view: {fov}")
                if lighting:
                    param_descriptions.append(f"lighting: {lighting}")
                if color_palette:
                    param_descriptions.append(f"color palette: {color_palette}")
                if composition:
                    param_descriptions.append(f"composition: {composition}")
                if style:
                    param_descriptions.append(f"style: {style}")
                
                full_prompt = f"{prompt}, {', '.join(param_descriptions)}"
            
            # Bria V2 API request format
            params = {
                "prompt": full_prompt,
                "sync": True,  # Synchronous mode for immediate response
                "model_version": "FIBO"
            }
            
            # Add additional parameters
            if additional_params:
                params.update(additional_params)
            
            logger.info(f"Generating image with FIBO V2 API: {full_prompt[:100]}...")
            logger.debug(f"Request parameters: {params}")
            
            # Make API request
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self._get_headers(),
                    json=params
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                
                response.raise_for_status()
                result = response.json()
            
            logger.info("Image generated successfully with FIBO V2")
            
            # Extract image URL from Bria V2 response format
            image_url = None
            if "result" in result:
                image_url = result["result"].get("image_url")
            elif "image_url" in result:
                image_url = result["image_url"]
            elif "url" in result:
                image_url = result["url"]
            
            return {
                "status": "success",
                "image_url": image_url,
                "parameters": {
                    "prompt": prompt,
                    "camera_angle": camera_angle,
                    "fov": fov,
                    "lighting": lighting,
                    "color_palette": color_palette,
                    "composition": composition,
                    "style": style
                },
                "raw_response": result
            }
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during generation: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response body: {e.response.text}")
            raise Exception(f"FIBO API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            raise
    
    async def batch_generate(
        self,
        requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch
        
        Args:
            requests: List of generation requests
        
        Returns:
            List of generation results
        """
        if len(requests) > settings.MAX_BATCH_SIZE:
            raise ValueError(f"Batch size exceeds maximum of {settings.MAX_BATCH_SIZE}")
        
        logger.info(f"Batch generating {len(requests)} images")
        
        results = []
        for i, request in enumerate(requests):
            try:
                result = await self.generate(**request)
                results.append(result)
                logger.info(f"Completed {i+1}/{len(requests)}")
            except Exception as e:
                logger.error(f"Failed to generate image {i+1}: {str(e)}")
                results.append({
                    "status": "failed",
                    "error": str(e),
                    "request": request
                })
        
        return results
    
    async def refine(
        self,
        image_url: str,
        refinement_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Refine an existing image
        
        Args:
            image_url: URL of image to refine
            refinement_params: Refinement parameters
        
        Returns:
            Refined image result
        """
        try:
            params = {
                "image_url": image_url,
                **refinement_params
            }
            
            params = self._enhance_parameters(params)
            
            logger.info(f"Refining image: {image_url}")
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.api_url}/refine",
                    headers=self._get_headers(),
                    json=params
                )
                response.raise_for_status()
                result = response.json()
            
            return {
                "status": "success",
                "image_url": result.get("url") or result.get("image_url"),
                "parameters": params,
                "raw_response": result
            }
            
        except Exception as e:
            logger.error(f"Error during refinement: {str(e)}")
            raise
    
    def get_parameter_options(self) -> Dict[str, List[str]]:
        """
        Get all available parameter options
        
        Returns:
            Dictionary of parameter names and their valid values
        """
        return {
            "camera_angle": [
                "eye-level",
                "low-angle",
                "high-angle",
                "dutch-tilt",
                "bird's-eye",
                "worm's-eye",
                "over-the-shoulder"
            ],
            "fov": [
                "wide",
                "standard",
                "telephoto",
                "ultra-wide",
                "macro"
            ],
            "lighting": [
                "natural",
                "studio",
                "dramatic",
                "golden-hour",
                "soft",
                "hard",
                "rim",
                "backlit",
                "three-point"
            ],
            "color_palette": [
                "vibrant",
                "pastel",
                "monochrome",
                "warm",
                "cool",
                "neon",
                "earth-tones",
                "jewel-tones"
            ],
            "composition": [
                "rule-of-thirds",
                "centered",
                "dynamic",
                "minimal",
                "symmetrical",
                "leading-lines",
                "frame-within-frame"
            ],
            "style": [
                "photorealistic",
                "cinematic",
                "editorial",
                "commercial",
                "artistic",
                "documentary",
                "fashion",
                "product"
            ]
        }
    
    async def test_connection(self) -> bool:
        """
        Test connection to FIBO API
        
        Returns:
            True if connection successful
        """
        try:
            result = await self.generate(
                prompt="test image",
                style="photorealistic"
            )
            return result.get("status") == "success"
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False


# Create singleton instance with fallback to mock
try:
    fibo_integration = FIBOIntegration()
    logger.info("FIBO Integration initialized successfully")
except Exception as e:
    logger.warning(f"Failed to initialize FIBO Integration: {str(e)}")
    logger.info("Falling back to Mock FIBO Integration for development")
    from mock_fibo import MockFIBOIntegration
    fibo_integration = MockFIBOIntegration()
