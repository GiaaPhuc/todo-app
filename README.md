# Todo App

Dự án Todo App tích hợp Streamlit (Frontend), FastAPI (Backend) và Firebase.

## 1. Cấu trúc
- `frontend/`: Giao diện ứng dụng viết bằng Streamlit.
- `backend/`: API Backend viết bằng FastAPI.

## 2. Cài đặt

Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## 3. Cấu hình
1. Thêm cấu hình frontend vào file `frontend/.streamlit/secrets.toml`.
2. Thêm credentials backend vào thư mục `backend/` với tên `firebase-adminsdk.json` và cấu hình trong file `backend/.env`.

## 4. Chạy ứng dụng

**Chạy Backend (FastAPI):**
```bash
cd backend
uvicorn main:app --reload
```

**Chạy Frontend (Streamlit):**
```bash
cd frontend
streamlit run app.py
```
