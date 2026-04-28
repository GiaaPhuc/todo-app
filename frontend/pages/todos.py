import streamlit as st
from utils.auth import is_logged_in, logout
from utils.api   import get_todos, create_todo, update_todo, delete_todo

st.set_page_config(page_title="Todo App", page_icon="✅", layout="centered")

if not is_logged_in():
    st.warning("Vui lòng đăng nhập.")
    st.stop()

# --- Header ---
col_title, col_user = st.columns([3, 1])
with col_title:
    st.title("Todo App")
with col_user:
    st.caption(st.session_state["user_info"].get("email", ""))
    if st.button("Đăng xuất", use_container_width=True):
        logout()

st.divider()

# --- Thêm task mới ---
st.subheader("Thêm task")
with st.form("new_task", clear_on_submit=True):
    title = st.text_input("Tên task")
    desc  = st.text_area("Mô tả", height=80)
    if st.form_submit_button("Thêm", use_container_width=True):
        if title.strip():
            create_todo(title.strip(), desc.strip())
            st.rerun()
        else:
            st.warning("Tên task không được để trống.")

st.divider()

# --- Danh sách task ---
STATUS_OPTIONS = ["pending", "in_progress", "done"]
STATUS_LABEL   = {
    "pending":     "Pending",
    "in_progress": "In Progress",
    "done":        "Done",
}
STATUS_ICON = {
    "pending":     "⏳",
    "in_progress": "🔄",
    "done":        "✅",
}

st.subheader("Danh sách task")
todos = get_todos()

if not todos:
    st.info("Chưa có task nào. Hãy thêm task đầu tiên.")
else:
    for todo in todos:
        icon   = STATUS_ICON.get(todo["status"], "")
        label  = STATUS_LABEL.get(todo["status"], todo["status"])
        with st.expander(f"{icon} [{label}]  {todo['title']}"):
            if todo.get("description"):
                st.caption(todo["description"])

            new_status = st.selectbox(
                "Trạng thái",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(todo["status"]),
                format_func=lambda s: STATUS_LABEL[s],
                key=f"sel_{todo['id']}",
            )

            col_update, col_delete = st.columns(2)
            with col_update:
                if st.button("Cập nhật", key=f"upd_{todo['id']}", use_container_width=True):
                    update_todo(todo["id"], new_status)
                    st.rerun()
            with col_delete:
                if st.button("Xoá", key=f"del_{todo['id']}", use_container_width=True):
                    delete_todo(todo["id"])
                    st.rerun()
