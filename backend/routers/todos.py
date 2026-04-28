from fastapi import APIRouter, Depends
from schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from services.firestore import create_todo, get_todos, update_todo_status, delete_todo
from dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=TodoResponse)
def create_todo_endpoint(todo: TodoCreate, user: dict = Depends(get_current_user)):
    result = create_todo(user["uid"], todo.title, todo.description)
    return result

@router.get("/", response_model=list[TodoResponse])
def get_todos_endpoint(user: dict = Depends(get_current_user)):
    return get_todos(user["uid"])

@router.patch("/{todo_id}")
def update_todo_endpoint(todo_id: str, todo_update: TodoUpdate, user: dict = Depends(get_current_user)):
    update_todo_status(todo_id, todo_update.status)
    return {"status": "success"}

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str, user: dict = Depends(get_current_user)):
    delete_todo(todo_id)
    return {"status": "success"}
