## ADDED Requirements
### Requirement: Attendance summary rows can be hidden (soft delete)
The system SHALL allow users to mark attendance summary rows as hidden from the attendance summary table via a context menu action; hidden rows SHALL not appear in the table and SHALL be excluded from attendance statistics.

#### Scenario: Hide selected row
- **WHEN** a user right-clicks a row in the attendance summary table and confirms delete
- **THEN** the row is marked as hidden and removed from the table view
- **AND** the row is excluded from all attendance summary calculations

#### Scenario: Cancel delete
- **WHEN** a user opens the delete action and selects cancel
- **THEN** no changes are applied to the row

### Requirement: Attendance summary delete operations are logged
The system SHALL record a delete log entry containing the current user account and a snapshot of the deleted row data.

#### Scenario: Log delete action
- **WHEN** a row is marked as hidden by a user
- **THEN** the system stores a log entry with user account, timestamp, and the row's data values
