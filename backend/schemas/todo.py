from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoUpdate(BaseModel):
    status: str  # "pending" | "in_progress" | "done"

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    user_id: str
    created_at: datetime
