# API 合約 (API Contracts)

此電子交接本系統主要是桌面應用程式，使用 tkinter 界面，因此沒有傳統的 REST API。但為了完整性，以下是界面組件之間的接口規範，以及與後端數據層的接口定義。

## 1. 數據訪問接口 (Data Access Interfaces)

### 1.1 用戶管理接口 (User Management Interface)
#### 方法: create_user(username: str, password: str, role: str) -> bool
- **目的**: 創建新用戶
- **參數**: 
  - username: 用戶名稱 (必需)
  - password: 密碼 (必需)
  - role: 角色 ('admin' 或 'user')，默認為 'user'
- **返回**: 成功或失敗布林值
- **異常**: 若用戶名已存在則返回 False

#### 方法: authenticate_user(username: str, password: str) -> dict
- **目的**: 驗證用戶憑證
- **參數**:
  - username: 用戶名稱 (必需)
  - password: 密碼 (必需)
- **返回**: 用戶信息字典或 None (驗證失敗)
- **異常**: 無匹配用戶時返回 None

#### 方法: update_user(user_id: int, username: str = None, password: str = None, role: str = None) -> bool
- **目的**: 更新用戶信息
- **參數**:
  - user_id: 要更新的用戶 ID
  - username: 新用戶名稱 (可選)
  - password: 新密碼 (可選)
  - role: 新角色 (可選)
- **返回**: 成功或失敗布林值
- **異常**: 若用戶不存在返回 False

#### 方法: delete_user(user_id: int) -> bool
- **目的**: 刪除用戶
- **參數**: 
  - user_id: 要刪除的用戶 ID
- **返回**: 成功或失敗布林值
- **異常**: 若用戶不存在返回 False

### 1.2 日報表接口 (Daily Report Interface)
#### 方法: create_daily_report(date: str, shift: str, area: str, author_id: int, summary_key_output: str, summary_issues: str, summary_countermeasures: str) -> int
- **目的**: 創建新日報表
- **參數**:
  - date: 日期 (YYYY-MM-DD)
  - shift: 班別 ('Day' 或 'Night')
  - area: 區域
  - author_id: 作者 ID
  - summary_key_output: Key Output 摘要
  - summary_issues: Issues 摘要
  - summary_countermeasures: Countermeasures 摘要
- **返回**: 新日報表的 ID
- **異常**: 數據驗證失敗時返回 0

#### 方法: get_daily_report(report_id: int) -> dict
- **目的**: 獲取特定日報表
- **參數**:
  - report_id: 日報表 ID
- **返回**: 包含日報表信息的字典
- **異常**: 若日報表不存在返回 None

#### 方法: update_daily_report(report_id: int, **kwargs) -> bool
- **目的**: 更新日報表
- **參數**:
  - report_id: 要更新的日報表 ID
  - **kwargs: 要更新的字段和值
- **返回**: 成功或失敗布林值
- **異常**: 若日報表不存在返回 False

#### 方法: delete_daily_report(report_id: int) -> bool
- **目的**: 刪除日報表
- **參數**:
  - report_id: 要刪除的日報表 ID
- **返回**: 成功或失敗布林值
- **異常**: 若日報表不存在返回 False

#### 方法: search_daily_reports(filters: dict) -> List[dict]
- **目的**: 搜尋日報表
- **參數**:
  - filters: 搜尋條件字典 (包含日期範圍、區域、作者等)
- **返回**: 日報表列表
- **異常**: 無異常

### 1.3 出勤記錄接口 (Attendance Record Interface)
#### 方法: add_attendance_entry(report_id: int, category: str, scheduled_count: int, present_count: int, absent_count: int, reason: str = "") -> bool
- **目的**: 添加出勤記錄
- **參數**:
  - report_id: 關聯的日報表 ID
  - category: 類別 ('Regular' 或 'Contract')
  - scheduled_count: 定員人數
  - present_count: 出勤人數
  - absent_count: 欠勤人數
  - reason: 原因 (可選)
- **返回**: 成功或失敗布林值
- **異常**: 數據驗證失敗時返回 False

#### 方法: update_attendance_entry(entry_id: int, **kwargs) -> bool
- **目的**: 更新出勤記錄
- **參數**:
  - entry_id: 要更新的記錄 ID
  - **kwargs: 要更新的字段和值
- **返回**: 成功或失敗布林值
- **異常**: 若記錄不存在返回 False

#### 方法: get_attendance_entries(report_id: int) -> List[dict]
- **目的**: 獲取指定日報表的出勤記錄
- **參數**:
  - report_id: 日報表 ID
