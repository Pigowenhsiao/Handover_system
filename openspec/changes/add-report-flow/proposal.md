# Change: Add login + basic info gating and link records to daily report

## Why
目前現代化介面允許未登入與未設定日報基本資訊就操作功能，且出勤/設備/批次資料未與日報表關聯，導致資料難以追蹤與一致性不足。

## What Changes
- 新增單一登入畫面，登入前不可進入主功能。
- 新增「基本資訊」保存門檻：未保存日期/班別/區域前，其他功能不可操作。
- 保存基本資訊時建立/更新 DailyReport，並保存摘要欄位。
- 出勤/設備異常/異常批次的新增與儲存都寫入對應的 DailyReport (report_id)。
- 所有頁面右上角顯示目前日報（日期/班別/區域）。

## Impact
- Affected specs: report-flow (new)
- Affected code: frontend/src/components/modern_main_frame.py, frontend/src/components/attendance_section_optimized.py, frontend/public/locales/*.json, models.py (existing tables reused)
