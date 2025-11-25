# 開發任務清單 (Tasks)

請依序執行以下步驟來構建應用程式：

## Phase 1: 基礎設施
1. [ ] 建立 `requirements.txt`: 包含 flask 或 fastapi, sqlalchemy, bcrypt, jwt, 以及其他相關套件。
2. [ ] 建立 `models.py`: 根據 `02_architecture.md` 實作 SQLAlchemy Classes 和 `init_db` 函數。
3. [ ] 建立 `auth.py`: 實作基於 JWT 或 Session 的密碼雜湊與驗證邏輯。

## Phase 2: 核心功能
4. [ ] 建立後端 API (使用 Flask 或 FastAPI): 實作 RESTful API 端點，包括使用者認證、日報表 CRUD 操作。
5. [ ] 建立前端頁面 (使用 React 或 Vue.js):
    - 登入頁面
    - 日報表填寫頁面 (包含動態表格輸入)
    - 日報表查詢頁面
6. [ ] 實作使用者管理功能:
    - 管理員介面 (新增、刪除、修改使用者)
    - 使用者權限控制

## Phase 3: 優化與測試
7. [ ] 添加圖片上傳處理邏輯 (儲存檔案到本機並記錄路徑)。
8. [ ] 實作前端表單驗證與錯誤處理。
9. [ ] 進行系統整合測試。
10. [ ] 部署配置與文檔撰寫。
