from typing import List, Optional
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class Project(BaseModel):
    id: int = Field(default_factory=lambda: len(Project._all) + 1)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    tasks: List['Task'] = Field(default=[])

    _all: List['Project'] = []  # In-memory store

    @validator('name')
    def name_word_limit(cls, v):
        if len(v.split()) > 30:
            raise ValueError("نام پروژه نمی‌تواند بیش از ۳۰ کلمه باشد.")
        return v

    @validator('description')
    def desc_word_limit(cls, v):
        if v and len(v.split()) > 150:
            raise ValueError("توضیحات پروژه نمی‌تواند بیش از ۱۵۰ کلمه باشد.")
        return v
