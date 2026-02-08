# Research: Architectural Decisions for Clean Code Structure

**Feature**: Clean Code Principles and Python Project Structure
**Branch**: `003-clean-code`
**Date**: 2026-01-30
**Status**: Complete

## Overview

This document captures the architectural decisions made during the planning phase for Spec-3. Each decision addresses a structural or design question with explicit rationale, tradeoffs, and references to specification requirements.

---

## Decision 1: Package Layout Depth

**Question**: Should we use flat packages (src/cli.py) or layered packages (src/cli/menu.py)?

**Options Considered**:

1. **Flat packages**: All modules at src/ root (src/cli.py, src/task_service.py, etc.)
2. **Layered packages**: Subdirectories for each layer (src/cli/, src/services/, etc.)
3. **Hybrid**: Some layers flat, some nested

**Selected Option**: Layered packages (Option 2)

**Tradeoffs**:
- ✅ Clear visual separation of layers in file system
- ✅ Easier to enforce layer boundaries
- ✅ Scalable as features grow
- ✅ Standard Python packaging practice
- ❌ Slightly more directory navigation
- ❌ Requires __init__.py files

**Rationale**:
- FR-001 requires "four distinct layers" - layered packages make this explicit
- FR-002 specifies "src/ directory with subdirectories for each layer"
- Spec explicitly shows directory structure with subdirectories
- Aligns with Python best practices for package organization
- Makes import violations immediately visible (e.g., `from storage.memory_store` in CLI is obviously wrong)

**References**: FR-001, FR-002, Spec Project Structure Detail

---

## Decision 2: CLI Design Split

**Question**: Should CLI be a single menu.py file or split into multiple command modules?

**Options Considered**:

1. **Single file**: All CLI logic in menu.py
2. **Command modules**: Separate files for add_command.py, view_command.py, etc.
3. **Handler pattern**: menu.py + handlers/ subdirectory

**Selected Option**: Single file (Option 1)

**Tradeoffs**:
- ✅ Simple for small feature set (5 operations)
- ✅ Easy to understand flow
- ✅ No over-engineering
- ✅ Stays within 300-line file limit
- ❌ Less scalable if features grow significantly
- ❌ All CLI logic in one place

**Rationale**:
- Constitution Principle VI: "Deterministic Scope Control - Only required features allowed"
- Only 5 core operations (Add, Delete, Update, View, Mark Complete/Incomplete)
- FR-027 allows up to 300 lines per file - single menu.py will fit comfortably
- Splitting into multiple files would be premature optimization
- Aligns with "no speculative features or over-engineering" principle
- Can refactor later if scope expands (but constitution prohibits this)

**References**: FR-027, Constitution Principle VI, FR-033

---

## Decision 3: Domain Model Style

**Question**: Should Task entity use dataclass or traditional class?

**Options Considered**:

1. **Dataclass**: Use @dataclass decorator
2. **Traditional class**: Manual __init__, __repr__, etc.
3. **NamedTuple**: Immutable tuple-based
4. **Pydantic**: Third-party validation library

**Selected Option**: Dataclass (Option 1)

**Tradeoffs**:
- ✅ Concise, readable syntax
- ✅ Automatic __init__, __repr__, __eq__
- ✅ Type hints built-in
- ✅ Standard library (no dependencies)
- ✅ Mutable (needed for updates)
- ❌ Less control over initialization
- ❌ Python 3.7+ required (we have 3.13+)

**Rationale**:
- FR-022, FR-023 require type hints - dataclass enforces this
- FR-035 specifies "pure data structures" - dataclass is ideal for this
- Constitution requires Python 3.13+ - dataclass fully supported
- Clarification specifies "Simple validation in domain (structural integrity)" - dataclass provides this via type hints
- No external dependencies allowed per constitution
- Reduces boilerplate while maintaining clarity

**References**: FR-022, FR-023, FR-035, Constitution Technology Stack

---

## Decision 4: Status Representation

**Question**: Should task completion status be a boolean flag or Enum?

**Options Considered**:

1. **Boolean**: `completed: bool`
2. **Enum**: `status: TaskStatus` with INCOMPLETE/COMPLETE
3. **String**: `status: str` with "incomplete"/"complete"
4. **Integer**: `status: int` with 0/1

**Selected Option**: Enum (Option 2)

