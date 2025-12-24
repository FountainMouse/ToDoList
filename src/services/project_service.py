from src.repositories.project_repository import ProjectRepository
from src.exceptions.repository_exceptions import NotFoundException
from src.models.project import Project
from typing import List, Optional

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, description: Optional[str]) -> Project:
        if len(name.split()) > 30:  # From Phase 1 PDF
            raise ValueError("نام پروژه باید کمتر از ۳۰ کلمه باشد.")
        return self.repo.add(name=name, description=description)

    def list_projects(self) -> List[Project]:
        return self.repo.get_all()

    def update_project(self, project_id: int, name: str, description: Optional[str]) -> Project:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"پروژه با شناسه {project_id} یافت نشد.")
        if len(name.split()) > 30:
            raise ValueError("نام پروژه باید کمتر از ۳۰ کلمه باشد.")
        self.repo.update(project=project, name=name, description=description)
        return project

    def delete_project(self, project_id: int):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"پروژه با شناسه {project_id} یافت نشد.")
        self.repo.delete(project)
