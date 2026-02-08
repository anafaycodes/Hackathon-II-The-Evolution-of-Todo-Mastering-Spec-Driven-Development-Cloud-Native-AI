# Data Model: Layer and Module Specifications

**Feature**: Clean Code Principles and Python Project Structure
**Branch**: `003-clean-code`
**Date**: 2026-01-30
**Status**: Complete

## Overview

This document defines the complete data model for the layered architecture, including detailed specifications for each layer, module, class, and function. It serves as the blueprint for module generation tasks.

---

## Layer Definitions

### Layer 1: CLI Layer

**Location**: `src/cli/`

**Responsibility**: Handle all user interaction, input parsing, output formatting, and menu display. Orchestrate calls to service layer based on user choices.

**Allowed Imports**:
- `from services.task_service import TaskService`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`
- Standard library: `sys`, `os` (if needed for exit/clear)

**Forbidden Imports**:
- `from storage.memory_store import ...` (VIOLATION: skip-level access)
- Any third-party libraries

**Public Interface**:
- Menu display functions
- User input collection functions
- Output formatting functions
- Command handler functions (add, view, update, delete, toggle)

**Quality Constraints**:
- No business logic (validation, data transformation)
- No direct storage access
- All console I/O happens here
- Functions ≤25 lines
- File ≤300 lines

**References**: FR-033, FR-037

---

### Layer 2: Service Layer

**Location**: `src/services/`

**Responsibility**: Implement business logic, validation rules, task lifecycle management, and orchestration between storage and domain layers.

**Allowed Imports**:
- `from storage.memory_store import InMemoryTaskStore`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`
- Standard library: `typing`, `re` (if needed for validation)

**Forbidden Imports**:
- `from cli.menu import ...` (VIOLATION: upward dependency)
- Any third-party libraries

**Public Interface**:
- Task CRUD operations (add, update, delete, list)
- Task status management (toggle complete/incomplete)
- Validation methods (exposed via operations)

**Quality Constraints**:
- No console I/O (print, input)
- No direct user interaction
- All business rules here
- Functions ≤25 lines
- File ≤300 lines

**References**: FR-034, FR-038

---

### Layer 3: Domain Layer

**Location**: `src/domain/`

**Responsibility**: Define pure data structures (entities) and simple structural validation. No dependencies on application layers.

**Allowed Imports**:
- `from utilities.constants import *` (if needed)
- Standard library: `dataclasses`, `enum`, `typing`

**Forbidden Imports**:
- `from cli.menu import ...` (VIOLATION)
- `from services.task_service import ...` (VIOLATION)
- `from storage.memory_store import ...` (VIOLATION)

**Public Interface**:
- Task entity (dataclass)
- TaskStatus enumeration
- Simple structural validation (via dataclass)

**Quality Constraints**:
- Pure data structures only
- No business logic
- No I/O operations
- No dependencies on other app layers
- One class per file (FR-028)
- Functions ≤25 lines
- Files ≤300 lines

**References**: FR-035, FR-039, FR-044

---

### Layer 4: Storage Layer

**Location**: `src/storage/`

**Responsibility**: Handle data persistence (in-memory), CRUD operations, ID generation, and data retrieval. No business rules.

