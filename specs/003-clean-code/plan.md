# Implementation Plan: Clean Code Principles and Python Project Structure

**Branch**: `003-clean-code` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)

**Input**: Structural specification from `/specs/003-clean-code/spec.md` with clarifications

## Summary

Define and enforce clean code principles and layered architecture for the Todo In-Memory Python Console App. This plan establishes structural quality standards, layer boundaries, naming conventions, and validation rules—not application features. All code generated via Claude Code must comply with these architectural and quality constraints.

**Key Clarifications Applied**:
- Google style docstrings (readable, well-supported)
- Utilities layer for cross-cutting concerns (5th layer)
- Function length ≤25 lines with documented exceptions
- Simple validation in domain, complex rules in service
- Constants in utilities/, configuration at project root

## Layered Architecture Sketch

### 5-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Layer                               │
│  Responsibility: User interaction, I/O formatting            │
│  Can import: services/, domain/, utilities/                  │
│  Cannot import: storage/                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  Responsibility: Business logic, validation, orchestration   │
│  Can import: storage/, domain/, utilities/                   │
│  Cannot import: cli/                                         │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
             ▼                       ▼
┌────────────────────────┐  ┌──────────────────────────────────┐
│    Domain Layer        │  │     Storage Layer                │
│  Responsibility:       │  │  Responsibility:                 │
│  Entity definitions    │  │  Data persistence (CRUD)         │
│  Simple validation     │  │  Can import: domain/, utilities/ │
│  Can import:           │  │  Cannot import: cli/, services/  │
│  utilities/ only       │  └──────────────────────────────────┘
│  Cannot import:        │
│  cli/, services/,      │
│  storage/              │
└────────────────────────┘
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
             ┌────────────────────────┐
             │   Utilities Layer      │
             │  Responsibility:       │
             │  Constants, helpers    │
             │  Cross-cutting concerns│
             │  Can import: Nothing   │
             │  Cannot import: All    │
             └────────────────────────┘
```

### Dependency Rules Matrix

| Layer | Can Import | Cannot Import | Rationale |
|-------|------------|---------------|-----------|
| CLI | services, domain, utilities | storage | CLI orchestrates via service, never direct storage access |
| Service | storage, domain, utilities | cli | Service is business logic, no UI concerns |
| Domain | utilities | cli, services, storage | Domain is pure, no dependencies on application layers |
| Storage | domain, utilities | cli, services | Storage uses domain entities, no business logic |
| Utilities | (none) | cli, services, domain, storage | Utilities are foundational, no upward dependencies |

### Layer Isolation Principle

**Vertical Dependencies Only**: Layers can only depend on layers below them or utilities (horizontal).

**No Circular Dependencies**: If A imports B, B cannot import A (directly or transitively).

**No Skip-Level Access**: CLI cannot import storage directly; must go through service.

## Package Structure Blueprint

### Directory Layout

```
project-root/
├── src/
│   ├── __init__.py                  # Package marker
│   │
│   ├── cli/
│   │   ├── __init__.py              # Exports public CLI interface
│   │   └── menu.py                  # Menu display, user interaction
│   │
│   ├── services/
│   │   ├── __init__.py              # Exports public service interface
│   │   └── task_service.py          # Business logic, validation
│   │
│   ├── domain/
│   │   ├── __init__.py              # Exports domain entities
│   │   └── task.py                  # Task dataclass, TaskStatus enum
│   │
│   ├── storage/
│   │   ├── __init__.py              # Exports storage interface
│   │   └── memory_store.py          # In-memory CRUD operations
│   │
│   ├── utilities/
│   │   ├── __init__.py              # Exports constants, helpers
│   │   └── constants.py             # MAX_TITLE_LENGTH, error messages
│   │
│   └── main.py                      # Application entry point
│
├── specs/                           # Feature specifications
├── history/                         # PHRs, ADRs
├── .specify/                        # Spec-Kit Plus templates
├── constitution.md                  # Project principles
├── README.md                        # Setup instructions
├── CLAUDE.md                        # Agent instructions
└── pyproject.toml                   # Python project config (optional)
```

### Module Naming Conventions

**Files**: `snake_case.py` (e.g., `task_service.py`, `memory_store.py`)

**Classes**: `PascalCase` (e.g., `TaskService`, `InMemoryTaskStore`, `Task`)

**Functions**: `snake_case` with verb prefix (e.g., `add_task`, `validate_title`, `list_tasks`)

**Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TITLE_LENGTH`, `DEFAULT_STATUS`)

