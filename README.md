<div align="center">

# ✅ Todo App

**Ứng dụng quản lý công việc cá nhân** — kiến trúc tách biệt Frontend / Backend,  
xác thực Firebase, lưu trữ Cloud Firestore, giao diện Streamlit theme cam nhạt.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-Auth%20%2B%20Firestore-FFCA28?style=flat-square&logo=firebase&logoColor=black)

---

👤 **Tác giả:** Võ Gia Phúc &nbsp;|&nbsp; 🎓 **Lớp:** 24CTT3 &nbsp;|&nbsp; 🏫 **Trường:** Đại học Khoa học Tự nhiên — ĐHQG TP.HCM

</div>

---

## 📑 Mục lục

| # | Mục |
|---|-----|
| 1 | [Giới thiệu](#1--giới-thiệu) |
| 2 | [Công nghệ sử dụng](#2--công-nghệ-sử-dụng) |
| 3 | [Cấu trúc dự án](#3--cấu-trúc-dự-án) |
| 4 | [Tính năng](#4--tính-năng) |
| 5 | [API Endpoints](#5--api-endpoints) |
| 6 | [Cài đặt môi trường](#6--cài-đặt-môi-trường) |
| 7 | [Cấu hình Firebase](#7--cấu-hình-firebase) |
| 8 | [Chạy ứng dụng](#8--chạy-ứng-dụng) |
| 9 | [Video Demo](#9--video-demo) |

---

## 1 · Giới thiệu

**Todo App** là ứng dụng quản lý công việc cá nhân cho phép người dùng:

- 🔐 Đăng ký / đăng nhập bằng **Email & Password** hoặc **Google OAuth 2.0** qua Firebase Authentication.
- 📝 Thêm task với đầy đủ thuộc tính: tên, mô tả, độ ưu tiên, trạng thái, ngày hết hạn, người phụ trách, tags và ghi chú.
- 📋 Xem, lọc, cập nhật và xóa task cá nhân.
- ☁️ Dữ liệu lưu trữ trên **Cloud Firestore**, phân tách riêng biệt theo từng người dùng.

---

## 2 · Công nghệ sử dụng

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| 🖥️ Frontend | Python · Streamlit · Pyrebase4 | Giao diện người dùng |
| ⚙️ Backend | Python · FastAPI · Uvicorn | REST API server |
| 🔐 Xác thực | Firebase Authentication | Email/Password · Google OAuth |
| 🗄️ Database | Cloud Firestore | Lưu trữ task theo user |
| 🛡️ Token | Firebase Admin SDK | Xác thực Bearer token |

---

## 3 · Cấu trúc dự án

```
todo-app/
├── backend/
│   ├── routers/
│   │   ├── auth.py            # Endpoint /auth/login, /auth/me
│   │   └── todos.py           # Endpoint CRUD /todos
│   ├── schemas/
│   │   └── todo.py            # Pydantic schemas: TodoCreate, TodoUpdate, TodoResponse
│   ├── services/
│   │   ├── firebase_admin.py  # Khởi tạo Firebase Admin SDK
│   │   └── firestore.py       # Thao tác với Cloud Firestore
│   ├── dependencies.py        # Dependency xác thực Bearer token
│   ├── main.py                # Khởi tạo FastAPI app, đăng ký router
│   └── .env                   # Biến môi trường backend (⚠️ không commit)
│
└── frontend/
    ├── pages/
    │   ├── login.py           # Trang đăng nhập (Email/Password + Google)
    │   ├── signup.py          # Trang đăng ký tài khoản mới
    │   └── todos.py           # Trang quản lý task (layout 2 cột, card HTML)
    ├── utils/
    │   ├── api.py             # Hàm gọi Backend API
    │   └── auth.py            # Kiểm tra trạng thái đăng nhập / đăng xuất
    ├── app.py                 # Landing page, xử lý Google OAuth callback
    └── .streamlit/
        ├── config.toml        # Theme giao diện (trắng + cam nhạt)
        └── secrets.toml       # Cấu hình Firebase client (⚠️ không commit)
```

---

## 4 · Tính năng

### 🔐 Xác thực người dùng

| Tính năng | Mô tả |
|---|---|
| Đăng ký | Tạo tài khoản mới bằng Email & Password |
| Đăng nhập | Email & Password hoặc Google OAuth 2.0 |
| Đăng xuất | Xóa session, quay về landing page |
| Bảo mật | Mọi request tới API đều xác thực qua Firebase ID Token |

### 📋 Quản lý Task

| Tính năng | Chi tiết |
|---|---|
| ➕ Thêm task | Tên · Mô tả · Độ ưu tiên · Trạng thái ban đầu · Ngày hết hạn · Người phụ trách · Tags · Ghi chú/Sub-tasks |
| 👁️ Xem danh sách | Hiển thị dạng **card** với badge priority, status và tags màu sắc |
| 🔍 Lọc task | Theo **trạng thái** (`Pending / In Progress / Done`) hoặc **độ ưu tiên** (`Low / Medium / High / Urgent`) |
| ✏️ Cập nhật | Thay đổi trạng thái task trực tiếp từ danh sách |
| 🗑️ Xóa task | Xóa vĩnh viễn khỏi Firestore |

### 🎨 Giao diện

- Theme sáng với màu chủ đạo **cam** `#F97316`, nền trắng `#FFFFFF` và nền phụ `#FFF7ED`.
- Mỗi task hiển thị dạng **card** có viền cam, badge priority/status/tags màu khác nhau theo mức độ.
- Layout **2 cột**: form thêm task (trái) và danh sách task (phải).

---

## 5 · API Endpoints

> 📖 Tài liệu Swagger UI đầy đủ tại: **`http://127.0.0.1:8000/docs`** (sau khi chạy backend)

| Method | Endpoint | Mô tả | Auth |
|---|---|---|:---:|
| `GET` | `/` | Kiểm tra server | — |
| `GET` | `/health` | Health check | — |
| `POST` | `/auth/login` | Xác thực token, trả thông tin user | 🔐 |
| `GET` | `/auth/me` | Lấy thông tin người dùng hiện tại | 🔐 |
| `POST` | `/todos/` | Tạo task mới | 🔐 |
| `GET` | `/todos/` | Lấy danh sách task của user | 🔐 |
| `PATCH` | `/todos/{todo_id}` | Cập nhật field của task | 🔐 |
| `DELETE` | `/todos/{todo_id}` | Xóa task | 🔐 |

<details>
<summary>📦 Request body — <code>POST /todos/</code></summary>

```json
{
  "title":       "Tên task (bắt buộc)",
  "description": "Mô tả chi tiết",
  "priority":    "low | medium | high | urgent",
  "due_date":    "YYYY-MM-DD",
  "assignee":    "Tên / email người phụ trách",
  "tags":        ["work", "urgent"],
  "notes":       "Ghi chú hoặc sub-tasks"
}
```

</details>

<details>
<summary>📦 Request body — <code>PATCH /todos/{todo_id}</code></summary>

```json
{
  "status":   "pending | in_progress | done",
  "priority": "low | medium | high | urgent",
  "due_date": "YYYY-MM-DD",
  "assignee": "...",
  "tags":     ["..."],
  "notes":    "..."
}
```

> Chỉ cần truyền các field cần cập nhật — các field bỏ trống sẽ được bỏ qua.

</details>

---

## 6 · Cài đặt môi trường

### Yêu cầu

- Python **3.10** trở lên
- `pip`

### Bước 1 — Clone repository

```bash
git clone <repository-url>
cd todo-app
```

### Bước 2 — Tạo virtual environment *(khuyến nghị)*

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

## 7 · Cấu hình Firebase

### 7.1 Backend — Firebase Admin SDK

1. Vào [Firebase Console](https://console.firebase.google.com) → **Project Settings** → **Service accounts**.
2. Nhấn **Generate new private key** → tải file JSON về.
3. Đặt file vào `backend/` với tên `firebase-adminsdk.json`.
4. Tạo file `backend/.env`:

```env
FIREBASE_CREDENTIALS=firebase-adminsdk.json
```

### 7.2 Frontend — Firebase Client SDK & Google OAuth

1. Vào Firebase Console → **Project Settings** → **Your apps** → Web app → lấy `firebaseConfig`.
2. Vào [Google Cloud Console](https://console.cloud.google.com) → **APIs & Services → Credentials** → tạo **OAuth 2.0 Client ID** (Web application).  
   Thêm `http://localhost:8501` vào **Authorized redirect URIs**.
3. Tạo file `frontend/.streamlit/secrets.toml`:

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

> ✅ File `frontend/.streamlit/config.toml` (theme giao diện) đã có sẵn trong repo — không cần tạo lại.

> ⚠️ **Bảo mật:** Không commit `firebase-adminsdk.json`, `.env` và `secrets.toml` lên repository (đã có trong `.gitignore`).

---

## 8 · Chạy ứng dụng

### ⚙️ Backend

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

### 🖥️ Frontend

Mở **terminal mới** (giữ nguyên terminal backend):

```bash
cd frontend
streamlit run app.py
```

Frontend mở tại `http://localhost:8501`.

---

## 9 · Video Demo

> 🎬 **Link video demo:** *(Cập nhật sau khi quay xong)*

Nội dung demo:

1. Giới thiệu ứng dụng và cấu trúc dự án.
2. Khởi động Backend (FastAPI) và Frontend (Streamlit).
3. Đăng ký tài khoản mới.
4. Đăng nhập bằng Email/Password và Google OAuth.
5. Thêm task với đầy đủ thuộc tính (priority, due date, assignee, tags, ghi chú).
6. Lọc task theo trạng thái và độ ưu tiên.
7. Cập nhật trạng thái và xóa task.
8. Minh họa dữ liệu lưu / đọc từ Cloud Firestore.
9. Đăng xuất.

---

<div align="center">

Made with ❤️ using **FastAPI** + **Streamlit** + **Firebase**

**Võ Gia Phúc** · Lớp 24CTT3 · Đại học Khoa học Tự nhiên — ĐHQG TP.HCM

</div>
