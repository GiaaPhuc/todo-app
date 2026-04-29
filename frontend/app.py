import urllib.parse
import requests as http_requests
import streamlit as st
from utils.auth import is_logged_in

st.set_page_config(page_title="Todo App", page_icon="✅", layout="centered")

st.markdown("""
<style>
/* Ẩn sidebar mặc định nếu không dùng */
[data-testid="stSidebar"] { display: none; }

/* Card wrapper cho mỗi task */
.task-card {
    background: #FFF7ED;
    border: 1px solid #FDBA74;
    border-left: 4px solid #F97316;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

/* Badge priority */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
}
.badge-low      { background: #D1FAE5; color: #065F46; }
.badge-medium   { background: #FEF3C7; color: #92400E; }
.badge-high     { background: #FFEDD5; color: #9A3412; }
.badge-urgent   { background: #FEE2E2; color: #991B1B; }
.badge-tag      { background: #E0F2FE; color: #075985; }

/* Divider nhạt */
hr { border-color: #FDBA74; }
</style>
""", unsafe_allow_html=True)


def handle_google_callback(code: str):
    """Đổi authorization code lấy Firebase idToken."""
    token_resp = http_requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code":          code,
            "client_id":     st.secrets["google_login"]["client_id"],
            "client_secret": st.secrets["google_login"]["client_secret"],
            "redirect_uri":  st.secrets["google_login"]["redirect_uri"],
            "grant_type":    "authorization_code",
        },
    )
    tokens = token_resp.json()
    id_token = tokens.get("id_token")

    if not id_token:
        st.error("Không lấy được token từ Google. Vui lòng thử lại.")
        st.query_params.clear()
        st.switch_page("pages/login.py")
        return

    api_key = st.secrets["firebase_client"]["apiKey"]
    fb_resp = http_requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}",
        json={
            "postBody":            f"id_token={id_token}&providerId=google.com",
            "requestUri":          st.secrets["google_login"]["redirect_uri"],
            "returnIdpCredential": True,
            "returnSecureToken":   True,
        },
    )
    fb_data = fb_resp.json()

    if "idToken" in fb_data:
        st.session_state["id_token"]  = fb_data["idToken"]
        st.session_state["user_info"] = {"email": fb_data.get("email", "")}
        st.query_params.clear()
        st.switch_page("pages/todos.py")
    else:
        err = fb_data.get("error", {}).get("message", "Lỗi không xác định")
        st.error(f"Đăng nhập Google thất bại: {err}")
        st.query_params.clear()
        st.switch_page("pages/login.py")


# --- Xử lý Google OAuth callback ---
if "code" in st.query_params:
    with st.spinner("Đang xác thực với Google..."):
        handle_google_callback(st.query_params["code"])
    st.stop()

# --- Đã đăng nhập → thẳng vào todos ---
if is_logged_in():
    st.switch_page("pages/todos.py")

# --- Landing page (chưa đăng nhập) ---
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <span style='font-size: 3.5rem;'>✅</span>
        <h1 style='font-size: 2.5rem; margin: 0.25rem 0 0.5rem 0;'>Todo App</h1>
        <p style='font-size: 1.1rem; color: #666;'>Quản lý công việc đơn giản, hiệu quả.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("### ➕ Thêm task")
    st.write("Tạo công việc mới với tiêu đề và mô tả chỉ trong vài giây.")
with col_b:
    st.markdown("### 📋 Xem task")
    st.write("Danh sách toàn bộ công việc, lọc theo trạng thái dễ dàng.")
with col_c:
    st.markdown("### 🔄 Cập nhật")
    st.write("Chuyển trạng thái từ Pending → In Progress → Done linh hoạt.")

st.divider()

col_left, col_mid, col_right = st.columns([1, 1, 1])
with col_mid:
    if st.button("Bắt đầu", use_container_width=True, type="primary"):
        st.switch_page("pages/login.py")
