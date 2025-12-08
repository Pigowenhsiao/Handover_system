# ‚>¯†-?„§‘Z‘oª‡3¯‡æñ†_Ý‡?_†rO‘^?†ÿñ†`S

## 1. ‚ÿ.‡>r‘Ý,Š¨ø

現況：程式庫已包含 Tkinter 桌面端 (`app.py`) 與 FastAPI 後端 (`backend/`)，多語 JSON 檔也存在，但仍缺少 uploads 目錄、Excel 匯入流程、模組化視圖檔、測試與部署文件/腳本，與 SPEC 任務表不符。

## 2. †SYŠŸ«†_Ý‡?_‘,.†-r

### 2.1 †sŠ¦zŠ"?‘"_‘O? (SPEC 01_multi-language-support)
- [ ] 「多語介面可切換」：多語檔存在，但未驗證成功準則，且任務表仍未同步
- [ ] 「語系快取/預載」：未有測試或完成證據

### 2.2 ‡O‚?›‘"T‡§Š«%‘?> (SPEC 02_multilang-labels)
- [ ] 「介面標籤覆蓋率 100%」：未驗證，成功準則未達
- [ ] 「本地化持久化」：僅檔案存在，未證實行為

### 2.3 †Ø§†<Š"~‚O,†SYŠŸ«‘"1†-, (SPEC 03_attendance-enhancement)
- [ ] 「排班/出勤 API 與 UI」：有程式碼，但未對照 SPEC 驗證
- [ ] 「性能/錯誤處理」：未驗證

## 3. ‡3¯‡æñ‘z‘<

### 3.1 †%?‡®_‡O‚?› (tkinter)
- 介面集中於 `app.py`，缺少原規劃的拆分視圖檔

### 3.2 †_O‡®_‹¬^‡ø­†O-†_Ý‡?_‹¬%
- FastAPI/SQLAlchemy/bcrypt 已存在，但與任務檔路徑不一致（config、auth、models 等）

### 3.3 ‚.?‡«r‘-Ø„¯
- 多語 JSON (`frontend/public/locales/*.json`) 已存在
- uploads/ 目錄未建立；Excel 匯入未實作

## 4. ‘S?Š­"†_Ý‡?_

### 4.1 ‚-<‡T¬Š¦zŠ"?
- Python 版本未鎖定；`requirements.txt` 已列出主要套件

### 4.2 „«¨‡""‘­+‘z
- Tkinter、FastAPI、SQLAlchemy、bcrypt 等已在需求檔；實作路徑與 SPEC 需調和

## 5. ‘r%Šœ?Š^Ø‚?<Š­O

- 需建立 uploads/ 目錄與相關上傳流程
- 需補齊匯入 Excel、檔案上傳、備份/匯出、測試與部署腳本

## 6. ‘^?†SY‘"T‘§-‚c-Š-%

- [ ] 多語切換、標籤覆蓋、性能與持久化等成功準則未驗證
- [ ] Excel 匯入與 uploads 上傳流程未達成
- [ ] 測試與部署準則未達成（測試目錄與腳本缺失）

## 7. ‡æ?Š®-

1. uploads/ 目錄缺失，相關上傳/匯出流程未落地
2. Excel 匯入功能未實作
3. 視圖拆分檔 (`views/*.py`) 依 SPEC 規劃但未存在
4. 後端/前端檔案路徑與任務描述不一致，需調和或更新 SPEC
5. 測試套件、部署腳本與文件（user/admin guide、release 目錄）缺失
6. 成功準則未驗證；不應標示為完成
