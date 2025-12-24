from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import ProjectCreate, ProjectInDB
from src.repositories.project_repository import ProjectRepository
from src.services.project_service import ProjectService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(db)
    return ProjectService(repo)

@router.post("/", response_model=ProjectInDB, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    try:
        project = service.create_project(
            name=project_data.name, 
            description=project_data.description
        )
        return project
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ProjectInDB])
def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()

@router.get("/{project_id}", response_model=ProjectInDB)
def get_project(
    project_id: int, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        project = service.update_project(project_id, None, None)  # Adjust if update not needed, use get
        return project
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{project_id}", response_model=ProjectInDB)
def update_project(
    project_id: int, 
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    try:
        updated_project = service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        return updated_project
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        service.delete_project(project_id)
        return 
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
