# ‚-<‡T¬„¯¯†<TŠ¦¦‘~Z (Implementation Tasks)

‘ÿ1‘"s‚>¯†-?„§‘Z‘oª‡3¯‡æñ‡s,ŠÝ?‘ÿ¬a??†_Ý‘-«Š"^†SŸa??‘,‘"s‘"­†z<†'OAPI†?^‡',‡"Y‘^?‡s,„¯¯†<T‘,.†-ra?,

## Phase 1: †Y§‡ZŠ"-‘-« (Infrastructure)

- [ ] T001 †¯§‡®<†ø^‘­^‡>r‚O,‡æ?‘< (backend/, frontend/, docs/, specs/, uploads/) — 現有 backend/frontend/docs/specs，但 uploads/ 未建立
- [ ] T002 [P] †r%Šœ?†_O‡®_„_?Š3'†-„¯ (FastAPI, SQLAlchemy, bcrypt, Pillow‡-%) — backend/database/connection.py 不存在；僅有 base.py / session.py
- [ ] T003 [P] †r%Šœ?†%?‡®_„_?Š3'†-„¯ (tkinter, i18n‡-%) — backend/config/settings.py 不存在；實際設定在 backend/core/config.py
- [ ] T004 †¯§‡®<†^?†<Š¦zŠ"?Š3Ø‘§?‘-Ø„¯ (zh.json, ja.json, en.json) †o" frontend/public/locales/ — 檔案已存在但未同步任務狀態

## Phase 2: ‘ÿ,†¨Ÿ†SYŠŸ« (Core Features)

- [ ] T005 †_Ý‡?_‘,‘"s†§®‘"­†z< (backend/models/user.py, daily_report.py, attendance.py, equipment.py, lot.py) — 僅有 backend/models/all_models.py 與根目錄 models.py，未依路徑拆檔
- [ ] T006 †_Ý‡?_Š¦?Š-%‡3¯‡æñ (backend/auth/user_auth.py) — 無此檔案，相關邏輯在 backend/core/security.py / 根目錄 auth.py
- [ ] T007 †¯§‡®<†sŠ¦zŠ"?‘"_‘O?‘­+‘z (backend/i18n/language_manager.py) — 無此路徑，語言管理在 backend/core/language_manager.py
- [X] T008 †%æ†¯§Š¦zŠ"?‚?,‘"Ø‡O‚?› (frontend/src/components/LanguageSelector.py)
- [ ] T009 †_Ý‡?_‘-†ÿñŠ­"†SYŠŸ« (backend/api/reports.py) — 實作位於 backend/api/v1/endpoints/reports.py
- [ ] T010 †_Ý‡?_†Ø§†<Š"~‚O,†SYŠŸ« (backend/api/attendance.py) — 實作位於 backend/api/v1/endpoints/attendance.py
- [ ] T011 †_Ý‡?_Š"-†,T‡ø†,,Š"~‚O,†SYŠŸ« (backend/api/equipment.py) — 實作位於 backend/api/v1/endpoints/equipment.py
- [ ] T012 †_Ý‡?_‡ø†,,‘%1‘ª­Š"~‚O,†SYŠŸ« (backend/api/lots.py) — 實作位於 backend/api/v1/endpoints/lots.py

## Phase 3: ‡O‚?›‚-<‡T¬ (UI Development)

