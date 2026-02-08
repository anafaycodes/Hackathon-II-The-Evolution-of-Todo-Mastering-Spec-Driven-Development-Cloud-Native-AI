# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-app` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-todo-app/spec.md` with clarifications

## Summary

Build a menu-driven console todo application with in-memory storage following clean code principles and spec-driven development. The app supports five core operations (Add, View, Update, Delete, Mark Complete/Incomplete) with strict validation and layered architecture.

**Key Clarifications Applied**:
- Menu-driven interface with numbered options
- Text limits: 100 chars (title), 500 chars (description)
- Unicode support with newline-to-space conversion
- Never reuse task IDs (monotonic increment)
- Display order: incomplete first, then complete, sorted by ID

## Architecture Sketch

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer                            │
│  (menu.py - User interaction, input/output formatting)  │
└────────────────────┬────────────────────────────────────┘
                     │ calls
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Service Layer                           │
│  (task_service.py - Business logic, validation)         │
└────────────┬───────────────────────┬────────────────────┘
             │ uses                  │ calls
             ▼                       ▼
┌────────────────────────┐  ┌──────────────────────────────┐
│    Domain Layer        │  │     Storage Layer            │
│  (task.py - Entity)    │  │  (memory_store.py - CRUD)    │
└────────────────────────┘  └──────────────────────────────┘
             │                       │
             └───────────┬───────────┘
                         │ both use
                         ▼
             ┌────────────────────────┐
             │   Utilities Layer      │
             │  (constants.py)        │
             └────────────────────────┘
```

### Layer Responsibilities

**CLI Layer** (`src/cli/menu.py`):
- Display main menu with numbered options (1-6)
- Parse user menu selections
- Prompt for task details (title, description, ID)
- Format task output for console display
- Handle invalid menu input gracefully
- **Allowed dependencies**: services, domain, utilities
- **Disallowed**: storage (must go through service)

**Service Layer** (`src/services/task_service.py`):
- Validate task title (non-empty, ≤100 chars)
- Validate task description (non-empty, ≤500 chars)
- Normalize text (convert newlines to spaces)
- Coordinate between storage and domain
- Implement business rules
- **Allowed dependencies**: storage, domain, utilities
- **Disallowed**: cli

**Domain Layer** (`src/domain/task.py`):
- Define Task dataclass with id, title, description, status
- Define TaskStatus enum (INCOMPLETE, COMPLETE)
- Simple structural validation (type checking)
- **Allowed dependencies**: utilities only
- **Disallowed**: cli, services, storage

**Storage Layer** (`src/storage/memory_store.py`):
- Maintain in-memory dictionary {id: Task}
- Generate unique sequential IDs (never reuse)
- Provide CRUD operations
- Return sorted task lists (by status then ID)
- **Allowed dependencies**: domain, utilities
- **Disallowed**: cli, services

**Utilities Layer** (`src/utilities/constants.py`):
- Define constants (MAX_TITLE_LENGTH=100, MAX_DESC_LENGTH=500)
- Define error messages
- **Allowed dependencies**: None
- **Disallowed**: All application layers

### Data Flow Example (Add Task)

```
User Input → CLI.display_menu()
          → CLI.handle_add_task()
          → CLI prompts for title/description
          → Service.add_task(title, desc)
          → Service validates & normalizes
          → Storage.create_task(title, desc)
          → Storage generates ID, creates Task
          → Storage stores in dict
          → Returns Task
          → Service returns Task
          → CLI formats & displays confirmation
