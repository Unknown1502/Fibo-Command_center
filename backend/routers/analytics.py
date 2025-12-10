"""
API router for A/B Testing & Analytics Dashboard.
Compare variants, track metrics, and get optimization insights.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics import analytics_manager

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateTestRequest(BaseModel):
    """Request model for creating an A/B test."""
    test_id: str = Field(..., description="Unique test identifier")
    name: str = Field(..., description="Test name/description")
    variant_a: Dict[str, Any] = Field(..., description="First variant parameters")
    variant_b: Dict[str, Any] = Field(..., description="Second variant parameters")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "test_id": "lighting_test_001",
                "name": "Soft vs Hard Lighting",
                "variant_a": {"lighting": "soft", "camera_angle": "eye_level"},
                "variant_b": {"lighting": "hard", "camera_angle": "eye_level"},
                "metadata": {"purpose": "Product photography optimization"}
            }
        }


class AddResultRequest(BaseModel):
    """Request model for adding test results."""
    variant: str = Field(..., description="Variant identifier ('a' or 'b')")
    score: float = Field(..., description="Quality score (0-100)", ge=0, le=100)
    feedback: Optional[str] = Field(default=None, description="Optional feedback notes")


class RecordMetricRequest(BaseModel):
    """Request model for recording a quality metric."""
    metric_name: str = Field(default='quality_score', description="Metric name")
    value: float = Field(..., description="Metric value")
    parameters: Dict[str, Any] = Field(..., description="Parameters used for generation")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


@router.post("/tests")
async def create_test(request: CreateTestRequest):
    """
    Create a new A/B test to compare parameter variants.
    
    **Use Cases:**
    - Test different lighting styles
    - Compare composition rules
    - Optimize color palettes
    - Find best camera angles
    
    **Returns:**
    - Created test with unique ID
    """
    try:
        test = analytics_manager.create_test(
            test_id=request.test_id,
            name=request.name,
            variant_a=request.variant_a,
            variant_b=request.variant_b,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "test": test.to_dict(),
            "message": f"A/B test '{request.name}' created successfully"
        }
    except Exception as e:
        logger.error(f"Failed to create test: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tests")
async def list_tests():
    """
    List all A/B tests with summary statistics.
    
    **Returns:**
    - List of tests with result counts and winners
    """
    return {
        "tests": analytics_manager.list_tests(),
        "total": len(analytics_manager.tests)
    }


@router.get("/tests/{test_id}")
async def get_test(test_id: str):
    """
    Get detailed results for a specific A/B test.
    
    **Returns:**
    - Complete test data including all results and winner
    """
    test = analytics_manager.get_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail=f"Test not found: {test_id}")
    
    return {
        "test": test.to_dict()
    }


@router.post("/tests/{test_id}/results")
async def add_test_result(test_id: str, request: AddResultRequest):
    """
    Add a result to an A/B test.
    
    **Returns:**
    - Updated test statistics
    """
    try:
        analytics_manager.add_test_result(
            test_id=test_id,
            variant=request.variant,
            score=request.score,
            feedback=request.feedback
        )
        
        test = analytics_manager.get_test(test_id)
        return {
            "success": True,
            "winner": test.get_winner(),
            "message": "Result added successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to add result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics")
async def record_metric(request: RecordMetricRequest):
    """
    Record a quality metric for analytics.
    
    **Use Cases:**
    - Track generation quality over time
    - Build performance history
    - Enable optimization recommendations
    
    **Returns:**
    - Confirmation of metric recorded
    """
    try:
        analytics_manager.record_metric(
            metric_name=request.metric_name,
            value=request.value,
            parameters=request.parameters,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "message": "Metric recorded successfully"
        }
    except Exception as e:
        logger.error(f"Failed to record metric: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance/{parameter_name}")
async def get_parameter_performance(
    parameter_name: str,
    metric_name: str = 'quality_score',
    days: int = 30
):
    """
    Analyze performance of different parameter values.
    
    **Use Cases:**
    - See which lighting style performs best
    - Compare camera angles
    - Identify optimal compositions
    - Data-driven parameter selection
    
    **Returns:**
    - Performance statistics for each parameter value
    - Ranking by average score
    """
    try:
        analysis = analytics_manager.get_parameter_performance(
            parameter_name=parameter_name,
            metric_name=metric_name,
            days=days
        )
        
        return analysis
    except Exception as e:
        logger.error(f"Performance analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def get_optimization_recommendations(
    parameters: Dict[str, Any],
    metric_name: str = 'quality_score'
):
    """
    Get parameter optimization recommendations based on historical data.
    
    **Use Cases:**
    - Optimize existing parameter sets
    - Data-driven improvements
    - Automated quality enhancement
    - Learn from past generations
    
    **Returns:**
    - Recommended parameter changes
    - Expected improvement scores
    - Confidence levels based on sample size
    """
    try:
        recommendations = analytics_manager.get_optimization_recommendations(
            current_parameters=parameters,
            metric_name=metric_name
        )
        
        return {
            "recommendations": recommendations,
            "total": len(recommendations),
            "message": "Generated optimization recommendations" if recommendations else "No improvements found"
        }
    except Exception as e:
        logger.error(f"Optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_quality_trends(days: int = 30):
    """
    Get quality metric trends over time.
    
    **Use Cases:**
    - Monitor quality improvements
    - Identify performance degradation
    - Track learning curve
    - Visualize progress
    
    **Returns:**
    - Daily average scores
    - Overall trend direction
    - Min/max scores per day
    """
    try:
        trends = analytics_manager.get_quality_trends(days=days)
        return trends
    except Exception as e:
        logger.error(f"Trends analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_summary():
    """
    Get comprehensive analytics dashboard summary.
    
    **Returns:**
    - Active A/B tests summary
    - Recent metrics
    - Top performing parameters
    - Quality trends
    """
    try:
        # Get recent trends
        trends = analytics_manager.get_quality_trends(days=7)
        
        # Get test summaries
        tests = analytics_manager.list_tests()
        active_tests = [t for t in tests if t['results_count_a'] + t['results_count_b'] < 50]
        
        # Get top performers for key parameters
        top_performers = {}
        for param in ['lighting', 'composition', 'style']:
            try:
                perf = analytics_manager.get_parameter_performance(param, days=30)
                if perf['ranking']:
                    top_performers[param] = perf['ranking'][0]
            except:
                pass
        
        return {
            "summary": {
                "total_tests": len(tests),
                "active_tests": len(active_tests),
                "total_metrics": len(analytics_manager.metrics_history),
                "avg_quality_7d": trends.get('overall_avg', 0)
            },
            "active_tests": active_tests[:5],  # Top 5
            "top_performers": top_performers,
            "trends": trends
        }
    except Exception as e:
        logger.error(f"Dashboard summary failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
