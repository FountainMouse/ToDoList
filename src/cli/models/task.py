from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from dateutil.parser import parse

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(BaseModel):
    id: int = Field(default_factory=lambda: len(Task._all) + 1)
    project_id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    _all: List['Task'] = []  # In-memory store

    @validator('title')
    def title_word_limit(cls, v):
        if len(v.split()) > 30:
            raise ValueError("عنوان تسک نمی‌تواند بیش از ۳۰ کلمه باشد.")
        return v

    @validator('description')
    def desc_word_limit(cls, v):
        if v and len(v.split()) > 150:
            raise ValueError("توضیحات تسک نمی‌تواند بیش از ۱۵۰ کلمه باشد.")
        return v

    @validator('deadline', pre=True)
    def parse_deadline(cls, v):
        if not v:
            return None
        try:
            dt = parse(v)
            if dt <= datetime.now():
                raise ValueError("مهلت زمانی باید در آینده باشد.")
            return dt
        except Exception:
            raise ValueError("فرمت مهلت زمانی نامعتبر است (مثال: 2025-12-31 14:30)")
