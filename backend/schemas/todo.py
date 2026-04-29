from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"       # "low" | "medium" | "high" | "urgent"
    due_date: Optional[str] = None           # "YYYY-MM-DD"
    assignee: Optional[str] = ""
    tags: Optional[List[str]] = []
    notes: Optional[str] = ""


class TodoUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class TodoResponse(BaseModel):
    id: str
    title: str
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[str] = None
    assignee: str = ""
    tags: List[str] = []
    notes: str = ""
    user_id: str
    created_at: datetime
