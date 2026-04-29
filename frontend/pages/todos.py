import streamlit as st
from utils.auth import is_logged_in, logout
from utils.api   import get_todos, create_todo, update_todo, delete_todo

st.set_page_config(page_title="Todo App", page_icon="✅", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }

.task-card {
    background: #FFF7ED;
    border: 1px solid #FDBA74;
    border-left: 4px solid #F97316;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

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
.badge-status   { background: #F3F4F6; color: #374151; }

hr { border-color: #FDBA74; }
</style>
""", unsafe_allow_html=True)

if not is_logged_in():
    st.warning("Vui lòng đăng nhập.")
    if st.button("Đăng nhập", type="primary", use_container_width=False):
        st.switch_page("pages/login.py")
    st.stop()

# --- Header ---
col_logo, col_user = st.columns([4, 1])
with col_logo:
    st.markdown("## ✅ Todo App")
with col_user:
    st.caption(st.session_state["user_info"].get("email", ""))
    if st.button("Đăng xuất", use_container_width=True):
        logout()

st.divider()

# --- Layout 2 cột ---
col_form, col_list = st.columns([1, 2])

# --- Cột trái: Form thêm task ---
PRIORITY_BADGE = {
    "low":    '<span class="badge badge-low">🟢 Low</span>',
    "medium": '<span class="badge badge-medium">🟡 Medium</span>',
    "high":   '<span class="badge badge-high">🟠 High</span>',
    "urgent": '<span class="badge badge-urgent">🔴 Urgent</span>',
}

STATUS_OPTIONS = ["pending", "in_progress", "done"]
STATUS_LABEL   = {"pending": "⏳ Pending", "in_progress": "🔄 In Progress", "done": "✅ Done"}

with col_form:
    st.markdown("### Thêm task mới")
    with st.form("new_task", clear_on_submit=True):
        title       = st.text_input("Tên task *")
        description = st.text_area("Mô tả", height=70)
        col_p, col_s = st.columns(2)
        with col_p:
            priority = st.selectbox(
                "Độ ưu tiên",
                ["low", "medium", "high", "urgent"],
                index=1,
                format_func=lambda x: {
                    "low":    "🟢 Low",
                    "medium": "🟡 Medium",
                    "high":   "🟠 High",
                    "urgent": "🔴 Urgent",
                }[x],
            )
        with col_s:
            init_status = st.selectbox(
                "Trạng thái",
                STATUS_OPTIONS,
                index=0,
                format_func=lambda s: STATUS_LABEL[s],
            )
        due_date   = st.date_input("Ngày hết hạn", value=None)
        assignee   = st.text_input("Người phụ trách")
        tags_input = st.text_input(
            "Tags (phân cách bằng dấu phẩy)",
            placeholder="work, personal, study",
        )
        notes = st.text_area(
            "Ghi chú / Sub-tasks",
            height=80,
            placeholder="- Bước 1\n- Bước 2",
        )

        if st.form_submit_button("Thêm task", use_container_width=True):
            if title.strip():
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                result = create_todo(
                    title       = title.strip(),
                    description = description.strip(),
                    priority    = priority,
                    due_date    = str(due_date) if due_date else None,
                    assignee    = assignee.strip(),
                    tags        = tags,
                    notes       = notes.strip(),
                )
                # cập nhật status nếu khác pending
                if init_status != "pending" and result.get("id"):
                    update_todo(result["id"], {"status": init_status})
                st.rerun()
            else:
                st.warning("Tên task không được để trống.")

# --- Cột phải: Danh sách task ---
with col_list:
    st.markdown("### 📋 Danh sách task")

    # Filter bar
    filter_status = st.selectbox(
        "Lọc theo trạng thái",
        ["Tất cả"] + STATUS_OPTIONS,
        format_func=lambda x: "Tất cả" if x == "Tất cả" else STATUS_LABEL[x],
    )
    filter_priority = st.selectbox(
        "Lọc theo độ ưu tiên",
        ["Tất cả", "low", "medium", "high", "urgent"],
    )

    todos = get_todos()

    if filter_status != "Tất cả":
        todos = [t for t in todos if t.get("status") == filter_status]
    if filter_priority != "Tất cả":
        todos = [t for t in todos if t.get("priority") == filter_priority]

    if not todos:
        st.info("Không có task nào phù hợp.")
    else:
        for todo in todos:
            tags_html     = "".join(
                f'<span class="badge badge-tag">{tag}</span>'
                for tag in todo.get("tags", [])
            )
            priority_html = PRIORITY_BADGE.get(todo.get("priority", "medium"), "")
            status_html   = f'<span class="badge badge-status">{STATUS_LABEL.get(todo.get("status", "pending"), todo.get("status", ""))}</span>'
            due           = f'📅 {todo["due_date"]}' if todo.get("due_date") else ""
            assignee_txt  = f'👤 {todo["assignee"]}' if todo.get("assignee") else ""

            card_html = (
                f'<div class="task-card">'
                f'<strong style="font-size:16px">{todo["title"]}</strong><br>'
                f'{priority_html}{status_html}'
                + (f'<span style="color:#78716C;font-size:13px;margin-left:6px">{due}</span>' if due else "")
                + (f'<span style="color:#78716C;font-size:13px;margin-left:8px">{assignee_txt}</span>' if assignee_txt else "")
                + (f'<div style="margin-top:6px">{tags_html}</div>' if tags_html else "")
                + (f'<p style="color:#57534E;font-size:13px;margin-top:6px;margin-bottom:0;white-space:pre-wrap">{todo["description"]}</p>' if todo.get("description") else "")
                + (f'<div style="background:#FEF3C7;padding:8px;border-radius:6px;font-size:12px;margin-top:6px;white-space:pre-wrap">{todo["notes"]}</div>' if todo.get("notes") else "")
                + '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([2, 1, 1], vertical_alignment="top")
            with c1:
                new_status = st.selectbox(
                    "",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(todo.get("status", "pending")),
                    format_func=lambda s: STATUS_LABEL[s],
                    key=f"sel_{todo['id']}",
                )
            with c2:
                if st.button("Cập nhật", key=f"upd_{todo['id']}", use_container_width=True):
                    update_todo(todo["id"], {"status": new_status})
                    st.rerun()
            with c3:
                if st.button("Xoá", key=f"del_{todo['id']}", use_container_width=True):
                    delete_todo(todo["id"])
                    st.rerun()

            st.markdown("<hr>", unsafe_allow_html=True)