**Tradeoffs**:
- ✅ Explicit, self-documenting
- ✅ Type-safe (can't assign invalid values)
- ✅ Extensible (could add ARCHIVED, DELETED later if needed)
- ✅ Clear in code: `task.status == TaskStatus.COMPLETE`
- ❌ Slightly more verbose than boolean
- ❌ Requires import of enum

**Rationale**:
- FR-019 requires "descriptive variable names that reveal intent" - `TaskStatus.COMPLETE` is more descriptive than `True`
- FR-023 requires return type hints - Enum provides stronger typing than bool
- Spec shows "status indicators (complete/incomplete)" - Enum makes these explicit states
- Better for future maintenance - boolean meaning can be ambiguous (True = complete or incomplete?)
- Aligns with clean code principle of explicit over implicit

**References**: FR-019, FR-023, Spec Functional Requirements

---

## Decision 5: Storage Container

**Question**: Should in-memory storage use dict (by ID) or list?

**Options Considered**:

1. **Dict by ID**: `{1: Task(...), 2: Task(...), ...}`
2. **List**: `[Task(...), Task(...), ...]`
3. **Dict by title**: `{"Task 1": Task(...), ...}`

**Selected Option**: Dict by ID (Option 1)

**Tradeoffs**:
- ✅ O(1) lookup by ID
- ✅ Natural key-value mapping
- ✅ Easy to check existence
- ✅ Efficient updates and deletes
- ❌ Requires ID generation logic
- ❌ Slightly more memory than list

**Rationale**:
- Spec requires "unique task ID" for Delete, Update, Mark operations
- FR-036 specifies "Generate unique IDs" as storage responsibility
- Dict provides O(1) lookup vs O(n) for list - better performance
- ID-based operations (get, update, delete) are more natural with dict
- List would require linear search for every ID-based operation
- Memory overhead negligible for in-memory console app

**References**: FR-036, Spec Functional Requirements (Delete Task, Update Task)

---

## Decision 6: Service Granularity

**Question**: Should we have a single TaskService or multiple services (TaskValidator, TaskManager, etc.)?

**Options Considered**:

1. **Single service**: TaskService with all business logic
2. **Multiple services**: TaskValidator, TaskManager, TaskFormatter
3. **Service + helpers**: TaskService + validation helper functions

**Selected Option**: Single service (Option 1)

**Tradeoffs**:
- ✅ Simple, cohesive design
- ✅ All task operations in one place
- ✅ No over-engineering
- ✅ Easy to understand
- ❌ Could grow large if features expand
- ❌ Mixes validation and orchestration

**Rationale**:
- Constitution Principle VI: "No speculative features or over-engineering allowed"
- Only 5 core operations - single service is sufficient
- FR-009 requires "each class has exactly one responsibility" - TaskService's responsibility is "task business logic"
- FR-027 allows 300 lines - single service will fit
- Splitting into multiple services would be premature abstraction
- Private helper methods (_validate_title, _normalize_text) provide internal structure
- Clarification allows "complex business rules in service layer" - single service can handle this

**References**: FR-009, FR-027, Constitution Principle VI

---

## Decision 7: Entry Point Location

**Question**: Should entry point be src/main.py or src/cli/runner.py?

**Options Considered**:

1. **src/main.py**: Entry point at src/ root
2. **src/cli/runner.py**: Entry point inside CLI layer
3. **Project root main.py**: Entry point at project root

**Selected Option**: src/main.py (Option 1)

**Tradeoffs**:
- ✅ Clear, conventional location
- ✅ Separates orchestration from CLI logic
- ✅ Easy to find
- ✅ Follows Python src/ layout best practice
- ❌ Not inside any specific layer

**Rationale**:
- FR-004 explicitly specifies "System MUST place main entry point at src/main.py"
- Spec Project Structure Detail shows "src/main.py" as entry point
- main.py orchestrates CLI and Service initialization - not pure CLI logic
- Placing in CLI layer would violate layer responsibility (CLI is for user interaction, not orchestration)
- Standard Python practice for src/ layout

**References**: FR-004, Spec Project Structure Detail

---

## Decision 8: Validation Location

**Question**: Where should validation logic live - domain or service?

**Options Considered**:

1. **All in domain**: Self-validating entities
2. **All in service**: Business rules layer
3. **Split**: Simple in domain, complex in service
4. **Separate validator**: Dedicated validation module

**Selected Option**: Split validation (Option 3)

**Tradeoffs**:
- ✅ Clear separation of concerns
- ✅ Domain handles structural integrity
- ✅ Service handles business rules
- ✅ Follows clarification guidance
- ❌ Requires understanding boundary
- ❌ Validation logic in two places

**Rationale**:
- Clarification explicitly specifies: "Simple validation in domain (structural integrity), complex business rules in service layer"
- FR-035 specifies domain as "pure data models only"
- FR-034 specifies service contains "validation"
- FR-044 allows domain to include "simple structural validation (e.g., non-empty fields, type checking)"
- FR-045 requires service to handle "complex business rules and validation involving multiple entities or external context"

**Domain Validation** (structural):
- Type checking via dataclass type hints
- Required fields via dataclass (no Optional)
- Immutability of ID (frozen field if needed)

**Service Validation** (business rules):
- Length limits (MAX_TITLE_LENGTH, MAX_DESC_LENGTH from constants)
- Content rules (non-empty strings, newline normalization)
- ID existence checks (task exists before update/delete)
- Cross-entity validation (if needed in future)

**References**: FR-034, FR-035, FR-044, FR-045, Clarification Session 2026-01-30

---

## Summary of Decisions

| Decision | Selected Option | Primary Rationale |
|----------|----------------|-------------------|
| Package Layout | Layered packages | FR-002 requires subdirectories, clear separation |
| CLI Design | Single menu.py | 5 operations fit in 300 lines, no over-engineering |
| Domain Model | Dataclass | Type hints, concise, standard library |
| Status Representation | Enum | Explicit, type-safe, self-documenting |
| Storage Container | Dict by ID | O(1) lookup, natural for ID-based operations |
| Service Granularity | Single TaskService | 5 operations, no premature abstraction |
| Entry Point | src/main.py | FR-004 explicit requirement |
| Validation Location | Split (domain + service) | Clarification guidance, separation of concerns |

---

## Architectural Principles Applied

1. **Simplicity First**: Chose single files over multiple when scope permits (menu.py, task_service.py)
2. **Explicit Over Implicit**: Enum over boolean, descriptive names over abbreviations
3. **Standard Library Preferred**: Dataclass over third-party, no external dependencies
4. **Performance Awareness**: Dict over list for ID-based lookups
5. **Separation of Concerns**: Split validation between domain (structural) and service (business rules)
6. **No Premature Optimization**: Single service, single CLI file - can refactor if needed (but constitution prevents scope growth)

---

## Open Questions (None)

All architectural decisions resolved. No NEEDS CLARIFICATION items remain.

---

## Next Steps

1. Generate data-model.md with detailed layer and module specifications
2. Generate contracts/ directory with interface definitions
3. Generate quickstart.md with validation checklists
4. Proceed to Phase 2 (/sp.tasks) for task breakdown

**Research Status**: ✅ COMPLETE
