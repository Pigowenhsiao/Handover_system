# Change: Improve SQLite concurrency handling

## Why
Multiple machines share the same SQLite database, leading to intermittent "database is locked" errors during writes.

## What Changes
- Enable SQLite WAL mode and busy timeout pragmas on every connection.
- Add commit retry logic for transient lock errors.
- Document the expected behavior and manual verification steps.

## Impact
- Affected specs: database-concurrency (new)
- Affected code: models.py
