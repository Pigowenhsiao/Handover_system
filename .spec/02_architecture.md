# 技術架構與資料庫設計 (Technical Plan)

## 1. 技術堆疊 (Tech Stack)
- **語言**: Python 3.9+
- **後端框架**: Flask 或 FastAPI (提供 RESTful API 服務)
- **前端框架**: React 或 Vue.js (動態用戶界面)
- **資料庫**: PostgreSQL 或 MySQL (伺服器式資料庫，支援併發訪問)
- **ORM**: SQLAlchemy (用於資料庫操作)
- **認證**: 基於 JWT (JSON Web Token) 或 Session 的使用者認證系統

## 2. 資料庫 Schema (SQLAlchemy Models)

### User Table
- id (PK)
- username (String, Unique)
- password_hash (String)
- role (String: 'admin', 'user')
- created_at (DateTime)
- updated_at (DateTime)

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

## 3. UI/UX 規劃
- **使用者管理頁面**：管理員可以進行使用者的新增、刪除和修改操作
- **填寫頁面 (Entry Page)**:
  - 使用動態表單處理「設備異常」與「異常批次」的多筆資料輸入
  - 圖片上傳功能，儲存至 `uploads/` 資料夾並記錄路徑
- **查詢頁面**：提供日期和區域篩選條件，顯示歷史報表清單
- **響應式設計**：支援不同尺寸的螢幕裝置
