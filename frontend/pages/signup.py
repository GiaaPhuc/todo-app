import streamlit as st
import pyrebase

st.set_page_config(page_title="Todo App — Đăng ký", page_icon="✅", layout="centered")

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

# --- UI ---
st.title("Todo App")
st.subheader("Tạo tài khoản mới")

email    = st.text_input("Email")
password = st.text_input("Mật khẩu", type="password")
confirm  = st.text_input("Xác nhận mật khẩu", type="password")

if st.button("Đăng ký", use_container_width=True):
    if not email or not password or not confirm:
        st.warning("Vui lòng điền đầy đủ thông tin.")
    elif password != confirm:
        st.error("Mật khẩu xác nhận không khớp.")
    elif len(password) < 6:
        st.error("Mật khẩu phải có ít nhất 6 ký tự.")
    else:
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Tạo tài khoản thành công!")
            st.info("Đang chuyển về trang đăng nhập...")
            st.switch_page("pages/login.py")
        except Exception as e:
            err = str(e)
            if "EMAIL_EXISTS" in err:
                st.error("Email này đã được đăng ký. Vui lòng dùng email khác.")
            elif "WEAK_PASSWORD" in err:
                st.error("Mật khẩu quá yếu. Vui lòng dùng mật khẩu mạnh hơn.")
            else:
                st.error("Đăng ký thất bại. Vui lòng thử lại.")

st.divider()

col_back, _ = st.columns([1, 2])
with col_back:
    if st.button("← Quay lại đăng nhập", use_container_width=True):
        st.switch_page("pages/login.py")
