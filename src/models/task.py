import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    status = Column(
        SQLEnum(TaskStatus, values_callable=lambda x: [e.value for e in x], create_type=False, native_enum=False),
        default=TaskStatus.TODO.value,
        nullable=False
    )
    deadline = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)  # Important for auto-close feature

    project = relationship("Project", back_populates="tasks")

    def __str__(self):
        dl = self.deadline.isoformat() if self.deadline else "None"
        return f"Task {self.id}: {self.title} ({self.status.value}) Deadline: {dl}"
