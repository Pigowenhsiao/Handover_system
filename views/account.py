from __future__ import annotations

from typing import Dict, Optional

import streamlit as st
from sqlalchemy.orm import Session

from auth import hash_password, verify_password
from i18n import t
from models import User


def render_password_change(db: Session, user: Optional[Dict[str, str]], *, lang: str = "zh") -> None:
    if not user:
        st.error(t("need_login", locale=lang))
        return
    st.header(t("change_password", locale=lang))
    with st.form("change-password-form"):
        old_password = st.text_input(t("old_password", locale=lang), type="password")
        new_password = st.text_input(t("new_password", locale=lang), type="password")
        confirm_password = st.text_input(t("confirm_password", locale=lang), type="password")
        submitted = st.form_submit_button(t("change_password", locale=lang))

    if not submitted:
        return

    if not new_password or new_password != confirm_password:
        st.error(t("password_mismatch", locale=lang))
        return

    try:
        current_user: Optional[User] = db.query(User).filter(User.id == user["id"]).first()
        if current_user is None:
            st.error(t("user_not_found", locale=lang))
            return
        if not verify_password(old_password, current_user.password_hash):
            st.error(t("password_incorrect", locale=lang))
            return

        current_user.password_hash = hash_password(new_password)
        db.commit()
        st.success(t("password_updated", locale=lang))
    except Exception as exc:
        db.rollback()
        st.error(t("password_update_fail", locale=lang, msg=exc))
