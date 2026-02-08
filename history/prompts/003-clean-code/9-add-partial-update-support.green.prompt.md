---
id: 9
title: Add Partial Update Support
stage: green
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5
feature: 003-clean-code
branch: 003-clean-code
user: developer
command: /sp.implement
labels: ["feature", "partial-update", "ux-improvement", "green"]
links:
  spec: specs/003-clean-code/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/services/task_service.py
  - src/cli/menu.py
tests:
  - Partial update - title only
  - Partial update - description only
  - Partial update - both fields
  - Partial update - whitespace preservation
  - Partial update - empty preservation
---

## Prompt

```text
If any field is empty by user in update section It means the field remains same and user don't want to update that field; (Update this feature in update task functionality)
```

## Response snapshot

**Feature Request:** Allow users to selectively update task fields by leaving inputs empty to preserve existing values.

**Implementation:**

**1. Service Layer Changes (task_service.py)**

Modified `update_task()` method to support partial updates:
- Retrieves existing task before validation
- Checks if title input is empty/whitespace
  - If empty: preserves existing title
  - If provided: validates and updates title
- Checks if description input is empty/whitespace
  - If empty: preserves existing description
  - If provided: validates and updates description
- Maintains all existing validation rules for non-empty inputs

**2. CLI Layer Changes (menu.py)**

Enhanced `handle_update_task()` for better UX:
- Added note: "Leave a field empty to keep its current value"
- Displays current task values before prompting for updates
- Shows current title and description
- Updated input prompts: "Enter new title (or press Enter to keep)"
- Improved error hint for partial updates

**3. Test Results**

All 5 test scenarios passed:
```
Test 1: Update only title (empty description)
  [PASS] Description preserved: True

Test 2: Update only description (empty title)
  [PASS] Title preserved: True

Test 3: Update both fields
  [PASS] Both updated: True

Test 4: Update with whitespace-only (should preserve)
  [PASS] Both preserved: True

Test 5: Update neither (both empty)
  [PASS] Both preserved: True
```

**Use Cases Enabled:**
- Update only title: provide new title, press Enter for description
- Update only description: press Enter for title, provide new description
- Update both: provide both new values
- Update neither: press Enter for both (no changes made)

**Backward Compatibility:**
- Existing behavior preserved when both fields provided
- All validation rules still apply to non-empty inputs
- No breaking changes to API or data model

**Architecture Compliance:**
- Changes isolated to service and CLI layers
- No storage layer modifications needed
- Layer boundaries maintained
- Clean separation of concerns

## Outcome

- ✅ Impact: Significantly improved update UX - users can now selectively update fields without re-entering unchanged values
- 🧪 Tests: 5 partial update scenarios tested and passing
- 📁 Files: 2 files modified (task_service.py, menu.py)
- 🔁 Next prompts: Consider adding bulk update operations, or implement task search/filter
- 🧠 Reflection: Partial updates are a common UX pattern that reduces friction. Implementation was straightforward by checking for empty input before validation. Showing current values helps users make informed decisions about what to update.

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation worked on first attempt
- Graders run and results (PASS/FAIL): All 5 partial update tests PASS
- Prompt variant (if applicable): Standard implementation with comprehensive testing
- Next experiment (smallest change to try): Add "skip" keyword as alternative to empty input, or implement field-by-field confirmation prompts
