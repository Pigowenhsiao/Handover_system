## ADDED Requirements

### Requirement: Login-first flow
The system SHALL present a single login screen before any other UI is accessible.

#### Scenario: User not logged in
- **GIVEN** the application is launched
- **WHEN** the user has not logged in
- **THEN** only the login screen is accessible and navigation is disabled

#### Scenario: Successful login
- **GIVEN** the user enters valid credentials
- **WHEN** the login is confirmed
- **THEN** the system shows the basic information screen

### Requirement: Basic information gating
The system SHALL require date, shift, and area to be saved before enabling other functions.

#### Scenario: Access blocked before basic info
- **GIVEN** basic information is not saved
- **WHEN** the user attempts to open attendance, equipment, or lot pages
- **THEN** the system blocks the action and shows a warning

#### Scenario: Access allowed after save
- **GIVEN** basic information is saved
- **WHEN** the user opens other pages
- **THEN** the pages are enabled and the current report context is displayed

### Requirement: Report context display
The system SHALL display the current report context (date/shift/area) on every page.

#### Scenario: Context updates
- **WHEN** the user changes date, shift, or area
- **THEN** the displayed context updates immediately

### Requirement: Data linking to DailyReport
The system SHALL persist attendance, equipment, and lot records with the corresponding DailyReport via report_id.

#### Scenario: Attendance save
- **GIVEN** a saved DailyReport context
- **WHEN** attendance data is saved
- **THEN** attendance records are stored with report_id

#### Scenario: Equipment and lot add
- **GIVEN** a saved DailyReport context
- **WHEN** equipment or lot records are added
- **THEN** each record is stored with report_id
