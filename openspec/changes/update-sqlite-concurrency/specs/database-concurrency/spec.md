## ADDED Requirements
### Requirement: SQLite concurrency hardening
The system SHALL configure SQLite for WAL mode and busy_timeout, and retry commits when transient lock errors occur.

#### Scenario: WAL and busy timeout enabled
- **WHEN** the application opens a SQLite connection
- **THEN** it sets `journal_mode=WAL` and a non-zero `busy_timeout`

#### Scenario: Retry commit on lock errors
- **WHEN** a commit fails with a transient "database is locked" error
- **THEN** the system retries the commit a bounded number of times before surfacing the error
