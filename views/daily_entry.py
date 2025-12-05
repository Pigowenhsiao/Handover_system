from __future__ import annotations

import os
from datetime import date, datetime
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from models import AttendanceEntry, DailyReport, EquipmentLog, LotLog
from i18n import t


ATTENDANCE_DEFAULT = pd.DataFrame(
    [
        {"category": "正社員", "scheduled_count": 0, "present_count": 0, "absent_count": 0, "reason": ""},
        {"category": "契約/派遣", "scheduled_count": 0, "present_count": 0, "absent_count": 0, "reason": ""},
    ]
)

EQUIPMENT_DEFAULT = pd.DataFrame(
    [
        {"equip_id": "", "description": "", "start_time": "", "impact_qty": 0, "action_taken": ""},
    ]
)

LOT_DEFAULT = pd.DataFrame(
    [
        {"lot_id": "", "description": "", "status": "", "notes": ""},
    ]
)

SHIFT_OPTIONS = ["Day", "Night"]
AREA_OPTIONS = ["etching_D", "etching_E", "litho", "thin_film"]


def save_uploaded_files(files: List, upload_dir: str = "uploads") -> List[str]:
    os.makedirs(upload_dir, exist_ok=True)
    saved_paths: List[str] = []
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    for index, file in enumerate(files):
        filename = f"{timestamp}_{index}_{file.name}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(file_path)

    return saved_paths