**Private**: Prefix with `_` (e.g., `_validate_title`, `_normalize_text`)

## Module Responsibility Map

### CLI Layer (`src/cli/`)

**menu.py**:
- **Responsibility**: Display menu, parse user input, format output
- **Public Functions**:
  - `display_menu() -> None`: Show numbered menu options
  - `get_user_choice() -> int`: Parse menu selection
  - `handle_add_task(service) -> None`: Add task flow
  - `handle_view_tasks(service) -> None`: View tasks flow
  - `handle_update_task(service) -> None`: Update task flow
  - `handle_delete_task(service) -> None`: Delete task flow
  - `handle_toggle_status(service) -> None`: Toggle status flow
  - `format_task_list(tasks) -> str`: Format tasks for display
- **Allowed Imports**: `from services.task_service import TaskService`, `from domain.task import Task, TaskStatus`, `from utilities.constants import *`
- **Prohibited**: No storage imports, no business logic, no validation

### Service Layer (`src/services/`)

**task_service.py**:
- **Responsibility**: Business logic, validation, orchestration
- **Public Functions**:
  - `add_task(title, desc) -> Task`: Validate, normalize, create
  - `list_tasks() -> list[Task]`: Get all, sort by status then ID
  - `update_task(id, title, desc) -> Task`: Validate, normalize, update
  - `delete_task(id) -> bool`: Validate ID, delete
  - `toggle_task_status(id) -> Task`: Validate ID, toggle
- **Private Functions**:
  - `_validate_title(title) -> str`: Check length, normalize
  - `_validate_description(desc) -> str`: Check length, normalize
  - `_normalize_text(text) -> str`: Convert newlines to spaces
- **Allowed Imports**: `from storage.memory_store import InMemoryTaskStore`, `from domain.task import Task, TaskStatus`, `from utilities.constants import *`
- **Prohibited**: No CLI imports, no console I/O

### Domain Layer (`src/domain/`)

**task.py**:
- **Responsibility**: Entity definitions, simple structural validation
- **Public Classes**:
  - `TaskStatus(Enum)`: INCOMPLETE, COMPLETE
  - `Task(dataclass)`: id, title, description, status
- **Validation**: Type checking via dataclass, no business rules
- **Allowed Imports**: `from utilities.constants import *` (if needed)
- **Prohibited**: No cli, services, storage imports

### Storage Layer (`src/storage/`)

**memory_store.py**:
- **Responsibility**: Data persistence, CRUD operations, ID generation
- **Public Functions**:
  - `create_task(title, desc) -> Task`: Generate ID, create, store
  - `get_task(id) -> Task | None`: Lookup by ID
  - `get_all_tasks() -> list[Task]`: Return all tasks
  - `update_task(id, title, desc) -> Task`: Update existing
  - `delete_task(id) -> bool`: Remove from storage
  - `toggle_status(id) -> Task`: Toggle task status
- **Private Functions**:
  - `_generate_id() -> int`: Increment counter, return new ID
- **Allowed Imports**: `from domain.task import Task, TaskStatus`, `from utilities.constants import *`
- **Prohibited**: No cli, services imports, no business logic

### Utilities Layer (`src/utilities/`)

