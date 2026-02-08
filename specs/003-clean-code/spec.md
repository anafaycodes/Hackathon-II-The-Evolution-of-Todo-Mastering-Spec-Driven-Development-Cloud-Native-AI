# Feature Specification: Clean Code Principles and Python Project Structure

**Feature Branch**: `003-clean-code`
**Created**: 2026-01-30
**Status**: Draft
**Input**: User description: "Clean Code Principles and Python Project Structure for Todo In-Memory Console App - enforcing maintainable architecture, readable code, and proper Python packaging discipline"

## Clarifications

### Session 2026-01-30

- Q: Docstring format standard (reStructuredText, Google, NumPy, or minimal) → A: Google style docstrings
- Q: Utility functions and cross-cutting concerns placement → A: Create separate utilities/ layer for shared helpers, logging, constants (accessible to all layers)
- Q: Function length limit exceptions (strict, allow with justification, exclude certain lines, or soft guideline) → A: Allow exceptions with justification - functions can exceed 25 lines if documented with comment explaining why splitting is impractical
- Q: Domain model validation logic placement → A: Simple validation in domain (structural integrity), complex business rules in service layer
- Q: Constants and configuration organization → A: Constants in utilities/ layer (src/utilities/constants.py), configuration files at project root

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Modular Layered Architecture (Priority: P1) 🎯 MVP

As a development team, we want the codebase organized into clear layers (CLI, Service, Domain, Storage) with single responsibilities, so that code is maintainable and changes are isolated to appropriate modules.

**Why this priority**: Without proper layering, the codebase becomes a tangled mess where business logic, UI, and storage are mixed. This is the foundation for all other clean code practices.

**Independent Test**: Can be fully tested by verifying that src/ directory contains separate subdirectories for cli/, services/, domain/, and storage/, and that no module violates layer boundaries (e.g., domain importing cli).

**Acceptance Scenarios**:

1. **Given** the project structure is created, **When** examining the src/ directory, **Then** separate subdirectories exist for cli/, services/, domain/, and storage/
2. **Given** a CLI module exists, **When** reviewing its imports, **Then** it only imports from services/ and domain/, never from storage/
3. **Given** a service module exists, **When** reviewing its code, **Then** it contains business logic but no console I/O operations
4. **Given** a domain module exists, **When** reviewing its dependencies, **Then** it has no imports from cli/, services/, or storage/
5. **Given** a storage module exists, **When** reviewing its code, **Then** it only handles data persistence without business rules

---

### User Story 2 - Single Responsibility and Small Functions (Priority: P2)

As a development team, we want each module, class, and function to have exactly one responsibility and stay small (≤25 lines for functions), so that code is easy to understand, test, and modify.

**Why this priority**: After establishing layers, ensuring each unit does one thing well prevents complexity from creeping back in. Small, focused functions are easier to reason about and test.

**Independent Test**: Can be tested by reviewing all functions and verifying none exceed 25 lines, none have multiple responsibilities, and all have descriptive names that reveal intent.

**Acceptance Scenarios**:

1. **Given** a function is written, **When** counting its lines, **Then** it contains 25 or fewer lines of code
2. **Given** a function exists, **When** describing what it does, **Then** the description uses a single verb and object (e.g., "validates task title")
3. **Given** a module is created, **When** reviewing its contents, **Then** all functions and classes serve a single, cohesive purpose
4. **Given** business logic is needed, **When** implemented, **Then** it is separated from I/O operations in different functions
5. **Given** a function has nested logic, **When** reviewing its structure, **Then** nesting depth does not exceed 3 levels

---

### User Story 3 - Explicit Naming and Type Hints (Priority: P3)

As a development team, we want all functions, classes, and variables to have descriptive, intention-revealing names with complete type hints, so that code is self-documenting and type-safe.

**Why this priority**: After structure and responsibilities are clear, explicit naming and types make the code readable without extensive comments. This reduces cognitive load and catches errors early.

**Independent Test**: Can be tested by verifying that all public functions have type hints for parameters and return values, all names are descriptive (no abbreviations like "tmp" or "util"), and function names use verbs while class names use nouns.

**Acceptance Scenarios**:

1. **Given** a function is defined, **When** reviewing its signature, **Then** all parameters have type hints and the return type is specified
2. **Given** a class is created, **When** reviewing its name, **Then** it uses a noun that describes the entity (e.g., Task, TaskService, InMemoryTaskStore)
3. **Given** a function is created, **When** reviewing its name, **Then** it uses a verb that describes the action (e.g., add_task, validate_title, list_tasks)
4. **Given** a variable is declared, **When** reviewing its name, **Then** it clearly indicates what it contains without abbreviations
5. **Given** code is written, **When** reviewing for generic names, **Then** no variables named "data", "tmp", "util", "handle", or similar exist

