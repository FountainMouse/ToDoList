from src.repositories.task_repository import TaskRepository
from src.exceptions.repository_exceptions import NotFoundException
from src.models.task import Task, TaskStatus
from typing import List, Optional
from datetime import datetime
from dateutil import parser as date_parser

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def get_task_by_id(self, project_id: int, task_id: int) -> Task:
        task = self.task_repo.get_by_id(project_id, task_id)
        if not task:
            raise NotFoundException(f"تسک با شناسه {task_id} در پروژه {project_id} یافت نشد.")
        return task

    def create_task(self, project_id: int, title: str, description: Optional[str], deadline: Optional[str]) -> Task:
        deadline_dt = date_parser.parse(deadline) if deadline else None
        return self.task_repo.add(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline_dt
        )

    def list_tasks_by_project(self, project_id: int) -> List[Task]:
        return self.task_repo.get_by_project(project_id)

    def update_task(self, project_id: int, task_id: int, title: str, description: Optional[str], deadline: Optional[str], status: TaskStatus) -> Task:
        task = self.task_repo.get_by_id(project_id, task_id)
        if not task:
            raise NotFoundException(f"تسک با شناسه {task_id} در پروژه {project_id} یافت نشد.")

        deadline_dt = date_parser.parse(deadline) if deadline else None
        closed_at = task.closed_at

        if status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            closed_at = datetime.now()
        elif status != TaskStatus.DONE and task.closed_at:
            closed_at = None

        self.task_repo.update(
            task=task,
            title=title,
            description=description,
            deadline=deadline_dt,
            status=status,
            closed_at=closed_at
        )
        return task

    def delete_task(self, project_id: int, task_id: int):
        task = self.task_repo.get_by_id(project_id, task_id)
        if not task:
            raise NotFoundException(f"تسک با شناسه {task_id} در پروژه {project_id} یافت نشد.")
        self.task_repo.delete(task)
