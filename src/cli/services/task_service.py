from typing import List, Optional
from typing import Optional
from src.cli.models.task import Task, TaskStatus
from src.cli.repositories.task_repository import TaskRepository
from src.cli.repositories.project_repository import ProjectRepository
from src.cli.exceptions.repository_exceptions import NotFoundException, InvalidStatusTransitionException
from typing import Optional, List

class TaskService:
    def __init__(self, task_repo: TaskRepository = TaskRepository(), project_repo: ProjectRepository = ProjectRepository()):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def create(self, project_id: int, title: str, description: Optional[str], deadline_str: Optional[str]) -> Task:
        self.project_repo.get_by_id(project_id)  # Check project exists
        task = Task(project_id=project_id, title=title, description=description, deadline=deadline_str)
        return self.task_repo.create(task)

    def list_by_project(self, project_id: int) -> List[Task]:
        self.project_repo.get_by_id(project_id)
        return self.task_repo.get_by_project(project_id)

    def update(self, task_id: int, title: str, description: Optional[str], deadline_str: Optional[str], status_str: Optional[str]) -> Task:
        task = self.task_repo.get_by_id(task_id)
        task.title = title
        task.description = description
        if deadline_str:
            task.deadline = deadline_str  # Validator handles
        if status_str:
            new_status = TaskStatus(status_str.lower())
            if task.status == TaskStatus.DONE and new_status != TaskStatus.DONE:
                raise InvalidStatusTransitionException("نمی‌توان وضعیت تسک تکمیل‌شده را تغییر داد.")
            task.status = new_status
        return self.task_repo.update(task)

    def change_status(self, task_id: int, status_str: str) -> Task:
        task = self.task_repo.get_by_id(task_id)
        new_status = TaskStatus(status_str.lower())
        if task.status == TaskStatus.DONE and new_status != TaskStatus.DONE:
            raise InvalidStatusTransitionException("نمی‌توان وضعیت تسک تکمیل‌شده را تغییر داد.")
        task.status = new_status
        return self.task_repo.update(task)

    def delete(self, task_id: int) -> None:
        self.task_repo.delete(task_id)