- [ ] T013 †%æ†¯§„,¯‡O‚?›‘­+‘z (frontend/src/components/MainApp.py) — 無此檔案，現有為 frontend/src/components/main_app_frame.py
- [ ] T014 †_Ý‡?_Š¦zŠ"?†^Ø‘?>‡æ,„¯ (frontend/src/components/LanguageSwitcher.py) — 無此檔案，現有為 LanguageSelector.js / language_selector.py
- [ ] T015 †_Ý‡?_†øZŠ^¦Š?o†-r (frontend/src/components/NavigationMenu.py) — 無此檔案
- [ ] T016 †_Ý‡?_‡T¯†.‡O‚?› (frontend/src/components/LoginPage.py) — 無此檔案
- [ ] T017 †_Ý‡?_‘-†ÿñŠ­"†­®†_®‡O‚?› (frontend/src/components/DailyReportForm.py) — 無此檔案；相關功能集中於 app.py / Tk UI
- [ ] T018 †_Ý‡?_†Ø§†<Š"~‚O,‡O‚?› (frontend/src/components/AttendanceSection.py) — 無此檔案；Tk UI 內含
- [ ] T019 †_Ý‡?_Š"-†,T‡ø†,,Š"~‚O,‡O‚?› (frontend/src/components/EquipmentLogSection.py) — 無此檔案；Tk UI 內含
- [ ] T020 †_Ý‡?_‡ø†,,‘%1‘ª­Š"~‚O,‡O‚?› (frontend/src/components/LotLogSection.py) — 無此檔案；Tk UI 內含
- [ ] T021 †_Ý‡?_‡,«‡æ?Š¬,†.‡O‚?› (frontend/src/components/SummarySection.py) — 無此檔案；Tk UI 內含
- [ ] T022 †_Ý‡?_†o-‡%Ø„,S†,3†SYŠŸ« (frontend/src/components/ImageUploader.py) — 無此檔案；上傳流程未落地

## Phase 4: ‚®~‡'s†SYŠŸ« (Advanced Features)

- [ ] T023 †_Ý‡?_„«¨‡""Š?.‡r­‡?+‡O‚?› (frontend/src/components/UserManagement.py) — 無此檔案
- [ ] T024 ‚-<‡T¬‘?o†ø<†'O‚?Z‘¨_†SYŠŸ« (backend/api/search.py) — 無此檔案
- [ ] T025 †_Ý‡?_†ÿñŠ­"†O_†Ø§†SYŠŸ« (backend/utils/report_exporter.py) — 無此檔案
- [ ] T026 †_Ý‡?_‘,‘"s†,T„¯«†'O‘?›†_c†SYŠŸ« (backend/utils/data_backup.py) — 無此檔案
- [ ] T027 †¯§‡®<‘"?„«o‘-Š¦OŠ"~‚O,‡3¯‡æñ (backend/utils/logger.py) — 無此檔案
- [ ] T028 †_Ý‡?_‡O‚?›„,¯‚­O†^Ø‘?>†SYŠŸ« (frontend/src/utils/theme_manager.py) — 無此檔案

## Phase 5: ‘,ªŠcÝŠ^Ø†,¦†O- (Testing & Optimization)

- [ ] T029 †¯§‡®<†-r†.Ÿ‘,ªŠcÝ†-„¯ (tests/unit_tests.py) — 無 tests/ 目錄
- [ ] T030 †¯§‡®<‘'†?^‘,ªŠcÝ (tests/integration_tests.py) — 無 tests/ 目錄
- [ ] T031 †YúŠ­O‘^ŠŸ«‘,ªŠcÝ†'O†,¦†O- (tests/performance_tests.py) — 無 tests/ 目錄
- [ ] T032 †YúŠ­O†r%†."‘?‘,ªŠcÝ (tests/security_tests.py) — 無 tests/ 目錄
- [ ] T033 ‚?ýŠ­O‡O‚?›†?_‡""‘?‘,ªŠcÝ (tests/usability_tests.py) — 無 tests/ 目錄

## Phase 6: ‚Ÿ"‡«ýŠ^Ø‘-Ø„¯ (Deployment & Documentation)

- [ ] T034 †%æ†¯§‘%"†O.Š.3‘oª (scripts/build_executable.py) — 無此檔案
- [ ] T035 ‘'ø†_®‡""‘^‘"?„«o‘%<†+S (docs/user_manual.md) — 無此檔案
- [ ] T036 ‘'ø†_®‡3¯‡æñ‡r­‡?+‘%<†+S (docs/admin_guide.md) — 無此檔案
- [ ] T037 †_Ý‘-«‘o?‡æ,‡3¯‡æñ‘,ªŠcÝ (tests/final_integration_test.py) — 無 tests/ 目錄
- [ ] T038 ‘§-†,T‚Ÿ"‡«ý‡%^‘oª (releases/v1.0.0/) — 無 releases/ 目錄
