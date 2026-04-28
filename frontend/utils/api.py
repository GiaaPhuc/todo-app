import requests
from utils.auth import get_auth_header, BACKEND_URL


def get_todos() -> list:
    r = requests.get(f"{BACKEND_URL}/todos", headers=get_auth_header())
    return r.json() if r.ok else []


def create_todo(title: str, description: str) -> dict:
    r = requests.post(
        f"{BACKEND_URL}/todos",
        json={"title": title, "description": description},
        headers=get_auth_header(),
    )
    return r.json() if r.ok else {}


def update_todo(todo_id: str, status: str):
    requests.patch(
        f"{BACKEND_URL}/todos/{todo_id}",
        json={"status": status},
        headers=get_auth_header(),
    )


def delete_todo(todo_id: str):
    requests.delete(
        f"{BACKEND_URL}/todos/{todo_id}",
        headers=get_auth_header(),
    )