---

### User Story 4 - Documentation and Dependency Management (Priority: P4)

As a development team, we want all public functions and classes to have docstrings, and all dependencies to follow proper direction rules (CLI → Services → Domain), so that the codebase is well-documented and maintainable.

**Why this priority**: Documentation and dependency management are important for long-term maintenance but can be added after the core structure, responsibilities, and naming are in place.

**Independent Test**: Can be tested by verifying that all public functions have docstrings, no circular imports exist, and dependency direction follows the rule: CLI → Services → Domain, Services → Storage → Domain.

**Acceptance Scenarios**:

1. **Given** a public function is defined, **When** reviewing its code, **Then** it has a docstring explaining purpose, parameters, and return value
2. **Given** a module imports another module, **When** checking dependency direction, **Then** it follows allowed patterns (CLI → Services, Services → Storage, etc.)
3. **Given** the domain layer exists, **When** reviewing its imports, **Then** it has no dependencies on CLI, Services, or Storage layers
4. **Given** a circular import is attempted, **When** the code is analyzed, **Then** it is detected and rejected
5. **Given** all modules are complete, **When** generating a dependency graph, **Then** all arrows point in the allowed direction without cycles

---

### Edge Cases

- What happens when refactoring reveals that a module has grown too large?
- How are exceptions to the 25-line function limit documented and reviewed?
- What happens when a utility function is only used by one layer - should it still be in utilities/?
- How is the boundary between simple domain validation and complex service validation determined in practice?

## Requirements *(mandatory)*

### Functional Requirements

#### Architecture and Structure
- **FR-001**: System MUST organize code into four distinct layers: CLI, Service, Domain, and Storage
- **FR-042**: System MUST provide a utilities/ layer for shared helpers, logging, constants, and cross-cutting concerns accessible to all layers
- **FR-046**: System MUST place shared constants in src/utilities/constants.py
- **FR-047**: System MUST place configuration files at project root (not in src/)
- **FR-002**: System MUST place all source code in src/ directory with subdirectories for each layer
- **FR-003**: System MUST create __init__.py files in all package directories
- **FR-004**: System MUST place main entry point at src/main.py
- **FR-005**: System MUST enforce dependency direction: CLI → Services → Domain, Services → Storage → Domain
- **FR-006**: System MUST prohibit circular imports between layers
- **FR-007**: System MUST prohibit domain layer from importing any other application layer

#### Single Responsibility
- **FR-008**: System MUST ensure each module has exactly one responsibility
- **FR-009**: System MUST ensure each class has exactly one responsibility
- **FR-010**: System MUST ensure each function has exactly one logical purpose
- **FR-011**: System MUST separate I/O operations from business logic in different functions
- **FR-012**: System MUST separate validation logic from data transformation logic

#### Function Design
- **FR-013**: System MUST limit functions to 25 lines or fewer (excluding docstrings)
- **FR-043**: System MUST allow function length exceptions when documented with inline comment justifying why splitting is impractical
- **FR-014**: System MUST limit nesting depth to 3 levels or fewer
- **FR-015**: System MUST ensure functions return explicit values rather than relying on side effects
- **FR-016**: System MUST avoid multi-purpose functions that do unrelated things

#### Naming Standards
- **FR-017**: System MUST use verb-based names for functions (e.g., add_task, validate_title)
- **FR-018**: System MUST use noun-based names for classes (e.g., Task, TaskService)
- **FR-019**: System MUST use descriptive variable names that reveal intent
- **FR-020**: System MUST prohibit generic names like "data", "tmp", "util", "handle"
- **FR-021**: System MUST follow PEP 8 naming conventions (snake_case for functions/variables, PascalCase for classes)

#### Type Hints and Documentation
- **FR-022**: System MUST provide type hints for all function parameters
- **FR-023**: System MUST provide return type hints for all functions
- **FR-024**: System MUST provide docstrings for all public functions and classes using Google style format
- **FR-025**: System MUST include parameter descriptions in docstrings using Args: section
- **FR-026**: System MUST include return value descriptions in docstrings using Returns: section
- **FR-041**: System MUST include exception descriptions in docstrings using Raises: section when applicable

#### Code Quality
- **FR-027**: System MUST limit files to 300 lines or fewer
- **FR-028**: System MUST limit domain files to one class per file
- **FR-029**: System MUST use explicit imports only (no wildcard imports)
- **FR-030**: System MUST remove all unused imports
- **FR-031**: System MUST avoid global mutable state
- **FR-032**: System MUST follow PEP 8 formatting standards