def render_daily_entry(db: Session, user: Optional[Dict[str, str]], *, lang: str = "zh") -> None:
    if not user:
        st.error(t("need_login", locale=lang))
        return
    st.header(t("daily_entry", locale=lang))
    st.caption("💡 " + t("summary", locale=lang))

    with st.form("daily-entry-form", clear_on_submit=True):
        st.markdown("### 1️⃣ " + t("date", locale=lang) + " / " + t("shift", locale=lang) + " / " + t("area", locale=lang))
        col1, col2, col3 = st.columns(3)
        with col1:
            report_date = st.date_input(t("date", locale=lang), value=date.today())
        with col2:
            shift = st.selectbox(t("shift", locale=lang), SHIFT_OPTIONS, index=0)
        with col3:
            area = st.selectbox(t("area", locale=lang), AREA_OPTIONS, index=0)

        st.markdown("### 2️⃣ " + t("attendance", locale=lang))
        st.caption("• " + t("scheduled_count", locale=lang) + "/" + t("present_count", locale=lang) + "/" + t("absent_count", locale=lang) + " • " + t("reason", locale=lang))
        attendance_df = st.data_editor(
            ATTENDANCE_DEFAULT,
            num_rows="dynamic",
            use_container_width=True,
            key="attendance_editor",
            column_config={
                "category": t("attendance_category", locale=lang),
                "scheduled_count": t("scheduled_count", locale=lang),
                "present_count": t("present_count", locale=lang),
                "absent_count": t("absent_count", locale=lang),
                "reason": t("reason", locale=lang),
            },
        )

        st.markdown("### 3️⃣ " + t("equipment", locale=lang))
        st.caption("• " + t("equip_id", locale=lang) + " / " + t("impact_qty", locale=lang) + " • " + t("start_time", locale=lang) + " / " + t("action_taken", locale=lang))
        equipment_df = st.data_editor(
            EQUIPMENT_DEFAULT,
            num_rows="dynamic",
            use_container_width=True,
            key="equipment_editor",
            column_config={
                "equip_id": t("equip_id", locale=lang),
                "description": t("description", locale=lang),
                "start_time": t("start_time", locale=lang),
                "impact_qty": t("impact_qty", locale=lang),
                "action_taken": t("action_taken", locale=lang),
            },
        )

        st.markdown("### 4️⃣ " + t("lots", locale=lang))
        st.caption("• " + t("lot_id", locale=lang) + " / " + t("status", locale=lang) + " • " + t("notes", locale=lang))
        lot_df = st.data_editor(
            LOT_DEFAULT,
            num_rows="dynamic",
            use_container_width=True,
            key="lot_editor",
            column_config={
                "lot_id": t("lot_id", locale=lang),
                "description": t("description", locale=lang),
                "status": t("status", locale=lang),
                "notes": t("notes", locale=lang),
            },
        )

        st.markdown("### 5️⃣ " + t("summary", locale=lang))
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            summary_key_output = st.text_area(t("key_output", locale=lang), height=120)
        with col_s2:
            summary_issues = st.text_area(t("key_issues", locale=lang), height=120)
        with col_s3:
            summary_countermeasures = st.text_area(t("countermeasures", locale=lang), height=120)

        st.markdown("### 6️⃣ " + t("upload_photos", locale=lang))
        uploaded_files = st.file_uploader(t("upload_photos", locale=lang), accept_multiple_files=True)

        submitted = st.form_submit_button("✅ " + t("submit", locale=lang))

    if not submitted:
        return

    # 驗證資料
    errors: List[str] = []
    att_rows = attendance_df.fillna("")
    equip_rows = equipment_df.fillna("")
    lot_rows = lot_df.fillna("")

    for idx, row in att_rows.iterrows():
        for field in ["scheduled_count", "present_count", "absent_count"]:
            try:
                value = int(row.get(field, 0) or 0)
                if value < 0:
                    errors.append(t("attendance_negative", locale=lang, row=idx + 1, field=field))
            except ValueError:
                errors.append(t("attendance_number", locale=lang, row=idx + 1, field=field))
    for idx, row in equip_rows.iterrows():
        try:
            value = int(row.get("impact_qty", 0) or 0)
            if value < 0:
                errors.append(t("equipment_negative", locale=lang, row=idx + 1))
        except ValueError:
            errors.append(t("equipment_number", locale=lang, row=idx + 1))

    if errors:
        st.error(t("validation_fail", locale=lang, msg="\n".join(errors)))
        return

    try:
        image_paths = save_uploaded_files(uploaded_files) if uploaded_files else []
    except Exception as exc:
        st.error(t("save_image_fail", locale=lang, msg=exc))
        return

    try:
        report = DailyReport(
            date=report_date,
            shift=shift,
            area=area,
            author_id=user["id"],
            summary_key_output=summary_key_output,
            summary_issues=summary_issues,
            summary_countermeasures=summary_countermeasures,
        )
        db.add(report)
        db.flush()

        for _, row in att_rows.iterrows():
            db.add(
                AttendanceEntry(
                    report_id=report.id,
                    category=str(row.get("category", "")),
                    scheduled_count=max(int(row.get("scheduled_count", 0) or 0), 0),
                    present_count=max(int(row.get("present_count", 0) or 0), 0),
                    absent_count=max(int(row.get("absent_count", 0) or 0), 0),
                    reason=str(row.get("reason", "")),
                )
            )

        for idx, row in equip_rows.iterrows():
            image_path = image_paths[idx] if idx < len(image_paths) else None
            db.add(
                EquipmentLog(
                    report_id=report.id,
                    equip_id=str(row.get("equip_id", "")),
                    description=str(row.get("description", "")),
                    start_time=str(row.get("start_time", "")),
                    impact_qty=max(int(row.get("impact_qty", 0) or 0), 0),
                    action_taken=str(row.get("action_taken", "")),
                    image_path=image_path,
                )
            )

        for _, row in lot_rows.iterrows():
            db.add(
                LotLog(
                    report_id=report.id,
                    lot_id=str(row.get("lot_id", "")),
                    description=str(row.get("description", "")),
                    status=str(row.get("status", "")),
                    notes=str(row.get("notes", "")),
                )
            )

        db.commit()
        st.success(t("submit_success", locale=lang))
    except Exception as exc:
        db.rollback()
        st.error(t("submit_fail", locale=lang, msg=exc))
