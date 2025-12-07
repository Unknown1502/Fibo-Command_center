"""
Workflows API Router
Handles automated workflow execution
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from workflows import get_workflow, WORKFLOWS
from database import get_db, Workflow as WorkflowModel
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()


class WorkflowRequest(BaseModel):
    """Request model for workflow execution"""
    workflow_type: str = Field(..., description="Type of workflow to execute")
    input_data: Dict[str, Any] = Field(..., description="Input data for workflow")
    project_id: Optional[int] = Field(None, description="Associated project ID")
    user_id: int = Field(default=1, description="User ID")


class WorkflowResponse(BaseModel):
    """Response model for workflow execution"""
    id: int
    workflow_type: str
    status: str
    total_generations: int
    completed_generations: int
    failed_generations: int
    results: Optional[List[Dict[str, Any]]]


@router.post("/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Execute an automated workflow
    
    Available workflow types:
    - **ecommerce**: E-commerce product photography pipeline
    - **social_media**: Social media campaign generation
    - **game_asset**: Game asset creation with variations
    
    Each workflow type requires specific input_data fields.
    """
    try:
        logger.info(f"Executing workflow: {request.workflow_type}")
        
        # Validate workflow type
        if request.workflow_type not in WORKFLOWS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown workflow type. Available types: {list(WORKFLOWS.keys())}"
            )
        
        # Create database record
        workflow_record = WorkflowModel(
            user_id=request.user_id,
            project_id=request.project_id,
            workflow_type=request.workflow_type,
            input_data=request.input_data,
            status="processing",
            started_at=datetime.utcnow()
        )
        db.add(workflow_record)
        db.commit()
        db.refresh(workflow_record)
        
        # Get workflow instance and execute
        workflow = get_workflow(request.workflow_type)
        result = await workflow.execute(request.input_data)
        
        # Update database record
        workflow_record.status = "completed"
        workflow_record.output_data = result
        workflow_record.total_generations = result.get("total_generated", 0) + result.get("total_failed", 0)
        workflow_record.completed_generations = result.get("total_generated", 0)
        workflow_record.failed_generations = result.get("total_failed", 0)
        workflow_record.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Workflow completed: {request.workflow_type}")
        
        return WorkflowResponse(
            id=workflow_record.id,
            workflow_type=request.workflow_type,
            status="completed",
            total_generations=workflow_record.total_generations,
            completed_generations=workflow_record.completed_generations,
            failed_generations=workflow_record.failed_generations,
            results=result.get("results", [])
        )
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
        
        # Update database with error
        if 'workflow_record' in locals():
            workflow_record.status = "failed"
            db.commit()
        
        # Import traceback for detailed error
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Full traceback:\n{error_details}")
        
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@router.get("/types")
async def get_workflow_types():
    """
    Get all available workflow types and their descriptions
    """
    return {
        "workflows": {
            "ecommerce": {
                "name": "E-commerce Product Pipeline",
                "description": "Generate complete product photography sets with multiple angles",
                "required_fields": ["product_name", "product_type"],
                "optional_fields": ["brand_colors", "style_preference"]
            },
            "social_media": {
                "name": "Social Media Campaign",
                "description": "Create platform-optimized content for social channels",
                "required_fields": ["campaign_theme", "brand_name"],
                "optional_fields": ["platforms", "tone"]
            },
            "game_asset": {
                "name": "Game Asset Generation",
                "description": "Produce game-ready visual assets with variations",
                "required_fields": ["asset_type", "description"],
                "optional_fields": ["game_style", "variations"]
            }
        }
    }


@router.get("/{workflow_id}")
async def get_workflow_by_id(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific workflow execution
    """
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "id": workflow.id,
        "workflow_type": workflow.workflow_type,
        "status": workflow.status,
        "input_data": workflow.input_data,
        "output_data": workflow.output_data,
        "total_generations": workflow.total_generations,
        "completed_generations": workflow.completed_generations,
        "failed_generations": workflow.failed_generations,
        "started_at": workflow.started_at,
        "completed_at": workflow.completed_at
    }


@router.get("/")
async def list_workflows(
    user_id: int = 1,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List all workflows for a user
    """
    workflows = db.query(WorkflowModel).filter(
        WorkflowModel.user_id == user_id
    ).order_by(
        WorkflowModel.started_at.desc()
    ).limit(limit).offset(offset).all()
    
    return {
        "workflows": [
            {
                "id": w.id,
                "workflow_type": w.workflow_type,
                "status": w.status,
                "total_generations": w.total_generations,
                "completed_generations": w.completed_generations,
                "started_at": w.started_at,
                "completed_at": w.completed_at
            }
            for w in workflows
        ],
        "total": len(workflows),
        "limit": limit,
        "offset": offset
    }
