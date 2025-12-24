from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.models.task import Task, TaskStatus
from src.exceptions.repository_exceptions import NotFoundException

class TaskRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def add(self, project_id: int, title: str, description: Optional[str], deadline: Optional[datetime]) -> Task:
        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline
        )
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task

    def get_by_project(self, project_id: int) -> List[Task]:
        return self.session.query(Task).filter(Task.project_id == project_id).all()

    def get_by_id(self, project_id: int, task_id: int) -> Optional[Task]:
        return self.session.query(Task).filter(
            Task.id == task_id,
            Task.project_id == project_id
        ).first()

    def update(
        self,
        task: Task,
        title: str,
        description: Optional[str],
        deadline: Optional[datetime],
        status: TaskStatus,
        closed_at: Optional[datetime]
    ) -> None:
        task.title = title
        task.description = description
        task.deadline = deadline
        task.status = status
        task.closed_at = closed_at
        self.session.commit()
        self.session.refresh(task)

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def get_overdue_and_open_tasks(self) -> List[Task]:
        now = datetime.now()
        return self.session.query(Task).filter(
            Task.deadline < now,
            Task.status.in_([TaskStatus.TODO, TaskStatus.DOING])
        ).all()
