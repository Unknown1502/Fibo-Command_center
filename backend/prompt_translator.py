"""
AI Prompt Translator
Converts natural language descriptions to optimized FIBO JSON parameters
Uses GPT-4 for intelligent parameter selection with reasoning
"""

import logging
from typing import Dict, Any, Optional
import json
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)


class PromptTranslator:
    """
    Professional AI-powered prompt translator
    Converts natural language to structured FIBO parameters
    """
    
    def __init__(self):
        # Priority: Groq (FREE + FAST) > Gemini (FREE) > OpenAI (PAID)
        if settings.USE_GROQ and settings.GROQ_API_KEY:
            logger.info("Using Groq (FREE) for AI translation")
            self.client = OpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = settings.GROQ_MODEL
        elif settings.USE_GEMINI and settings.GEMINI_API_KEY:
            logger.info("Using Google Gemini (FREE) for AI translation")
            # Gemini requires different client - will use fallback for now
            self.client = None
            self.model = settings.GEMINI_MODEL
        elif settings.OPENAI_API_KEY:
            logger.info("Using OpenAI for AI translation")
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = "gpt-4-turbo-preview"
        else:
            logger.warning("No AI API key configured. Using intelligent fallback mode.")
            self.client = None
            self.model = "fallback"
        
        # FIBO parameter knowledge base
        self.parameter_guide = {
            "camera_angle": {
                "options": ["eye-level", "low-angle", "high-angle", "dutch-tilt", "bird's-eye"],
                "meanings": {
                    "eye-level": "Neutral perspective, viewer at subject height. Natural, documentary feel.",
                    "low-angle": "Looking up at subject. Conveys power, dominance, grandeur.",
                    "high-angle": "Looking down at subject. Shows vulnerability, overview, context.",
                    "dutch-tilt": "Tilted horizon. Creates tension, unease, dynamic energy.",
                    "bird's-eye": "Directly from above. Maps, patterns, overhead view."
                }
            },
            "fov": {
                "options": ["wide", "standard", "telephoto"],
                "meanings": {
                    "wide": "Broad view, environmental context, dramatic perspective distortion.",
                    "standard": "Natural human vision (50mm). Balanced, realistic.",
                    "telephoto": "Compressed perspective, isolates subject, cinematic feel."
                }
            },
            "lighting": {
                "options": ["natural", "studio", "dramatic", "golden-hour", "soft", "hard"],
                "meanings": {
                    "natural": "Realistic daylight. Authentic, documentary style.",
                    "studio": "Controlled, even lighting. Professional product photography.",
                    "dramatic": "High contrast, shadows. Moody, cinematic atmosphere.",
                    "golden-hour": "Warm sunset/sunrise light. Romantic, beautiful.",
                    "soft": "Diffused, minimal shadows. Flattering, gentle.",
                    "hard": "Sharp shadows, high contrast. Edgy, graphic."
                }
            },
            "color_palette": {
                "options": ["vibrant", "pastel", "monochrome", "warm", "cool", "neon"],
                "meanings": {
                    "vibrant": "Rich, saturated colors. Energetic, eye-catching.",
                    "pastel": "Soft, desaturated colors. Gentle, elegant, sophisticated.",
                    "monochrome": "Black and white or single color. Timeless, classic, dramatic.",
                    "warm": "Reds, oranges, yellows. Inviting, cozy, energetic.",
                    "cool": "Blues, greens, purples. Calm, professional, modern.",
                    "neon": "Bright, electric colors. Bold, futuristic, energetic."
                }
            },
            "composition": {
                "options": ["rule-of-thirds", "centered", "dynamic", "minimal"],
                "meanings": {
                    "rule-of-thirds": "Classic composition. Balanced, professional.",
                    "centered": "Subject in center. Bold, symmetrical, impactful.",
                    "dynamic": "Diagonal lines, movement. Energetic, modern.",
                    "minimal": "Simple, clean. Focus on essential elements."
                }
            },
            "style": {
                "options": ["photorealistic", "cinematic", "editorial", "commercial", "artistic"],
                "meanings": {
                    "photorealistic": "Realistic photography. Natural, believable.",
                    "cinematic": "Film-like quality. Dramatic, narrative-driven.",
                    "editorial": "Magazine-style. Polished, aspirational.",
                    "commercial": "Product-focused. Clean, appealing.",
                    "artistic": "Creative interpretation. Expressive, unique."
                }
            }
        }
    
    async def translate(
        self,
        user_prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Translate natural language to FIBO parameters
        
        Args:
            user_prompt: Natural language description
            context: Optional context (product type, brand, etc.)
            
        Returns:
            {
                "intent": str,
                "mood": str,
                "parameters": dict,
                "reasoning": dict,
                "confidence": float,
                "suggestions": list
            }
        """
        try:
            logger.info(f"Translating prompt: {user_prompt[:100]}...")
            
            # Check if client is available
            if not self.client:
                logger.warning("OpenAI client not initialized. Using fallback.")
                return self._get_fallback_response(user_prompt)
            
            # Build system prompt with FIBO knowledge
            system_prompt = self._build_system_prompt()
            
            # Build user message with context
            user_message = self._build_user_message(user_prompt, context)
            
            # Call GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for consistent output
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Validate parameters
            validated_params = self._validate_parameters(result.get("parameters", {}))
            
            # Add quality score
            result["parameters"] = validated_params
            result["confidence"] = self._calculate_confidence(result)
            
            logger.info(f"Translation complete. Confidence: {result['confidence']:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}", exc_info=True)
            # Return safe defaults
            return self._get_fallback_response(user_prompt)
    
    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with FIBO expertise"""
        return f"""You are an expert visual director and photography technical consultant specializing in FIBO image generation.

Your role is to analyze user requests and translate them into optimal FIBO parameters.

FIBO Parameters Available:

1. CAMERA ANGLE: {json.dumps(self.parameter_guide['camera_angle']['meanings'], indent=2)}

2. FIELD OF VIEW: {json.dumps(self.parameter_guide['fov']['meanings'], indent=2)}

3. LIGHTING: {json.dumps(self.parameter_guide['lighting']['meanings'], indent=2)}

4. COLOR PALETTE: {json.dumps(self.parameter_guide['color_palette']['meanings'], indent=2)}

5. COMPOSITION: {json.dumps(self.parameter_guide['composition']['meanings'], indent=2)}

6. STYLE: {json.dumps(self.parameter_guide['style']['meanings'], indent=2)}

Your Response Format (JSON):
{{
    "intent": "What the user wants to achieve",
    "mood": "The emotional/aesthetic goal",
    "parameters": {{
        "camera_angle": "selected_option",
        "fov": "selected_option",
        "lighting": "selected_option",
        "color_palette": "selected_option",
        "composition": "selected_option",
        "style": "selected_option",
        "prompt": "refined FIBO prompt"
    }},
    "reasoning": {{
        "camera_angle": "Why this angle fits the intent",
        "fov": "Why this FOV works",
        "lighting": "Lighting choice explanation",
        "color_palette": "Color choice reasoning",
        "composition": "Composition justification",
        "style": "Style selection rationale"
    }},
    "suggestions": [
        "Alternative camera angle to try",
        "Lighting variation to consider",
        "Other creative suggestion"
    ]
}}

Guidelines:
- Analyze user intent carefully (product showcase, storytelling, mood, etc.)
- Consider context (e-commerce, editorial, cinematic, etc.)
- Provide clear reasoning for each choice
- Suggest alternatives for experimentation
- Keep prompt concise but descriptive"""
    
    def _build_user_message(
        self,
        user_prompt: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Build user message with context"""
        message = f"User Request: {user_prompt}"
        
        if context:
            message += f"\n\nContext:\n{json.dumps(context, indent=2)}"
        
        message += "\n\nAnalyze this request and provide optimal FIBO parameters with detailed reasoning."
        
        return message
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and correct parameters"""
        validated = {}
        
        # Validate each parameter against allowed values
        for param, value in params.items():
            if param == "prompt":
                validated[param] = value
                continue
            
            if param in self.parameter_guide:
                allowed = self.parameter_guide[param]["options"]
                if value in allowed:
                    validated[param] = value
                else:
                    # Use first option as fallback
                    validated[param] = allowed[0]
                    logger.warning(f"Invalid {param}: {value}, using {allowed[0]}")
        
        return validated
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score based on reasoning quality"""
        try:
            reasoning = result.get("reasoning", {})
            
            # More detailed reasoning = higher confidence
            avg_length = sum(len(r) for r in reasoning.values()) / max(len(reasoning), 1)
            
            # Normalize to 0-1 range
            confidence = min(avg_length / 100, 1.0)
            
            # Boost if suggestions provided
            if result.get("suggestions"):
                confidence = min(confidence + 0.1, 1.0)
            
            return round(confidence, 2)
            
        except:
            return 0.7
    
    def _get_fallback_response(self, user_prompt: str) -> Dict[str, Any]:
        """Provide safe fallback when AI translation fails"""
        return {
            "intent": "General image generation",
            "mood": "Balanced and professional",
            "parameters": {
                "camera_angle": "eye-level",
                "fov": "standard",
                "lighting": "natural",
                "color_palette": "vibrant",
                "composition": "rule-of-thirds",
                "style": "photorealistic",
                "prompt": user_prompt
            },
            "reasoning": {
                "camera_angle": "Eye-level provides neutral perspective",
                "fov": "Standard FOV mimics natural vision",
                "lighting": "Natural lighting for realistic results",
                "color_palette": "Vibrant colors for visual appeal",
                "composition": "Rule of thirds is professionally balanced",
                "style": "Photorealistic for versatility"
            },
            "confidence": 0.5,
            "suggestions": [
                "Try low-angle for more dramatic effect",
                "Consider dramatic lighting for moodier atmosphere"
            ],
            "fallback": True
        }


# Global instance
prompt_translator = PromptTranslator()
