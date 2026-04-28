import streamlit as st

BACKEND_URL = "http://localhost:8000"


def get_auth_header() -> dict:
    return {"Authorization": f"Bearer {st.session_state.get('id_token', '')}"}


def is_logged_in() -> bool:
    return bool(st.session_state.get("id_token"))


def logout():
    for key in ["id_token", "user_info"]:
        st.session_state.pop(key, None)
    st.rerun()
