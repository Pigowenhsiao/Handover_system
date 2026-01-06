## 1. Implementation
- [x] 1.1 Add SQLite pragmas for WAL and busy_timeout on connect.
- [x] 1.2 Add commit retry for transient database-locked errors.
- [x] 1.3 Add retry/timeout constants for tuning.
- [x] 1.4 Add manual verification notes.

## Manual Verification
- Open two app instances against the same database and perform overlapping writes; confirm transient lock errors are retried.
- Confirm the database reports WAL mode and a non-zero busy_timeout.
