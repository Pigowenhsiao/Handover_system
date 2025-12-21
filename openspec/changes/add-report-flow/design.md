# Design Notes: Report Flow & Linking

## Flow
- App 啟動後顯示登入畫面，成功登入後進入「基本資訊」畫面。
- 未保存基本資訊（日期/班別/區域）時，其他頁面與功能按鈕停用。
- 保存基本資訊後，建立/更新 DailyReport 並記錄 report_id，解鎖其他頁面。

## Data Linking
- AttendanceEntry / EquipmentLog / LotLog 全部以 report_id 對應 DailyReport。
- 出勤儲存採 upsert：同一 report_id 下的 Regular/Contract 寫入或覆寫。
- 設備異常與批次新增寫入新記錄；歷史查詢依 report_id 篩選。

## UI
- 頁首右側顯示目前日報資訊（日期/班別/區域）。
- 基本資訊保存成功時顯示提示與 report_id。
