from fastapi import APIRouter, Depends
from dependencies import get_current_user

router = APIRouter()

@router.post("/login")
def login(user: dict = Depends(get_current_user)):
    return {"message": "Login successful", "user": user}

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user
