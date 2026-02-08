# Quickstart: Structure Validation Guide

**Feature**: Clean Code Principles and Python Project Structure
**Branch**: `003-clean-code`
**Date**: 2026-01-30

## Overview

This guide provides validation checklists for verifying that the codebase adheres to Spec-3 clean code principles and architectural constraints. Use these checklists after module generation and before marking tasks complete.

---

## 1. Structure Validation Checklist

Verify folder tree matches blueprint and all required packages exist.

### Directory Structure

- [ ] **SV-001**: `src/` directory exists at project root
- [ ] **SV-002**: `src/__init__.py` exists (package marker)
- [ ] **SV-003**: `src/cli/` subdirectory exists
- [ ] **SV-004**: `src/cli/__init__.py` exists
- [ ] **SV-005**: `src/services/` subdirectory exists
- [ ] **SV-006**: `src/services/__init__.py` exists
- [ ] **SV-007**: `src/domain/` subdirectory exists
- [ ] **SV-008**: `src/domain/__init__.py` exists
- [ ] **SV-009**: `src/storage/` subdirectory exists
- [ ] **SV-010**: `src/storage/__init__.py` exists
- [ ] **SV-011**: `src/utilities/` subdirectory exists
- [ ] **SV-012**: `src/utilities/__init__.py` exists

### Required Modules

- [ ] **SV-013**: `src/main.py` exists (entry point)
- [ ] **SV-014**: `src/cli/menu.py` exists
- [ ] **SV-015**: `src/services/task_service.py` exists
- [ ] **SV-016**: `src/domain/task.py` exists
- [ ] **SV-017**: `src/storage/memory_store.py` exists
- [ ] **SV-018**: `src/utilities/constants.py` exists

### No Extra Files

- [ ] **SV-019**: No `.py` files in `src/` root except `main.py` and `__init__.py`
- [ ] **SV-020**: No subdirectories in `src/` except the 5 layers
- [ ] **SV-021**: No extra modules in layer directories (only specified modules)

**Validation Command**:
```bash
# List all Python files
find src -name "*.py" -type f

# Expected output:
# src/__init__.py
# src/main.py
# src/cli/__init__.py
# src/cli/menu.py
# src/services/__init__.py
# src/services/task_service.py
# src/domain/__init__.py
# src/domain/task.py
# src/storage/__init__.py
# src/storage/memory_store.py
# src/utilities/__init__.py
# src/utilities/constants.py
```

**Pass Criteria**: Exactly 12 Python files, no more, no less

**Regeneration Trigger**: Missing directories, missing __init__.py, extra files

---

## 2. Dependency Validation Checklist

Verify no forbidden imports and dependency direction is correct.

### CLI Layer Dependencies

- [ ] **DV-001**: `cli/menu.py` imports from `services.task_service` ✅
- [ ] **DV-002**: `cli/menu.py` imports from `domain.task` ✅
- [ ] **DV-003**: `cli/menu.py` imports from `utilities.constants` ✅
- [ ] **DV-004**: `cli/menu.py` does NOT import from `storage.memory_store` ❌
- [ ] **DV-005**: `cli/menu.py` uses only standard library beyond allowed imports

**Validation Command**:
```bash
grep -E "^from|^import" src/cli/menu.py
```

**Pass Criteria**: Only imports from services, domain, utilities, and stdlib

**Regeneration Trigger**: Import from storage layer detected

---

### Service Layer Dependencies

- [ ] **DV-006**: `services/task_service.py` imports from `storage.memory_store` ✅
- [ ] **DV-007**: `services/task_service.py` imports from `domain.task` ✅
- [ ] **DV-008**: `services/task_service.py` imports from `utilities.constants` ✅
- [ ] **DV-009**: `services/task_service.py` does NOT import from `cli.menu` ❌
- [ ] **DV-010**: `services/task_service.py` uses only standard library beyond allowed imports

**Validation Command**:
```bash
grep -E "^from|^import" src/services/task_service.py
```

**Pass Criteria**: Only imports from storage, domain, utilities, and stdlib

**Regeneration Trigger**: Import from CLI layer detected

---

### Domain Layer Dependencies

- [ ] **DV-011**: `domain/task.py` imports from `utilities.constants` (optional) ✅
- [ ] **DV-012**: `domain/task.py` does NOT import from `cli.menu` ❌
- [ ] **DV-013**: `domain/task.py` does NOT import from `services.task_service` ❌
- [ ] **DV-014**: `domain/task.py` does NOT import from `storage.memory_store` ❌
- [ ] **DV-015**: `domain/task.py` uses only standard library (dataclasses, enum)

**Validation Command**:
```bash
grep -E "^from|^import" src/domain/task.py
```