```

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory dictionary
**Testing**: Manual validation against acceptance scenarios
**Target Platform**: Console (Windows/Linux/macOS)
**Project Type**: Single application
**Performance Goals**: <1 second per operation, support 100+ tasks
**Constraints**: Memory-only, no persistence, single-user
**Scale/Scope**: Simple CRUD app, ~5 modules, ~500 LOC total

## Constitution Check

✅ **Spec Authority**: All requirements traced to spec.md
✅ **Agentic Development**: All code via Claude Code prompts
✅ **Traceability**: Each module maps to spec requirements
✅ **Clean Code**: Layered architecture, ≤25 line functions, type hints
✅ **Architecture Discipline**: 5 layers with clear boundaries
✅ **Scope Control**: Only 5 core features, no extras

## Project Structure

### Documentation (this feature)

```
specs/001-todo-app/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── checklists/
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Task breakdown (to be created by /sp.tasks)
```

### Source Code (repository root)

```
src/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── menu.py          # Menu display, user interaction
├── domain/
│   ├── __init__.py
│   └── task.py          # Task dataclass, TaskStatus enum
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic, validation
├── storage/
│   ├── __init__.py
│   └── memory_store.py  # In-memory CRUD operations
├── utilities/
│   ├── __init__.py
│   └── constants.py     # Shared constants, error messages
└── main.py              # Application entry point

