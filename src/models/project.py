from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __str__(self):
        return f"Project {self.id}: {self.name}"
