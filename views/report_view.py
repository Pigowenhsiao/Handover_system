from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st
from sqlalchemy import and_
from sqlalchemy.orm import Session

from i18n import t
from models import DailyReport


def render_report_view(db: Session, *, lang: str = "zh") -> None:
    st.header(t("history", locale=lang))

    today = date.today()
    start_date, end_date = st.date_input(
        t("select_range", locale=lang),
        value=(today.replace(day=1), today),
    )
    area = st.selectbox(t("area", locale=lang), [t("area_all", locale=lang), "etching_D", "etching_E", "litho", "thin_film"], index=0)

    if st.button(t("query", locale=lang)):
        query = db.query(DailyReport)
        try:
            if start_date and end_date:
                query = query.filter(and_(DailyReport.date >= start_date, DailyReport.date <= end_date))
            if area != t("area_all", locale=lang):
                query = query.filter(DailyReport.area == area)

            reports = query.order_by(DailyReport.date.desc()).all()
        except Exception as exc:
            st.error(t("query_fail", locale=lang, msg=exc))
            return

        if not reports:
            st.info(t("no_data", locale=lang))
            return

        data = [
            {
                t("date", locale=lang): r.date,
                t("shift", locale=lang): r.shift,
                t("area", locale=lang): r.area,
                "ID": r.author_id,
                t("summary", locale=lang): (r.summary_issues or "")[:50],
                "created": r.created_at,
            }
            for r in reports
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(t("export_csv", locale=lang), data=csv_data, file_name="reports.csv", mime="text/csv")
