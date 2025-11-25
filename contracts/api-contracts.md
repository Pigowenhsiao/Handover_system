# API 合約規範 (API Contracts)

## 1. 認證相關端點

### POST /api/auth/login
**功能**: 使用者登入
**請求體**:
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```
**回應**:
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (default: 'bearer')",
  "user": {
    "id": "integer",
    "username": "string",
    "role": "string"
  }
}
```
**狀態碼**: 200 (成功), 401 (認證失敗)

### POST /api/auth/logout
**功能**: 使用者登出
**回應**: 200 (成功)

## 2. 使用者管理端點 (僅管理員權限)

### GET /api/users
**功能**: 獲取所有使用者列表
**回應**:
```json
{
  "users": [
    {
      "id": "integer",
      "username": "string",
      "role": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```
**狀態碼**: 200 (成功), 403 (權限不足)

### POST /api/users
**功能**: 創建新使用者
**請求體**:
```json
{
  "username": "string (3-80 chars, required)",
  "password": "string (min 6 chars, required)",
  "role": "string ('admin' or 'user', default: 'user')"
}
```
**回應**: 
```json
{
  "id": "integer",
  "username": "string",
  "role": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**狀態碼**: 201 (創建成功), 400 (請求錯誤), 403 (權限不足)

### PUT /api/users/{user_id}
**功能**: 更新使用者資訊
**請求體**:
```json
{
  "username": "string (optional)",
  "password": "string (optional, min 6 chars)",
  "role": "string ('admin' or 'user', optional)"
}
```
**回應**: 
```json
{
  "id": "integer",
  "username": "string",
  "role": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**狀態碼**: 200 (更新成功), 400 (請求錯誤), 403 (權限不足), 404 (使用者不存在)

### DELETE /api/users/{user_id}
**功能**: 刪除使用者
**回應**: 204 (成功刪除)
**狀態碼**: 204 (成功), 403 (權限不足), 404 (使用者不存在)

## 3. 日報表相關端點

### GET /api/reports
**功能**: 查詢日報表（支援篩選）
**參數**:
- start_date (string, format: YYYY-MM-DD, optional)
- end_date (string, format: YYYY-MM-DD, optional)
- area (string, optional, values: etching_D, etching_E, litho, thin_film)
- author_id (integer, optional)
**回應**:
```json
{
  "reports": [
    {
      "id": "integer",
      "date": "date",
      "shift": "string",
      "area": "string",
      "author": {
        "id": "integer",
        "username": "string"
      },
      "created_at": "datetime",
      "summary_key_output": "text",
      "summary_issues": "text",
      "summary_countermeasures": "text"
    }
  ]
}
```
**狀態碼**: 200 (成功)

### GET /api/reports/{report_id}
**功能**: 獲取特定日報表詳情
**回應**:
```json
{
  "id": "integer",
  "date": "date",
  "shift": "string",
  "area": "string",
  "author": {
    "id": "integer",
    "username": "string"
  },
  "created_at": "datetime",
  "summary_key_output": "text",
  "summary_issues": "text",
  "summary_countermeasures": "text",
  "attendance_entries": [
    {
      "id": "integer",
      "category": "string",
      "scheduled_count": "integer",
      "present_count": "integer",
      "absent_count": "integer",
      "reason": "text"
    }
  ],
  "equipment_logs": [
    {
      "id": "integer",
      "equip_id": "string",
      "description": "text",
      "start_time": "string",
      "impact_qty": "integer",
      "action_taken": "text",
      "image_path": "string"
    }
  ],
  "lot_logs": [
    {
      "id": "integer",
      "lot_id": "string",
      "description": "text",
      "status": "text",
      "notes": "text"
    }
  ]
}
```
**狀態碼**: 200 (成功), 404 (報表不存在)

### POST /api/reports
**功能**: 創建新日報表
**請求體**:
```json
{
  "date": "date (required)",
  "shift": "string ('Day' or 'Night', required)",
  "area": "string (required)",
  "summary_key_output": "text (optional)",
  "summary_issues": "text (optional)",
  "summary_countermeasures": "text (optional)",
  "attendance_entries": [
    {
      "category": "string ('Regular' or 'Contract', required)",
      "scheduled_count": "integer (default: 0)",
      "present_count": "integer (default: 0)",
      "absent_count": "integer (default: 0)",
      "reason": "text (optional)"
    }
  ],
  "equipment_logs": [
    {
      "equip_id": "string (required)",
      "description": "text (required)",
      "start_time": "string (optional)",
      "impact_qty": "integer (default: 0)",
      "action_taken": "text (optional)"
    }
  ],
  "lot_logs": [
    {
      "lot_id": "string (required)",
      "description": "text (required)",
      "status": "text (optional)",
      "notes": "text (optional)"
    }
  ]
}
```
**回應**: 
```json
{
  "id": "integer",
  "date": "date",
  "shift": "string",
  "area": "string",
  "author_id": "integer",
  "created_at": "datetime",
  "summary_key_output": "text",
  "summary_issues": "text",
  "summary_countermeasures": "text"
}
```
**狀態碼**: 201 (創建成功), 400 (請求錯誤)

### PUT /api/reports/{report_id}
**功能**: 更新日報表
**請求體**: 與 POST /api/reports 相同
**回應**: 與 POST /api/reports 相同
**狀態碼**: 200 (更新成功), 400 (請求錯誤), 403 (權限不足), 404 (報表不存在)

### DELETE /api/reports/{report_id}
**功能**: 刪除日報表
**回應**: 204 (成功刪除)
**狀態碼**: 204 (成功), 403 (權限不足), 404 (報表不存在)

## 4. 圖片上傳端點

### POST /api/upload/image
**功能**: 上傳圖片
**請求**: multipart/form-data
- file: 圖片文件 (required, max size: 10MB)
- report_id: 關聯的日報表ID (optional)
**回應**:
```json
{
  "file_path": "string",
  "file_url": "string",
  "message": "string"
}
```
**狀態碼**: 201 (上傳成功), 400 (檔案錯誤), 413 (檔案太大)