from firebase_admin import firestore
from datetime import datetime, timezone


def _db():
    """Lazy Firestore client — Firebase must be initialized before calling."""
    return firestore.client()


def create_todo(user_id: str, data: dict) -> dict:
    doc_ref = _db().collection("todos").document()
    payload = {
        "title":       data.get("title"),
        "description": data.get("description", ""),
        "status":      "pending",
        "priority":    data.get("priority", "medium"),
        "due_date":    data.get("due_date", None),
        "assignee":    data.get("assignee", ""),
        "tags":        data.get("tags", []),
        "notes":       data.get("notes", ""),
        "user_id":     user_id,
        "created_at":  datetime.now(timezone.utc),
    }
    doc_ref.set(payload)
    return {"id": doc_ref.id, **payload}


def get_todos(user_id: str) -> list:
    docs = (
        _db()
        .collection("todos")
        .where("user_id", "==", user_id)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def update_todo(todo_id: str, fields: dict):
    _db().collection("todos").document(todo_id).update(fields)


def delete_todo(todo_id: str):
    _db().collection("todos").document(todo_id).delete()