**constants.py**:
- **Responsibility**: Shared constants, error messages
- **Public Constants**:
  - `MAX_TITLE_LENGTH = 100`
  - `MAX_DESC_LENGTH = 500`
  - `ERROR_EMPTY_TITLE = "Title cannot be empty"`
  - `ERROR_EMPTY_DESC = "Description cannot be empty"`
  - `ERROR_TITLE_TOO_LONG = "Title cannot exceed 100 characters"`
  - `ERROR_DESC_TOO_LONG = "Description cannot exceed 500 characters"`
  - `ERROR_TASK_NOT_FOUND = "Task not found"`
- **Allowed Imports**: None (standard library only if needed)
- **Prohibited**: No application layer imports

## Key Design Decisions

### Decision 1: Utilities Layer Placement

**Options Considered**:
- A) No utilities layer (constants in each layer)
- B) Utilities as 5th layer (accessible to all)
- C) Utilities in domain layer

**Selected**: B - Utilities as 5th layer

**Tradeoffs**:
- ✅ Single source of truth for constants
- ✅ Prevents duplication
- ✅ Clear separation of cross-cutting concerns
- ❌ Adds one more layer to understand

**Rationale**: Clarification specifies "Create separate utilities/ layer for shared helpers, logging, constants (accessible to all layers)." Provides designated place for cross-cutting concerns without violating layer boundaries.

### Decision 2: Docstring Format

**Options Considered**:
- A) reStructuredText (Sphinx default)
- B) Google style
- C) NumPy style
- D) Minimal (one-line only)

**Selected**: B - Google style

**Tradeoffs**:
- ✅ Highly readable
- ✅ Well-supported by tools
- ✅ Clean, structured format
- ❌ Slightly more verbose than minimal

**Rationale**: Clarification specifies "Google style docstrings." Provides good balance of readability and structure. Example:

```python
def add_task(title: str, description: str) -> Task:
    """Add a new task with validation.

    Args:
        title: Task title (1-100 characters)
        description: Task description (1-500 characters)

    Returns:
        Created Task object

    Raises:
        ValueError: If title or description invalid
    """
```

### Decision 3: Function Length Enforcement

**Options Considered**:
- A) Strict 25-line limit (no exceptions)
- B) 25-line guideline with documented exceptions
- C) No limit (trust developer judgment)

**Selected**: B - 25-line limit with documented exceptions

**Tradeoffs**:
- ✅ Encourages small functions
- ✅ Allows pragmatic exceptions
- ✅ Forces justification for violations
- ❌ Requires documentation overhead

**Rationale**: Clarification specifies "Allow exceptions with justification - functions can exceed 25 lines if documented with comment explaining why splitting is impractical." Provides flexibility for legitimate cases (complex error handling, initialization) while maintaining spirit of rule.

**Exception Documentation Format**:
```python
# FUNCTION LENGTH EXCEPTION: Complex error handling for multiple validation
# scenarios requires 35 lines. Splitting would reduce readability by
# separating tightly coupled validation logic.
def validate_and_normalize_task_data(title, desc):
    # ... 35 lines of validation logic
```

### Decision 4: Validation Placement

**Options Considered**:
- A) All validation in domain (self-validating entities)
- B) All validation in service (business rules)
- C) Split: simple in domain, complex in service

**Selected**: C - Split validation

**Tradeoffs**:
- ✅ Domain handles structural integrity
- ✅ Service handles business rules
- ✅ Clear separation of concerns
- ❌ Requires understanding of boundary

**Rationale**: Clarification specifies "Simple validation in domain (structural integrity), complex business rules in service layer." Domain validates types and structure (via dataclass), service validates length limits and content rules.

**Domain Validation** (structural):
- Type checking (via type hints)
- Required fields (via dataclass)

**Service Validation** (business rules):
- Length limits (≤100 chars title, ≤500 chars description)
- Content rules (non-empty, newline normalization)
- ID existence checks

### Decision 5: Constants Organization

**Options Considered**:
- A) Constants in each layer's module
- B) Constants in utilities/constants.py
- C) Constants in domain layer
- D) Configuration file (YAML/JSON)

