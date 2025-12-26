## Requirements
### Requirement: Summary Actual import supports sheet selection
The system SHALL allow users to choose an Excel worksheet when importing Summary Actual data.

#### Scenario: Select worksheet for import
- **WHEN** an Excel file contains multiple worksheets
- **THEN** the system prompts the user to select a worksheet for import

### Requirement: Summary Actual import skips all-zero rows
The system SHALL skip importing rows where Plan, Completed, In Process, On Track, At Risk, Delayed, No Data, and Scrapped are all zero.

#### Scenario: Skip zero rows
- **WHEN** a Summary Actual row has all zero values across the numeric columns
- **THEN** the row is not imported into the table

### Requirement: Summary Actual table supports delete action
The system SHALL provide a context menu delete action for Summary Actual rows.

#### Scenario: Delete selected rows
- **WHEN** a user right-clicks selected rows in the Summary Actual table and chooses delete
- **THEN** the selected rows are removed from the view and data source
