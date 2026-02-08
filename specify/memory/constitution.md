<!--
Sync Impact Report:
- Version change: [INITIAL] → 1.0.0
- Initial constitution creation for Todo In-Memory Python Console App
- Principles defined: Spec Authority, Agentic Development, Traceability, Clean Code, Architecture Discipline, Scope Control
- Templates requiring updates:
  ✅ constitution.md (this file)
  ✅ plan-template.md (validated - Constitution Check section aligns)
  ✅ spec-template.md (validated - user stories with priorities align)
  ✅ tasks-template.md (validated - phase structure and traceability align)
- Follow-up TODOs: None - all templates validated
-->

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Spec Authority
The specification artifacts are the single source of truth for all development work. Code MUST NOT contradict the spec. Any ambiguity discovered during implementation MUST trigger spec refinement before coding proceeds. All features, behaviors, and constraints MUST be traceable to a spec requirement.

**Rationale**: Prevents scope creep, ensures reproducibility, and maintains alignment between intent and implementation in an agentic workflow.

### II. Agentic Development (NON-NEGOTIABLE)
All development MUST follow the Agentic Dev Stack workflow: Write Specification → Generate Implementation Plan → Break Plan into Atomic Tasks → Execute Tasks via Claude Code → Iterate through prompt-driven refinement. Manual coding is PROHIBITED at any stage. All code MUST be generated through Claude Code prompts. Every implementation step MUST map back to spec and task artifacts.

**Rationale**: Ensures full traceability, reproducibility, and auditability of the development process. Enables regeneration over manual patching.

### III. Traceability
Every module, function, and code change MUST map to a spec requirement. Task IDs MUST be referenced in Claude Code prompts. Changes MUST update spec artifacts first before implementation. Prompts, iterations, and outputs MUST be preserved for auditability through Prompt History Records (PHRs).

**Rationale**: Maintains clear lineage from requirements to implementation, enabling verification and audit of all development decisions.

### IV. Clean Code Standards
Code MUST adhere to Single Responsibility Principle per module/function. Naming MUST be clear and descriptive for commands, services, and models. Dead code and unused imports are PROHIBITED. Functions MUST remain small and composable. Console UX MUST remain simple and predictable. No speculative features or over-engineering allowed.

**Rationale**: Ensures maintainability, readability, and simplicity in a constrained console application context.

### V. Architecture Discipline
Separation of concerns is MANDATORY with distinct layers: CLI Interface Layer, Todo Service Layer, In-Memory Store, and Domain Models. Tight coupling between layers is PROHIBITED. Each layer MUST have clear responsibilities and interfaces.

**Rationale**: Enables testability, maintainability, and clear boundaries in a simple application architecture.

### VI. Deterministic Scope Control
Only required features are allowed—no speculative or extra features. No persistence layer—memory-only storage is ENFORCED. Features beyond the five core operations (Add, Delete, Update, View, Mark Complete/Incomplete) are PROHIBITED unless explicitly added to the spec.

**Rationale**: Prevents feature creep and maintains focus on demonstrating the agentic development workflow with minimal complexity.

## Functional Requirements

The console application MUST implement exactly these five core features:

1. **Add Task**: Accept title (required) and description (required)
2. **Delete Task**: Remove task by unique task ID
3. **Update Task**: Edit title and/or description of existing task
4. **View Tasks**: List all tasks with status indicators (complete/incomplete)
5. **Mark Complete/Incomplete**: Toggle task completion status

No additional features are permitted without spec amendment.

## Behavioral Standards

### CLI Behavior
- Menu-driven or command-driven interface allowed
- Output MUST be human-readable
- Error messages MUST be explicit and actionable
- Invalid inputs MUST NOT crash the program

### Data Rules
- Storage MUST be in-memory only (no files, databases, or external storage)
- IDs MUST be unique within runtime session
- State resets when program exits (expected behavior)

### Validation
- Empty titles are PROHIBITED
- Invalid IDs MUST return safe error responses
- Update operations MUST verify task existence before proceeding

## Technology Stack

**Required**:
- Python 3.13+
- UV package manager
- Claude Code for all code generation
- Spec-Kit Plus for spec, plan, and task artifacts

**Prohibited**:
- External databases
- Web frameworks
- GUI frameworks
- Persistence libraries

## Repository Structure

The GitHub repository MUST contain:
- `.specify/memory/constitution.md` — this constitution
- `specs/<feature>/` — specification versions and artifacts
- `src/` — Python source code
- `README.md` — setup and run instructions
- `CLAUDE.md` — Claude Code usage instructions
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records

No deviation from this layout is allowed without constitutional amendment.

## Development Workflow

### Prompting Standards for Claude Code
Claude Code prompts MUST:
- Reference spec sections explicitly
- Reference task IDs when implementing
- Request full file outputs (not fragments)
- Require docstrings and type hints
- Ask for refactoring when complexity increases

### Quality Gates
Implementation is accepted ONLY if:
- All five required features work correctly
- No manual code edits were made
- Spec artifacts exist and are complete
- Repository structure matches constitution
- Code is readable and modular
- CLI usage is stable and error-safe
- All tasks trace back to spec requirements

### Failure Conditions
The project is considered INVALID if:
- Manual coding occurs
- Features are added beyond scope
- Persistence is introduced
- Spec artifacts are missing
- Code is not traceable to tasks
- Structure deviates from required layout

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of the proposed change with rationale
2. Version bump following semantic versioning (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
3. Update of all dependent templates and documentation
4. Sync Impact Report documenting affected artifacts

All development work MUST verify compliance with these principles. Complexity MUST be justified against the principle of simplicity. Use `CLAUDE.md` for runtime development guidance specific to Claude Code agent behavior.

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30
