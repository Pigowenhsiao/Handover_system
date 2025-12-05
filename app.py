from __future__ import annotations

from typing import Dict, Optional

import streamlit as st
from sqlalchemy.orm import Session

from auth import verify_password
from i18n import LANG_LABELS, set_locale, t
from models import SessionLocal, User, init_db
from views.daily_entry import render_daily_entry
from views.report_view import render_report_view
from views.user_management import render_user_management
from views.account import render_password_change
from views.report_view import render_report_view


def get_db_session() -> Session:
    return SessionLocal()


def ensure_session_state() -> None:
    st.session_state.setdefault("authentication_status", False)
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("current_page", "填寫日報")
    st.session_state.setdefault("lang", "zh")


def do_logout() -> None:
    st.session_state["authentication_status"] = False
    st.session_state["user"] = None
    st.session_state["current_page"] = "填寫日報"


def handle_login(db: Session) -> None:
    lang = st.session_state.get("lang", "zh")
    st.subheader(t("login", locale=lang))
    with st.form("login-form"):
        username = st.text_input(t("username", locale=lang))
        password = st.text_input(t("password", locale=lang), type="password")
        submitted = st.form_submit_button(t("login_button", locale=lang))

    if not submitted:
        return

    try:
        user: Optional[User] = db.query(User).filter(User.username == username).first()
    except Exception as exc:
        st.error(t("login_error", locale=lang, msg=exc))
        return

    if user is None or not verify_password(password, user.password_hash):
        st.error(t("login_failed", locale=lang))
        return

    st.session_state["authentication_status"] = True
    st.session_state["user"] = {"id": user.id, "username": user.username, "role": user.role}
    st.success(t("login_success", locale=lang))


def render_sidebar(user: Optional[Dict[str, str]]) -> None:
    lang = st.session_state.get("lang", "zh")
    st.sidebar.title(t("nav", locale=lang))
    lang_choice = st.sidebar.selectbox(
        t("language", locale=lang) + " / Language / 言語",
        options=list(LANG_LABELS.keys()),
        format_func=lambda code: LANG_LABELS.get(code, code),
        index=list(LANG_LABELS.keys()).index(lang) if lang in LANG_LABELS else 0,
    )
    st.session_state["lang"] = lang_choice
    set_locale(lang_choice)
    lang = lang_choice

    if user:
        st.sidebar.write(f"{t('user_label', locale=lang)}：{user.get('username')}（{user.get('role')}）")
        options = [t("nav_daily_entry", locale=lang), t("nav_report_view", locale=lang), t("nav_change_password", locale=lang)]
        if user.get("role") == "admin":
            options.append(t("nav_user_mgmt", locale=lang))
        current = st.session_state.get("current_page", options[0])
        idx = options.index(current) if current in options else 0
        page = st.sidebar.radio(t("nav", locale=lang), options, index=idx)
        st.session_state["current_page"] = page
        st.sidebar.button(t("logout", locale=lang), on_click=do_logout)
    else:
        st.sidebar.info(t("need_login", locale=lang))


def main() -> None:
    st.set_page_config(page_title=t("app_title"), layout="wide")
    ensure_session_state()
    init_db()

    user = st.session_state.get("user")
    render_sidebar(user)

    if not st.session_state["authentication_status"]:
        with get_db_session() as db:
            handle_login(db)
        return

    lang = st.session_state.get("lang", "zh")
    page = st.session_state.get("current_page", t("nav_daily_entry", locale=lang))
    with get_db_session() as db:
        if page == t("nav_daily_entry", locale=lang):
            render_daily_entry(db, user, lang=lang)
        elif page == t("nav_report_view", locale=lang):
            render_report_view(db, lang=lang)
        elif page == t("nav_user_mgmt", locale=lang):
            if user and user.get("role") == "admin":
                render_user_management(db, user, lang=lang)
            else:
                st.error(t("only_admin", locale=lang))
        elif page == t("nav_change_password", locale=lang):
            render_password_change(db, user, lang=lang)
        else:
            st.error("未知頁面")


if __name__ == "__main__":
    main()
