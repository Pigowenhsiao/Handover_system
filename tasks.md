# 開發任務清單 (Tasks)

## 專案：電子交接本系統 (Handover System)

基於需求規格、實施計劃、數據模型和API合約生成的任務清單。

## Phase 1: 設置 (Setup)

- [ ] T001 建立專案目錄結構 (backend/, frontend/, docs/)
- [ ] T002 建立 backend/requirements.txt (包含 fastapi, uvicorn, sqlalchemy, psycopg2-binary, python-jose[cryptography], passlib[bcrypt], python-multipart)
- [ ] T003 建立環境變數文件 .env (包含 DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, UPLOADS_DIR, MAX_FILE_SIZE)
- [ ] T004 設定 PostgreSQL 資料庫連線配置
- [ ] T005 [P] 建立 Git 存儲庫並初始化 .gitignore

## Phase 2: 基礎設施 (Foundational)

- [ ] T006 建立後端資料庫模型 (models.py) - 根據 data-model.md 實作 User, DailyReport, AttendanceEntry, EquipmentLog, LotLog
- [ ] T007 建立 Pydantic 模式 (schemas.py) - 對應數據模型
- [ ] T008 建立數據庫連線管理 (database.py) - PostgreSQL 連接和會話管理
- [ ] T009 建立 JWT 認證工具 (auth.py) - 使用者認證與密碼雜湊，包含 token 有效期管理
- [ ] T010 實作錯誤處理和日誌記錄 (utils/error_handler.py, utils/logger.py)
- [ ] T011 初始化數據庫表結構 (init_db.py) - 建立所有數據模型對應的表

## Phase 3: [US1] 使用者登入功能

目標：實現使用者透過帳號密碼登入的功能

獨立測試標準：使用者可以使用有效的帳號密碼登入並獲得 JWT token

- [ ] T012 [US1] 建立認證 API 端點 (api/auth.py) - 實作 POST /api/auth/login 和 POST /api/auth/logout
- [ ] T013 [US1] 實作密碼驗證邏輯 (auth.py) - 驗證使用者輸入的密碼
- [ ] T014 [US1] 實作 JWT token 生成、驗證和過期管理 (auth.py)
- [ ] T015 [US1] 建立登入前端頁面 (frontend/src/pages/Login.js)
- [ ] T016 [US1] 實作前端登入表單驗證 (frontend/src/components/LoginForm.js)
- [ ] T017 [US1] 實作前端與後端 API 串接 (frontend/src/services/authService.js)

## Phase 4: [US2] 日報表填寫功能

目標：實現填寫出勤、設備異常、異常批次和總結，並能上傳照片的功能

獨立測試標準：使用者可以填寫並提交完整的日報表，包含多個動態數據和上傳圖片

- [ ] T018 [US2] 建立日報表 API 端點 (api/reports.py) - 實作 POST /api/reports
- [ ] T019 [US2] 建立出勤記錄 API 端點 (api/reports.py) - 處理 AttendanceEntry 關聯數據
- [ ] T020 [US2] 建立設備異常 API 端點 (api/reports.py) - 處理 EquipmentLog 關聯數據
- [ ] T021 [US2] 建立異常批次 API 端點 (api/reports.py) - 處理 LotLog 關聯數據
- [ ] T022 [US2] 建立前端日報表填寫頁面 (frontend/src/pages/DailyReportForm.js)
- [ ] T023 [US2] 實作動態表格組件 (frontend/src/components/DynamicTable.js) - 用於設備異常和異常批次輸入
- [ ] T024 [US2] 實作日期和下拉選單組件 (frontend/src/components/DatePicker.js, SelectArea.js)
- [ ] T025 [US2] 實作圖片上傳組件 (frontend/src/components/ImageUpload.js)
- [ ] T026 [US2] 實作前端表單驗證 (frontend/src/components/FormValidation.js)
- [ ] T027 [US2] 連接前端與後端 API (frontend/src/services/reportService.js)

## Phase 5: [US3] 下拉選單功能

目標：實現班別和區域的下拉選單選擇，以減少輸入錯誤

獨立測試標準：使用者可以透過下拉選單選擇班別和區域，而不是手動輸入

