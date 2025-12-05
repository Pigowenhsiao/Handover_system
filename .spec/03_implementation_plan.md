# 開發任務清單 (Tasks)

請依序執行以下步驟來構建應用程式：

## Phase 1: 基礎設施
1. [ ] 建立 `requirements.txt`: 包含 tkinter（系統套件）、sqlalchemy、pandas（匯出）、bcrypt。
2. [ ] 建立 `models.py`: 根據 `02_architecture.md` 實作 SQLAlchemy Classes 和 `init_db` 函數。
3. [ ] 建立 `auth.py`: 實作密碼雜湊與驗證邏輯。

## Phase 2: 核心功能（桌面）
4. [ ] 建立 `app.py`: tkinter 主視窗與登入/Session 管理、功能分頁/按鈕導航。
5. [ ] 建立 `views/daily_entry.py`（或同檔內模組化函式）：
    - 實作 PDF 對應輸入介面（日期/班別/區域 + 出勤/設備異常/異常批次表格 + 總結）。
    - 使用表格型元件（Treeview 或自訂表格）支援多筆輸入。
    - 實作資料儲存（寫入 SQLite）。
6. [ ] 建立 `views/report_view.py`：
    - 依日期/區域篩選，表格顯示歷史報表。
    - 匯出 CSV。
7. [ ] 建立 `views/user_management.py`：
    - 管理員新增/修改密碼/刪除使用者。
8. [ ] 建立匯入模組（Excel）：
     - 讀取 xlsx（pandas/openpyxl），預覽並驗證欄位。
     - 匯入出勤/設備異常/異常批次資料，錯誤需提示並中止寫入。

## Phase 3: 優化與測試
9. [ ] 添加圖片上傳處理（檔案選擇器，儲存到 `uploads/`）。
10. [ ] 測試登入、資料寫入、匯入、查詢與匯出流程；確認權限檢查。
