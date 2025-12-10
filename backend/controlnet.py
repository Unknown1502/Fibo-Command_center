"""
ControlNet Integration for advanced composition control.
Edge detection, pose estimation, depth maps for precise image generation.
"""

import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Literal, Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class ControlNetProcessor:
    """
    Processes control images for ControlNet-style composition control.
    Provides edge detection, depth estimation, and pose preprocessing.
    """
    
    CONTROL_TYPES = [
        'canny_edge',      # Edge detection
        'depth_map',       # Depth estimation
        'normal_map',      # Surface normals
        'hed_edge',        # Holistically-nested edge detection
        'scribble',        # Sketch/scribble processing
        'pose',            # Pose estimation (simplified)
    ]
    
    def __init__(self):
        self.edge_thresholds = {
            'low': (50, 150),
            'medium': (100, 200),
            'high': (150, 250)
        }
    
    def process_control_image(
        self,
        image_data: bytes,
        control_type: Literal['canny_edge', 'depth_map', 'normal_map', 'hed_edge', 'scribble', 'pose'],
        strength: float = 1.0,
        **kwargs
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Process an input image to create a control image for ControlNet.
        
        Args:
            image_data: Input image as bytes
            control_type: Type of control processing
            strength: Control strength (0-1), higher = stronger influence
            **kwargs: Additional parameters for specific control types
        
        Returns:
            Tuple of (processed_control_image_bytes, metadata)
        """
        try:
            # Load image
            img = Image.open(io.BytesIO(image_data))
            img_array = np.array(img)
            
            # Convert to RGB if needed
            if len(img_array.shape) == 2:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
            elif img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
            
            # Process based on control type
            if control_type == 'canny_edge':
                processed = self._canny_edge(img_array, strength, **kwargs)
                
            elif control_type == 'depth_map':
                processed = self._depth_map(img_array, strength, **kwargs)
                
            elif control_type == 'normal_map':
                processed = self._normal_map(img_array, strength, **kwargs)
                
            elif control_type == 'hed_edge':
                processed = self._hed_edge(img_array, strength, **kwargs)
                
            elif control_type == 'scribble':
                processed = self._scribble(img_array, strength, **kwargs)
                
            elif control_type == 'pose':
                processed = self._pose_estimation(img_array, strength, **kwargs)
                
            else:
                raise ValueError(f"Unsupported control type: {control_type}")
            
            # Convert back to PIL Image
            processed_img = Image.fromarray(processed)
            
            # Save to bytes
            output = io.BytesIO()
            processed_img.save(output, format='PNG')
            output.seek(0)
            
            metadata = {
                'control_type': control_type,
                'strength': strength,
                'original_size': img.size,
                'processed_size': processed_img.size
            }
            
            return output.read(), metadata
            
        except Exception as e:
            logger.error(f"Control image processing failed: {str(e)}")
            raise
    
    def _canny_edge(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """Canny edge detection."""
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Get thresholds based on strength
        sensitivity = kwargs.get('sensitivity', 'medium')
        low, high = self.edge_thresholds.get(sensitivity, (100, 200))
        
        # Adjust thresholds by strength
        low = int(low * strength)
        high = int(high * strength)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, low, high)
        
        # Invert (white edges on black background)
        edges = cv2.bitwise_not(edges)
        
        # Convert to RGB
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        return edges_rgb
    
    def _depth_map(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """
        Simplified depth map estimation.
        In production, use a proper depth estimation model like MiDaS.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Use gradient magnitude as a simple depth proxy
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize
        gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
        gradient = gradient.astype(np.uint8)
        
        # Invert (darker = farther)
        depth = cv2.bitwise_not(gradient)
        
        # Apply strength
        depth = cv2.addWeighted(depth, strength, np.ones_like(depth) * 128, 1 - strength, 0)
        
        # Convert to RGB
        depth_rgb = cv2.cvtColor(depth.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        
        return depth_rgb
    
    def _normal_map(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """
        Generate surface normal map from image.
        Simplified version for demonstration.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate gradients
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Create normal map (simplified)
        # R = x gradient, G = y gradient, B = constant
        normal_map = np.zeros_like(img_array)
        normal_map[:, :, 0] = cv2.normalize(grad_x, None, 0, 255, cv2.NORM_MINMAX)
        normal_map[:, :, 1] = cv2.normalize(grad_y, None, 0, 255, cv2.NORM_MINMAX)
        normal_map[:, :, 2] = 128  # Constant Z
        
        # Apply strength
        normal_map = cv2.addWeighted(normal_map.astype(np.uint8), strength, 
                                      np.ones_like(normal_map) * 128, 1 - strength, 0)
        
        return normal_map.astype(np.uint8)
    
    def _hed_edge(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """
        Holistically-nested edge detection (simplified).
        In production, use a pre-trained HED model.
        """
        # Use multi-scale edge detection as approximation
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect edges at multiple scales
        edges1 = cv2.Canny(gray, 50, 150)
        edges2 = cv2.Canny(gray, 100, 200)
        edges3 = cv2.Canny(gray, 150, 250)
        
        # Combine
        combined = cv2.bitwise_or(edges1, cv2.bitwise_or(edges2, edges3))
        
        # Invert
        combined = cv2.bitwise_not(combined)
        
        # Apply strength
        combined = cv2.addWeighted(combined, strength, np.ones_like(combined) * 255, 1 - strength, 0)
        
        # Convert to RGB
        edges_rgb = cv2.cvtColor(combined.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        
        return edges_rgb
    
    def _scribble(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """Process scribble/sketch style control."""
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Edge detection with low threshold for sketch effect
        edges = cv2.Canny(gray, 30, 100)
        
        # Dilate to make lines thicker (sketch-like)
        kernel = np.ones((2, 2), np.uint8)
        sketch = cv2.dilate(edges, kernel, iterations=1)
        
        # Invert
        sketch = cv2.bitwise_not(sketch)
        
        # Add some noise for hand-drawn effect
        noise = np.random.randint(0, 30, sketch.shape, dtype=np.uint8)
        sketch = cv2.subtract(sketch, noise)
        
        # Apply strength
        sketch = cv2.addWeighted(sketch, strength, np.ones_like(sketch) * 255, 1 - strength, 0)
        
        # Convert to RGB
        sketch_rgb = cv2.cvtColor(sketch.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        
        return sketch_rgb
    
    def _pose_estimation(self, img_array: np.ndarray, strength: float, **kwargs) -> np.ndarray:
        """
        Simplified pose detection.
        In production, use OpenPose or MediaPipe for proper pose estimation.
        """
        # For demonstration, use edge detection with emphasis on vertical structures
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 100, 200)
        
        # Emphasize vertical lines (body parts)
        kernel_vert = np.ones((5, 1), np.uint8)
        vertical = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel_vert)
        
        # Emphasize horizontal lines (shoulders, hips)
        kernel_horiz = np.ones((1, 5), np.uint8)
        horizontal = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel_horiz)
        
        # Combine
        pose = cv2.bitwise_or(vertical, horizontal)
        
        # Invert
        pose = cv2.bitwise_not(pose)
        
        # Apply strength
        pose = cv2.addWeighted(pose, strength, np.ones_like(pose) * 255, 1 - strength, 0)
        
        # Convert to RGB
        pose_rgb = cv2.cvtColor(pose.astype(np.uint8), cv2.COLOR_GRAY2RGB)
        
        return pose_rgb
    
    def get_control_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available control types."""
        return {
            'canny_edge': {
                'name': 'Canny Edge Detection',
                'description': 'Detects edges for precise composition control',
                'use_case': 'Architecture, products, precise shapes',
                'parameters': ['sensitivity: low|medium|high']
            },
            'depth_map': {
                'name': 'Depth Map',
                'description': 'Estimates depth for 3D-aware generation',
                'use_case': 'Landscapes, portraits, spatial control',
                'parameters': []
            },
            'normal_map': {
                'name': 'Normal Map',
                'description': 'Surface normals for texture and lighting control',
                'use_case': '3D objects, surface details',
                'parameters': []
            },
            'hed_edge': {
                'name': 'HED Edge Detection',
                'description': 'Soft edges preserving natural structure',
                'use_case': 'Natural scenes, organic shapes',
                'parameters': []
            },
            'scribble': {
                'name': 'Scribble/Sketch',
                'description': 'Hand-drawn sketch style control',
                'use_case': 'Conceptual designs, rough layouts',
                'parameters': []
            },
            'pose': {
                'name': 'Pose Estimation',
                'description': 'Human pose detection for character control',
                'use_case': 'Character art, fashion, portraits',
                'parameters': []
            }
        }


# Global instance
controlnet_processor = ControlNetProcessor()