- [ ] T028 [US3] 在日報表填寫頁面添加班別下拉選單 (frontend/src/components/ShiftSelect.js)
- [ ] T029 [US3] 在日報表填寫頁面添加區域下拉選單 (frontend/src/components/AreaSelect.js)
- [ ] T030 [US3] 實作預設選項和驗證邏輯 (frontend/src/components/DailyReportForm.js)
- [ ] T031 [US3] 更新 API 驗證以確保班別和區域值的有效性 (api/reports.py)

## Phase 6: [US4] 報表查詢功能

目標：實現管理者查詢特定日期範圍的報表，並匯出資料的功能

獨立測試標準：管理者可以根據日期範圍和區域篩選查詢日報表，並匯出結果

- [ ] T032 [US4] 擴充日報表 API 端點 (api/reports.py) - 實作 GET /api/reports 查詢功能
- [ ] T033 [US4] 實作日期和區域篩選邏輯 (api/reports.py)
- [ ] T034 [US4] 實作報表匯出功能 (api/reports.py) - 支援 CSV 格式匯出
- [ ] T035 [US4] 建立前端報表查詢頁面 (frontend/src/pages/ReportQuery.js)
- [ ] T036 [US4] 實作篩選條件組件 (frontend/src/components/FilterPanel.js)
- [ ] T037 [US4] 實作報表列表顯示組件 (frontend/src/components/ReportList.js)
- [ ] T038 [US4] 實作報表匯出功能 (frontend/src/services/exportService.js)

## Phase 7: [US5] 使用者管理功能

目標：實現系統管理員維護介面來管理使用者帳號（新增、刪除、修改）

獨立測試標準：管理員可以新增、刪除和修改使用者帳號資訊

- [ ] T039 [US5] 建立使用者管理 API 端點 (api/users.py) - 實作 GET, POST, PUT, DELETE /api/users
- [ ] T040 [US5] 實作權限檢查中間件 (middleware/auth.py) - 確保只有管理員可訪問使用者管理端點
- [ ] T041 [US5] 建立前端使用者管理頁面 (frontend/src/pages/UserManagement.js)
- [ ] T042 [US5] 實作使用者列表組件 (frontend/src/components/UserList.js)
- [ ] T043 [US5] 實作使用者新增表單組件 (frontend/src/components/AddUserForm.js)
- [ ] T044 [US5] 實作使用者編輯表單組件 (frontend/src/components/EditUserForm.js)
- [ ] T045 [US5] 實作權限控制組件 (frontend/src/components/ProtectedRoute.js)

## Phase 8: [US2] 圖片上傳功能

目標：實現圖片上傳功能，將圖片與日報表關聯

獨立測試標準：使用者可以在日報表中上傳圖片，圖片正確保存並與報表關聯

- [ ] T046 [US2] 建立圖片上傳 API 端點 (api/upload.py) - 實作 POST /api/upload/image
- [ ] T047 [US2] 實作圖片存儲邏輯 (api/upload.py) - 保存到 uploads/ 目錄並記錄路徑
- [ ] T048 [US2] 實作圖片驗證邏輯 (api/upload.py) - 驗證檔案類型和大小
- [ ] T049 [US2] 更新設備異常模型以關聯圖片路徑 (models.py)

## Phase 9: 整合測試與優化

- [ ] T050 建立後端單元測試 (tests/test_models.py, test_api.py)
- [ ] T051 建立前端端到端測試 (tests/e2e.test.js)
- [ ] T052 整合測試 - 驗證前端和後端協作正常
- [ ] T053 效能優化 - 添加數據庫查詢索引 (根據 data-model.md 的建議)
- [ ] T054 安全性測試 - 驗證認證與授權機制
- [ ] T055 API 文件更新 - 使用 FastAPI 自動生成的 Swagger 文檔

## Phase 10: 部署與部署配置

- [ ] T056 建立 Dockerfile - 容器化後端應用
- [ ] T057 建立 docker-compose.yml - 整合後端、前端和 PostgreSQL
- [ ] T058 撰寫部署文件 (docs/deployment.md) - 包含環境設置和部署步驟
- [ ] T059 建立 CI/CD 配置文件 (.github/workflows/deploy.yml)
- [ ] T060 進行最終測試並修正在部署環境中發現的問題