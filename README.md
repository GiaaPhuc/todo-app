# Todo App

Ứng dụng quản lý công việc (To-do) được xây dựng theo kiến trúc tách biệt Frontend – Backend, tích hợp Firebase Authentication và Firestore.

---

## Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Công nghệ sử dụng](#2-công-nghệ-sử-dụng)
3. [Cấu trúc dự án](#3-cấu-trúc-dự-án)
4. [Tính năng](#4-tính-năng)
5. [API Endpoints](#5-api-endpoints)
6. [Cài đặt môi trường](#6-cài-đặt-môi-trường)
7. [Cấu hình Firebase](#7-cấu-hình-firebase)
8. [Chạy Backend](#8-chạy-backend)
9. [Chạy Frontend](#9-chạy-frontend)
10. [Video Demo](#10-video-demo)

---

## 1. Giới thiệu

Todo App là ứng dụng nhỏ cho phép người dùng:

- Đăng ký / đăng nhập bằng **Email & Password** hoặc **Google OAuth** thông qua Firebase Authentication.
- Thêm, xem, cập nhật trạng thái và xóa công việc (task) của cá nhân.
- Dữ liệu task được lưu trữ và đọc từ **Cloud Firestore**, riêng biệt theo từng người dùng.

---

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Frontend | Python · Streamlit · Pyrebase4 |
| Backend | Python · FastAPI · Uvicorn |
| Xác thực | Firebase Authentication (Email/Password, Google OAuth) |
| Database | Cloud Firestore (Firebase) |
| Xác thực token | Firebase Admin SDK |

---

## 3. Cấu trúc dự án

```
todo-app/
├── backend/
│   ├── routers/
│   │   ├── auth.py          # Endpoint /auth/login, /auth/me
│   │   └── todos.py         # Endpoint CRUD /todos
│   ├── schemas/
│   │   └── todo.py          # Pydantic schemas (TodoCreate, TodoUpdate, TodoResponse)
│   ├── services/
│   │   ├── firebase_admin.py  # Khởi tạo Firebase Admin SDK
│   │   └── firestore.py       # Thao tác với Cloud Firestore
│   ├── dependencies.py      # Dependency xác thực Bearer token
│   ├── main.py              # Khởi tạo FastAPI app, đăng ký router
│   └── .env                 # Biến môi trường backend (không commit)
├── frontend/
│   ├── pages/
│   │   ├── login.py         # Trang đăng nhập (Email/Password + Google)
│   │   ├── signup.py        # Trang đăng ký tài khoản mới
│   │   └── todos.py         # Trang quản lý task
│   ├── utils/
│   │   ├── api.py           # Hàm gọi Backend API
│   │   └── auth.py          # Hàm kiểm tra trạng thái đăng nhập / đăng xuất
│   ├── app.py               # Landing page, xử lý Google OAuth callback
│   └── .streamlit/
│       └── secrets.toml     # Cấu hình Firebase client (không commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 4. Tính năng

### Xác thực người dùng
- **Đăng ký** tài khoản mới bằng Email & Password.
- **Đăng nhập** bằng Email & Password hoặc **Google OAuth 2.0**.
- **Đăng xuất** và xóa session hiện tại.
- Nhận diện người dùng sau khi đăng nhập qua Firebase ID Token.

### Quản lý Task (feature chính)
- **Thêm task**: nhập tên và mô tả, lưu vào Firestore với trạng thái `pending`.
- **Xem danh sách task**: hiển thị toàn bộ task của người dùng đang đăng nhập.
- **Cập nhật trạng thái**: chuyển qua ba mức `Pending → In Progress → Done`.
- **Xóa task**: xóa task khỏi Firestore.

---

## 5. API Endpoints

| Method | Endpoint | Mô tả | Xác thực |
|---|---|---|---|
| GET | `/` | Kiểm tra server đang chạy | Không |
| GET | `/health` | Health check | Không |
| POST | `/auth/login` | Xác thực token, trả thông tin user | Bearer Token |
| GET | `/auth/me` | Lấy thông tin người dùng hiện tại | Bearer Token |
| POST | `/todos/` | Tạo task mới | Bearer Token |
| GET | `/todos/` | Lấy danh sách task của user | Bearer Token |
| PATCH | `/todos/{todo_id}` | Cập nhật trạng thái task | Bearer Token |
| DELETE | `/todos/{todo_id}` | Xóa task | Bearer Token |

> Tài liệu API tương tác đầy đủ có tại: `http://127.0.0.1:8000/docs` (Swagger UI) sau khi chạy backend.

---

## 6. Cài đặt môi trường

### Yêu cầu
- Python **3.10** trở lên
- `pip`

### Bước 1 — Clone repository

```bash
git clone <repository-url>
cd todo-app
```

### Bước 2 — Tạo và kích hoạt virtual environment (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Bước 3 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

## 7. Cấu hình Firebase

### 7.1 Backend — Firebase Admin SDK

1. Vào [Firebase Console](https://console.firebase.google.com) → Project Settings → **Service accounts**.
2. Nhấn **Generate new private key** → tải file JSON về.
3. Đặt file vào thư mục `backend/` với tên `firebase-adminsdk.json`.
4. Tạo file `backend/.env` với nội dung:

```env
FIREBASE_CREDENTIALS=firebase-adminsdk.json
```

### 7.2 Frontend — Firebase Client SDK & Google OAuth

1. Vào Firebase Console → Project Settings → **Your apps** → Web app → lấy `firebaseConfig`.
2. Vào [Google Cloud Console](https://console.cloud.google.com) → **APIs & Services → Credentials** → tạo OAuth 2.0 Client ID (Web application), thêm `http://localhost:8501` vào **Authorized redirect URIs**.
3. Tạo file `frontend/.streamlit/secrets.toml` với nội dung:

```toml
[firebase_client]
apiKey            = "YOUR_API_KEY"
authDomain        = "YOUR_PROJECT.firebaseapp.com"
projectId         = "YOUR_PROJECT_ID"
storageBucket     = "YOUR_PROJECT.appspot.com"
messagingSenderId = "YOUR_SENDER_ID"
appId             = "YOUR_APP_ID"

[google_login]
client_id     = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
redirect_uri  = "http://localhost:8501"
```

> **Lưu ý bảo mật:** Không commit `firebase-adminsdk.json`, `.env` và `secrets.toml` lên repository (đã được liệt kê trong `.gitignore`).

---

## 8. Chạy Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend khởi động tại `http://127.0.0.1:8000`.

Kiểm tra nhanh:

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

---

## 9. Chạy Frontend

Mở terminal **mới** (giữ nguyên terminal backend đang chạy):

```bash
cd frontend
streamlit run app.py
```

Frontend mở tại `http://localhost:8501`.

---

## 10. Video Demo

> **Link video demo:** *(Cập nhật sau khi quay xong)*

Video demo thể hiện:
1. Giới thiệu ứng dụng và cấu trúc dự án.
2. Khởi động Backend (FastAPI).
3. Khởi động Frontend (Streamlit).
4. Đăng ký tài khoản mới.
5. Đăng nhập bằng Email/Password và Google OAuth.
6. Demo feature chính: thêm, xem, cập nhật trạng thái và xóa task.
7. Minh họa dữ liệu được lưu và đọc từ Cloud Firestore.
8. Đăng xuất.
