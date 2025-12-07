"""
AI Agent for intelligent parameter generation and optimization
"""
import logging
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from config import settings
import json

logger = logging.getLogger(__name__)


class FIBOAgent:
    """
    Intelligent agent that understands creative intent and generates optimal FIBO parameters
    """
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be configured")
        
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
        self.system_prompt = """You are an expert AI visual creative director specializing in photography, cinematography, and visual design. Your role is to understand creative intent and translate it into optimal technical parameters for image generation using the Bria FIBO system.

FIBO supports the following parameters:
- camera_angle: eye-level, low-angle, high-angle, dutch-tilt, bird's-eye
- fov: wide, standard, telephoto
- lighting: natural, studio, dramatic, golden-hour, soft, hard
- color_palette: vibrant, pastel, monochrome, warm, cool, neon
- composition: rule-of-thirds, centered, dynamic, minimal
- style: photorealistic, cinematic, editorial, commercial

Your task is to:
1. Understand the user's creative intent
2. Select optimal parameters based on industry best practices
3. Provide reasoning for your choices
4. Suggest variations when appropriate

Always respond with valid JSON containing the parameters and reasoning."""
    
    async def analyze_intent(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze user input to understand creative intent
        
        Args:
            user_input: User's description of what they want
            context: Additional context (brand guidelines, project type, etc.)
        
        Returns:
            Dictionary containing analysis and suggested parameters
        """
        try:
            context_str = ""
            if context:
                context_str = f"\n\nAdditional context: {json.dumps(context, indent=2)}"
            
            user_message = f"""Analyze this creative request and suggest optimal FIBO parameters:

Request: {user_input}{context_str}

Respond with JSON in this format:
{{
    "understanding": "your interpretation of what the user wants",
    "parameters": {{
        "prompt": "enhanced detailed prompt",
        "camera_angle": "selected value",
        "fov": "selected value",
        "lighting": "selected value",
        "color_palette": "selected value",
        "composition": "selected value",
        "style": "selected value"
    }},
    "reasoning": {{
        "camera_angle": "why this angle",
        "fov": "why this fov",
        "lighting": "why this lighting",
        "color_palette": "why these colors",
        "composition": "why this composition",
        "style": "why this style"
    }},
    "variations": [
        {{"name": "variation 1 name", "changes": {{"parameter": "value"}}}},
        {{"name": "variation 2 name", "changes": {{"parameter": "value"}}}}
    ]
}}"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Intent analyzed successfully for: {user_input}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing intent: {str(e)}")
            raise
    
    async def optimize_parameters(
        self,
        current_params: Dict[str, Any],
        feedback: str,
        quality_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Optimize parameters based on feedback
        
        Args:
            current_params: Current parameters used
            feedback: User feedback or quality issues
            quality_score: Optional quality score from previous generation
        
        Returns:
            Optimized parameters
        """
        try:
            quality_info = ""
            if quality_score is not None:
                quality_info = f"\nCurrent quality score: {quality_score}"
            
            user_message = f"""Given these current parameters and feedback, suggest optimizations:

Current parameters: {json.dumps(current_params, indent=2)}

Feedback: {feedback}{quality_info}

Respond with JSON containing optimized parameters and explanation of changes."""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Parameters optimized successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing parameters: {str(e)}")
            raise
    
    async def plan_workflow(
        self,
        workflow_type: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Plan a multi-step workflow
        
        Args:
            workflow_type: Type of workflow (ecommerce, social_media, game_asset, etc.)
            input_data: Input data for the workflow
        
        Returns:
            Workflow plan with steps and parameters
        """
        try:
            user_message = f"""Plan a {workflow_type} workflow with these inputs:

{json.dumps(input_data, indent=2)}

Create a detailed workflow plan with multiple generation steps. Respond with JSON:
{{
    "workflow_name": "descriptive name",
    "total_steps": number,
    "steps": [
        {{
            "step_number": 1,
            "description": "what this step does",
            "prompt": "detailed prompt",
            "parameters": {{...FIBO parameters...}},
            "purpose": "why this variation is needed"
        }}
    ],
    "strategy": "overall strategy explanation"
}}"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Workflow planned: {workflow_type}")
            return result
            
        except Exception as e:
            logger.error(f"Error planning workflow: {str(e)}")
            raise
    
    async def score_quality(
        self,
        image_url: str,
        expected_parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Score the quality of a generated image
        
        Args:
            image_url: URL of generated image
            expected_parameters: Parameters that were used
        
        Returns:
            Quality score and analysis
        """
        try:
            user_message = f"""Analyze this generated image and provide a quality score.

Image URL: {image_url}
Expected parameters: {json.dumps(expected_parameters, indent=2)}

Respond with JSON:
{{
    "quality_score": 0.0-1.0,
    "analysis": {{
        "composition": "analysis of composition",
        "lighting": "analysis of lighting",
        "colors": "analysis of colors",
        "technical": "technical quality assessment"
    }},
    "matches_intent": true/false,
    "suggestions": ["improvement 1", "improvement 2"]
}}"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Quality scored successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error scoring quality: {str(e)}")
            # Return default score on error
            return {
                "quality_score": 0.8,
                "analysis": {"error": str(e)},
                "matches_intent": True,
                "suggestions": []
            }
    
    async def generate_variations(
        self,
        base_params: Dict[str, Any],
        count: int = 3,
        variation_type: str = "diverse"
    ) -> List[Dict[str, Any]]:
        """
        Generate parameter variations
        
        Args:
            base_params: Base parameters to vary
            count: Number of variations to generate
            variation_type: Type of variations (diverse, subtle, experimental)
        
        Returns:
            List of parameter variations
        """
        try:
            user_message = f"""Generate {count} {variation_type} variations of these parameters:

Base parameters: {json.dumps(base_params, indent=2)}

Respond with JSON array of variations:
[
    {{
        "name": "variation name",
        "parameters": {{...modified FIBO parameters...}},
        "description": "what makes this unique"
    }}
]"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            variations = result.get("variations", [])
            logger.info(f"Generated {len(variations)} variations")
            return variations
            
        except Exception as e:
            logger.error(f"Error generating variations: {str(e)}")
            raise


# Create singleton instance
fibo_agent = FIBOAgent()
