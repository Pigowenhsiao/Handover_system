# 數據模型 (Data Model)

## 1. 使用者表 (User Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **username** (VARCHAR(80), UNIQUE, NOT NULL): 使用者名稱
- **password_hash** (VARCHAR(255), NOT NULL): 密碼哈希值 (使用 bcrypt)
- **role** (VARCHAR(20), DEFAULT 'user'): 角色 ('admin', 'user')
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間
- **updated_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP): 更新時間

### 關係
- 一對多關係: User → DailyReport (author_id)

## 2. 日報表 (DailyReport Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **date** (DATE, NOT NULL): 日期
- **shift** (VARCHAR(10), NOT NULL): 班別 ('Day', 'Night')
- **area** (VARCHAR(20), NOT NULL): 區域 ('etching_D', 'etching_E', 'litho', 'thin_film')
- **author_id** (INTEGER, FOREIGN KEY → User.id, NOT NULL): 填寫者 ID
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間
- **updated_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP): 更新時間
- **summary_key_output** (TEXT): Key Machine Output 摘要
- **summary_issues** (TEXT): Key Issues 摘要
- **summary_countermeasures** (TEXT): Countermeasures 摘要

### 關係
- 多對一關係: DailyReport → User (author_id)
- 一對多關係: DailyReport → AttendanceEntry (report_id)
- 一對多關係: DailyReport → EquipmentLog (report_id)
- 一對多關係: DailyReport → LotLog (report_id)

## 3. 出勤記錄 (AttendanceEntry Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **report_id** (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL): 關聯日報表 ID
- **category** (VARCHAR(20), NOT NULL): 類別 ('Regular', 'Contract')
- **scheduled_count** (INTEGER, DEFAULT 0): 定員人數
- **present_count** (INTEGER, DEFAULT 0): 出勤人數
- **absent_count** (INTEGER, DEFAULT 0): 欠勤人數
- **reason** (TEXT): 理由
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間

### 關係
- 多對一關係: AttendanceEntry → DailyReport (report_id)

## 4. 設備異常記錄 (EquipmentLog Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **report_id** (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL): 關聯日報表 ID
- **equip_id** (VARCHAR(50), NOT NULL): 設備 ID
- **description** (TEXT, NOT NULL): 異常描述
- **start_time** (VARCHAR(20)): 發生時刻
- **impact_qty** (INTEGER, DEFAULT 0): 影響數量
- **action_taken** (TEXT): 對應內容
- **image_path** (VARCHAR(255), NULLABLE): 圖片路徑
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間

### 關係
- 多對一關係: EquipmentLog → DailyReport (report_id)

## 5. 異常批次記錄 (LotLog Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **report_id** (INTEGER, FOREIGN KEY → DailyReport.id, NOT NULL): 關聯日報表 ID
- **lot_id** (VARCHAR(50), NOT NULL): 批號
- **description** (TEXT, NOT NULL): 異常描述
- **status** (TEXT): 處置狀況
- **notes** (TEXT): 特記事項
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間

### 關係
- 多對一關係: LotLog → DailyReport (report_id)

## 6. 語言資源 (LanguageResource Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **language_code** (VARCHAR(10), NOT NULL): 語言代碼 ('zh', 'ja', 'en')
- **resource_key** (VARCHAR(255), NOT NULL): 資源鍵
- **resource_value** (TEXT, NOT NULL): 資源值
- **namespace** (VARCHAR(100), DEFAULT 'common'): 命名空間
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間
- **updated_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP): 更新時間
- **updated_by** (INTEGER, FOREIGN KEY → User.id): 最後更新用戶

### 關係
- 多對一關係: LanguageResource → User (updated_by)

## 7. 語言設置 (LanguageSetting Table)
### 欄位定義
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 唯一標識符
- **user_id** (INTEGER, FOREIGN KEY → User.id): 用戶 ID (NULL 表示系統級設定)
- **language_code** (VARCHAR(10), NOT NULL): 語言代碼
- **is_default** (BOOLEAN, DEFAULT FALSE): 是否為默認語言
- **is_active** (BOOLEAN, DEFAULT TRUE): 是否啟用
- **created_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP): 創建時間
- **updated_at** (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP): 更新時間

### 關係
- 多對一關係: LanguageSetting → User (user_id)

## 8. 索引建議
- DailyReport.date: 提升按日期查詢的效能
- DailyReport.area: 提升按區域篩選的效能
- DailyReport.author_id: 提升按作者查詢的效能
- AttendanceEntry.report_id: 提升關聯查詢效能
- EquipmentLog.report_id: 提升關聯查詢效能
- LotLog.report_id: 提升關聯查詢效能
- LanguageResource.language_code: 提升按語言查詢效能
- LanguageResource.resource_key: 提升按鍵查詢效能

## 9. 驗證規則
- DailyReport.date: 必須是有效的日期格式
- DailyReport.shift: 僅限於 'Day' 或 'Night'
- DailyReport.area: 僅限於 'etching_D', 'etching_E', 'litho', 'thin_film'
- AttendanceEntry.category: 僅限於 'Regular' 或 'Contract'
- AttendanceEntry.scheduled_count, present_count, absent_count: 必須為非負整數
- AttendanceEntry.present_count + AttendanceEntry.absent_count <= AttendanceEntry.scheduled_count
- User.username: 長度 3-80 字元，具唯一性
- User.role: 僅限於 'admin' 或 'user'
- LanguageResource.language_code: 僅限於 'zh', 'ja', 'en'