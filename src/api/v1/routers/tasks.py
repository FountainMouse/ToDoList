from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import TaskCreate, TaskUpdate, TaskInDB
from src.models.task import TaskStatus
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo)

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
def create_task_for_project(
    project_id: int,
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    try:
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None 
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[TaskInDB])
def list_tasks_for_project(
    project_id: int,
    service: TaskService = Depends(get_task_service)
):
    return service.list_tasks_by_project(project_id)

@router.get("/{task_id}", response_model=TaskInDB)
def get_task_for_project(
    project_id: int,
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    try:
        task = service.get_task_by_id(project_id, task_id)
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{task_id}", response_model=TaskInDB)
def update_task_for_project(
    project_id: int, 
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    try:
        updated_task = service.update_task(
            project_id=project_id,
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None,
            status=task_data.status
        )
        return updated_task
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_for_project(
    project_id: int, 
    task_id: int, 
    service: TaskService = Depends(get_task_service)
):
    try:
        service.delete_task(project_id, task_id)
        return 
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