**Pass Criteria**: Only imports from utilities (optional) and stdlib

**Regeneration Trigger**: Import from any application layer detected

---

### Storage Layer Dependencies

- [ ] **DV-016**: `storage/memory_store.py` imports from `domain.task` ✅
- [ ] **DV-017**: `storage/memory_store.py` imports from `utilities.constants` (optional) ✅
- [ ] **DV-018**: `storage/memory_store.py` does NOT import from `cli.menu` ❌
- [ ] **DV-019**: `storage/memory_store.py` does NOT import from `services.task_service` ❌
- [ ] **DV-020**: `storage/memory_store.py` uses only standard library beyond allowed imports

**Validation Command**:
```bash
grep -E "^from|^import" src/storage/memory_store.py
```

**Pass Criteria**: Only imports from domain, utilities, and stdlib

**Regeneration Trigger**: Import from CLI or service layer detected

---

### Utilities Layer Dependencies

- [ ] **DV-021**: `utilities/constants.py` does NOT import from `cli.menu` ❌
- [ ] **DV-022**: `utilities/constants.py` does NOT import from `services.task_service` ❌
- [ ] **DV-023**: `utilities/constants.py` does NOT import from `domain.task` ❌
- [ ] **DV-024**: `utilities/constants.py` does NOT import from `storage.memory_store` ❌
- [ ] **DV-025**: `utilities/constants.py` uses only standard library (if any imports)

**Validation Command**:
```bash
grep -E "^from|^import" src/utilities/constants.py
```

**Pass Criteria**: No application layer imports

**Regeneration Trigger**: Any application layer import detected

---

### Circular Dependency Check

- [ ] **DV-026**: No circular imports detected (manual verification or tool)

**Validation Method**: Import all modules in Python REPL
```python
import src.utilities.constants
import src.domain.task
import src.storage.memory_store
import src.services.task_service
import src.cli.menu
import src.main
```

**Pass Criteria**: All imports succeed without ImportError

**Regeneration Trigger**: ImportError due to circular dependency

---

### Wildcard Import Check

- [ ] **DV-027**: No wildcard imports except `from utilities.constants import *`

**Validation Command**:
```bash
grep "from .* import \*" src/**/*.py
```

**Pass Criteria**: Only `from utilities.constants import *` appears (if at all)

**Regeneration Trigger**: Wildcard import from non-utilities module

---

## 3. Clean Code Validation Checklist

Verify functions are small, focused, and well-named.

### Function Length

- [ ] **CC-001**: All functions ≤25 lines (excluding docstrings and blank lines)
- [ ] **CC-002**: Any exceptions documented with inline comment

**Validation Method**: Manual review or script
```python
def count_function_lines(function_text):
    lines = [l for l in function_text.split('\n')
             if l.strip()
             and not l.strip().startswith('#')
             and not l.strip().startswith('"""')
             and not l.strip().startswith("'''")]
    return len(lines)
```

**Pass Criteria**: 100% compliance or documented exceptions

**Regeneration Trigger**: Function exceeds 25 lines without justification comment

---

### Single Responsibility

- [ ] **CC-003**: Each function has one clear purpose
- [ ] **CC-004**: Function can be described with single verb + object
- [ ] **CC-005**: No functions doing multiple unrelated things

**Validation Method**: Manual review - describe each function in one sentence

**Pass Criteria**: All functions have single, clear responsibility

**Regeneration Trigger**: Function does multiple unrelated things

---

### Naming Conventions

- [ ] **CC-006**: All function names use `snake_case` with verb prefix
- [ ] **CC-007**: All class names use `PascalCase` with noun
- [ ] **CC-008**: All constants use `UPPER_SNAKE_CASE`
- [ ] **CC-009**: All variables use `snake_case` with descriptive names

**Validation Command**:
```bash
# Check for prohibited generic names
grep -rn "\\bdata\\b\\|\\btmp\\b\\|\\butil\\b\\|\\bhandle\\b" src/ --include="*.py"
```

**Pass Criteria**: No prohibited generic names found

**Regeneration Trigger**: Generic names (data, tmp, util, handle) detected

---

### Nesting Depth

- [ ] **CC-010**: All functions have nesting depth ≤3 levels

**Validation Method**: Manual review or AST analysis

**Example Violation**:
```python
if condition:           # Level 1
    for item in items:  # Level 2
        if item.valid:  # Level 3
            while True: # Level 4 - VIOLATION
                pass
```

**Pass Criteria**: No nesting exceeds 3 levels

**Regeneration Trigger**: Nesting depth exceeds 3 levels

---

### No Dead Code

