from fastapi import APIRouter, Depends
from schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from services.firestore import create_todo, get_todos, update_todo, delete_todo
from dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=TodoResponse)
async def create(body: TodoCreate, user=Depends(get_current_user)):
    return create_todo(user["uid"], body.dict())


@router.get("/", response_model=list[TodoResponse])
async def read_all(user=Depends(get_current_user)):
    return get_todos(user["uid"])


@router.patch("/{todo_id}")
async def update(todo_id: str, body: TodoUpdate, user=Depends(get_current_user)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    update_todo(todo_id, fields)
    return {"message": "updated"}


@router.delete("/{todo_id}")
async def delete(todo_id: str, user=Depends(get_current_user)):
    delete_todo(todo_id)
    return {"status": "success"}