**Allowed Imports**:
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *` (if needed)
- Standard library: `typing`

**Forbidden Imports**:
- `from cli.menu import ...` (VIOLATION)
- `from services.task_service import ...` (VIOLATION)

**Public Interface**:
- Create task (with ID generation)
- Read task (by ID, all tasks)
- Update task
- Delete task
- Toggle task status

**Quality Constraints**:
- No business logic (validation, transformation)
- No console I/O
- Only data operations
- Functions ≤25 lines
- File ≤300 lines

**References**: FR-036, FR-040

---

### Layer 5: Utilities Layer

**Location**: `src/utilities/`

**Responsibility**: Provide shared constants, error messages, and cross-cutting concerns accessible to all layers.

**Allowed Imports**:
- Standard library only (if needed)

**Forbidden Imports**:
- `from cli.menu import ...` (VIOLATION)
- `from services.task_service import ...` (VIOLATION)
- `from domain.task import ...` (VIOLATION)
- `from storage.memory_store import ...` (VIOLATION)

**Public Interface**:
- Constants (MAX_TITLE_LENGTH, MAX_DESC_LENGTH)
- Error messages (ERROR_EMPTY_TITLE, etc.)
- Shared helper functions (if needed)

**Quality Constraints**:
- No application layer dependencies
- No business logic
- Pure constants and utilities
- Functions ≤25 lines
- File ≤300 lines

**References**: FR-042, FR-046

---

## Module Definitions

### Module 1: src/utilities/constants.py

**Layer**: Utilities

**Responsibility**: Define shared constants and error messages used across all layers.

**Size Target**: ≤100 lines (simple constants file)

**Public Constants**:
```python
MAX_TITLE_LENGTH: int = 100
MAX_DESC_LENGTH: int = 500
ERROR_EMPTY_TITLE: str = "Title cannot be empty"
ERROR_EMPTY_DESC: str = "Description cannot be empty"
ERROR_TITLE_TOO_LONG: str = "Title cannot exceed 100 characters"
ERROR_DESC_TOO_LONG: str = "Description cannot exceed 500 characters"
ERROR_TASK_NOT_FOUND: str = "Task not found"
ERROR_INVALID_ID: str = "Invalid task ID"
```

**Allowed Imports**: None (or standard library if needed)

**Forbidden Imports**: All application layers

**Quality Checks**:
- [ ] All constants use UPPER_SNAKE_CASE
- [ ] No magic numbers in other modules (all here)
- [ ] Module docstring present
- [ ] File ≤100 lines

**References**: FR-046, FR-021

---

### Module 2: src/domain/task.py

**Layer**: Domain

**Responsibility**: Define Task entity and TaskStatus enumeration with simple structural validation.

**Size Target**: ≤150 lines

**Public Classes**:

```python
class TaskStatus(Enum):
    """Task completion status enumeration."""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

@dataclass
class Task:
    """Task entity representing a todo item.

    Attributes:
        id: Unique task identifier
        title: Task title (1-100 characters)
        description: Task description (1-500 characters)
        status: Task completion status
    """
    id: int
    title: str
    description: str
    status: TaskStatus
```

**Allowed Imports**:
- `from dataclasses import dataclass`
- `from enum import Enum`
- `from utilities.constants import *` (if needed)

**Forbidden Imports**: cli, services, storage

**Quality Checks**:
- [ ] TaskStatus enum has INCOMPLETE and COMPLETE values
- [ ] Task dataclass has all 4 fields with type hints
- [ ] Class docstrings present (Google style)
- [ ] No business logic (validation in service)
- [ ] File ≤150 lines
- [ ] One class per concept (Task and TaskStatus related)

**References**: FR-035, FR-044, FR-028

---

### Module 3: src/storage/memory_store.py

**Layer**: Storage

**Responsibility**: Provide in-memory CRUD operations for tasks with ID generation.

**Size Target**: ≤200 lines

**Public Class**:

```python
class InMemoryTaskStore:
    """In-memory storage for tasks with CRUD operations.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task store."""

    def create_task(self, title: str, description: str) -> Task:
        """Create and store a new task.

        Args:
            title: Task title
            description: Task description

        Returns:
            Created Task object with assigned ID
        """

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all Task objects
        """

    def update_task(self, task_id: int, title: str | None, description: str | None) -> Task | None:
        """Update existing task.

        Args:
            task_id: Unique task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated Task object if found, None otherwise
        """

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            True if deleted, False if not found
        """

    def toggle_task_status(self, task_id: int) -> Task | None:
        """Toggle task completion status.

        Args:
            task_id: Unique task identifier

        Returns:
            Updated Task object if found, None otherwise
        """

    def _generate_id(self) -> int:
        """Generate unique task ID.

        Returns:
            New unique task ID
        """
