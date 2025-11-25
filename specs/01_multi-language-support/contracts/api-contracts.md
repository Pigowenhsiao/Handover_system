# 多語言支持功能API合約 (API Contracts)

## 1. 語言資源管理端點

### GET /api/languages/resources
**功能**: 獲取指定語言的翻譯資源
**參數**:
- lang (string, required) - 語言代碼，例如 "zh", "ja", "en"
- namespace (string, optional) - 命名空間，例如 "common", "validation"
**回應**:
```json
{
  "lang": "string",
  "namespace": "string",
  "resources": {
    "key1": "translation1",
    "key2": "translation2",
    "nested": {
      "key3": "nested translation"
    }
  }
}
```
**狀態碼**: 200 (成功), 400 (參數錯誤), 404 (語言資源不存在)

### POST /api/languages/resources
**功能**: 創建或更新翻譯資源 (管理員權限)
**請求體**:
```json
{
  "language_code": "string (required)",
  "namespace": "string (optional, default: 'common')",
  "resources": {
    "key1": "translation1",
    "key2": "translation2"
  }
}
```
**回應**:
```json
{
  "success": "boolean",
  "message": "string",
  "updated_resources": ["key1", "key2"]
}
```
**狀態碼**: 200 (更新成功), 400 (請求錯誤), 403 (權限不足)

### PUT /api/languages/resources/{resource_id}
**功能**: 更新單個翻譯資源 (管理員權限)
**請求體**:
```json
{
  "resource_value": "string (required)"
}
```
**回應**:
```json
{
  "id": "integer",
  "language_code": "string",
  "resource_key": "string",
  "resource_value": "string",
  "namespace": "string"
}
```
**狀態碼**: 200 (更新成功), 400 (請求錯誤), 403 (權限不足), 404 (資源不存在)

### DELETE /api/languages/resources/{resource_id}
**功能**: 刪除翻譯資源 (管理員權限)
**回應**: 204 (成功刪除)
**狀態碼**: 204 (成功), 403 (權限不足), 404 (資源不存在)

## 2. 語言設置端點

### GET /api/languages/settings
**功能**: 獲取用戶或系統的語言設置
**回應**:
```json
{
  "current_language": "string",
  "available_languages": [
    {
      "code": "string",
      "name": "string",
      "is_active": "boolean"
    }
  ],
  "is_default": "boolean"
}
```
**狀態碼**: 200 (成功)

### PUT /api/languages/settings
**功能**: 更新用戶的語言設置
**請求體**:
```json
{
  "language_code": "string (required)"
}
```
**回應**:
```json
{
  "success": "boolean",
  "message": "string",
  "new_language": "string"
}
```
**狀態碼**: 200 (更新成功), 400 (參數錯誤)

## 3. 管理員語言管理端點

### GET /api/admin/languages
**功能**: 獲取所有語言包列表 (管理員權限)
**回應**:
```json
{
  "languages": [
    {
      "id": "integer",
      "language_code": "string",
      "pack_name": "string",
      "version": "string",
      "is_active": "boolean",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```
**狀態碼**: 200 (成功), 403 (權限不足)

### POST /api/admin/languages
**功能**: 創建新的語言包 (管理員權限)
**請求體**:
```json
{
  "language_code": "string (required)",
  "pack_name": "string (required)",
  "version": "string (optional)"
}
```
**回應**:
```json
{
  "id": "integer",
  "language_code": "string",
  "pack_name": "string",
  "version": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**狀態碼**: 201 (創建成功), 400 (參數錯誤), 403 (權限不足)

### PUT /api/admin/languages/{lang_id}
**功能**: 更新語言包設置 (管理員權限)
**請求體**:
```json
{
  "pack_name": "string (optional)",
  "version": "string (optional)",
  "is_active": "boolean (optional)"
}
```
**回應**:
```json
{
  "id": "integer",
  "language_code": "string",
  "pack_name": "string",
  "version": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**狀態碼**: 200 (更新成功), 400 (參數錯誤), 403 (權限不足), 404 (語言包不存在)

### POST /api/admin/languages/import
**功能**: 匯入語言資源文件 (管理員權限)
**請求**: multipart/form-data
- file: 語言資源文件 (JSON 格式，required)
- language_code: 語言代碼 (required)
- namespace: 命名空間 (optional)
**回應**:
```json
{
  "success": "boolean",
  "message": "string",
  "imported_count": "integer",
  "updated_count": "integer"
}
```
**狀態碼**: 200 (匯入成功), 400 (檔案錯誤), 403 (權限不足)