from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.models.task import TaskStatus

# --- Task Schemas ---

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: TaskStatus = TaskStatus.TODO

class TaskInDB(TaskBase):
    id: int
    project_id: int
    status: TaskStatus
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Project Schemas ---

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectInDB(ProjectBase):
    id: int
    tasks: List[TaskInDB] = []

    class Config:
        from_attributes = True
