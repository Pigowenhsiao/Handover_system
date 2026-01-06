# Change: Refactor shared functions and UI helpers

## Why
Repeated UI patterns and data-handling logic are duplicated across modules, which increases inconsistency risk and slows maintenance. Centralizing shared behaviors improves consistency and reduces future change cost without altering external behavior.

## What Changes
- Introduce shared UI helper modules for section headers, labeled inputs, and button rows
- Centralize Treeview/table setup and CRUD/context menu wiring
- Centralize attendance/overtime validation and totals logic
- Centralize report key/date/shift/area helpers and settings access
- Centralize i18n widget registration and translation application
- Centralize import pipelines for Delay List and Summary Actual
- Update call sites to use shared helpers with no behavior change
- Update specs and documentation (`@fun.md`, `@API.md`)

## Impact
- Affected specs: attendance, delay-list, summary-actual, ui-helpers (new)
- Affected code: `frontend/src/components/modern_main_frame.py`, `frontend/src/components/widgets.py`, `frontend/src/utils/*`, `frontend/i18n/*`, `tests/*`
