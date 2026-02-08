# Storage Layer Contract

**Layer**: Storage (Data Persistence)
**Location**: `src/storage/`
**Module**: `memory_store.py`

## Responsibilities

- Handle data persistence (in-memory)
- Provide CRUD operations for tasks
- Generate unique task IDs
- Return domain entities
- No business rules or validation

## Dependencies

**Allowed**:
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *` (if needed)
- Standard library: `typing`

**Forbidden**:
- `from cli.menu import ...` (application layer)
- `from services.task_service import ...` (application layer)

## Public Interface

### InMemoryTaskStore Class

In-memory storage for tasks with CRUD operations.

**Purpose**: Provide data persistence layer using in-memory dictionary

**Attributes**:
- `_tasks: dict[int, Task]` - Dictionary mapping task IDs to Task objects (private)
- `_next_id: int` - Counter for generating unique task IDs (private)

**Storage Strategy**: Dict by ID for O(1) lookup

---

### \_\_init\_\_() -> None

Initialize empty task store.

**Purpose**: Set up empty storage and ID counter

**Parameters**: None

**Returns**: None

**Initial State**:
- `_tasks = {}`
- `_next_id = 1`

---

### create_task(title: str, description: str) -> Task

Create and store a new task.

**Purpose**: Generate ID, create Task object, store in memory

**Parameters**:
- `title: str` - Task title (pre-validated by service)
- `description: str` - Task description (pre-validated by service)

**Returns**: `Task` - Created task object with assigned ID

**Process**:
1. Generate new unique ID
2. Create Task object with INCOMPLETE status
3. Store in `_tasks` dict
4. Return created task

**Assumptions**: Title and description already validated by service layer

---

### get_task(task_id: int) -> Task | None

Retrieve task by ID.

**Purpose**: Lookup task in storage

**Parameters**:
- `task_id: int` - Unique task identifier

**Returns**:
- `Task` - Task object if found
- `None` - If task not found

**Complexity**: O(1) lookup

**No Exceptions**: Returns None instead of raising exception

---

### get_all_tasks() -> list[Task]

Retrieve all tasks.

**Purpose**: Return all tasks in storage

**Parameters**: None

**Returns**: `list[Task]` - List of all Task objects

**Ordering**: No guaranteed order (service layer handles sorting)

**Empty Case**: Returns empty list `[]` if no tasks

---

### update_task(task_id: int, title: str | None, description: str | None) -> Task | None

Update existing task.

**Purpose**: Modify task fields in storage

**Parameters**:
- `task_id: int` - Unique task identifier
- `title: str | None` - New title (None to keep current)
- `description: str | None` - New description (None to keep current)

**Returns**:
- `Task` - Updated task object if found
- `None` - If task not found

**Process**:
1. Lookup task by ID
2. If not found, return None
3. Update title if provided
4. Update description if provided
5. Return updated task

**Assumptions**: Title and description already validated by service layer

**Immutability**: Task object is mutable, updated in place

---

### delete_task(task_id: int) -> bool

Delete task by ID.

**Purpose**: Remove task from storage

**Parameters**:
- `task_id: int` - Unique task identifier

**Returns**:
- `True` - If task was deleted
- `False` - If task not found

**Process**:
1. Check if task exists
2. If exists, remove from `_tasks` dict
3. Return True if deleted, False otherwise

**Permanent**: No soft delete, task is removed from memory

---

### toggle_task_status(task_id: int) -> Task | None

Toggle task completion status.

**Purpose**: Switch task between INCOMPLETE and COMPLETE

**Parameters**:
- `task_id: int` - Unique task identifier

**Returns**:
- `Task` - Updated task object if found
- `None` - If task not found

**Process**:
1. Lookup task by ID
2. If not found, return None
3. Toggle status (INCOMPLETE ↔ COMPLETE)
4. Return updated task

**Toggle Logic**:
- `INCOMPLETE` → `COMPLETE`
- `COMPLETE` → `INCOMPLETE`

---

## Private Interface

### _generate_id() -> int

Generate unique task ID.

**Purpose**: Provide monotonically increasing IDs

**Parameters**: None

**Returns**: `int` - New unique task ID

**Process**:
1. Get current `_next_id` value
2. Increment `_next_id`
3. Return previous value

**Thread Safety**: Not thread-safe (single-threaded console app)

**ID Reuse**: IDs not reused after deletion (counter only increments)

---

## Quality Constraints

- ✅ No business logic (validation, transformation)
- ✅ No console I/O
- ✅ Only data operations
- ✅ Functions ≤25 lines
- ✅ File ≤200 lines
- ✅ All public methods have type hints
- ✅ All public methods have Google-style docstrings

## Design Decisions

### Why Dict by ID?

**Rationale**:
- O(1) lookup by ID (vs O(n) for list)
- Natural key-value mapping
- Easy existence checks
- Efficient updates and deletes

**Alternatives Considered**:
- List: O(n) lookup, requires linear search
- Dict by title: Titles not unique, poor key choice

### Why Return None vs Raise Exception?

**Rationale**:
- Storage layer is data-focused, not business logic
- Service layer decides if missing task is error
- Allows service to provide better error messages
- Simpler storage implementation

**Pattern**: Storage returns None, service raises ValueError

---

## Error Handling Strategy

- No exceptions raised by storage layer
- Return None for not found cases
- Service layer handles error logic
- Validation assumed complete before storage calls

---

## Testing Considerations

- Test ID generation (sequential, unique)
- Test CRUD operations
- Test not found cases (return None)
- Test toggle logic (both directions)
- Test empty store (get_all returns [])
- Test update with None values (no change)

## Usage Examples

### Creating Tasks

```python
store = InMemoryTaskStore()
task1 = store.create_task("Buy milk", "Get 2% milk")
task2 = store.create_task("Write code", "Implement feature X")
# task1.id = 1, task2.id = 2
```

### Retrieving Tasks

```python
task = store.get_task(1)  # Returns Task or None
all_tasks = store.get_all_tasks()  # Returns list[Task]
```

### Updating Tasks

```python
updated = store.update_task(1, title="Buy groceries", description=None)
# Updates title, keeps description
```

### Deleting Tasks

```python
deleted = store.delete_task(1)  # Returns True if deleted
```

### Toggling Status

```python
task = store.toggle_task_status(1)  # INCOMPLETE → COMPLETE
task = store.toggle_task_status(1)  # COMPLETE → INCOMPLETE
```

---

## References

- FR-036: Storage layer responsibilities
- FR-040: Storage layer prohibitions
- Research Decision 5: Dict vs list for storage
- Research Decision 8: Validation in service, not storage
