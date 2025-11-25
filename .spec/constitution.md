# Project Constitution

此文件定義了專案中不可協商的原則。AI 代理必須始終遵守這些規則。

## 1. 技術棧約束 (Tech Stack Constraints)
- **禁止使用 Web 框架**: 不得使用 Django, Flask, FastAPI 等傳統 Web 框架。所有 UI 必須純粹基於 **Streamlit**。
- **資料庫**: 嚴格使用 **SQLite** 和 **SQLAlchemy (ORM)**。禁止使用 Raw SQL 字串，以防止注入攻擊。
- **Python 版本**: 代碼必須相容 Python 3.9+。

## 2. 使用者體驗與介面 (UX/UI Principles)
- **還原度優先**: 輸入介面必須盡可能還原 PDF (25.11.24E_etching_Daily_Report.pdf) 的邏輯結構。
- **表格編輯**: 凡是涉及多行數據輸入（如出勤、設備異常），**必須**使用 `st.data_editor`，禁止使用多個獨立的 `text_input`。
- **語言**: 除非代碼註解或變數名稱，否則所有 UI 顯示文字（Labels, Buttons, Messages）必須是 **繁體中文 (Traditional Chinese)**。
- **導航**: 必須使用 Streamlit 的 Sidebar 進行功能切換。

## 3. 程式碼品質 (Code Quality)
- **模組化**: 禁止將所有代碼寫在單一 `app.py` 中。必須將視圖 (Views) 分離至 `views/` 資料夾，模型 (Models) 分離至 `models.py`。
- **型別提示**: 所有函數定義必須包含 Type Hints (例如 `def connect_db() -> Engine:`)。
- **錯誤處理**: 資料庫操作必須包含 `try-except` 區塊，並使用 `st.error` 顯示友善的錯誤訊息。

## 4. 安全性 (Security)
- **密碼存儲**: 使用者密碼禁止以明文存儲，必須使用 `bcrypt` 進行雜湊處理。
- **Session 管理**: 敏感操作（如刪除報表）前必須檢查 `st.session_state['authentication_status']`。
