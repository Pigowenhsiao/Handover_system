## Context
Multiple desktop clients share a single SQLite file over a network share. Concurrent writes can produce transient lock errors.

## Goals / Non-Goals
- Goals: Reduce "database is locked" incidents during concurrent writes; keep local SQLite deployment.
- Non-Goals: Guarantee full multi-writer safety across unreliable network filesystems; migrate to a server database.

## Decisions
- Decision: Enable WAL mode and set busy_timeout on each SQLite connection.
- Decision: Retry commit on lock errors with bounded retries and backoff.

## Risks / Trade-offs
- WAL files on network shares can still encounter locking issues; retries only mitigate transient failures.

## Migration Plan
- No schema changes; apply runtime connection settings on next app start.

## Open Questions
- None.
