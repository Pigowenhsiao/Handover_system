## Context
The UI layer currently repeats patterns for constructing sections, tables, and form rows. Data validation and import pipelines are implemented inline in multiple places. This change consolidates these patterns into shared helpers while preserving existing behavior.

## Goals / Non-Goals
- Goals: reduce duplication, enforce consistent UI/table behaviors, keep existing behavior unchanged, simplify future updates
- Non-Goals: add new user-facing features, change data schema, alter API contracts

## Decisions
- Decision: introduce shared helper modules in `frontend/src/utils/` and/or `frontend/src/components/` for UI composition and data handling
- Decision: keep helpers small and focused (single-responsibility), use existing patterns and naming

## Risks / Trade-offs
- Risk: unintended UI behavior changes due to shared logic
  - Mitigation: update call sites incrementally and verify with existing scripts/manual checklist

## Migration Plan
1. Add helpers (no call-site changes)
2. Update call sites in `modern_main_frame.py` sequentially by section
3. Run verification scripts and manual checklist

## Open Questions
- Confirm which UI sections are highest priority for helper extraction
- Confirm acceptable scope for manual UI testing in this environment
