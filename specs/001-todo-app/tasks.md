# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: Tests are NOT included in this task list (not requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- All source code in `src/` with layered subdirectories

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with src/ directory and layer subdirectories (cli/, services/, domain/, storage/, utilities/) with __init__.py files
- [X] T002 [P] Create constants module in src/utilities/constants.py with MAX_TITLE_LENGTH=100, MAX_DESC_LENGTH=500, and error message constants

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain entities that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Create TaskStatus enum in src/domain/task.py with INCOMPLETE and COMPLETE values
- [X] T004 Create Task dataclass in src/domain/task.py with id, title, description, and status fields (depends on T003)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with titles and descriptions and see them listed in the console

**Independent Test**: Launch the app, add 2-3 tasks with different titles/descriptions, view the task list, and verify all tasks appear with correct details and "Incomplete" status

**Spec Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-010, FR-011, FR-013, FR-014, FR-015, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023

### Implementation for User Story 1

- [X] T005 [P] [US1] Create InMemoryTaskStore class in src/storage/memory_store.py with create_task(), get_task(), and get_all_tasks() methods, ID generation logic (starts at 1, never reuses), and in-memory dict storage
- [X] T006 [US1] Implement TaskService class in src/services/task_service.py with add_task() method (validates title/description length, normalizes newlines to spaces) and list_tasks() method (sorts by status then ID: incomplete first, then complete) (depends on T005)
- [X] T007 [US1] Implement menu display and user interaction in src/cli/menu.py with display_menu(), get_user_choice(), handle_add_task(), handle_view_tasks(), format_task_list(), and error handling for validation failures (depends on T006)
- [X] T008 [US1] Create application entry point in src/main.py that initializes InMemoryTaskStore, TaskService, and runs main menu loop with exit option (depends on T007)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks and view them in sorted order

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Create 3 tasks, mark 2 as complete, view the list to verify status indicators show correctly, then mark 1 back to incomplete and verify the toggle works

**Spec Requirements**: FR-006, FR-012, FR-013, FR-014

### Implementation for User Story 2

- [X] T009 [US2] Add toggle_task_status() method to InMemoryTaskStore in src/storage/memory_store.py that toggles between INCOMPLETE and COMPLETE status
- [X] T010 [US2] Add toggle_task_status() method to TaskService in src/services/task_service.py that validates task ID exists and calls storage layer (depends on T009)
- [X] T011 [US2] Add handle_toggle_status() function to CLI in src/cli/menu.py that prompts for task ID, calls service, and displays success/error messages (depends on T010)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create, view, and mark tasks complete/incomplete

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can edit task titles and descriptions to correct mistakes or update information

**Independent Test**: Create a task, update its title only, verify the change, then update its description only, verify that change, and confirm the status remains unchanged

**Spec Requirements**: FR-007, FR-008, FR-010, FR-012, FR-013, FR-014, FR-018, FR-019, FR-020, FR-021

### Implementation for User Story 3

- [X] T012 [US3] Add update_task() method to InMemoryTaskStore in src/storage/memory_store.py that updates title and/or description while preserving status
- [X] T013 [US3] Add update_task() method to TaskService in src/services/task_service.py that validates task ID exists, validates new title/description (if provided), normalizes text, and calls storage layer (depends on T012)
- [X] T014 [US3] Add handle_update_task() function to CLI in src/cli/menu.py that prompts for task ID and new title/description (allowing skip), calls service, and displays success/error messages (depends on T013)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - users can create, view, mark complete, and update tasks

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can remove tasks they no longer need to keep the list clean

**Independent Test**: Create 5 tasks, delete 2 specific tasks by ID, view the list to confirm they're gone, and verify the remaining 3 tasks are still present and unchanged

**Spec Requirements**: FR-009, FR-012, FR-013, FR-014

### Implementation for User Story 4

- [X] T015 [US4] Add delete_task() method to InMemoryTaskStore in src/storage/memory_store.py that removes task from dict and returns success boolean
- [X] T016 [US4] Add delete_task() method to TaskService in src/services/task_service.py that validates task ID exists and calls storage layer (depends on T015)
- [X] T017 [US4] Add handle_delete_task() function to CLI in src/cli/menu.py that prompts for task ID, calls service, and displays success/error messages (depends on T016)

**Checkpoint**: All user stories should now be independently functional - full CRUD operations available

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation and quality assurance across all user stories

- [X] T018 Manual testing against all acceptance scenarios from spec.md (User Stories 1-4) to verify functional requirements
- [X] T019 Validate clean code compliance: verify layer boundaries, check function lengths ≤25 lines, confirm type hints and docstrings present, validate no circular imports

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable

### Within Each User Story

- Storage layer before service layer
- Service layer before CLI layer
- CLI layer before main entry point (US1 only)
- Story complete before moving to next priority

### Parallel Opportunities

- T002 can run in parallel with T001 (different files)
- T003 can run in parallel with T002 (different files)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within US2, US3, US4: Storage and service tasks must be sequential, but different stories can run in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch US1 tasks:
Task T005: "Create InMemoryTaskStore class in src/storage/memory_store.py..."
# Wait for T005 to complete, then:
Task T006: "Implement TaskService class in src/services/task_service.py..." (depends on T005)
# Wait for T006 to complete, then:
Task T007: "Implement menu display and user interaction in src/cli/menu.py..." (depends on T006)
# Wait for T007 to complete, then:
Task T008: "Create application entry point in src/main.py..." (depends on T007)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004) - CRITICAL
3. Complete Phase 3: User Story 1 (T005-T008)
4. **STOP and VALIDATE**: Test User Story 1 independently against acceptance scenarios
5. Demo basic task creation and viewing functionality

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T005-T008) → Test independently → Demo (MVP: Create and View!)
3. Add User Story 2 (T009-T011) → Test independently → Demo (Now with status tracking!)
4. Add User Story 3 (T012-T014) → Test independently → Demo (Now with editing!)
5. Add User Story 4 (T015-T017) → Test independently → Demo (Full CRUD complete!)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T004)
2. Once Foundational is done:
   - Developer A: User Story 1 (T005-T008) - MUST complete first for MVP
   - After US1 complete, developers can work in parallel:
     - Developer A: User Story 2 (T009-T011)
     - Developer B: User Story 3 (T012-T014)
     - Developer C: User Story 4 (T015-T017)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 19

**By Phase**:
- Phase 1 (Setup): 2 tasks
- Phase 2 (Foundational): 2 tasks
- Phase 3 (User Story 1 - P1 MVP): 4 tasks
- Phase 4 (User Story 2 - P2): 3 tasks
- Phase 5 (User Story 3 - P3): 3 tasks
- Phase 6 (User Story 4 - P4): 3 tasks
- Phase 7 (Polish): 2 tasks

**Parallelizable Tasks**: 3 tasks marked with [P]

**MVP Scope**: Phases 1-3 (T001-T008) = 8 tasks

**Independent Test Criteria**:
- US1: Can create and view tasks with validation
- US2: Can toggle task status (builds on US1)
- US3: Can update task details (builds on US1)
- US4: Can delete tasks (builds on US1)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All tasks reference spec requirements (FR-XXX) in plan.md
- All code generated via Claude Code prompts with task ID references
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No tests included (not requested in specification)
- Focus on clean, layered architecture with ≤25 line functions
- All functions require type hints and Google-style docstrings
