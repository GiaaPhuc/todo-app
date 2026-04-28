import urllib.parse
import streamlit as st
import pyrebase

st.set_page_config(page_title="Todo App — Đăng nhập", page_icon="✅", layout="centered")

# --- Firebase init ---
try:
    firebase_config = dict(st.secrets["firebase_client"])
    if "databaseURL" not in firebase_config:
        firebase_config["databaseURL"] = ""
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
except Exception:
    st.error("Chưa cấu hình Firebase. Vui lòng điền thông tin vào `.streamlit/secrets.toml`.")
    st.stop()


def get_google_auth_url() -> str:
    params = {
        "client_id":     st.secrets["google_login"]["client_id"],
        "redirect_uri":  st.secrets["google_login"]["redirect_uri"],
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "offline",
        "prompt":        "select_account",
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)


# --- UI ---
st.title("Todo App")
st.subheader("Đăng nhập")

email    = st.text_input("Email")
password = st.text_input("Mật khẩu", type="password")

col_login, col_signup = st.columns(2)

with col_login:
    if st.button("Đăng nhập", use_container_width=True):
        if not email or not password:
            st.warning("Vui lòng nhập email và mật khẩu.")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["id_token"]  = user["idToken"]
                st.session_state["user_info"] = {"email": email}
                st.switch_page("pages/todos.py")
            except Exception:
                st.error("Sai email hoặc mật khẩu.")

with col_signup:
    if st.button("Đăng ký", use_container_width=True):
        st.switch_page("pages/signup.py")

st.divider()

# --- Google Login ---
google_url = get_google_auth_url()
st.link_button("Đăng nhập bằng Google", url=google_url, use_container_width=True)