- [ ] **CC-011**: No unused functions
- [ ] **CC-012**: No commented-out code blocks
- [ ] **CC-013**: No unreachable code

**Validation Method**: Manual review + code coverage tools

**Pass Criteria**: All defined functions are called, no commented code

**Regeneration Trigger**: Unused function or commented code detected

---

## 4. Type & Documentation Validation Checklist

Verify type hints and docstrings are present and correct.

### Type Hints

- [ ] **TD-001**: All public functions have parameter type hints
- [ ] **TD-002**: All public functions have return type hints
- [ ] **TD-003**: Type hints use modern syntax (`list[Task]` not `List[Task]`)
- [ ] **TD-004**: Optional parameters use `| None` syntax (Python 3.10+)

**Validation Command**:
```bash
# Check for missing type hints (manual review)
grep -A 5 "^def " src/**/*.py | grep -v ":" | grep -v "self"
```

**Pass Criteria**: 100% of public functions have complete type hints

**Regeneration Trigger**: Missing type hint on public function

---

### Docstrings

- [ ] **TD-005**: All public functions have docstrings
- [ ] **TD-006**: All public classes have docstrings
- [ ] **TD-007**: All modules have module-level docstrings
- [ ] **TD-008**: Docstrings follow Google style format

**Validation Method**: Check for docstring after function/class definition

**Pass Criteria**: 100% of public APIs have docstrings

**Regeneration Trigger**: Missing docstring on public function/class

---

### Docstring Content

- [ ] **TD-009**: Docstrings include `Args:` section (if parameters exist)
- [ ] **TD-010**: Docstrings include `Returns:` section (if not None)
- [ ] **TD-011**: Docstrings include `Raises:` section (if exceptions raised)
- [ ] **TD-012**: Docstrings are accurate and up-to-date

**Example Google Style Docstring**:
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

**Pass Criteria**: All docstrings have required sections

**Regeneration Trigger**: Missing required docstring section

---

## 5. Module Responsibility Validation Checklist

Verify each module has single, clear responsibility.

### CLI Layer

- [ ] **MR-001**: `cli/menu.py` contains only user interaction code
- [ ] **MR-002**: `cli/menu.py` has no business logic (validation, transformation)
- [ ] **MR-003**: `cli/menu.py` has no direct storage access
- [ ] **MR-004**: All console I/O happens in CLI layer

**Validation Method**: Manual review - check for validation logic, storage calls

**Pass Criteria**: CLI only handles I/O and orchestration

**Regeneration Trigger**: Business logic or storage access in CLI

---

### Service Layer

- [ ] **MR-005**: `services/task_service.py` contains only business logic
- [ ] **MR-006**: `services/task_service.py` has no console I/O (print, input)
- [ ] **MR-007**: `services/task_service.py` orchestrates storage and domain
- [ ] **MR-008**: All validation logic in service layer

**Validation Method**: Manual review - check for print/input statements

**Pass Criteria**: Service only handles business logic

**Regeneration Trigger**: Console I/O in service layer

---

### Domain Layer

- [ ] **MR-009**: `domain/task.py` contains only data structures
- [ ] **MR-010**: `domain/task.py` has no business logic
- [ ] **MR-011**: `domain/task.py` has no I/O operations
- [ ] **MR-012**: Domain is pure (no side effects)

**Validation Method**: Manual review - check for logic beyond dataclass

**Pass Criteria**: Domain only defines entities

**Regeneration Trigger**: Business logic or I/O in domain

---

### Storage Layer

- [ ] **MR-013**: `storage/memory_store.py` contains only data operations
- [ ] **MR-014**: `storage/memory_store.py` has no business logic (validation)
- [ ] **MR-015**: `storage/memory_store.py` has no console I/O
- [ ] **MR-016**: Storage only handles CRUD operations

**Validation Method**: Manual review - check for validation logic

**Pass Criteria**: Storage only handles data persistence

**Regeneration Trigger**: Business logic or I/O in storage

---

### Utilities Layer

- [ ] **MR-017**: `utilities/constants.py` contains only constants
- [ ] **MR-018**: `utilities/constants.py` has no business logic
- [ ] **MR-019**: `utilities/constants.py` has no application layer dependencies

**Validation Method**: Manual review - check for logic or imports

**Pass Criteria**: Utilities only defines constants

**Regeneration Trigger**: Logic or app layer imports in utilities

---

## 6. File Quality Validation Checklist

Verify file-level quality constraints.

### File Length

- [ ] **FQ-001**: All files ≤300 lines
- [ ] **FQ-002**: `utilities/constants.py` ≤100 lines (simple constants)
- [ ] **FQ-003**: `main.py` ≤100 lines (simple orchestration)

