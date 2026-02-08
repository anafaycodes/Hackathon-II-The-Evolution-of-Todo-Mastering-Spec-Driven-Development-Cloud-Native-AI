# Contributing to Todo In-Memory Python Console App

Thank you for your interest in contributing! This project follows spec-driven development principles with strict quality standards.

## Development Workflow

This project uses **Spec-Driven Development (SDD)** with the following workflow:

```
Constitution → Specification → Plan → Tasks → Implementation → Validation
```

### 1. Constitution First

All changes must align with the project constitution (`.specify/memory/constitution.md`):

- **Spec Authority**: Code must not contradict specifications
- **Agentic Development**: All code generated via Claude Code prompts
- **Traceability**: Every change maps to spec requirements
- **Clean Code**: Functions ≤25 lines, type hints, docstrings
- **Architecture Discipline**: Respect 5-layer boundaries
- **Scope Control**: No features beyond spec

### 2. Specification Changes

Before implementing features:

1. Update `specs/001-todo-app/spec.md` with new requirements
2. Add user stories with acceptance scenarios
3. Define success criteria
4. Run `/sp.analyze` to validate consistency
5. Get approval before proceeding

### 3. Implementation Planning

After spec approval:

1. Update `specs/001-todo-app/plan.md` with architecture decisions
2. Document design tradeoffs
3. Update `specs/001-todo-app/tasks.md` with atomic tasks
4. Ensure all tasks reference spec requirements

### 4. Code Generation

All code must be generated via Claude Code:

```bash
# Example prompt format
Task: T020 - Add task priority feature
Spec Requirements: FR-024, FR-025
Acceptance Criteria:
- Priority levels: High, Medium, Low
- Default priority: Medium
- Display priority in task list

Generate src/domain/task.py with updated Task dataclass...
```

**Never manually edit generated code**. Instead:
- Refine the prompt
- Regenerate the entire file
- Document the change in a PHR (Prompt History Record)

## Code Quality Standards

### Layer Architecture

Respect the 5-layer architecture:

```
CLI → Services → Domain
         ↓
      Storage → Domain
         ↓
     Utilities
```

**Allowed Dependencies:**
- CLI: services, domain, utilities
- Services: storage, domain, utilities
- Domain: utilities only
- Storage: domain, utilities
- Utilities: none

**Prohibited:**
- CLI cannot import storage
- Services cannot import CLI
- Domain cannot import CLI, services, or storage
- No circular imports

### Function Quality

All functions must:
- ✅ Be ≤25 lines (excluding docstrings)
- ✅ Have complete type hints
- ✅ Have Google-style docstrings
- ✅ Have single responsibility
- ✅ Use descriptive names (verbs for functions, nouns for classes)

**Exception**: Functions >25 lines require inline justification:
```python
# FUNCTION LENGTH EXCEPTION: Complex error handling requires 35 lines.
# Splitting would reduce readability by separating tightly coupled logic.
def complex_validation(...):
    ...
```

### Naming Conventions

- **Functions**: `snake_case` with verb prefix (`add_task`, `validate_title`)
- **Classes**: `PascalCase` with noun (`TaskService`, `InMemoryTaskStore`)
- **Constants**: `UPPER_SNAKE_CASE` (`MAX_TITLE_LENGTH`)
- **Private**: Prefix with `_` (`_validate_title`, `_normalize_text`)

**Prohibited Names**: `data`, `tmp`, `util`, `handle`, `process`, `do`, `manager`

### Documentation

All public functions and classes require Google-style docstrings:

```python
def add_task(title: str, description: str) -> Task:
    """Add a new task with validation.

    Args:
        title: Task title (1-100 characters)
        description: Task description (1-500 characters)

    Returns:
        The newly created Task object

    Raises:
        ValueError: If title or description invalid
    """
```

## Testing

### Acceptance Testing

Test against spec acceptance scenarios:

```python
# User Story 1, Scenario 1
task = service.add_task("Buy groceries", "Milk, eggs, bread")
assert task.id == 1
assert task.status == TaskStatus.INCOMPLETE
```

### Clean Code Validation

Run validation before committing:

```bash
python -c "
import ast
from pathlib import Path

# Check layer boundaries
# Check function lengths
# Check type hints
# Check docstrings
"
```

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b 002-feature-name
   ```

2. **Update Specifications**
   - Add requirements to `specs/002-feature-name/spec.md`
   - Create implementation plan in `plan.md`
   - Break down into tasks in `tasks.md`

3. **Generate Code via Claude Code**
   - Reference task IDs in prompts
   - Generate complete files (not patches)
   - Create PHRs for all prompts

4. **Validate Quality**
   - Run acceptance tests
   - Run clean code validation
   - Verify layer boundaries
   - Check traceability

5. **Create Pull Request**
   - Title: `[Feature] Brief description`
   - Link to spec document
   - List completed tasks
   - Include test results

6. **Review Checklist**
   - [ ] All tasks marked complete in tasks.md
   - [ ] All acceptance tests pass
   - [ ] Clean code validation passes
   - [ ] Layer boundaries respected
   - [ ] Type hints complete
   - [ ] Docstrings present
   - [ ] PHRs created for all prompts
   - [ ] No manual code edits

## Common Issues

### Import Errors

Run as module from project root:
```bash
python -m src.main
```

Not:
```bash
python src/main.py  # Will fail with ModuleNotFoundError
```

### Layer Boundary Violations

**Wrong**:
```python
# In CLI layer
from src.storage.memory_store import InMemoryTaskStore  # ❌
```

**Right**:
```python
# In CLI layer
from src.services.task_service import TaskService  # ✅
```

### Missing Type Hints

**Wrong**:
```python
def add_task(title, description):  # ❌
    ...
```

**Right**:
```python
def add_task(title: str, description: str) -> Task:  # ✅
    ...
```

## Development Tools

### Spec-Kit Plus Commands

```bash
/sp.specify    # Create/update specification
/sp.plan       # Create implementation plan
/sp.tasks      # Generate task breakdown
/sp.implement  # Execute implementation
/sp.analyze    # Validate consistency
```

### Quality Enforcement

Use the `todo-quality-enforcer` agent:
```bash
# Review code quality
claude-code --agent todo-quality-enforcer
```

## Questions?

- Check the [README.md](README.md) for usage
- Review `specs/001-todo-app/spec.md` for requirements
- See `specs/001-todo-app/plan.md` for architecture
- Read `.specify/memory/constitution.md` for principles

## Code of Conduct

- Respect the spec-driven workflow
- Never bypass quality gates
- Document all decisions
- Maintain traceability
- Follow clean code principles

---

**Remember**: Quality over speed. Every line of code should be traceable to a spec requirement.
