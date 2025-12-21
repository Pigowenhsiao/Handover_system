## ADDED Requirements

### Requirement: Calendar date selection
The system SHALL provide a calendar picker for all date fields and prevent manual text input.

#### Scenario: Daily report date
- **GIVEN** the user is on the daily report page
- **WHEN** the user selects a date
- **THEN** the date is filled via the calendar picker only

#### Scenario: Date filters
- **GIVEN** the user is on delay list or summary actual pages
- **WHEN** the user selects start/end dates
- **THEN** the fields are populated via the calendar picker

#### Scenario: Edit dialogs
- **GIVEN** the user edits a delay or summary actual row
- **WHEN** the user updates the date
- **THEN** the date is selected via the calendar picker