**Selected**: B - Constants in utilities/constants.py

**Tradeoffs**:
- ✅ Single source of truth
- ✅ Easy to find and update
- ✅ No duplication
- ❌ All layers depend on utilities

**Rationale**: Clarification specifies "Constants in utilities/ layer (src/utilities/constants.py), configuration files at project root." Provides centralized location for magic numbers and error messages. Configuration files (if needed) stay at project root for deployment flexibility.

## Clean Code Enforcement Rules

### Rule 1: Function Length

**Limit**: ≤25 lines (excluding docstrings and blank lines)

**Validation**:
```python
def count_function_lines(function_text):
    lines = [l for l in function_text.split('\n')
             if l.strip() and not l.strip().startswith('#')
             and not in_docstring(l)]
    return len(lines)
```

**Exception**: Allowed if documented with comment explaining why splitting is impractical

**Enforcement**: Manual review during code gate

### Rule 2: Single Responsibility

**Principle**: Each function does one thing, describable with single verb + object

**Validation**: Manual review - can you describe function with one sentence using one verb?

**Examples**:
- ✅ `validate_title` - validates title
- ✅ `normalize_text` - normalizes text
- ❌ `validate_and_save_task` - does two things (validate AND save)

**Enforcement**: Code review checklist

### Rule 3: Type Hints

**Requirement**: All public functions must have type hints for parameters and return values

**Validation**:
```python
import ast
def check_type_hints(function_node):
    has_param_hints = all(arg.annotation for arg in function_node.args.args)
    has_return_hint = function_node.returns is not None
    return has_param_hints and has_return_hint
```

**Enforcement**: Automated check during code gate

### Rule 4: Docstrings

**Requirement**: All public functions and classes must have Google-style docstrings

**Format**:
```python
"""Brief description (one line).

Longer description if needed (optional).

Args:
    param1: Description
    param2: Description

Returns:
    Description of return value

Raises:
    ExceptionType: When this exception is raised
"""
```

**Validation**: Check for docstring presence, verify Google format

**Enforcement**: Automated check + manual review

### Rule 5: Naming Conventions

**Functions**: `snake_case` with verb prefix (e.g., `add_task`, `get_user_choice`)

**Classes**: `PascalCase` with noun (e.g., `TaskService`, `InMemoryTaskStore`)

**Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TITLE_LENGTH`)

**Variables**: `snake_case` with descriptive names (no `tmp`, `data`, `util`)

**Validation**: Regex patterns + prohibited name list

**Enforcement**: Automated check

### Rule 6: Nesting Depth

**Limit**: ≤3 levels of nesting

**Example**:
```python
# Level 1
if condition:
    # Level 2
    for item in items:
        # Level 3
        if item.valid:
            # Level 4 - VIOLATION
```

**Validation**: AST analysis counting nested blocks

**Enforcement**: Automated check

### Rule 7: File Length

**Limit**: ≤300 lines per file

**Validation**: Line count (excluding blank lines and comments)

**Enforcement**: Automated check

### Rule 8: No Generic Names

**Prohibited**: `data`, `tmp`, `temp`, `util`, `handle`, `process`, `do`, `manager`

**Validation**: Grep for prohibited names in variable declarations

**Enforcement**: Automated check

## Dependency Validation Model

### Import Analysis

**Allowed Import Patterns**:
```python
# CLI Layer
from services.task_service import TaskService  # ✅
from domain.task import Task, TaskStatus       # ✅
from utilities.constants import *              # ✅
from storage.memory_store import ...           # ❌ VIOLATION

# Service Layer
from storage.memory_store import InMemoryTaskStore  # ✅
from domain.task import Task                        # ✅
from utilities.constants import *                   # ✅
from cli.menu import ...                            # ❌ VIOLATION

# Domain Layer
from utilities.constants import *              # ✅
from services.task_service import ...          # ❌ VIOLATION
from storage.memory_store import ...           # ❌ VIOLATION
from cli.menu import ...                       # ❌ VIOLATION

