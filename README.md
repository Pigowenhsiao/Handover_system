# 電子交接本系統使用說明

## 概述
單機桌面應用（tkinter），Python 3.9+ 與本機 SQLite。支援登入、日報填寫（出勤、設備異常、異常批次、總結、照片路徑記錄）、報表查詢與匯出、趨勢圖表。介面文字為繁體中文。

## 系統需求
- Python 3.9+
- 依賴套件：`sqlalchemy`, `pandas`, `bcrypt`, `openpyxl`, `matplotlib`（詳見 `requirements.txt`，需系統提供 tkinter / python3-tk）
- 可讀寫本機 SQLite 檔案（無需遠端服務）

## 快速開始
1) 安裝 Python 3.9+  
2) `pip install -r requirements.txt`  
3) 執行 `python app.py`（或 `python3 app.py`）  
4) 首次啟動會自動建立資料庫與預設管理員帳號（請登入後修改密碼）

## 功能說明
- 登入/登出：本機 Session 管理。
- 日報填寫：PDF 對應欄位，班別/區域下拉；出勤預設兩行（正社員/契約），設備異常與異常批次可新增多筆；圖片路徑可記錄（未內嵌預覽）。
- 總結：Key Machine Output / Key Issues / Countermeasures。
- 報表：人員出勤/設備異常/異常 LOT 三種報表；支援日/週（週一~週日）/月/自訂期間；表格與圖表並列展示；各報表獨立 CSV 匯出。
- 使用者管理（管理員）：新增/刪除/重設密碼。
- 匯入：預留「匯入 Excel」按鈕（待提供格式後實作）。

## 數據庫
- 本機 SQLite 檔案，模型定義於 `models.py`。
- 主要表格：User、DailyReport、AttendanceEntry、EquipmentLog、LotLog。

## 技術架構
- UI：tkinter，介面文字為繁體中文。
- 應用層：本機 Session，Notebook 分頁導覽。
- 資料層：SQLAlchemy ORM 對 SQLite，禁止 Raw SQL。

## 注意事項
1. 確保 `uploads/` 可寫入以儲存圖片。
2. 不需網路與後端 API，所有邏輯本機執行。
3. 密碼以 bcrypt 雜湊存放，請妥善保管管理員密碼。

## 組織結構
- `app.py`: tkinter 主入口、登入、分頁（填寫日報/歷史查詢/使用者管理）
- `models.py`: SQLAlchemy 模型與 `init_db`
- `auth.py`: 密碼雜湊與驗證
- `uploads/`: 圖片儲存位置（目前記錄路徑，未自動複製）

## 疑難排解
1. 確認已安裝依賴 `pip install -r requirements.txt`
2. 若啟動失敗，請查看終端錯誤訊息
3. 確認 `app.py`、`models.py`、`auth.py` 存在且可讀
4. 確認目前使用者對資料庫檔與 `uploads/` 有讀寫權限
