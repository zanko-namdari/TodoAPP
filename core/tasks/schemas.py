from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskBaseSchema(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Bread, Eggs")
    due_date: Optional[datetime] = Field(None, example="2024-12-31T23:59:59Z")
    status: Optional[StatusEnum] = Field(StatusEnum.pending, example="pending")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[StatusEnum]


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2024-01-01T12:00:00Z")
    updated_at: datetime = Field(..., example="2024-01-02T12:00:00Z")