# Storage Layer
from domain.task import Task                   # ✅
from utilities.constants import *              # ✅
from services.task_service import ...          # ❌ VIOLATION
from cli.menu import ...                       # ❌ VIOLATION

# Utilities Layer
from cli.menu import ...                       # ❌ VIOLATION
from services.task_service import ...          # ❌ VIOLATION
from domain.task import ...                    # ❌ VIOLATION
from storage.memory_store import ...           # ❌ VIOLATION
```

### Dependency Validation Script

```python
# Pseudo-code for dependency validation
LAYER_RULES = {
    'cli': {'allowed': ['services', 'domain', 'utilities'], 'prohibited': ['storage']},
    'services': {'allowed': ['storage', 'domain', 'utilities'], 'prohibited': ['cli']},
    'domain': {'allowed': ['utilities'], 'prohibited': ['cli', 'services', 'storage']},
    'storage': {'allowed': ['domain', 'utilities'], 'prohibited': ['cli', 'services']},
    'utilities': {'allowed': [], 'prohibited': ['cli', 'services', 'domain', 'storage']}
}

def validate_imports(file_path, imports):
    layer = detect_layer(file_path)  # Extract from path
    rules = LAYER_RULES[layer]

    for imp in imports:
        imported_layer = extract_layer(imp)
        if imported_layer in rules['prohibited']:
            return f"VIOLATION: {layer} cannot import {imported_layer}"
        if imported_layer not in rules['allowed'] and imported_layer != layer:
            return f"VIOLATION: {layer} cannot import {imported_layer}"

    return "PASS"
