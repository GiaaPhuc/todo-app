import requests
from utils.auth import get_auth_header, BACKEND_URL


def get_todos() -> list:
    r = requests.get(f"{BACKEND_URL}/todos", headers=get_auth_header())
    return r.json() if r.ok else []


def create_todo(title, description="", priority="medium",
                due_date=None, assignee="", tags=[], notes="") -> dict:
    payload = {
        "title":       title,
        "description": description,
        "priority":    priority,
        "due_date":    due_date,
        "assignee":    assignee,
        "tags":        tags,
        "notes":       notes,
    }
    r = requests.post(f"{BACKEND_URL}/todos",
                      json=payload, headers=get_auth_header())
    return r.json() if r.ok else {}


def update_todo(todo_id: str, fields: dict):
    requests.patch(f"{BACKEND_URL}/todos/{todo_id}",
                   json=fields, headers=get_auth_header())


def delete_todo(todo_id: str):
    requests.delete(f"{BACKEND_URL}/todos/{todo_id}",
                    headers=get_auth_header())
