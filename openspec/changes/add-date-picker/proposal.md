# Change: Add calendar date picker for all date inputs

## Why
目前日期欄位需要手動輸入，容易格式錯誤，也不符合「不可直接輸入」的操作需求。

## What Changes
- 日報表日期改為日曆選擇器，不允許手動輸入。
- 延遲清單與 Summary Actual 的日期篩選欄位改為日曆選擇器。
- 延遲清單與 Summary Actual 的編輯視窗日期欄位改為日曆選擇器。
- 新增共用的日曆選擇器彈窗與多語系文字。

## Impact
- Affected specs: ui-calendar (new)
- Affected code: frontend/src/components/modern_main_frame.py, frontend/public/locales/*.json