#### Layer Responsibilities
- **FR-033**: CLI layer MUST handle user interaction, input parsing, and output formatting only
- **FR-034**: Service layer MUST contain business logic, validation, and task lifecycle operations only
- **FR-035**: Domain layer MUST define entities and pure data models only
- **FR-044**: Domain layer MAY include simple structural validation (e.g., non-empty fields, type checking)
- **FR-045**: Service layer MUST handle complex business rules and validation involving multiple entities or external context
- **FR-036**: Storage layer MUST handle data persistence operations only
- **FR-037**: CLI layer MUST NOT contain business rules or modify storage directly
- **FR-038**: Service layer MUST NOT perform console I/O operations
- **FR-039**: Domain layer MUST NOT depend on any other application layer
- **FR-040**: Storage layer MUST NOT contain business rules or CLI formatting

### Key Entities

- **Layer**: A logical grouping of modules with a specific responsibility (CLI, Service, Domain, Storage)
- **Module**: A Python file containing related functions and/or classes
- **Function**: A callable unit of code with a single responsibility
- **Class**: A blueprint for objects representing domain entities or services
- **Dependency**: An import relationship between modules
- **Type Hint**: Python type annotation for parameters and return values
- **Docstring**: Documentation string describing purpose and usage

### Assumptions

- Python 3.13+ is used with full type hint support
- PEP 8 is the accepted style guide
- Functions naturally stay small when they have single responsibilities
- Type hints improve code quality and catch errors early
- Docstrings are written for public APIs, not internal helpers
- Layer boundaries are enforced through code review and validation
- The project uses standard Python packaging with src/ layout
- No external linting tools are required (manual review is sufficient)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of code is organized into the four defined layers (CLI, Service, Domain, Storage)
- **SC-002**: 0% of functions exceed 25 lines (excluding docstrings and comments)
- **SC-003**: 100% of public functions have complete type hints (parameters and return values)
- **SC-004**: 100% of public functions and classes have docstrings
- **SC-005**: 0% of modules violate dependency direction rules (all dependencies flow correctly)
- **SC-006**: 0% of circular imports exist in the codebase
- **SC-007**: 100% of function names use verbs, 100% of class names use nouns
- **SC-008**: 0% of files exceed 300 lines
- **SC-009**: 0% of generic variable names (data, tmp, util, handle) exist in the codebase
- **SC-010**: 100% of modules have a single, clearly defined responsibility

## Constraints

- No single-file implementation allowed
- No mixed responsibility modules allowed
- No business logic in CLI layer
- No storage logic in service layer
- No hidden global mutable state
- No dynamic runtime patching
- Functions must stay under 25 lines
- Files must stay under 300 lines
- All imports must be explicit (no wildcards)
- PEP 8 compliance is mandatory

## Out of Scope

The following are explicitly excluded from this specification:

- Feature behavior and requirements (covered in 001-todo-app)
- Development workflow and process (covered in 002-dev-workflow)
- Testing frameworks or test implementation
- Deployment and packaging details
- Performance optimization strategies
- Security implementation details
- Logging framework selection
- Error handling patterns (beyond separation of concerns)
- Configuration management approaches
- CLI command syntax and user experience

## Project Structure Detail

### Required Directory Layout

```
project-root/
│
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── menu.py              # User interaction and command handling
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task.py              # Task entity definition
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py      # Business logic and validation
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── memory_store.py      # In-memory data persistence
│   │
│   ├── utilities/
│   │   ├── __init__.py
│   │   └── constants.py         # Shared constants and helpers
│   │
│   └── main.py                  # Application entry point
│
├── specs/                       # Feature specifications
├── history/                     # Prompt history and ADRs
├── .specify/                    # Spec-Kit Plus templates
├── constitution.md              # Project principles
├── README.md                    # Setup and usage
├── CLAUDE.md                    # Claude Code instructions
└── pyproject.toml              # Python project configuration
```

### Layer Responsibilities Summary

**CLI Layer** (`src/cli/`):
- Display menus and prompts
- Parse user input
- Format output for console
- Call service layer methods
- Handle user interaction flow

**Service Layer** (`src/services/`):
- Implement business rules
- Validate task data
- Coordinate between storage and domain
- Manage task lifecycle
- Return results to CLI

**Domain Layer** (`src/domain/`):
- Define Task entity
- Define status enumeration
- Pure data structures
- No dependencies on other layers

**Storage Layer** (`src/storage/`):
- Store tasks in memory collection
- Provide CRUD operations
- Generate unique IDs
- Return domain entities

### Dependency Flow

```
CLI Layer
   ↓ (calls)
Service Layer
   ↓ (calls)
Storage Layer
   ↓ (uses)
Domain Layer
```

All layers can use Domain, but Domain uses nothing.
