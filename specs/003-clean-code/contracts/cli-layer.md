# CLI Layer Contract

**Layer**: CLI (User Interaction)
**Location**: `src/cli/`
**Module**: `menu.py`

## Responsibilities

- Display menu options to user
- Parse and validate user input
- Format output for console display
- Orchestrate service layer calls based on user choices
- Handle user interaction flow

## Dependencies

**Allowed**:
- `from services.task_service import TaskService`
- `from domain.task import Task, TaskStatus`
- `from utilities.constants import *`
- Standard library: `sys` (for exit)

**Forbidden**:
- `from storage.memory_store import ...` (skip-level access violation)

## Public Interface

### display_menu() -> None

Display main menu options to user.

**Purpose**: Show numbered menu with available operations

**Parameters**: None

**Returns**: None

**Side Effects**: Prints menu to console

**Example Output**:
```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit
```

---

### get_user_choice() -> int

Get and validate user menu choice.

**Purpose**: Prompt user for menu selection and validate input

**Parameters**: None

**Returns**: `int` - Selected menu option number (1-6)

**Raises**: None (loops until valid input)

**Side Effects**: Prints prompt, reads from stdin

---

### handle_add_task(service: TaskService) -> None

Handle add task flow.

**Purpose**: Prompt for task details and create new task via service

**Parameters**:
- `service: TaskService` - Service layer instance

**Returns**: None

**Side Effects**:
- Prompts user for title and description
- Calls `service.add_task()`
- Displays success or error message

**Error Handling**: Catches `ValueError` from service and displays error message

---

### handle_view_tasks(service: TaskService) -> None

Handle view tasks flow.

**Purpose**: Retrieve and display all tasks

**Parameters**:
- `service: TaskService` - Service layer instance

**Returns**: None

**Side Effects**:
- Calls `service.list_tasks()`
- Formats and displays task list

**Display Format**:
```
[1] ☐ Task Title
    Description text
[2] ☑ Completed Task
    Description text
```

---

### handle_update_task(service: TaskService) -> None

Handle update task flow.

**Purpose**: Prompt for task ID and new details, update task via service

**Parameters**:
- `service: TaskService` - Service layer instance

**Returns**: None

**Side Effects**:
- Prompts user for task ID
- Prompts for new title and description (optional)
- Calls `service.update_task()`
- Displays success or error message

**Error Handling**: Catches `ValueError` from service and displays error message

---

### handle_delete_task(service: TaskService) -> None

Handle delete task flow.

**Purpose**: Prompt for task ID and delete task via service

**Parameters**:
- `service: TaskService` - Service layer instance

**Returns**: None

**Side Effects**:
- Prompts user for task ID
- Calls `service.delete_task()`
- Displays success or error message

**Error Handling**: Catches `ValueError` from service and displays error message

---

### handle_toggle_status(service: TaskService) -> None

Handle toggle status flow.

**Purpose**: Prompt for task ID and toggle completion status via service

**Parameters**:
- `service: TaskService` - Service layer instance

**Returns**: None

**Side Effects**:
- Prompts user for task ID
- Calls `service.toggle_task_status()`
- Displays success or error message

**Error Handling**: Catches `ValueError` from service and displays error message

---

### format_task_list(tasks: list[Task]) -> str

Format task list for display.

**Purpose**: Convert list of Task objects to formatted string

**Parameters**:
- `tasks: list[Task]` - List of Task objects to format

**Returns**: `str` - Formatted string for console output

**Format**:
- Each task on multiple lines
- ID in brackets
- Status indicator (☐ incomplete, ☑ complete)
- Title on first line
- Description indented on second line

**Example**:
```
[1] ☐ Buy groceries
    Get milk, eggs, and bread
[2] ☑ Finish report
    Complete quarterly report
```

---

### display_message(message: str) -> None

Display message to user.

**Purpose**: Print message to console with formatting

**Parameters**:
- `message: str` - Message text to display

**Returns**: None

**Side Effects**: Prints message to console

---

### get_task_input() -> tuple[str, str]

Prompt for task title and description.

**Purpose**: Collect task details from user

**Parameters**: None

**Returns**: `tuple[str, str]` - (title, description)

**Side Effects**: Prompts user and reads from stdin

**Validation**: None (validation happens in service layer)

---

## Quality Constraints

- ✅ No business logic (validation, transformation)
- ✅ No direct storage access
- ✅ All console I/O happens in this layer
- ✅ Functions ≤25 lines
- ✅ File ≤300 lines
- ✅ All functions have type hints
- ✅ All functions have Google-style docstrings

## Testing Considerations

- Mock `TaskService` for unit testing
- Test user input validation (menu choices)
- Test error message display
- Test task list formatting

## References

- FR-033: CLI layer responsibilities
- FR-037: CLI layer prohibitions
- Spec: User interaction requirements
