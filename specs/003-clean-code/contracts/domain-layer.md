# Domain Layer Contract

**Layer**: Domain (Pure Data Models)
**Location**: `src/domain/`
**Module**: `task.py`

## Responsibilities

- Define pure data structures (entities)
- Provide simple structural validation via type system
- Define domain enumerations
- No dependencies on application layers

## Dependencies

**Allowed**:
- `from dataclasses import dataclass`
- `from enum import Enum`
- `from utilities.constants import *` (if needed)

**Forbidden**:
- `from cli.menu import ...` (application layer)
- `from services.task_service import ...` (application layer)
- `from storage.memory_store import ...` (application layer)

## Public Interface

### TaskStatus Enumeration

Task completion status enumeration.

**Purpose**: Define valid task status values

**Type**: `Enum`

**Values**:
- `INCOMPLETE = "incomplete"` - Task not yet completed
- `COMPLETE = "complete"` - Task completed

**Usage**:
```python
task.status = TaskStatus.INCOMPLETE
if task.status == TaskStatus.COMPLETE:
    print("Task is done!")
```

**Design Decision**: Enum over boolean for clarity and extensibility

---

### Task Dataclass

Task entity representing a todo item.

**Purpose**: Define task data structure with type safety

**Type**: `@dataclass`

**Attributes**:
- `id: int` - Unique task identifier (assigned by storage layer)
- `title: str` - Task title (1-100 characters, validated by service)
- `description: str` - Task description (1-500 characters, validated by service)
- `status: TaskStatus` - Task completion status

**Structural Validation**:
- Type checking via dataclass type hints
- Required fields (no Optional)
- Enforced by Python runtime

**Business Validation**:
- Length limits (handled by service layer)
- Content rules (handled by service layer)

**Example**:
```python
task = Task(
    id=1,
    title="Buy groceries",
    description="Get milk, eggs, and bread",
    status=TaskStatus.INCOMPLETE
)
```

**Immutability**: Fields are mutable (needed for updates)

**Equality**: Automatic `__eq__` based on all fields

**String Representation**: Automatic `__repr__` for debugging

---

## Design Decisions

### Why Dataclass?

**Rationale**:
- Concise syntax
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints built-in
- Standard library (no dependencies)
- Mutable (needed for updates)

**Alternatives Considered**:
- Traditional class: Too much boilerplate
- NamedTuple: Immutable (incompatible with updates)
- Pydantic: External dependency (prohibited)

### Why Enum for Status?

**Rationale**:
- Explicit, self-documenting
- Type-safe (can't assign invalid values)
- Extensible (could add ARCHIVED, DELETED later)
- Clear in code: `TaskStatus.COMPLETE` vs `True`

**Alternatives Considered**:
- Boolean: Less clear, not extensible
- String: Not type-safe, typo-prone
- Integer: Not self-documenting

### Validation Placement

**Domain Validation** (structural):
- Type checking (via type hints)
- Required fields (via dataclass)

**Service Validation** (business rules):
- Length limits (≤100 chars title, ≤500 chars description)
- Content rules (non-empty, newline normalization)
- ID existence checks

**Rationale**: Clarification specifies "Simple validation in domain (structural integrity), complex business rules in service layer"

---

## Quality Constraints

- ✅ Pure data structures only
- ✅ No business logic
- ✅ No I/O operations
- ✅ No dependencies on other app layers
- ✅ One class per file (Task and TaskStatus are related)
- ✅ Functions ≤25 lines (N/A - dataclass)
- ✅ File ≤150 lines
- ✅ All classes have docstrings

## Usage Examples

### Creating a Task

```python
from domain.task import Task, TaskStatus

task = Task(
    id=1,
    title="Write documentation",
    description="Complete API documentation",
    status=TaskStatus.INCOMPLETE
)
```

### Checking Status

```python
if task.status == TaskStatus.COMPLETE:
    print("Task is done!")
else:
    print("Task is pending")
```

### Updating Status

```python
task.status = TaskStatus.COMPLETE
```

### Comparing Tasks

```python
task1 = Task(1, "Title", "Desc", TaskStatus.INCOMPLETE)
task2 = Task(1, "Title", "Desc", TaskStatus.INCOMPLETE)
assert task1 == task2  # True (same values)
```

---

## Testing Considerations

- Test dataclass creation
- Test type enforcement (if possible)
- Test enum values
- Test equality comparison
- No business logic to test (in service layer)

## References

- FR-035: Domain layer responsibilities
- FR-039: Domain layer prohibitions
- FR-044: Simple structural validation in domain
- FR-028: One class per file
- Research Decision 3: Dataclass vs traditional class
- Research Decision 4: Enum vs boolean