tests/                   # (Optional - not in MVP scope)
├── unit/
├── integration/
└── contract/
```

**Structure Decision**: Single project layout with src/ directory. Five layers (CLI, Service, Domain, Storage, Utilities) provide clear separation of concerns. Main entry point at src/main.py initializes and runs the menu loop.

## Key Design Decisions

### Decision 1: Task ID Generation Strategy

**Options Considered**:
- A) UUID strings (universally unique)
- B) Sequential integers starting at 1 (simple counter)
- C) Timestamp-based IDs

**Selected**: B - Sequential integers starting at 1

**Tradeoffs**:
- ✅ Simple, predictable, user-friendly
- ✅ Easy to type and remember
- ✅ Meets requirement FR-022 (never reuse IDs)
- ❌ Not globally unique (only session-unique)
- ❌ Predictable sequence

**Rationale**: Spec requires simple integers (Assumptions section). User-friendly for console input. No need for global uniqueness in single-session, single-user app. Counter increments on each create, never decrements on delete.

### Decision 2: In-Memory Data Structure

**Options Considered**:
- A) List of Task objects (simple, ordered)
- B) Dictionary {id: Task} (fast lookup)
- C) Two lists (incomplete, complete) for fast display

**Selected**: B - Dictionary {id: Task}

**Tradeoffs**:
- ✅ O(1) lookup by ID for update/delete/mark operations
- ✅ Easy to check ID existence
- ✅ Natural fit for unique ID requirement
- ❌ Requires sorting for display (acceptable overhead)
- ❌ Slightly more memory than list

**Rationale**: Most operations (update, delete, mark complete) require ID lookup. Dictionary provides O(1) access. Display sorting is infrequent and acceptable for 100+ tasks. Clean separation: storage handles dict, service handles sorting logic.

### Decision 3: Status Representation

**Options Considered**:
- A) Boolean (is_complete: True/False)
- B) Enum (TaskStatus.INCOMPLETE, TaskStatus.COMPLETE)
- C) String ("incomplete", "complete")

**Selected**: B - Enum (TaskStatus)

**Tradeoffs**:
- ✅ Type-safe, prevents invalid values
- ✅ Self-documenting code
- ✅ Easy to extend if needed
- ✅ Clear in comparisons and sorting
- ❌ Slightly more verbose than boolean

**Rationale**: Spec allows "Boolean or enumeration" (Key Entities). Enum provides better clarity and type safety. Aligns with clean code principle of explicit naming. Makes sorting logic clearer (INCOMPLETE < COMPLETE).

### Decision 4: Validation Location

**Options Considered**:
- A) CLI layer validates before calling service
- B) Service layer validates (business rules)
- C) Domain layer validates (self-validating entities)
- D) Split: CLI validates format, Service validates business rules

**Selected**: B - Service layer validates

**Tradeoffs**:
- ✅ Centralized validation logic
- ✅ Reusable if CLI changes
- ✅ Clear separation: CLI handles I/O, Service handles rules
- ✅ Aligns with clean code spec (complex rules in service)
- ❌ CLI must handle validation errors from service

**Rationale**: Clean code spec clarifies: "Simple validation in domain (structural integrity), complex business rules in service layer." Title/description length and content rules are business rules. Service layer is the right place. Domain only does structural validation (type checking via dataclass).

### Decision 5: Error Signaling Method

**Options Considered**:
- A) Exceptions for all errors
- B) Return tuples (success: bool, result/error)
- C) Result objects (Success/Failure types)
- D) Exceptions for validation, None for not-found

**Selected**: A - Exceptions for all errors

**Tradeoffs**:
- ✅ Pythonic, standard library pattern
- ✅ Clear error propagation
- ✅ Forces error handling
- ✅ Clean separation of happy path and error path
- ❌ Requires try/except blocks in CLI

**Rationale**: Python convention. Spec requires "clear error messages for all validation failures" (FR-013). Exceptions provide clear error types (ValueError for validation, KeyError for not-found). CLI layer catches and displays user-friendly messages.

### Decision 6: Text Normalization Strategy

**Options Considered**:
- A) Normalize in CLI before sending to service
- B) Normalize in service before storage
- C) Normalize in domain entity constructor
- D) Store raw, normalize only for display

**Selected**: B - Normalize in service before storage

**Tradeoffs**:
- ✅ Consistent data in storage
- ✅ Single normalization point
- ✅ Service owns business rules
- ❌ Cannot retrieve original text with newlines

**Rationale**: Spec requires "convert newline characters to spaces" (FR-021). This is a business rule (data transformation), belongs in service layer. Normalization happens once at creation/update, stored normalized. Simpler than normalizing at display time.

### Decision 7: Display Ordering Implementation

**Options Considered**:
- A) Storage returns pre-sorted list
- B) Service sorts after retrieving from storage
- C) Maintain two separate storage structures (incomplete, complete)

**Selected**: B - Service sorts after retrieving from storage

**Tradeoffs**:
- ✅ Storage stays simple (just CRUD)
- ✅ Sorting logic in service (business rule)
- ✅ Flexible if sorting rules change
- ❌ Sorts on every view operation

**Rationale**: Sorting by status then ID is a business rule (FR-023), belongs in service layer. Storage provides unsorted dict, service converts to sorted list for display. Clean separation of concerns. Performance acceptable for 100+ tasks.

## Domain Model Design

### Task Entity

```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    """Task completion status."""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique task identifier (never reused)
        title: Short description (1-100 chars)
        description: Detailed explanation (1-500 chars)
        status: Completion status (INCOMPLETE or COMPLETE)
    """
    id: int
    title: str
    description: str
    status: TaskStatus
```

**Design Notes**:
- Immutable after creation (dataclass with frozen=False for status updates)
- Simple structural validation via type hints
- No business logic in domain (pure data)
- Status enum provides type safety

### Entity Relationships

```
Task (standalone entity)
  - No relationships
  - Self-contained
  - No foreign keys or references
```

**Rationale**: Simple domain with single entity. No relationships needed for MVP scope.

## Storage Strategy (In-Memory Only)

### InMemoryTaskStore

**Data Structure**:
```python
{
    1: Task(id=1, title="...", description="...", status=TaskStatus.INCOMPLETE),
    2: Task(id=2, title="...", description="...", status=TaskStatus.COMPLETE),
    3: Task(id=3, title="...", description="...", status=TaskStatus.INCOMPLETE),
}
```

**ID Generation**:
- Counter starts at 1
- Increments on each create
- Never decrements (even after delete)
- Thread-safe not required (single-user)

**Operations**:
- `create_task(title, desc) -> Task`: Generate ID, create Task, store, return
- `get_task(id) -> Task | None`: Lookup by ID, return or None
- `get_all_tasks() -> list[Task]`: Return all tasks as list
- `update_task(id, title, desc) -> Task`: Update existing, return updated
- `delete_task(id) -> bool`: Remove from dict, return success
- `toggle_status(id) -> Task`: Toggle status, return updated

**Persistence**: None. Data lost on exit (FR-016).

## Service Layer Operations Mapping

### TaskService

Maps spec requirements to service methods:

| Spec Requirement | Service Method | Description |
|------------------|----------------|-------------|
| FR-001, FR-010, FR-011, FR-018, FR-019, FR-020, FR-021 | `add_task(title, desc) -> Task` | Validate, normalize, create task |
| FR-004, FR-023 | `list_tasks() -> list[Task]` | Get all, sort by status then ID |
| FR-007, FR-008, FR-010, FR-018, FR-019, FR-020, FR-021 | `update_task(id, title, desc) -> Task` | Validate, normalize, update |
| FR-009, FR-012 | `delete_task(id) -> bool` | Validate ID exists, delete |
| FR-006, FR-012 | `toggle_task_status(id) -> Task` | Validate ID exists, toggle |

**Validation Rules** (implemented in service):
- Title: non-empty, ≤100 chars, normalize newlines
- Description: non-empty, ≤500 chars, normalize newlines
- ID: must exist in storage for update/delete/toggle

**Error Handling**:
- Raise `ValueError` for validation failures (empty, too long)
- Raise `KeyError` for invalid task IDs
- Clear error messages per FR-013

## CLI Command Flow Design

### Menu Structure

```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

### Command Flows

**1. Add Task**:
```
User selects 1
→ CLI prompts: "Enter title: "
→ User enters title
→ CLI prompts: "Enter description: "
→ User enters description
→ CLI calls service.add_task(title, desc)
→ Service validates & creates
→ CLI displays: "Task #X created successfully"
→ Return to menu
```

**2. View Tasks**:
```
User selects 2
→ CLI calls service.list_tasks()
→ Service returns sorted list
→ CLI formats and displays:
  === Tasks ===
  [Incomplete]
  #1: Title | Description | Status: Incomplete
  #3: Title | Description | Status: Incomplete
  [Complete]
  #2: Title | Description | Status: Complete
→ Return to menu
```

**3. Update Task**:
```
User selects 3
→ CLI prompts: "Enter task ID: "
→ User enters ID
→ CLI prompts: "Enter new title (or press Enter to keep): "
→ User enters title or skips
→ CLI prompts: "Enter new description (or press Enter to keep): "
→ User enters description or skips
→ CLI calls service.update_task(id, title, desc)
→ Service validates & updates
→ CLI displays: "Task #X updated successfully"
→ Return to menu
```

**4. Delete Task**:
```
User selects 4
→ CLI prompts: "Enter task ID: "
→ User enters ID
→ CLI calls service.delete_task(id)
→ Service deletes
→ CLI displays: "Task #X deleted successfully"
→ Return to menu
```

**5. Mark Complete/Incomplete**:
```
User selects 5
→ CLI prompts: "Enter task ID: "
→ User enters ID
→ CLI calls service.toggle_task_status(id)
→ Service toggles status
→ CLI displays: "Task #X marked as [Complete/Incomplete]"
→ Return to menu
```

**6. Exit**:
```
User selects 6
→ CLI displays: "Goodbye!"
→ Exit program
```

### Error Handling in CLI

```python
try:
    service.add_task(title, desc)
except ValueError as e:
    print(f"Error: {e}")
except KeyError as e:
    print(f"Error: Task not found")
```

## Error Handling Strategy

### Error Types

| Error Condition | Exception Type | Error Message | Handling Layer |
|-----------------|----------------|---------------|----------------|
| Empty title | ValueError | "Title cannot be empty" | Service → CLI |
| Title too long | ValueError | "Title cannot exceed 100 characters" | Service → CLI |
| Empty description | ValueError | "Description cannot be empty" | Service → CLI |
| Description too long | ValueError | "Description cannot exceed 500 characters" | Service → CLI |
| Invalid task ID | KeyError | "Task not found" | Service → CLI |
| Invalid menu choice | ValueError | "Invalid choice. Please enter 1-6" | CLI only |
| Non-numeric input | ValueError | "Please enter a valid number" | CLI only |

### Error Propagation

```
Service Layer: Raises exceptions with clear messages
       ↓
CLI Layer: Catches exceptions, displays user-friendly messages
       ↓
User: Sees error, returns to menu (no crash)
```

**Rationale**: Spec requires "handle invalid inputs without crashing" (FR-014) and "clear error messages" (FR-013). Exception-based approach provides clean separation and forced error handling.

## Validation Rules

### Title Validation (Service Layer)

```python
def _validate_title(title: str) -> str:
    """Validate and normalize title.

    Args:
        title: Raw title input

    Returns:
        Normalized title

    Raises:
        ValueError: If title is empty or exceeds 100 characters
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    normalized = title.replace('\n', ' ').replace('\r', ' ')

    if len(normalized) > 100:
        raise ValueError("Title cannot exceed 100 characters")

    return normalized