- **返回**: 出勤記錄列表
- **異常**: 若日報表不存在返回空列表

### 1.4 設備異常接口 (Equipment Log Interface)
#### 方法: add_equipment_log(report_id: int, equip_id: str, description: str, start_time: str = "", impact_qty: int = 0, action_taken: str = "", image_path: str = "") -> bool
- **目的**: 添加設備異常記錄
- **參數**:
  - report_id: 關聯的日報表 ID
  - equip_id: 設備 ID
  - description: 異常描述
  - start_time: 開始時間 (可選)
  - impact_qty: 影響數量 (可選)
  - action_taken: 對應措施 (可選)
  - image_path: 圖片路徑 (可選)
- **返回**: 成功或失敗布林值
- **異常**: 數據驗證失敗時返回 False

#### 方法: update_equipment_log(log_id: int, **kwargs) -> bool
- **目的**: 更新設備異常記錄
- **參數**:
  - log_id: 要更新的記錄 ID
  - **kwargs: 要更新的字段和值
- **返回**: 成功或失敗布林值
- **異常**: 若記錄不存在返回 False

### 1.5 異常批次接口 (Lot Log Interface)
#### 方法: add_lot_log(report_id: int, lot_id: str, description: str, status: str = "", notes: str = "") -> bool
- **目的**: 添加異常批次記錄
- **參數**:
  - report_id: 關聯的日報表 ID
  - lot_id: 批號
  - description: 異常描述
  - status: 狀態 (可選)
  - notes: 備註 (可選)
- **返回**: 成功或失敗布林值
- **異常**: 數據驗證失敗時返回 False

#### 方法: update_lot_log(log_id: int, **kwargs) -> bool
- **目的**: 更新異常批次記錄
- **參數**:
  - log_id: 要更新的記錄 ID
  - **kwargs: 要更新的字段和值
- **返回**: 成功或失敗布林值
- **異常**: 若記錄不存在返回 False

## 2. 界面組件接口 (UI Component Interfaces)

### 2.1 語言切換接口 (Language Switch Interface)
#### 方法: change_language(language_code: str) -> bool
- **目的**: 切換應用程式語言
- **參數**:
  - language_code: 目標語言代碼 ('ja', 'en', 'zh')
- **返回**: 成功或失敗布林值
- **異常**: 若語言代碼不受支援返回 False

#### 方法: get_available_languages() -> List[str]
- **目的**: 獲取支援的語言列表
- **返回**: 支援語言代碼列表
- **異常**: 無異常

#### 方法: get_current_language() -> str
- **目的**: 獲取當前語言
- **返回**: 目前使用的語言代碼
- **異常**: 無異常

### 2.2 圖片處理接口 (Image Processing Interface)
#### 方法: upload_image(file_path: str) -> str
- **目的**: 上傳並處理圖片
- **參數**:
  - file_path: 來源圖片路徑
- **返回**: 處理後的圖片存儲路徑
- **異常**: 若文件類型不支援或處理失敗則拋出異常

#### 方法: resize_image(image_path: str, max_size: tuple) -> str
- **目的**: 調整圖片大小
- **參數**:
  - image_path: 圖片路徑
  - max_size: 最大大小 (寬度, 高度)
- **返回**: 調整大小後圖片路徑
- **異常**: 若處理失敗則拋出異常

## 3. 回調接口 (Callback Interfaces)

### 3.1 表格雙擊事件回調 (Table Double Click Callback)
界面組件應支援雙擊事件，用於將選定項目數據帶入修改區域：
- **事件名稱**: on_table_double_click
- **參數**: 
  - table_name: 表格名稱
  - selected_row_index: 所選行索引
  - row_data: 行數據字典
- **處理**: 將 row_data 中的數據填入相應的輸入欄位

### 3.2 保存回調 (Save Callback)
界面組件應提供統一的保存事件處理：
- **事件名稱**: on_save
- **觸發條件**: 點擊保存按鈕或按下 Ctrl+S
- **執行**: 驗證數據並保存到數據庫

## 4. 錯誤處理接口 (Error Handling Interface)

### 4.1 一般錯誤處理
- 所有接口應使用統一的錯誤處理機制
- 錯誤應記錄到日誌系統中
- 用戶應收到有意義的錯誤消息

### 4.2 數據驗證錯誤
- 所有數據輸入點都應進行驗證
- 錯誤應在界面層顯示給用戶
- 應提供具體的修正建議