```

### Circular Dependency Detection

```python
def detect_circular_dependencies(module_graph):
    """Detect cycles in module dependency graph using DFS."""
    visited = set()
    rec_stack = set()

    def has_cycle(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in module_graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in module_graph:
        if node not in visited:
            if has_cycle(node):
                return True
    return False
```

## Structural Quality Checklist

### Layer Architecture Checklist

- [ ] **LA-01**: src/ directory exists
- [ ] **LA-02**: cli/ subdirectory exists with __init__.py
- [ ] **LA-03**: services/ subdirectory exists with __init__.py
- [ ] **LA-04**: domain/ subdirectory exists with __init__.py
- [ ] **LA-05**: storage/ subdirectory exists with __init__.py
- [ ] **LA-06**: utilities/ subdirectory exists with __init__.py
- [ ] **LA-07**: main.py exists at src/ root
- [ ] **LA-08**: No files outside designated layer directories

### Dependency Compliance Checklist

- [ ] **DC-01**: CLI layer imports only services, domain, utilities
- [ ] **DC-02**: Service layer imports only storage, domain, utilities
- [ ] **DC-03**: Domain layer imports only utilities
- [ ] **DC-04**: Storage layer imports only domain, utilities
- [ ] **DC-05**: Utilities layer imports no application layers
- [ ] **DC-06**: No circular dependencies detected
- [ ] **DC-07**: No skip-level imports (e.g., CLI → Storage)

### Function Quality Checklist

- [ ] **FQ-01**: All functions ≤25 lines (or documented exception)
- [ ] **FQ-02**: All public functions have type hints
- [ ] **FQ-03**: All public functions have Google-style docstrings
- [ ] **FQ-04**: All functions have single responsibility
- [ ] **FQ-05**: Function names use verbs (e.g., add_task, validate_title)
- [ ] **FQ-06**: No generic variable names (data, tmp, util)
- [ ] **FQ-07**: Nesting depth ≤3 levels
- [ ] **FQ-08**: No functions with multiple unrelated responsibilities

### Class Quality Checklist

- [ ] **CQ-01**: Class names use nouns (PascalCase)
- [ ] **CQ-02**: Classes have single responsibility
- [ ] **CQ-03**: Public classes have docstrings
- [ ] **CQ-04**: Domain files have ≤1 class per file
- [ ] **CQ-05**: Class methods follow function quality rules

### File Quality Checklist

- [ ] **FI-01**: All files ≤300 lines
- [ ] **FI-02**: File names use snake_case
- [ ] **FI-03**: All Python files have module-level docstring
- [ ] **FI-04**: No unused imports
- [ ] **FI-05**: Imports organized (stdlib, third-party, local)
- [ ] **FI-06**: No wildcard imports (except utilities.constants)

### Naming Compliance Checklist

- [ ] **NC-01**: Functions use snake_case with verb prefix
- [ ] **NC-02**: Classes use PascalCase with noun
- [ ] **NC-03**: Constants use UPPER_SNAKE_CASE
- [ ] **NC-04**: Variables use snake_case with descriptive names
- [ ] **NC-05**: No prohibited names (data, tmp, util, handle)
- [ ] **NC-06**: Private functions/methods prefixed with _

### Documentation Checklist

- [ ] **DOC-01**: All public functions have docstrings
- [ ] **DOC-02**: All public classes have docstrings
- [ ] **DOC-03**: Docstrings follow Google style format
- [ ] **DOC-04**: Docstrings include Args, Returns, Raises sections
- [ ] **DOC-05**: Function length exceptions documented with comment
- [ ] **DOC-06**: Module-level docstrings present

## Claude Code Module Task Model

### Task Template for Module Generation

```
Task: [Task ID]: Generate [module_name] in [layer]
Spec Requirements: [FR-XXX from 003-clean-code spec]
Acceptance Criteria:
- Module placed in correct layer directory
- Follows dependency rules for [layer]
- All functions ≤25 lines (or documented exception)
- All public functions have type hints and Google-style docstrings
- Function names use verbs, class names use nouns
- No generic variable names
- Nesting depth ≤3 levels

Generate src/[layer]/[module_name].py with:
- Module-level docstring
- Required imports (only from allowed layers)
- [Specific classes/functions needed]
- Type hints for all functions
- Google-style docstrings for all public functions
- Single responsibility per function
- Descriptive variable names

Output the complete file.
```

### Module Generation Phases

**Phase 1: Utilities Layer** (no dependencies)
- Generate constants.py first (foundation for all layers)

**Phase 2: Domain Layer** (depends on utilities)
- Generate task.py (TaskStatus enum, Task dataclass)

**Phase 3: Storage Layer** (depends on domain, utilities)
- Generate memory_store.py (InMemoryTaskStore class)

**Phase 4: Service Layer** (depends on storage, domain, utilities)
- Generate task_service.py (TaskService class)

**Phase 5: CLI Layer** (depends on services, domain, utilities)
- Generate menu.py (menu functions)

**Phase 6: Entry Point** (depends on cli)
- Generate main.py (application entry point)

### Validation After Each Module

After generating each module, validate:
1. **Layer Placement**: File in correct directory
2. **Imports**: Only allowed layers imported
3. **Function Length**: All functions ≤25 lines (or documented)
4. **Type Hints**: All public functions have hints
5. **Docstrings**: All public functions have Google-style docs
6. **Naming**: Functions use verbs, classes use nouns
7. **Single Responsibility**: Each function does one thing

## Next Steps

1. **Run `/sp.tasks`** to generate task breakdown for enforcing clean code principles
2. **Create validation scripts** for automated checks (import analysis, function length, etc.)
3. **Document clean code standards** in team guidelines
4. **Establish code review checklist** based on structural quality checklist
5. **Train team** on layer boundaries and dependency rules

## Notes

- This plan defines structural quality standards, not application features
- All code generated must comply with these architectural constraints
- Validation is hybrid: automated checks + manual review
- Layer boundaries are enforced through import analysis
- Clean code principles are enforced through checklists and validation scripts
- Google-style docstrings provide readable, structured documentation
- Function length limit encourages small, focused functions with pragmatic exceptions