**Validation Command**:
```bash
wc -l src/**/*.py
```

**Pass Criteria**: All files within limits

**Regeneration Trigger**: File exceeds line limit

---

### Import Organization

- [ ] **FQ-004**: Imports organized (stdlib, third-party, local)
- [ ] **FQ-005**: No unused imports
- [ ] **FQ-006**: All imports explicit (no wildcards except utilities.constants)

**Validation Method**: Manual review or linter (flake8, pylint)

**Pass Criteria**: Clean, organized imports

**Regeneration Trigger**: Unused imports or poor organization

---

### PEP 8 Compliance

- [ ] **FQ-007**: Indentation is 4 spaces
- [ ] **FQ-008**: Line length ≤79 characters (or 100 if reasonable)
- [ ] **FQ-009**: Two blank lines between top-level definitions
- [ ] **FQ-010**: One blank line between methods

**Validation Command**:
```bash
# If using linter
flake8 src/
```

**Pass Criteria**: PEP 8 compliant

**Regeneration Trigger**: PEP 8 violations

---

## 7. Regeneration Triggers

When to regenerate vs patch modules.

### Always Regenerate

- Structural violations (wrong layer, missing imports)
- Dependency violations (forbidden imports)
- Architectural violations (business logic in wrong layer)
- Major naming violations (wrong conventions)
- Missing type hints or docstrings

### Consider Patching (But Prefer Regeneration)

- Typos in strings
- Minor formatting issues
- Comment updates

### Regeneration Process

1. Identify violation and rule ID
2. Document what needs to change
3. Regenerate entire module (not patch)
4. Re-run all validation checklists
5. Verify violation resolved

**Rationale**: Regeneration ensures consistency and catches related issues

---

## 8. Validation Workflow

### After Each Module Generation

1. Run Structure Validation (Section 1)
2. Run Dependency Validation (Section 2) for that module
3. Run Clean Code Validation (Section 3) for that module
4. Run Type & Documentation Validation (Section 4) for that module
5. Run Module Responsibility Validation (Section 5) for that module
6. Document any violations
7. Regenerate if violations found

### After All Modules Generated

1. Run full Structure Validation (Section 1)
2. Run full Dependency Validation (Section 2)
3. Run full Clean Code Validation (Section 3)
4. Run full Type & Documentation Validation (Section 4)
5. Run full Module Responsibility Validation (Section 5)
6. Run File Quality Validation (Section 6)
7. Test circular imports (import all modules)
8. Document final validation status

### Before Marking Tasks Complete

1. All validation checklists pass
2. No regeneration triggers active
3. All modules exist and are correct
4. Application runs without errors

---

## 9. Success Criteria Mapping

Map validation to Spec-3 success criteria.

| Success Criterion | Validation Checklist | Target |
|-------------------|---------------------|--------|
| SC-001: 100% code in 4 layers | Section 1 (Structure) | All modules in correct layers |
| SC-002: 0% functions >25 lines | Section 3 (CC-001, CC-002) | 100% compliance |
| SC-003: 100% type hints | Section 4 (TD-001, TD-002) | All public functions |
| SC-004: 100% docstrings | Section 4 (TD-005, TD-006) | All public APIs |
| SC-005: 0% dependency violations | Section 2 (All DV checks) | No forbidden imports |
| SC-006: 0% circular imports | Section 2 (DV-026) | All imports succeed |
| SC-007: 100% naming compliance | Section 3 (CC-006 to CC-009) | All names follow conventions |
| SC-008: 0% files >300 lines | Section 6 (FQ-001 to FQ-003) | All files within limits |
| SC-009: 0% generic names | Section 3 (CC-009) | No prohibited names |
| SC-010: 100% single responsibility | Section 5 (All MR checks) | Each module has one purpose |

---

## 10. Quick Reference

### Validation Commands

```bash
# Structure check
find src -name "*.py" -type f | wc -l  # Should be 12

# Dependency check (example for CLI)
grep -E "^from|^import" src/cli/menu.py

# Generic names check
grep -rn "\\bdata\\b\\|\\btmp\\b\\|\\butil\\b" src/ --include="*.py"

# File length check
wc -l src/**/*.py

# Import test
python3 -c "import src.main"
```

### Pass/Fail Summary

- ✅ **PASS**: All checklists complete, no violations
- ⚠️ **WARNING**: Minor issues, consider patching
- ❌ **FAIL**: Violations detected, regeneration required

---

## References

- Spec-3: specs/003-clean-code/spec.md
- Plan: specs/003-clean-code/plan.md
- Data Model: specs/003-clean-code/data-model.md
- Contracts: specs/003-clean-code/contracts/

**Quickstart Status**: ✅ COMPLETE
