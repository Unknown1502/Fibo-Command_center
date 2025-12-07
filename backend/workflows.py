"""
Automated workflow implementations
"""
import logging
from typing import Dict, Any, List
from fibo_integration import fibo_integration
from fibo_agent import fibo_agent

logger = logging.getLogger(__name__)


class BaseWorkflow:
    """Base class for all workflows"""
    
    def __init__(self):
        self.fibo = fibo_integration
        self.agent = fibo_agent
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow - to be implemented by subclasses"""
        raise NotImplementedError


class EcommerceWorkflow(BaseWorkflow):
    """
    E-commerce product photography workflow
    Generates complete product photography sets with multiple angles
    """
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute e-commerce workflow
        
        Args:
            input_data: {
                "product_name": str,
                "product_type": str,
                "brand_colors": List[str],
                "style_preference": str
            }
        
        Returns:
            Workflow results with all generated images
        """
        try:
            logger.info(f"Starting e-commerce workflow for: {input_data.get('product_name')}")
            
            # Step 1: Get workflow plan from agent (with fallback)
            try:
                workflow_plan = await self.agent.plan_workflow("ecommerce", input_data)
            except Exception as e:
                logger.warning(f"Agent plan failed, using default workflow: {str(e)}")
                workflow_plan = {"status": "using_defaults"}
            
            # Step 2: Define standard e-commerce angles
            angles = [
                {"name": "Front View", "camera_angle": "eye-level", "composition": "centered"},
                {"name": "45 Degree", "camera_angle": "eye-level", "composition": "rule-of-thirds"},
                {"name": "Side View", "camera_angle": "eye-level", "composition": "centered"},
                {"name": "Top View", "camera_angle": "bird's-eye", "composition": "centered"},
                {"name": "Detail Shot", "camera_angle": "low-angle", "composition": "minimal"},
                {"name": "Lifestyle 1", "camera_angle": "eye-level", "composition": "dynamic"},
                {"name": "Lifestyle 2", "camera_angle": "high-angle", "composition": "rule-of-thirds"}
            ]
            
            # Step 3: Generate base prompt
            base_prompt = f"Professional product photography of {input_data.get('product_name')}, {input_data.get('product_type')}"
            
            # Step 4: Generate each angle
            results = []
            for i, angle_config in enumerate(angles):
                try:
                    # Try to get agent suggestions (with fallback)
                    try:
                        intent_analysis = await self.agent.analyze_intent(
                            f"{base_prompt}, {angle_config['name']}",
                            context=input_data
                        )
                        params = intent_analysis.get("parameters", {})
                    except Exception as e:
                        logger.warning(f"Agent analysis failed for {angle_config['name']}, using defaults: {str(e)}")
                        params = {"prompt": f"{base_prompt}, {angle_config['name']}"}
                    
                    # Merge angle config with agent suggestions
                    params.update(angle_config)
                    
                    # Generate image
                    generation_result = await self.fibo.generate(
                        prompt=params.get("prompt", base_prompt),
                        camera_angle=params.get("camera_angle"),
                        fov=params.get("fov", "standard"),
                        lighting=params.get("lighting", "studio"),
                        color_palette=params.get("color_palette", "vibrant"),
                        composition=params.get("composition"),
                        style="commercial"
                    )
                    
                    results.append({
                        "angle": angle_config["name"],
                        "status": "success",
                        "result": generation_result
                    })
                    
                    logger.info(f"Generated {angle_config['name']} ({i+1}/{len(angles)})")
                    
                except Exception as e:
                    logger.error(f"Failed to generate {angle_config['name']}: {str(e)}")
                    results.append({
                        "angle": angle_config["name"],
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Step 5: Compile results
            successful = [r for r in results if r["status"] == "success"]
            failed = [r for r in results if r["status"] == "failed"]
            
            return {
                "workflow_type": "ecommerce",
                "status": "completed",
                "total_generated": len(successful),
                "total_failed": len(failed),
                "results": results,
                "summary": {
                    "product": input_data.get("product_name"),
                    "angles_completed": [r["angle"] for r in successful],
                    "angles_failed": [r["angle"] for r in failed]
                }
            }
            
        except Exception as e:
            logger.error(f"E-commerce workflow failed: {str(e)}")
            raise


class SocialMediaWorkflow(BaseWorkflow):
    """
    Social media campaign workflow
    Generates platform-optimized content for various social channels
    """
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute social media workflow
        
        Args:
            input_data: {
                "campaign_theme": str,
                "brand_name": str,
                "platforms": List[str],
                "tone": str
            }
        
        Returns:
            Platform-optimized social media content
        """
        try:
            logger.info(f"Starting social media workflow: {input_data.get('campaign_theme')}")
            
            # Define platform specs
            platform_configs = {
                "instagram_post": {
                    "name": "Instagram Post",
                    "aspect_ratio": "1:1",
                    "style": "vibrant",
                    "composition": "centered"
                },
                "instagram_story": {
                    "name": "Instagram Story",
                    "aspect_ratio": "9:16",
                    "style": "dynamic",
                    "composition": "rule-of-thirds"
                },
                "facebook": {
                    "name": "Facebook Post",
                    "aspect_ratio": "1.91:1",
                    "style": "engaging",
                    "composition": "dynamic"
                },
                "linkedin": {
                    "name": "LinkedIn Post",
                    "aspect_ratio": "1.91:1",
                    "style": "professional",
                    "composition": "minimal"
                },
                "twitter": {
                    "name": "Twitter Post",
                    "aspect_ratio": "16:9",
                    "style": "bold",
                    "composition": "centered"
                }
            }
            
            platforms = input_data.get("platforms", ["instagram_post", "facebook"])
            base_prompt = f"{input_data.get('campaign_theme')} for {input_data.get('brand_name')}"
            
            results = []
            for platform in platforms:
                if platform not in platform_configs:
                    continue
                
                config = platform_configs[platform]
                
                try:
                    # Get agent analysis (with fallback)
                    try:
                        intent_analysis = await self.agent.analyze_intent(
                            f"Social media {config['name']}: {base_prompt}",
                            context=input_data
                        )
                        params = intent_analysis.get("parameters", {})
                    except Exception as e:
                        logger.warning(f"Agent analysis failed for {config['name']}, using defaults: {str(e)}")
                        params = {"prompt": f"Social media {config['name']}: {base_prompt}"}
                    
                    # Generate for platform
                    generation_result = await self.fibo.generate(
                        prompt=params.get("prompt", base_prompt),
                        camera_angle=params.get("camera_angle", "eye-level"),
                        fov=params.get("fov", "standard"),
                        lighting=params.get("lighting", "natural"),
                        color_palette=params.get("color_palette", "vibrant"),
                        composition=config.get("composition"),
                        style="commercial"
                    )
                    
                    results.append({
                        "platform": config["name"],
                        "status": "success",
                        "result": generation_result
                    })
                    
                    logger.info(f"Generated {config['name']}")
                    
                except Exception as e:
                    logger.error(f"Failed {config['name']}: {str(e)}")
                    results.append({
                        "platform": config["name"],
                        "status": "failed",
                        "error": str(e)
                    })
            
            successful = [r for r in results if r["status"] == "success"]
            
            return {
                "workflow_type": "social_media",
                "status": "completed",
                "total_generated": len(successful),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Social media workflow failed: {str(e)}")
            raise


class GameAssetWorkflow(BaseWorkflow):
    """
    Game asset generation workflow
    Creates game-ready visual assets with consistent style
    """
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute game asset workflow
        
        Args:
            input_data: {
                "asset_type": str,
                "game_style": str,
                "description": str,
                "variations": int
            }
        
        Returns:
            Game asset variations
        """
        try:
            logger.info(f"Starting game asset workflow: {input_data.get('asset_type')}")
            
            asset_type = input_data.get("asset_type", "character")
            game_style = input_data.get("game_style", "realistic")
            description = input_data.get("description", "")
            variations_count = int(input_data.get("variations", 4))
            
            base_prompt = f"{game_style} game {asset_type}: {description}"
            
            # Get workflow plan (with fallback)
            try:
                workflow_plan = await self.agent.plan_workflow("game_asset", input_data)
            except Exception as e:
                logger.warning(f"Agent plan failed, using default workflow: {str(e)}")
                workflow_plan = {"status": "using_defaults"}
            
            # Generate variations
            results = []
            angles = ["front", "side", "back", "isometric"]
            
            for i, angle in enumerate(angles[:variations_count]):
                try:
                    # Get agent analysis (with fallback)
                    try:
                        intent_analysis = await self.agent.analyze_intent(
                            f"{base_prompt}, {angle} view",
                            context={"game_style": game_style, "asset_type": asset_type}
                        )
                        params = intent_analysis.get("parameters", {})
                    except Exception as e:
                        logger.warning(f"Agent analysis failed for {angle} view, using defaults: {str(e)}")
                        params = {"prompt": f"{base_prompt}, {angle} view"}
                    
                    generation_result = await self.fibo.generate(
                        prompt=params.get("prompt", base_prompt),
                        camera_angle=params.get("camera_angle", "eye-level"),
                        fov=params.get("fov", "standard"),
                        lighting=params.get("lighting", "studio"),
                        color_palette=params.get("color_palette", "vibrant"),
                        composition="centered",
                        style="artistic"
                    )
                    
                    results.append({
                        "variation": f"{angle} view",
                        "status": "success",
                        "result": generation_result
                    })
                    
                    logger.info(f"Generated {angle} view ({i+1}/{variations_count})")
                    
                except Exception as e:
                    logger.error(f"Failed {angle} view: {str(e)}")
                    results.append({
                        "variation": f"{angle} view",
                        "status": "failed",
                        "error": str(e)
                    })
            
            successful = [r for r in results if r["status"] == "success"]
            failed = [r for r in results if r["status"] == "failed"]
            
            return {
                "workflow_type": "game_asset",
                "status": "completed",
                "total_generated": len(successful),
                "total_failed": len(failed),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Game asset workflow failed: {str(e)}")
            raise


# Workflow registry
WORKFLOWS = {
    "ecommerce": EcommerceWorkflow,
    "social_media": SocialMediaWorkflow,
    "game_asset": GameAssetWorkflow
}


def get_workflow(workflow_type: str) -> BaseWorkflow:
    """Get workflow instance by type"""
    workflow_class = WORKFLOWS.get(workflow_type)
    if not workflow_class:
        raise ValueError(f"Unknown workflow type: {workflow_type}")
    return workflow_class()
