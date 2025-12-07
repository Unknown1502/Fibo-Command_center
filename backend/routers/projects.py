"""
Projects API Router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from database import get_db, Project
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()


class ProjectCreate(BaseModel):
    """Model for creating a project"""
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    project_type: Optional[str] = Field(None, description="Project type")
    settings: Optional[Dict[str, Any]] = Field(None, description="Project settings")
    user_id: int = Field(default=1)


class ProjectResponse(BaseModel):
    """Response model for project"""
    id: int
    name: str
    description: Optional[str]
    project_type: Optional[str]
    settings: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project"""
    db_project = Project(
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        project_type=project.project_type,
        settings=project.settings or {}
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    user_id: int = 1,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all projects for a user"""
    projects = db.query(Project).filter(
        Project.user_id == user_id
    ).order_by(
        Project.updated_at.desc()
    ).limit(limit).offset(offset).all()
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.name = project_update.name
    project.description = project_update.description
    project.project_type = project_update.project_type
    project.settings = project_update.settings
    project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
