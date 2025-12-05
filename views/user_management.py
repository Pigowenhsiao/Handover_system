from __future__ import annotations

from typing import Dict, Optional

import streamlit as st
from sqlalchemy.orm import Session

from auth import hash_password
from i18n import t
from models import User


def render_user_management(db: Session, user: Optional[Dict[str, str]], *, lang: str = "zh") -> None:
    if not user or user.get("role") != "admin":
        st.error(t("must_be_admin", locale=lang))
        return

    st.header(t("user_mgmt", locale=lang))

    st.subheader(t("existing_users", locale=lang))
    try:
        users = db.query(User).all()
        for u in users:
            cols = st.columns([2, 1, 1, 1, 1])
            cols[0].write(f"{u.username}（{u.role}）")
            new_role = cols[1].selectbox(t("role_label", locale=lang), ["admin", "user"], index=0 if u.role == "admin" else 1, key=f"role-{u.id}")
            new_password = cols[2].text_input(t("new_password_optional", locale=lang), type="password", key=f"pwd-{u.id}")
            update_clicked = cols[3].button(t("update", locale=lang), key=f"update-{u.id}")
            delete_confirm = cols[3].checkbox(t("confirm_delete", locale=lang), key=f"confirm-{u.id}")
            delete_clicked = cols[4].button(t("delete", locale=lang), key=f"delete-{u.id}")

            if update_clicked:
                try:
                    u.role = new_role
                    if new_password:
                        u.password_hash = hash_password(new_password)
                    db.commit()
                    st.success(t("update_success", locale=lang, name=u.username))
                except Exception as exc:
                    db.rollback()
                    st.error(t("update_fail", locale=lang, msg=exc))
            if delete_clicked:
                if not delete_confirm:
                    st.warning(t("delete_warning", locale=lang))
                    continue
                try:
                    db.delete(u)
                    db.commit()
                    st.success(t("delete_success", locale=lang, name=u.username))
                except Exception as exc:
                    db.rollback()
                    st.error(t("delete_fail", locale=lang, msg=exc))
    except Exception as exc:
        st.error(t("query_fail", locale=lang, msg=exc))

    st.divider()
    st.subheader(t("add_user", locale=lang))
    with st.form("add-user-form"):
        username = st.text_input(t("username", locale=lang))
        password = st.text_input(t("password", locale=lang), type="password")
        role = st.selectbox(t("role_label", locale=lang), ["user", "admin"])
        submitted = st.form_submit_button(t("add", locale=lang))

    if not submitted:
        return

    if not username or not password:
        st.error(t("empty_user_pass", locale=lang))
        return

    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            st.error(t("username_exists", locale=lang))
            return
        new_user = User(username=username, password_hash=hash_password(password), role=role)
        db.add(new_user)
        db.commit()
        st.success(t("add_success", locale=lang, name=username))
    except Exception as exc:
        db.rollback()
        st.error(t("add_fail", locale=lang, msg=exc))
