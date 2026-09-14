"""Pydantic schemas define the shape of data in/out of the API."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """What the client sends when creating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)


class Task(BaseModel):
    """What the API returns for a task."""

    id: int
    title: str
    description: str = ""
    completed: bool = False
