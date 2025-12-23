from typing import List, Optional
from typing import Optional
from typing import List, Optional
from src.cli.models.project import Project
from src.cli.exceptions.repository_exceptions import NotFoundException, AlreadyExistsException

class ProjectRepository:
    def create(self, project: Project) -> Project:
        Project._all.append(project)
        return project

    def get_all(self) -> List[Project]:
        return sorted(Project._all, key=lambda p: p.created_at)

    def get_by_id(self, project_id: int) -> Project:
        for p in Project._all:
            if p.id == project_id:
                return p
        raise NotFoundException(f"پروژه با شناسه {project_id} یافت نشد.")

    def get_by_name(self, name: str) -> Optional[Project]:
        for p in Project._all:
            if p.name == name:
                return p
        return None

    def update(self, project: Project) -> Project:
        for i, p in enumerate(Project._all):
            if p.id == project.id:
                Project._all[i] = project
                return project
        raise NotFoundException()

    def delete(self, project_id: int) -> None:
        project = self.get_by_id(project_id)
        # Cascade delete tasks
        from src.cli.repositories.task_repository import TaskRepository
        task_repo = TaskRepository()
        task_repo.delete_by_project(project_id)
        Project._all = [p for p in Project._all if p.id != project_id]
