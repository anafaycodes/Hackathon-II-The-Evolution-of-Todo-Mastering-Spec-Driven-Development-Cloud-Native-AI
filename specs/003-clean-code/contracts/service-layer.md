# Service Layer Contract

**Layer**: Service (Business Logic)
**Location**: `src/services/`
**Module**: `task_service.py`

## Responsibilities

- Implement business logic and validation rules
- Orchestrate between storage and domain layers
- Manage task lifecycle operations
- Validate and normalize user input
- Return results to CLI layer

## Dependencies

**Allowed**:
- `from storage.memory_store import InMemoryTaskStore`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`
- Standard library: `typing`

**Forbidden**:
- `from cli.menu import ...` (upward dependency violation)

## Public Interface

### TaskService Class

Main service class for task business logic.

**Attributes**:
- `_store: InMemoryTaskStore` - Storage layer instance (private)

---

### \_\_init\_\_(store: InMemoryTaskStore) -> None

Initialize service with storage dependency.

**Purpose**: Set up service with dependency injection

**Parameters**:
- `store: InMemoryTaskStore` - Storage layer instance

**Returns**: None

**Design Pattern**: Dependency injection (store passed in, not created internally)

---

### add_task(title: str, description: str) -> Task

Add new task with validation.

**Purpose**: Validate input, normalize text, create task via storage

**Parameters**:
- `title: str` - Task title (raw user input)
- `description: str` - Task description (raw user input)

**Returns**: `Task` - Created task object with assigned ID

**Raises**:
- `ValueError` - If title is empty
- `ValueError` - If title exceeds MAX_TITLE_LENGTH (100 chars)
- `ValueError` - If description is empty
- `ValueError` - If description exceeds MAX_DESC_LENGTH (500 chars)

**Business Rules**:
1. Title must be non-empty after stripping whitespace
2. Title must be ≤100 characters
3. Description must be non-empty after stripping whitespace
4. Description must be ≤500 characters
5. Text is normalized (extra whitespace removed)

**Process**:
1. Validate and normalize title
2. Validate and normalize description
3. Call `store.create_task()`
4. Return created task

---

### list_tasks() -> list[Task]

List all tasks sorted by status then ID.

**Purpose**: Retrieve all tasks with consistent ordering

**Parameters**: None

**Returns**: `list[Task]` - List of all tasks

**Sorting**:
1. Incomplete tasks first
2. Complete tasks second
3. Within each group, sort by ID ascending

**Example Order**:
```
[1] ☐ Task A (incomplete)
[3] ☐ Task C (incomplete)
[2] ☑ Task B (complete)
[4] ☑ Task D (complete)
```

---

### update_task(task_id: int, title: str | None, description: str | None) -> Task

Update existing task with validation.

**Purpose**: Validate input, update task fields, persist changes

**Parameters**:
- `task_id: int` - Unique task identifier
- `title: str | None` - New title (None to keep current)
- `description: str | None` - New description (None to keep current)

**Returns**: `Task` - Updated task object

**Raises**:
- `ValueError` - If task not found
- `ValueError` - If title validation fails (when provided)
- `ValueError` - If description validation fails (when provided)

**Business Rules**:
1. Task must exist
2. If title provided, must pass validation
3. If description provided, must pass validation
4. If both None, no changes made (but not an error)

**Process**:
1. Check task exists
2. Validate and normalize title (if provided)
3. Validate and normalize description (if provided)
4. Call `store.update_task()`
5. Return updated task

---

### delete_task(task_id: int) -> bool

Delete task by ID.

**Purpose**: Remove task from storage

**Parameters**:
- `task_id: int` - Unique task identifier

**Returns**: `bool` - True if deleted

**Raises**:
- `ValueError` - If task not found

**Business Rules**:
1. Task must exist before deletion
2. Deletion is permanent (no soft delete)

**Process**:
1. Check task exists
2. Call `store.delete_task()`
3. Return True

---

### toggle_task_status(task_id: int) -> Task

Toggle task completion status.

**Purpose**: Switch task between incomplete and complete

**Parameters**:
- `task_id: int` - Unique task identifier

**Returns**: `Task` - Updated task object

**Raises**:
- `ValueError` - If task not found

**Business Rules**:
1. Task must exist
2. INCOMPLETE → COMPLETE
3. COMPLETE → INCOMPLETE

**Process**:
1. Check task exists
2. Call `store.toggle_task_status()`
3. Return updated task

---

## Private Interface

### _validate_title(title: str) -> str

Validate and normalize title.

**Purpose**: Apply business rules to title input

**Parameters**:
- `title: str` - Raw title input

**Returns**: `str` - Normalized title

**Raises**:
- `ValueError` - If title empty after stripping
- `ValueError` - If title exceeds MAX_TITLE_LENGTH

**Normalization**:
1. Strip leading/trailing whitespace
2. Replace multiple spaces with single space
3. Remove newlines

**Validation**:
1. Check non-empty
2. Check length ≤100

---

### _validate_description(description: str) -> str

Validate and normalize description.

**Purpose**: Apply business rules to description input

**Parameters**:
- `description: str` - Raw description input

**Returns**: `str` - Normalized description

**Raises**:
- `ValueError` - If description empty after stripping
- `ValueError` - If description exceeds MAX_DESC_LENGTH

**Normalization**:
1. Strip leading/trailing whitespace
2. Replace multiple spaces with single space
3. Replace newlines with spaces

**Validation**:
1. Check non-empty
2. Check length ≤500

---

### _normalize_text(text: str) -> str

Normalize text by removing extra whitespace.

**Purpose**: Consistent text formatting

**Parameters**:
- `text: str` - Raw text input

**Returns**: `str` - Normalized text

**Normalization**:
1. Strip leading/trailing whitespace
2. Replace multiple spaces with single space
3. Replace newlines with spaces

---

## Quality Constraints

- ✅ No console I/O (print, input)
- ✅ No direct user interaction
- ✅ All business rules implemented here
- ✅ Functions ≤25 lines
- ✅ File ≤250 lines
- ✅ All public methods have type hints
- ✅ All public methods have Google-style docstrings

## Error Handling Strategy

- Use `ValueError` for all validation failures
- Include descriptive error messages from constants
- Let exceptions propagate to CLI layer
- No silent failures

## Testing Considerations

- Mock `InMemoryTaskStore` for unit testing
- Test all validation rules
- Test normalization logic
- Test error cases (empty strings, too long, not found)
- Test sorting logic in `list_tasks()`

## References

- FR-034: Service layer responsibilities
- FR-038: Service layer prohibitions
- FR-045: Complex business rules in service
- Clarification: Validation placement
