# 數據模型設計 (Data Model)

## 1. User 模型
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- username (VARCHAR(80), UNIQUE, NOT NULL)
- password_hash (VARCHAR(255), NOT NULL)
- role (VARCHAR(20), DEFAULT 'user', CHECK: 'admin' OR 'user')
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)

### 關係
- 一對多關係: User → DailyReport (author_id)

## 2. DailyReport 模型
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- date (DATE, NOT NULL)
- shift (VARCHAR(10), NOT NULL, CHECK: 'Day' OR 'Night')
- area (VARCHAR(20), NOT NULL, CHECK: 'etching_D', 'etching_E', 'litho', 'thin_film')
- author_id (INTEGER, FOREIGN KEY → User.id, NOT NULL)
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- summary_key_output (TEXT)
- summary_issues (TEXT)
- summary_countermeasures (TEXT)

### 關係
- 多對一關係: DailyReport → User (author_id)
- 一對多關係: DailyReport → AttendanceEntry (report_id)
- 一對多關係: DailyReport → EquipmentLog (report_id)
- 一對多關係: DailyReport → LotLog (report_id)

## 3. AttendanceEntry 模型
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- report_id (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL)
- category (VARCHAR(20), NOT NULL, CHECK: 'Regular' OR 'Contract')
- scheduled_count (INTEGER, DEFAULT 0)
- present_count (INTEGER, DEFAULT 0)
- absent_count (INTEGER, DEFAULT 0)
- reason (TEXT)

### 關係
- 多對一關係: AttendanceEntry → DailyReport (report_id)

## 4. EquipmentLog 模型
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- report_id (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL)
- equip_id (VARCHAR(50), NOT NULL)
- description (TEXT, NOT NULL)
- start_time (VARCHAR(20))  # 可以轉換為 TIME 類型，但保留為 VARCHAR 以保持靈活
- impact_qty (INTEGER, DEFAULT 0)
- action_taken (TEXT)
- image_path (VARCHAR(255), NULLABLE)

### 關係
- 多對一關係: EquipmentLog → DailyReport (report_id)

## 5. LotLog 模型
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- report_id (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL)
- lot_id (VARCHAR(50), NOT NULL)
- description (TEXT, NOT NULL)
- status (TEXT)
- notes (TEXT)

### 關係
- 多對一關係: LotLog → DailyReport (report_id)

## 6. 索引建議
- DailyReport.date: 提升日期查詢性能
- DailyReport.area: 提升區域篩選性能
- DailyReport.author_id: 提升使用者報表查詢性能
- AttendanceEntry.report_id: 提升報表關聯查詢性能
- EquipmentLog.report_id: 提升報表關聯查詢性能
- LotLog.report_id: 提升報表關聯查詢性能

## 7. 驗證規則
- DailyReport.date: 必須是有效的日期格式
- DailyReport.shift: 限制為 'Day' 或 'Night'
- DailyReport.area: 限制為 'etching_D', 'etching_E', 'litho', 'thin_film'
- AttendanceEntry.category: 限制為 'Regular' 或 'Contract'
- AttendanceEntry.scheduled_count, present_count, absent_count: 必須為非負整數
- AttendanceEntry.absent_count: 必須 <= scheduled_count
- User.username: 長度 3-80 字符，唯一性
- User.role: 限制為 'admin' 或 'user'