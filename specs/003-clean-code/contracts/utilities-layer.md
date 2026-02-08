# Utilities Layer Contract

**Layer**: Utilities (Cross-Cutting Concerns)
**Location**: `src/utilities/`
**Module**: `constants.py`

## Responsibilities

- Provide shared constants accessible to all layers
- Define error messages for consistent user feedback
- Define configuration values (length limits, defaults)
- Provide cross-cutting helper functions (if needed)

## Dependencies

**Allowed**:
- Standard library only (if needed)

**Forbidden**:
- `from cli.menu import ...` (application layer)
- `from services.task_service import ...` (application layer)
- `from domain.task import ...` (application layer)
- `from storage.memory_store import ...` (application layer)

**Rationale**: Utilities are foundational - no upward dependencies

## Public Interface

### Constants

#### MAX_TITLE_LENGTH: int

Maximum allowed length for task titles.

**Value**: `100`

**Purpose**: Enforce consistent title length limit across application

**Usage**: Service layer validation

**Rationale**: Reasonable limit for console display, prevents excessively long titles

---

#### MAX_DESC_LENGTH: int

Maximum allowed length for task descriptions.

**Value**: `500`

**Purpose**: Enforce consistent description length limit across application

**Usage**: Service layer validation

**Rationale**: Allows detailed descriptions while preventing abuse

---

### Error Messages

#### ERROR_EMPTY_TITLE: str

Error message for empty title validation failure.

**Value**: `"Title cannot be empty"`

**Purpose**: Consistent error message for empty title

**Usage**: Service layer raises ValueError with this message

---

#### ERROR_EMPTY_DESC: str

Error message for empty description validation failure.

**Value**: `"Description cannot be empty"`

**Purpose**: Consistent error message for empty description

**Usage**: Service layer raises ValueError with this message

---

#### ERROR_TITLE_TOO_LONG: str

Error message for title length validation failure.

**Value**: `"Title cannot exceed 100 characters"`

**Purpose**: Consistent error message for title length

**Usage**: Service layer raises ValueError with this message

**Note**: Includes specific limit (100) for clarity

---

#### ERROR_DESC_TOO_LONG: str

Error message for description length validation failure.

**Value**: `"Description cannot exceed 500 characters"`

**Purpose**: Consistent error message for description length

**Usage**: Service layer raises ValueError with this message

**Note**: Includes specific limit (500) for clarity

---

#### ERROR_TASK_NOT_FOUND: str

Error message for task not found.

**Value**: `"Task not found"`

**Purpose**: Consistent error message for missing task

**Usage**: Service layer raises ValueError when task ID doesn't exist

---

#### ERROR_INVALID_ID: str

Error message for invalid task ID.

**Value**: `"Invalid task ID"`

**Purpose**: Consistent error message for invalid ID format

**Usage**: CLI or service layer when ID is not a valid integer

---

## Design Decisions

### Why Constants in Utilities?

**Rationale**:
- Single source of truth
- Easy to find and update
- No duplication across layers
- All layers can access without circular dependencies

**Alternatives Considered**:
- Constants in each layer: Duplication, inconsistency risk
- Constants in domain: Domain should be pure data, not configuration
- Configuration file: Overkill for simple console app

### Why String Error Messages?

**Rationale**:
- Simple, readable
- Easy to update
- Consistent across application
- No need for error codes or complex error handling

**Alternatives Considered**:
- Error codes: Too complex for simple app
- Exception classes: Over-engineering for this scope
- Inline strings: Duplication, inconsistency risk

### Why These Specific Limits?

**MAX_TITLE_LENGTH = 100**:
- Fits comfortably on console line
- Long enough for descriptive titles
- Short enough to prevent abuse

**MAX_DESC_LENGTH = 500**:
- Allows detailed descriptions
- Prevents excessively long text
- Reasonable for in-memory storage

---

## Quality Constraints

- ✅ No application layer dependencies
- ✅ No business logic
- ✅ Pure constants and utilities
- ✅ File ≤100 lines (simple constants file)
- ✅ All constants use UPPER_SNAKE_CASE
- ✅ Module docstring present

## Usage Examples

### In Service Layer

```python
from utilities.constants import (
    MAX_TITLE_LENGTH,
    MAX_DESC_LENGTH,
    ERROR_EMPTY_TITLE,
    ERROR_TITLE_TOO_LONG
)

def _validate_title(self, title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError(ERROR_EMPTY_TITLE)
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(ERROR_TITLE_TOO_LONG)
    return title
```

### In CLI Layer

```python
from utilities.constants import ERROR_TASK_NOT_FOUND

try:
    service.delete_task(task_id)
except ValueError as e:
    if str(e) == ERROR_TASK_NOT_FOUND:
        print(f"Error: {e}")
```

---

## Extension Points

If additional cross-cutting concerns are needed in the future:

### Logging Configuration

```python
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
```

### Display Configuration

```python
TASK_STATUS_INCOMPLETE: str = "☐"
TASK_STATUS_COMPLETE: str = "☑"
MENU_SEPARATOR: str = "=" * 40
```

### Validation Helpers

```python
def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    return " ".join(text.split())
```

**Note**: These are examples only - not required for current scope per constitution

---

## Testing Considerations

- Test constants have expected values
- Test constants are accessible from all layers
- No business logic to test (pure constants)

## References

- FR-042: Utilities layer for cross-cutting concerns
- FR-046: Constants in utilities/constants.py
- FR-047: Configuration files at project root (not in utilities)
- Research Decision 5: Constants organization
- Clarification: Constants in utilities/ layer
