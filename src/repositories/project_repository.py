from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.project import Project
from src.exceptions.repository_exceptions import NotFoundException

class ProjectRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def add(self, name: str, description: Optional[str]) -> Project:
        new_project = Project(name=name, description=description)
        self.session.add(new_project)
        self.session.commit()
        self.session.refresh(new_project)
        return new_project

    def get_all(self) -> List[Project]:
        return self.session.query(Project).all()

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def update(self, project: Project, name: str, description: Optional[str]) -> None:
        project.name = name
        project.description = description
        self.session.commit()
        self.session.refresh(project)

    def delete(self, project: Project) -> None:
        self.session.delete(project)
        self.session.commit()
