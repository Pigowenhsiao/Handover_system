## ADDED Requirements
### Requirement: Shared UI helper construction
The system SHALL provide shared helper functions for standard UI elements (section headers, labeled inputs, button rows, and Treeview tables) to keep layout and behavior consistent across modules.

#### Scenario: Use shared helpers for tables
- **WHEN** a module renders a standard Treeview table
- **THEN** the shared table helper is used for column definitions, styling, and context menu wiring

### Requirement: Shared translation application
The system SHALL provide shared helper utilities to register widgets with translation keys and apply translations when the active language changes.

#### Scenario: Apply translations through shared helper
- **WHEN** the active language changes
- **THEN** registered widgets update their labels via the shared translation helper
