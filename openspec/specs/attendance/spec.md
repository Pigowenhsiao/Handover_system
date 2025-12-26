## Requirements
### Requirement: Edit attendance summary rows
The system SHALL allow editing attendance summary rows (date, shift, area) via a double-click action and an explicit update action.

#### Scenario: Update summary row
- **WHEN** a user double-clicks a summary row and updates date/shift/area
- **THEN** the report is saved and the summary table reflects the changes

### Requirement: Track attendance summary modifications
The system SHALL record and display the latest modifier and timestamp for attendance summary rows.

#### Scenario: Track last modification
- **WHEN** the user updates a summary row
- **THEN** the system records and displays the latest modifier and timestamp as the last column

### Requirement: Prevent summary update conflicts
The system SHALL reject updates when the updated date/shift/area would conflict with an existing report.

#### Scenario: Prevent key conflicts
- **WHEN** the updated date/shift/area would conflict with an existing report
- **THEN** the system rejects the update and shows a warning

### Requirement: Attendance summary rows can be hidden (soft delete)
The system SHALL allow users to mark attendance summary rows as hidden from the attendance summary table via a context menu action; hidden rows SHALL not appear in the table and SHALL be excluded from attendance statistics.

#### Scenario: Hide selected row
- **WHEN** a user right-clicks a row in the attendance summary table and confirms delete
- **THEN** the row is marked as hidden and removed from the table view
- **AND** the row is excluded from all attendance summary calculations

#### Scenario: Cancel delete
- **WHEN** a user opens the delete action and selects cancel
- **THEN** no changes are applied to the row

### Requirement: Hidden attendance rows are automatically restored on new input
The system SHALL automatically clear the hidden flag when a user later inputs data for the same date, shift, and area, and SHALL include the row in the table and statistics.

#### Scenario: New input restores hidden row
- **WHEN** a user saves a report with the same date, shift, and area as a hidden row
- **THEN** the hidden flag is cleared and the row is included in the table and statistics

### Requirement: Attendance summary delete operations are logged
The system SHALL record a delete log entry containing the current user account and a snapshot of the deleted row data.

#### Scenario: Log delete action
- **WHEN** a row is marked as hidden by a user
- **THEN** the system stores a log entry with user account, timestamp, and the row's data values
