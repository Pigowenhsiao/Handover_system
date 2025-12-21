# Change: 更新總結頁面為出勤統計儀表板

## Why
目前總結頁面僅提供文字欄位與假資料統計，無法滿足管理者需要的出勤統計總覽與視覺化。

## What Changes
- 總結頁面改為「出勤統計」：新增日期區間（開始/結束）與「確定」按鈕。
- 依日期區間彙整 DailyReport + AttendanceEntry，表格顯示「日期/區域/正職出勤/正職缺勤/契約出勤/契約缺勤/備註」。
- 下方加入兩個圖表：出勤率比例圖（出勤 vs 缺勤）與出勤人數堆疊柱狀圖（正職/契約）。
- 圖表文字支援中文/日文顯示（CJK 字型設定與回退策略）。
- 新增/更新多語資源鍵以覆蓋表格、按鈕與圖表標籤。

## Impact
- Affected specs: `summary-dashboard`
- Affected code: `frontend/src/components/modern_main_frame.py`, `frontend/public/locales/*.json`