```

### Description Validation (Service Layer)

```python
def _validate_description(description: str) -> str:
    """Validate and normalize description.

    Args:
        description: Raw description input

    Returns:
        Normalized description

    Raises:
        ValueError: If description is empty or exceeds 500 characters
    """
    if not description or not description.strip():
        raise ValueError("Description cannot be empty")

    normalized = description.replace('\n', ' ').replace('\r', ' ')

    if len(normalized) > 500:
        raise ValueError("Description cannot exceed 500 characters")

    return normalized
```

### ID Validation (Service Layer)

```python
def _validate_task_exists(task_id: int) -> None:
    """Validate that task ID exists.

    Args:
        task_id: Task ID to validate

    Raises:
        KeyError: If task ID does not exist
    """
    if not self.storage.get_task(task_id):
        raise KeyError(f"Task #{task_id} not found")
```

## Task Decomposition for Claude Code

### Task Groups

**Phase 1: Foundation** (Setup)
- T001: Create project structure (directories, __init__.py files)
- T002: Define constants (src/utilities/constants.py)

**Phase 2: Domain** (Core entities)
- T003: Define TaskStatus enum (src/domain/task.py)
- T004: Define Task dataclass (src/domain/task.py)

**Phase 3: Storage** (Data layer)
- T005: Implement InMemoryTaskStore class (src/storage/memory_store.py)
- T006: Implement ID generation logic
- T007: Implement CRUD operations

**Phase 4: Service** (Business logic)
- T008: Implement TaskService class (src/services/task_service.py)
- T009: Implement validation methods
- T010: Implement add_task method
- T011: Implement list_tasks with sorting
- T012: Implement update_task method
- T013: Implement delete_task method
- T014: Implement toggle_task_status method

**Phase 5: CLI** (User interface)
- T015: Implement menu display (src/cli/menu.py)
- T016: Implement menu selection handling
- T017: Implement add task flow
- T018: Implement view tasks flow
- T019: Implement update task flow
- T020: Implement delete task flow
- T021: Implement toggle status flow
- T022: Implement error handling and display

**Phase 6: Integration** (Entry point)
- T023: Implement main.py entry point
- T024: Implement main loop
- T025: Manual testing against acceptance scenarios

### Task Characteristics

Each task:
- ✅ Targets one module/file
- ✅ References spec requirements (FR-XXX)
- ✅ Has clear acceptance criteria
- ✅ Produces full file output
- ✅ Is independently regenerable
- ✅ Includes type hints and Google-style docstrings
- ✅ Follows ≤25 line function limit (with exceptions documented)

## Iteration & Regeneration Rules

### When to Regenerate

1. **Validation Error**: If generated code fails validation (missing type hints, wrong structure)
   - Refine prompt with specific requirements
   - Regenerate entire file

2. **Spec Mismatch**: If code doesn't match spec requirements
   - Update spec if spec was wrong
   - Refine prompt if code was wrong
   - Regenerate entire file

3. **Clean Code Violation**: If code violates clean code principles
   - Refine prompt with clean code requirements
   - Regenerate entire file

### Never Patch

- ❌ Do not manually edit generated code
- ❌ Do not use sed/awk to modify files
- ✅ Always regenerate full files via new prompts
- ✅ Keep prompt history in PHRs

### Prompt Requirements

Every Claude Code prompt must:
- Reference task ID (e.g., "T008: Implement TaskService class")
- Reference spec requirements (e.g., "Implements FR-001, FR-010, FR-011")
- Include acceptance criteria
- Specify file path
- Request full file output with type hints and docstrings

## Quality Validation Plan

### Functional Validation

Test against acceptance scenarios from spec:

**User Story 1** (Create and View):
- [ ] Add task with title and description → task created with ID
- [ ] View tasks → see all tasks with correct details
- [ ] View empty list → see "No tasks found"
- [ ] Add task with empty title → see error message
- [ ] Add task with empty description → see error message

**User Story 2** (Mark Complete):
- [ ] Mark incomplete task complete → status changes
- [ ] Mark complete task incomplete → status changes
- [ ] Mark with invalid ID → see error message
- [ ] View mixed statuses → clearly distinguish complete/incomplete

**User Story 3** (Update):
- [ ] Update title only → title changes, description/status unchanged
- [ ] Update description only → description changes, title/status unchanged
- [ ] Update both → both change, status unchanged
- [ ] Update with invalid ID → see error message
- [ ] Update with empty title → see error message

**User Story 4** (Delete):
- [ ] Delete task → task removed from list
- [ ] Delete with invalid ID → see error message
- [ ] Delete same task twice → see error message

### Structural Validation

**Layer Boundaries**:
- [ ] CLI only imports services, domain, utilities
- [ ] Service only imports storage, domain, utilities
- [ ] Domain only imports utilities
- [ ] Storage only imports domain, utilities
- [ ] Utilities imports nothing
- [ ] No circular imports

**Clean Code Compliance**:
- [ ] All functions ≤25 lines (or documented exception)
- [ ] All public functions have type hints
- [ ] All public functions have Google-style docstrings
- [ ] All functions have single responsibility
- [ ] Nesting depth ≤3 levels
- [ ] No generic variable names (data, tmp, util)
- [ ] Function names use verbs, class names use nouns
- [ ] Files ≤300 lines

**Project Structure**:
- [ ] src/ directory exists
- [ ] cli/, services/, domain/, storage/, utilities/ subdirectories exist
- [ ] All directories have __init__.py
- [ ] main.py at src/ root

### Process Validation

**Spec-Driven Compliance**:
- [ ] All code generated via Claude Code prompts
- [ ] All prompts reference task IDs and spec requirements
- [ ] No manual code edits in git history
- [ ] PHRs exist for all implementation prompts
- [ ] All requirements (FR-001 through FR-023) implemented

### Performance Validation

- [ ] Add task completes in <1 second
- [ ] View tasks with 100 tasks completes in <1 second
- [ ] Update task completes in <1 second
- [ ] Delete task completes in <1 second
- [ ] Mark complete completes in <1 second

## Success Criteria Mapping

| Success Criterion | Validation Method |
|-------------------|-------------------|
| SC-001: Create task in 3 interactions | Manual test: count interactions |
| SC-002: Distinguish complete/incomplete | Manual test: view mixed tasks |
| SC-003: Full lifecycle without crashes | Manual test: all operations |
| SC-004: 100% clear error messages | Manual test: all error scenarios |
| SC-005: Unique IDs throughout session | Manual test: create, delete, create |
| SC-006: 100+ tasks without degradation | Manual test: create 100 tasks, measure time |
| SC-007: <1 second per operation | Manual test: time each operation |
| SC-008: Readable console output | Manual test: review formatting |

## Next Steps

1. **Run `/sp.tasks`** to generate atomic task breakdown from this plan
2. **Execute tasks sequentially** via Claude Code prompts
3. **Validate after each phase** using quality validation checklist
4. **Create PHRs** for all implementation prompts
5. **Manual testing** against acceptance scenarios
6. **Document any deviations** in ADRs if needed

## Notes

- This plan assumes Python 3.13+ with standard library only
- No external dependencies required (no pyproject.toml setup needed initially)
- UV package manager mentioned in spec but not required for MVP
- Testing framework not in scope (manual validation sufficient)
- Focus on clean, simple implementation following spec exactly
