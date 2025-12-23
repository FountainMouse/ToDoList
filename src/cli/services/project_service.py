from typing import List, Optional
from typing import Optional
from src.cli.models.project import Project
from src.cli.repositories.project_repository import ProjectRepository
from src.cli.exceptions.repository_exceptions import AlreadyExistsException, MaxLimitExceededException
import os
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()
MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))

class ProjectService:
    def __init__(self, repo: ProjectRepository = ProjectRepository()):
        self.repo = repo

    def create(self, name: str, description: Optional[str]) -> Project:
        if len(self.repo.get_all()) >= MAX_PROJECTS:
            raise MaxLimitExceededException(f"حداکثر تعداد پروژه ({MAX_PROJECTS}) رسیده است.")
        if self.repo.get_by_name(name):
            raise AlreadyExistsException("پروژه‌ای با این نام وجود دارد.")
        project = Project(name=name, description=description)
        return self.repo.create(project)

    def list(self) -> List[Project]:
        return self.repo.get_all()

    def update(self, project_id: int, name: str, description: Optional[str]) -> Project:
        project = self.repo.get_by_id(project_id)
        if name != project.name and self.repo.get_by_name(name):
            raise AlreadyExistsException("نام جدید تکراری است.")
        project.name = name
        project.description = description
        return self.repo.update(project)

    def delete(self, project_id: int) -> None:
        self.repo.delete(project_id)
