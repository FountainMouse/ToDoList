from typing import List, Optional
from typing import Optional
from typing import List
from src.cli.models.task import Task
from src.cli.exceptions.repository_exceptions import NotFoundException, MaxLimitExceededException
import os
from dotenv import load_dotenv

load_dotenv()
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 50))

class TaskRepository:
    def create(self, task: Task) -> Task:
        tasks_in_project = self.get_by_project(task.project_id)
        if len(tasks_in_project) >= MAX_TASKS:
            raise MaxLimitExceededException(f"حداکثر تعداد تسک در پروژه ({MAX_TASKS}) رسیده است.")
        Task._all.append(task)
        return task

    def get_by_project(self, project_id: int) -> List[Task]:
        tasks = [t for t in Task._all if t.project_id == project_id]
        return sorted(tasks, key=lambda t: t.created_at)

    def get_by_id(self, task_id: int) -> Task:
        for t in Task._all:
            if t.id == task_id:
                return t
        raise NotFoundException(f"تسک با شناسه {task_id} یافت نشد.")

    def update(self, task: Task) -> Task:
        for i, t in enumerate(Task._all):
            if t.id == task.id:
                Task._all[i] = task
                return task
        raise NotFoundException()

    def delete(self, task_id: int) -> None:
        Task._all = [t for t in Task._all if t.id != task_id]

    def delete_by_project(self, project_id: int) -> None:
        Task._all = [t for t in Task._all if t.project_id != project_id]
