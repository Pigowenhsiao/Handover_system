# 技術架構與資料庫設計 (Technical Plan)

## 1. 技術堆疊 (Tech Stack)
- **語言**: Python 3.9+
- **UI**: tkinter 桌面應用（單機執行，不經由瀏覽器）
- **資料庫**: SQLite（檔案型，離線可用）
- **ORM/DB 操作**: SQLAlchemy（如需輕量可用 sqlite3，但避免 Raw SQL）
- **認證**: 本機 Session + Bcrypt，無 JWT、無外部認證服務
- **檔案處理**: pandas/openpyxl 讀取 Excel，內建 CSV 匯出

## 2. 資料庫 Schema (SQLAlchemy Models)

### User Table
- id (PK)
- username (String, Unique)
- password_hash (String)
- role (String: 'admin', 'user')

### DailyReport Table (主表)
- id (PK)
- date (Date)
- shift (String)
- area (String)
- author_id (FK -> User.id)
- created_at (DateTime)
- summary_key_output (Text)
- summary_issues (Text)
- summary_countermeasures (Text)

### AttendanceEntry Table
- id (PK)
- report_id (FK -> DailyReport.id)
- category (String: 'Regular', 'Contract')
- scheduled_count (Int)
- present_count (Int)
- absent_count (Int)
- reason (Text)

### EquipmentLog Table
- id (PK)
- report_id (FK -> DailyReport.id)
- equip_id (String)
- description (Text)
- start_time (String)
- impact_qty (Int)
- action_taken (Text)
- image_path (String, Optional)

### LotLog Table
- id (PK)
- report_id (FK -> DailyReport.id)
- lot_id (String)
- description (Text)
- status (Text)
- notes (Text)

## 3. UI/UX 規劃（桌面）
- **主視窗**：標題列 + 主內容區，登入後顯示功能分頁/按鈕（填寫日報、歷史查詢、使用者管理、登出）。
- **填寫頁面**：
  - 基礎資訊（日期/班別/區域）使用下拉/日期選擇。
  - 出勤/設備異常/異常批次使用表格型元件（如 Treeview + 編輯對話框）支援多筆輸入。
  - 總結使用多行文字框。
  - 圖片上傳：檔案選擇器，檔案複製到 `uploads/` 並記錄路徑。
- **匯入**：提供 Excel (xlsx) 檔匯入功能；匯入前預覽與驗證，錯誤需提示並中止寫入。
- **查詢頁面**：日期/區域篩選，表格呈現歷史報表，可匯出 CSV。
- **使用者管理**：帳號/角色列表，提供新增/修改密碼/刪除操作；需檢查權限（僅 admin）。
- **語系**：介面文字預設繁體中文；如需多語切換，可透過既有語言資源庫載入對應翻譯。
