# 快速入門指南 (Quickstart Guide)

## 系統架構概覽

電子交接本系統採用前後端分離架構：
- 後端：使用 FastAPI 框架提供 RESTful API 服務
- 前端：使用 React 框架構建用戶界面
- 資料庫：使用 PostgreSQL 存儲系統數據
- 認證：使用 JWT (JSON Web Token) 進行用戶認證

## 開發環境設置

### 1. 後端設置 (FastAPI)

#### 安裝依賴
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### 開發服務器啟動
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### API 文檔
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. 前端設置 (React)

#### 安裝依賴
```bash
npm install react react-dom axios
```

#### 開發服務器啟動
```bash
npm start
```

### 3. 資料庫設置

#### PostgreSQL 設置
1. 安裝 PostgreSQL 13+
2. 創建數據庫
```sql
CREATE DATABASE handover_system;
CREATE USER handover_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE handover_system TO handover_user;
```

## 系統配置

### 環境變量設置
創建 `.env` 文件：
```
DATABASE_URL=postgresql://handover_user:secure_password@localhost/handover_system
SECRET_KEY=your_very_long_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOADS_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

## 主要功能實現

### 1. 使用者認證
- 使用 JWT token 認證
- 登入/登出功能
- 權限檢查中間件
- 密碼使用 bcrypt 加密

### 2. 數據模型
- User: 管理系統使用者
- DailyReport: 保存每日交接報告
- AttendanceEntry: 出勤記錄
- EquipmentLog: 設備異常記錄
- LotLog: 異常批次記錄

### 3. API 端點
- `/api/auth/`: 認證相關
- `/api/users/`: 使用者管理 (管理員專用)
- `/api/reports/`: 交接報告 CRUD 操作
- `/api/upload/image`: 圖片上傳

## 開發指南

### 添加新功能
1. 根據需求更新數據模型
2. 創建相應的 API 端點
3. 在前端實現對應的界面組件
4. 添加必要的驗證和測試

### 擴展數據模型
1. 在 `models.py` 中定義新的數據模型
2. 在 `schemas.py` 中定義 Pydantic 模型
3. 創建相應的 API 端點
4. 在 `database.py` 中創建數據庫表

### 添加前端組件
1. 在 `src/components/` 中創建新組件
2. 使用 React Hooks 管理狀態
3. 使用 axios 與後端 API 通信
4. 添加表單驗證邏輯

## 部署指南

### 生產環境設置
1. 使用環境變量安全地存儲敏感配置
2. 使用反向代理 (如 Nginx) 處理靜態文件
3. 配置 SSL 證書以啟用 HTTPS
4. 使用進程管理器 (如 PM2) 管理應用程序

### 部署腳本
```bash
# 構建前端
npm run build

# 部署後端
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```