```

**Allowed Imports**:
- `from domain.task import Task, TaskStatus`
- `from typing import Optional` (for Python <3.10 compatibility)

**Forbidden Imports**: cli, services

**Quality Checks**:
- [ ] All public methods have type hints
- [ ] All public methods have Google-style docstrings
- [ ] Uses dict for O(1) lookup
- [ ] ID generation is private method
- [ ] No business logic (validation)
- [ ] Functions ≤25 lines
- [ ] File ≤200 lines

**References**: FR-036, FR-040

---

### Module 4: src/services/task_service.py

**Layer**: Service

**Responsibility**: Implement business logic, validation, and orchestration for task operations.

**Size Target**: ≤250 lines

**Public Class**:

```python
class TaskService:
    """Service layer for task business logic and validation.

    Attributes:
        _store: Storage layer instance for data persistence
    """

    def __init__(self, store: InMemoryTaskStore) -> None:
        """Initialize service with storage dependency.

        Args:
            store: Storage layer instance
        """

    def add_task(self, title: str, description: str) -> Task:
        """Add new task with validation.

        Args:
            title: Task title (1-100 characters)
            description: Task description (1-500 characters)

        Returns:
            Created Task object

        Raises:
            ValueError: If title or description invalid
        """

    def list_tasks(self) -> list[Task]:
        """List all tasks sorted by status then ID.

        Returns:
            List of Task objects (incomplete first, then complete)
        """

    def update_task(self, task_id: int, title: str | None, description: str | None) -> Task:
        """Update existing task with validation.

        Args:
            task_id: Unique task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found or validation fails
        """

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            True if deleted

        Raises:
            ValueError: If task not found
        """

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Unique task identifier

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found
        """

    def _validate_title(self, title: str) -> str:
        """Validate and normalize title.

        Args:
            title: Raw title input

        Returns:
            Normalized title

        Raises:
            ValueError: If title invalid
        """

    def _validate_description(self, description: str) -> str:
        """Validate and normalize description.

        Args:
            description: Raw description input

        Returns:
            Normalized description

        Raises:
            ValueError: If description invalid
        """

    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing extra whitespace.

        Args:
            text: Raw text input

        Returns:
            Normalized text
        """
```

**Allowed Imports**:
- `from storage.memory_store import InMemoryTaskStore`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`

**Forbidden Imports**: cli

**Quality Checks**:
- [ ] All public methods have type hints
- [ ] All public methods have Google-style docstrings
- [ ] Validation logic present (length, empty checks)
- [ ] No console I/O
- [ ] Private methods for validation
- [ ] Functions ≤25 lines
- [ ] File ≤250 lines

**References**: FR-034, FR-038, FR-045

---

### Module 5: src/cli/menu.py

**Layer**: CLI

**Responsibility**: Display menu, handle user input, format output, orchestrate service calls.

**Size Target**: ≤300 lines

**Public Functions**:

```python
def display_menu() -> None:
    """Display main menu options."""

def get_user_choice() -> int:
    """Get and validate user menu choice.

    Returns:
        Selected menu option number
    """

def handle_add_task(service: TaskService) -> None:
    """Handle add task flow.

    Args:
        service: TaskService instance
    """

def handle_view_tasks(service: TaskService) -> None:
    """Handle view tasks flow.

    Args:
        service: TaskService instance
    """

def handle_update_task(service: TaskService) -> None:
    """Handle update task flow.

    Args:
        service: TaskService instance
    """

def handle_delete_task(service: TaskService) -> None:
    """Handle delete task flow.

    Args:
        service: TaskService instance
    """

def handle_toggle_status(service: TaskService) -> None:
    """Handle toggle status flow.

    Args:
        service: TaskService instance
    """

def format_task_list(tasks: list[Task]) -> str:
    """Format task list for display.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted string for console output
    """

def display_message(message: str) -> None:
    """Display message to user.

    Args:
        message: Message text
    """

def get_task_input() -> tuple[str, str]:
    """Prompt for task title and description.

    Returns:
        Tuple of (title, description)
    """
```

**Allowed Imports**:
- `from services.task_service import TaskService`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`
- Standard library: `sys` (for exit)

**Forbidden Imports**: storage

**Quality Checks**:
- [ ] All functions have type hints
- [ ] All functions have Google-style docstrings
- [ ] No business logic (validation, transformation)
- [ ] All console I/O here
- [ ] Functions ≤25 lines
- [ ] File ≤300 lines

**References**: FR-033, FR-037

---

### Module 6: src/main.py

**Layer**: Entry Point (orchestration)

**Responsibility**: Initialize application, create dependencies, start main loop.

**Size Target**: ≤100 lines

**Public Functions**:

```python
def main() -> None:
    """Application entry point.

    Initializes storage, service, and CLI layers, then starts main loop.
    """

def run_main_loop(service: TaskService) -> None:
    """Run main application loop.

    Args:
        service: TaskService instance
    """

if __name__ == "__main__":
    main()
```

**Allowed Imports**:
- `from cli.menu import *`
- `from services.task_service import TaskService`
- `from storage.memory_store import InMemoryTaskStore`

**Forbidden Imports**: None (orchestration layer)

**Quality Checks**:
- [ ] All functions have type hints
- [ ] All functions have Google-style docstrings
- [ ] Dependency injection (store → service → CLI)
- [ ] Clean exit handling
- [ ] Functions ≤25 lines
- [ ] File ≤100 lines

**References**: FR-004

---

## Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                          main.py                                 │
│  - Orchestrates initialization                                   │
│  - Creates store → service → CLI                                 │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────────────┐
             │                                                      │
             ▼                                                      ▼
┌────────────────────────────┐                    ┌────────────────────────────┐
│       cli/menu.py          │                    │  services/task_service.py  │
│  - display_menu()          │───────────────────>│  - add_task()              │
│  - get_user_choice()       │                    │  - list_tasks()            │
│  - handle_add_task()       │                    │  - update_task()           │
│  - handle_view_tasks()     │                    │  - delete_task()           │
│  - handle_update_task()    │                    │  - toggle_task_status()    │
│  - handle_delete_task()    │                    │  - _validate_title()       │
│  - handle_toggle_status()  │                    │  - _validate_description() │
│  - format_task_list()      │                    │  - _normalize_text()       │
└────────────┬───────────────┘                    └────────────┬───────────────┘
             │                                                  │
             │                                                  │
             │                                                  ▼
             │                                    ┌────────────────────────────┐
             │                                    │ storage/memory_store.py    │
             │                                    │  - create_task()           │
             │                                    │  - get_task()              │
             │                                    │  - get_all_tasks()         │
             │                                    │  - update_task()           │
             │                                    │  - delete_task()           │
             │                                    │  - toggle_task_status()    │
             │                                    │  - _generate_id()          │
             │                                    └────────────┬───────────────┘
             │                                                  │
             └──────────────────────┬───────────────────────────┘
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │     domain/task.py          │
                      │  - TaskStatus (Enum)        │
                      │  - Task (dataclass)         │
                      └─────────────┬───────────────┘
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │  utilities/constants.py     │
                      │  - MAX_TITLE_LENGTH         │
                      │  - MAX_DESC_LENGTH          │
                      │  - ERROR_* messages         │
                      └─────────────────────────────┘
```

**Dependency Rules**:
- Arrows point from dependent to dependency
- No cycles (acyclic graph)
- Utilities accessible to all (horizontal dependency)
- Vertical dependencies flow downward only

---

## Module Responsibility Summary

| Module | Layer | Primary Responsibility | Key Functions/Classes |
|--------|-------|------------------------|----------------------|
| constants.py | Utilities | Shared constants | MAX_TITLE_LENGTH, ERROR_* |
| task.py | Domain | Entity definitions | Task, TaskStatus |
| memory_store.py | Storage | Data persistence | InMemoryTaskStore |
| task_service.py | Service | Business logic | TaskService |
| menu.py | CLI | User interaction | display_menu, handle_* |
| main.py | Entry Point | Orchestration | main, run_main_loop |

---

## Implementation Order (Dependency-Based)

1. **utilities/constants.py** (no dependencies)
2. **domain/task.py** (depends on utilities)
3. **storage/memory_store.py** (depends on domain, utilities)
4. **services/task_service.py** (depends on storage, domain, utilities)
5. **cli/menu.py** (depends on services, domain, utilities)
6. **main.py** (depends on cli, services, storage)

---

## Validation Checkpoints

After each module generation:
- [ ] Module in correct layer directory
- [ ] __init__.py exists in layer directory
- [ ] Imports follow allowed/forbidden rules
- [ ] All public functions have type hints
- [ ] All public functions have Google-style docstrings
- [ ] Functions ≤25 lines (or documented exception)
- [ ] File ≤300 lines
- [ ] No generic variable names (data, tmp, util)
- [ ] Naming conventions followed (snake_case functions, PascalCase classes)

---

## Next Steps

1. Generate contracts/ directory with interface specifications
2. Generate quickstart.md with validation checklists
3. Proceed to /sp.tasks for task breakdown

**Data Model Status**: ✅ COMPLETE
