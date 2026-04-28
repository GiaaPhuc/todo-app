from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, todos
from services.firebase_admin import init_firebase

app = FastAPI(title="Todo App API")
init_firebase()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])

@app.get("/")
def root():
    return {"message": "Todo App API is running", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
