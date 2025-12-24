from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.models.task import TaskStatus
from datetime import datetime

class AutocloseOverdueTasksCommand:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def execute(self) -> int:
        closed_count = 0
        overdue_tasks = self.task_repo.get_overdue_and_open_tasks()
        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = datetime.now()
            self.task_repo.session.commit()
            closed_count += 1
        return closed_count
