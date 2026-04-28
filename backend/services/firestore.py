from firebase_admin import firestore
from datetime import datetime, timezone


def _db():
    """Lazy Firestore client — Firebase must be initialized before calling."""
    return firestore.client()


def create_todo(user_id: str, title: str, description: str) -> dict:
    doc_ref = _db().collection("todos").document()
    data = {
        "title": title,
        "description": description,
        "status": "pending",
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
    }
    doc_ref.set(data)
    return {"id": doc_ref.id, **data}


def get_todos(user_id: str) -> list:
    docs = (
        _db()
        .collection("todos")
        .where("user_id", "==", user_id)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def update_todo_status(todo_id: str, status: str):
    _db().collection("todos").document(todo_id).update({"status": status})


def delete_todo(todo_id: str):
    _db().collection("todos").document(todo_id).delete()
