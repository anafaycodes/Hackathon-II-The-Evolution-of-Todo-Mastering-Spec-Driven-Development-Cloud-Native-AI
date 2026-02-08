# Implementation Plan: Spec-Driven Development Workflow

**Branch**: `002-dev-workflow` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)

**Input**: Process specification from `/specs/002-dev-workflow/spec.md` with clarifications

## Summary

Implement a spec-driven development workflow that enforces constitution-first, spec-first engineering with prompt-driven code generation, comprehensive traceability, and hybrid review gates. This plan defines how the workflow itself is implemented, validated, and audited—not application features.

**Key Clarifications Applied**:
- Hybrid gate enforcement (automated + manual review)
- Emergency bypass allowed with retroactive documentation
- Regenerate on mismatch; update spec if spec was wrong
- PHRs for all Claude Code interactions (comprehensive audit trail)
- Task splitting allowed with subtask naming (T005a, T005b)

## Process Architecture

### Workflow Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Constitution Artifact                         │
│  (.specify/memory/constitution.md - Project principles)         │
└────────────────────────┬────────────────────────────────────────┘
                         │ governs
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Specification Artifacts                         │
│  (specs/###-feature/spec.md - Requirements, user stories)       │
└────────────────────────┬────────────────────────────────────────┘
                         │ informs
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Implementation Plan                            │
│  (specs/###-feature/plan.md - Architecture, decisions)          │
└────────────────────────┬────────────────────────────────────────┘
                         │ breaks down into
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Task Breakdown                                │
│  (specs/###-feature/tasks.md - Atomic work items)               │
└────────────────────────┬────────────────────────────────────────┘
                         │ executed via
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Claude Code Prompt Layer                         │
│  (history/prompts/###-feature/*.prompt.md - PHRs)               │
└────────────────────────┬────────────────────────────────────────┘
                         │ generates
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Generated Code Outputs                         │
│  (src/**/*.py - Application code)                               │
└────────────────────────┬────────────────────────────────────────┘
                         │ validated by
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Review & Regeneration Loop                          │
│  (Hybrid gates: automated + manual)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │ if pass
                         ▼
                    Finalized Code
                         │ if fail
                         └──────> Refine Prompt → Regenerate
```

### Component Responsibilities

**Constitution Artifact** (`.specify/memory/constitution.md`):
- **Input**: Project principles, constraints, quality standards
- **Output**: Governance rules for all development
- **Responsibility**: Define non-negotiable principles
- **Dependency**: None (first artifact created)

**Specification Artifacts** (`specs/###-feature/spec.md`):
- **Input**: Feature requirements, user stories, acceptance criteria
- **Output**: Technology-agnostic requirements
- **Responsibility**: Define WHAT to build (not HOW)
- **Dependency**: Constitution must exist first (FR-001)

**Implementation Plan** (`specs/###-feature/plan.md`):
- **Input**: Spec requirements, architecture decisions
- **Output**: Module structure, design decisions, task strategy
- **Responsibility**: Define HOW to build (architecture)
- **Dependency**: Spec must exist first (FR-002)

**Task Breakdown** (`specs/###-feature/tasks.md`):
- **Input**: Plan modules, spec requirements
- **Output**: Atomic, testable work items with IDs
- **Responsibility**: Break plan into executable units
- **Dependency**: Plan must exist first (FR-003)

**Claude Code Prompt Layer** (`history/prompts/###-feature/*.prompt.md`):
- **Input**: Task ID, spec reference, acceptance criteria
- **Output**: PHR with prompt text and generated code
- **Responsibility**: Execute tasks, capture provenance
- **Dependency**: Tasks must exist first (FR-004)

**Generated Code Outputs** (`src/**/*.py`):
- **Input**: Claude Code generation from prompts
- **Output**: Application source files
- **Responsibility**: Implement functionality
- **Dependency**: Prompts must exist first (FR-005)

**Review & Regeneration Loop**:
- **Input**: Generated code, validation results
- **Output**: Pass/fail decision, refined prompts
- **Responsibility**: Validate compliance, trigger regeneration
- **Dependency**: Code must exist to review

**Artifact History Store** (`history/`):
- **Input**: PHRs, ADRs, audit logs
- **Output**: Immutable history of decisions
- **Responsibility**: Preserve traceability
- **Dependency**: Continuous throughout workflow

### Regeneration Loop Path

```
Code Generated
     ↓
Validation Check
     ↓
  Pass? ──Yes──> Finalize
     ↓ No
Identify Issue
     ↓
Spec Wrong? ──Yes──> Update Spec → Regenerate
     ↓ No
Refine Prompt
     ↓
Regenerate Code
     ↓
(Loop back to Validation)
```

## Technical Context

**Language/Version**: Process definition (language-agnostic)
**Primary Dependencies**: Claude Code CLI, Git, Spec-Kit Plus templates
**Storage**: File-based artifacts in defined directory structure
**Testing**: Hybrid validation (automated + manual review)
**Target Platform**: Development workflow (not runtime)
**Project Type**: Process implementation
**Performance Goals**: N/A (workflow efficiency, not runtime performance)
**Constraints**: All code via Claude Code, no manual edits (except emergency bypass)
**Scale/Scope**: Governs all features in project

## Constitution Check

✅ **Spec Authority**: Workflow enforces spec-first development
✅ **Agentic Development**: All code via Claude Code prompts (FR-005)
✅ **Traceability**: Code → Task → Plan → Spec mapping (FR-010)
✅ **Clean Code**: Enforced through review gates
✅ **Architecture Discipline**: Plan required before tasks
✅ **Scope Control**: Gates prevent scope creep

## Artifact Inventory & Versioning Model

### Artifact Types

| Artifact Type | Location | Versioning | Mutability |
|---------------|----------|------------|------------|
| Constitution | `.specify/memory/constitution.md` | Semantic (MAJOR.MINOR.PATCH) | Amendable with process |
| Specification | `specs/###-feature/spec.md` | Git commits | Amendable before code |
| Plan | `specs/###-feature/plan.md` | Git commits | Amendable before tasks |
| Tasks | `specs/###-feature/tasks.md` | Git commits | Amendable during implementation |
| PHR | `history/prompts/###-feature/NNN-*.prompt.md` | Immutable (append-only) | Immutable |
| ADR | `history/adr/NNN-*.md` | Immutable (append-only) | Immutable |
| Code | `src/**/*.py` | Git commits | Via regeneration only |

### Versioning Strategy

**Decision**: Incremental versioning with Git commits

**Options Considered**:
- A) Snapshot versioning (full copies at each stage)
- B) Incremental versioning (Git commits track changes)
- C) Hybrid (Git for code, snapshots for specs)

**Selected**: B - Incremental versioning with Git

**Tradeoffs**:
- ✅ Standard Git workflow
- ✅ Efficient storage
- ✅ Built-in diff and history
- ✅ Branch-based feature isolation
- ❌ Requires Git discipline

**Rationale**: Spec requires "version all artifacts" (FR-013). Git provides natural versioning with commit history, diffs, and branch isolation. Each feature branch maintains its own artifact evolution. Constitution uses semantic versioning for governance changes.

### Directory Structure

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # v1.0.0 (semantic versioning)
│   ├── templates/                   # Spec-Kit Plus templates
│   └── scripts/                     # Automation scripts
├── specs/
│   ├── 001-todo-app/
│   │   ├── spec.md                  # Feature requirements
│   │   ├── plan.md                  # Implementation plan
│   │   ├── tasks.md                 # Task breakdown
│   │   └── checklists/              # Validation checklists
│   ├── 002-dev-workflow/
│   │   ├── spec.md
│   │   ├── plan.md (this file)
│   │   └── tasks.md
│   └── 003-clean-code/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── history/
│   ├── prompts/
│   │   ├── constitution/            # Constitution-related PHRs
│   │   ├── 001-todo-app/            # Feature-specific PHRs
│   │   ├── 002-dev-workflow/
│   │   ├── 003-clean-code/
│   │   └── general/                 # General PHRs
│   └── adr/                         # Architecture Decision Records
├── src/                             # Generated application code
└── CLAUDE.md                        # Agent instructions
```

## Key Design Decisions

### Decision 1: Prompt Template Strictness

**Options Considered**:
- A) Fixed template (all prompts must follow exact format)
- B) Flexible guidelines (prompts adapt to context)
- C) Hybrid (core fields required, details flexible)

**Selected**: C - Hybrid (required fields + flexible details)

**Tradeoffs**:
- ✅ Ensures traceability (required fields)
- ✅ Allows context-appropriate detail
- ✅ Balances structure and flexibility
- ❌ Requires validation of required fields

**Rationale**: Spec requires prompts reference task ID and spec section (FR-007). PHR template defines required fields (id, title, stage, date, task reference). Prompt text itself can be flexible to suit the specific task context. Automated validation checks required fields.

**Required Prompt Fields**:
- Task ID reference (e.g., "T008: Implement TaskService")
- Spec requirement reference (e.g., "Implements FR-001, FR-010")
- Acceptance criteria
- File path for output
- Request for full file with type hints and docstrings

### Decision 2: Task Size Granularity

**Options Considered**:
- A) Micro tasks (one function per task)
- B) Small-batch tasks (one module per task)
- C) Medium tasks (one feature component per task)

**Selected**: B - Small-batch tasks (one module per task)

**Tradeoffs**:
- ✅ Atomic enough for single prompt
- ✅ Produces complete, testable units
- ✅ Reduces task overhead
- ❌ May need splitting if module too complex

**Rationale**: Spec requires tasks be "atomic and testable" (FR-017) and "completable in single prompt" (SC-007). One module per task provides natural atomicity. If a task proves too large during implementation, split into subtasks (T005a, T005b) per FR-025/FR-026.

### Decision 3: Regeneration Policy

**Options Considered**:
- A) Full-file regeneration always
- B) Patch edits for small changes
- C) Hybrid (patches for typos, regeneration for logic)

**Selected**: A - Full-file regeneration always

**Tradeoffs**:
- ✅ Maintains prompt-to-code traceability
- ✅ Ensures consistency
- ✅ Prevents manual edit drift
- ❌ More overhead for small fixes

**Rationale**: Spec requires "regeneration over patching" (FR-015) and "prohibit manual code edits" (FR-006). Full-file regeneration ensures every line of code traces to a prompt. Emergency bypass (FR-022) is the only exception, requiring retroactive documentation.

### Decision 4: Traceability Mapping Format

**Options Considered**:
- A) ID tags in code comments (e.g., # Task: T008)
- B) Manifest file (traceability.json)
- C) PHR-based mapping (prompt → code relationship)
- D) Git commit messages with task IDs

**Selected**: C - PHR-based mapping + D - Git commit messages

**Tradeoffs**:
- ✅ PHRs capture full prompt-to-code relationship
- ✅ Git commits provide file-level traceability
- ✅ No code pollution with metadata
- ✅ Immutable audit trail
- ❌ Requires PHR discipline

**Rationale**: Spec requires "maintain traceability from code → task → plan → spec" (FR-010). PHRs capture the prompt (which references task ID and spec), the generated code, and metadata. Git commits link code changes to tasks via commit messages. No need for in-code tags that pollute source.

**Traceability Chain**:
```
Code file (src/services/task_service.py)
  ↓ (via git commit message)
Task ID (T008)
  ↓ (via tasks.md)
Plan section (Service Layer Operations)
  ↓ (via plan.md)
Spec requirements (FR-001, FR-010, FR-011)
  ↓ (via spec.md)
User story (US1: Create and View Tasks)
```

### Decision 5: Review Gate Enforcement

**Options Considered**:
- A) Per-phase gates (after each workflow stage)
- B) Final-only gate (at end of feature)
- C) Continuous validation (on every commit)

**Selected**: A - Per-phase gates (after each workflow stage)

**Tradeoffs**:
- ✅ Catches issues early
- ✅ Prevents cascading errors
- ✅ Clear stage boundaries
- ❌ More overhead

**Rationale**: Spec requires "review gates at each workflow stage" (FR-011). Gates after spec, plan, tasks, and code prevent downstream rework. Hybrid enforcement (FR-021): automated checks for objective criteria (file exists, format valid), manual review for subjective criteria (architecture soundness, requirement clarity).

**Gate Stages**:
1. **Spec Gate**: After spec.md created
2. **Plan Gate**: After plan.md created
3. **Task Gate**: After tasks.md created
4. **Code Gate**: After code generated

### Decision 6: Prompt Storage Format

**Options Considered**:
- A) Markdown files (human-readable)
- B) JSON/YAML (structured, machine-readable)
- C) Database (queryable)

**Selected**: A - Markdown files (PHR template format)

**Tradeoffs**:
- ✅ Human-readable
- ✅ Git-friendly (diffs work well)
- ✅ Supports YAML frontmatter for metadata
- ✅ Markdown body for prompt/response text
- ❌ Requires parsing for automation

**Rationale**: Spec requires "store all prompts in history/prompts/" (FR-008). PHR template uses markdown with YAML frontmatter, providing both human readability and structured metadata. Git tracks changes naturally. Automation can parse YAML frontmatter when needed.

### Decision 7: Emergency Bypass Documentation

**Options Considered**:
- A) Block all manual edits (no exceptions)
- B) Allow bypass, require immediate documentation
- C) Allow bypass, require retroactive documentation within 24 hours
- D) Allow bypass, retroactive documentation optional

**Selected**: C - Allow bypass with mandatory retroactive documentation

**Tradeoffs**:
- ✅ Handles critical production issues
- ✅ Maintains traceability (eventually)
- ✅ Pragmatic balance
- ❌ Risk of incomplete documentation

**Rationale**: Spec clarification allows "emergency bypass for critical issues with mandatory retroactive documentation" (FR-022). Critical production bugs can be fixed immediately via manual edit, but team MUST create spec/task/prompt afterward to restore traceability. Incomplete retroactive documentation is a workflow violation flagged in audits.

## Prompt Governance Framework

### Prompt Quality Requirements

All Claude Code prompts MUST include:

1. **Task Reference**: "T008: Implement TaskService class"
2. **Spec Reference**: "Implements FR-001, FR-010, FR-011"
3. **Acceptance Criteria**: "Service validates title ≤100 chars, description ≤500 chars"
4. **File Path**: "src/services/task_service.py"
5. **Output Format**: "Full file with type hints and Google-style docstrings"
6. **Constraints**: "Functions ≤25 lines, follow clean code principles"

### Prompt Template

```markdown
Task: [Task ID and description]
Spec Requirements: [FR-XXX, FR-YYY]
Acceptance Criteria:
- [Criterion 1]
- [Criterion 2]

Generate [file path] with the following:
- [Specific requirements]
- Type hints for all functions
- Google-style docstrings
- Functions ≤25 lines (document exceptions)
- [Any other constraints]

Output the complete file.
```

### Prompt Validation (Automated)

Automated checks before prompt execution:
- [ ] Task ID referenced
- [ ] Spec requirement(s) referenced
- [ ] File path specified
- [ ] Acceptance criteria listed
- [ ] Output format specified

### PHR Creation (Comprehensive)

Per FR-024, create PHR for ALL Claude Code interactions:
- Implementation prompts (code generation)
- Question prompts (clarifications)
- Exploratory prompts (investigation)
- Debugging prompts (issue diagnosis)

**PHR Template Fields** (from `.specify/templates/phr-template.prompt.md`):
- id, title, stage, date, surface, model
- feature, branch, user, command
- labels, links (spec, ticket, adr, pr)
- files (created/modified), tests (run/added)
- Prompt text (full, verbatim)
- Response text (concise summary)
- Outcome, evaluation notes

## Task Generation Method

### Task Categories

**Artifact Creation Tasks**:
- Create constitution.md
- Create spec.md for feature
- Create plan.md for feature
- Create tasks.md for feature

**Spec Validation Tasks**:
- Validate spec has no implementation details
- Validate spec requirements are testable
- Validate spec success criteria are measurable

**Prompt Template Tasks**:
- Define prompt template format
- Create prompt validation script
- Document prompt quality requirements

**Traceability Mapping Tasks**:
- Define traceability chain format
- Create traceability validation script
- Document audit trail requirements

**Review Gate Setup Tasks**:
- Define gate criteria for each stage
- Create automated validation scripts
- Document manual review checklist

**Audit Logging Tasks**:
- Define PHR template
- Create PHR generation script
- Document audit trail format

### Task Characteristics

Each task MUST include:
- **Spec Clause Reference**: Which FR-XXX it implements
- **Artifact Output**: What file(s) it produces
- **Acceptance Criteria**: How to verify completion
- **Regeneration Rule**: When/how to regenerate
- **Evidence Requirement**: What proves it's done

### Task Splitting Protocol

When task proves too large during implementation (FR-025):

1. **Identify split point**: Logical module/function boundary
2. **Create subtasks**: T005a, T005b, T005c
3. **Update tasks.md**: Add subtasks, mark original as split
4. **Maintain traceability**: Subtasks reference original T005 (FR-027)
5. **Document reason**: Why split was necessary

**Example**:
```markdown
- [ ] T005: Implement InMemoryTaskStore (SPLIT - see subtasks below)
  - [ ] T005a: Implement ID generation and storage initialization
  - [ ] T005b: Implement create and get operations
  - [ ] T005c: Implement update, delete, and toggle operations
```

## Review Gate Design

### Gate Stages and Criteria

**Spec Gate** (after spec.md created):

**Automated Checks**:
- [ ] File exists at `specs/###-feature/spec.md`
- [ ] Contains required sections (User Scenarios, Requirements, Success Criteria)
- [ ] No code snippets or implementation details detected
- [ ] All requirements have FR-XXX identifiers

**Manual Review**:
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] User stories have clear priorities
- [ ] Scope is clearly bounded

**Pass Criteria**: All automated checks pass + manual review approves

---

**Plan Gate** (after plan.md created):

**Automated Checks**:
- [ ] File exists at `specs/###-feature/plan.md`
- [ ] Contains architecture sketch
- [ ] Contains design decisions section
- [ ] References spec.md

**Manual Review**:
- [ ] Architecture aligns with clean code principles
- [ ] Design decisions are justified
- [ ] Module boundaries are clear
- [ ] Task decomposition strategy is sound

**Pass Criteria**: All automated checks pass + manual review approves

---

**Task Gate** (after tasks.md created):

**Automated Checks**:
- [ ] File exists at `specs/###-feature/tasks.md`
- [ ] All tasks have unique IDs (T001, T002, etc.)
- [ ] All tasks reference spec requirements
- [ ] Task dependencies are documented

**Manual Review**:
- [ ] Tasks are atomic (completable in single prompt)
- [ ] Tasks are testable
- [ ] All spec requirements covered by tasks
- [ ] Task order is logical

**Pass Criteria**: All automated checks pass + manual review approves

---

**Code Gate** (after code generated):

**Automated Checks**:
- [ ] All code files have corresponding PHRs
- [ ] Git history shows only Claude Code commits (or documented emergency bypass)
- [ ] No manual edits detected (git blame analysis)
- [ ] All files follow project structure

**Manual Review**:
- [ ] Code matches plan architecture
- [ ] Code implements spec requirements
- [ ] Clean code principles followed
- [ ] Traceability chain is complete

**Pass Criteria**: All automated checks pass + manual review approves

### Gate Documentation

Each gate pass/fail MUST be documented in:
- `specs/###-feature/checklists/[stage]-gate.md`

**Format**:
```markdown
# [Stage] Gate Review

**Date**: 2026-01-30
**Reviewer**: [Name/Agent]
**Status**: PASS / FAIL

## Automated Checks
- [x] Check 1: PASS
- [x] Check 2: PASS

## Manual Review
- [x] Criterion 1: PASS - [Notes]
- [x] Criterion 2: PASS - [Notes]

## Decision
PASS - Proceed to next stage

## Issues Identified
None / [List issues if FAIL]
```

## Traceability Mapping Method

### Traceability Chain

```
Code File
  ↓ (git commit message with task ID)
PHR (history/prompts/###-feature/NNN-*.prompt.md)
  ↓ (references task ID in frontmatter)
Task (tasks.md, line with task ID)
  ↓ (references spec requirements)
Plan Section (plan.md, section describing module)
  ↓ (references spec requirements)
Spec Requirement (spec.md, FR-XXX)
  ↓ (part of user story)
User Story (spec.md, US#)
```

### Validation Method

**Forward Trace** (Spec → Code):
1. Select spec requirement (e.g., FR-001)
2. Find tasks referencing FR-001 in tasks.md
3. Find PHRs referencing those task IDs
4. Find code files listed in PHR frontmatter
5. Verify code exists and implements requirement

**Backward Trace** (Code → Spec):
1. Select code file (e.g., src/services/task_service.py)
2. Find git commit that created/modified it
3. Extract task ID from commit message
4. Find task in tasks.md
5. Find spec requirements referenced by task
6. Verify code implements those requirements

### Traceability Audit Script

```bash
# Pseudo-code for traceability validation
for each code_file in src/**/*.py:
    commit = git log --follow code_file | head -1
    task_id = extract_task_id(commit.message)
    if not task_id:
        ERROR: "No task ID in commit for {code_file}"

    task = find_task(tasks.md, task_id)
    if not task:
        ERROR: "Task {task_id} not found in tasks.md"

    spec_refs = extract_spec_refs(task)
    if not spec_refs:
        ERROR: "Task {task_id} has no spec references"

    for spec_ref in spec_refs:
        requirement = find_requirement(spec.md, spec_ref)
        if not requirement:
            ERROR: "Requirement {spec_ref} not found in spec.md"

    print("✓ {code_file} → {task_id} → {spec_refs}")
```

## Compliance Validation Checklist

### Workflow Ordering Compliance

- [ ] Constitution exists before any specs (FR-001)
- [ ] Specs exist before plans (FR-002)
- [ ] Plans exist before tasks (FR-003)
- [ ] Tasks exist before code prompts (FR-004)

### Artifact Completeness

- [ ] Constitution.md exists with version number
- [ ] Each feature has spec.md, plan.md, tasks.md
- [ ] All code files have corresponding PHRs
- [ ] All significant decisions have ADRs (FR-019)

### Prompt Compliance

- [ ] All prompts reference task IDs (FR-007)
- [ ] All prompts reference spec requirements (FR-007)
- [ ] All prompts are deterministic (FR-018)
- [ ] PHRs exist for all interactions (FR-024)

### Code Provenance

- [ ] All code generated via Claude Code (FR-005)
- [ ] No manual edits (except documented emergency bypass) (FR-006)
- [ ] Git history shows Claude Code authorship (FR-020)
- [ ] Emergency bypasses have retroactive documentation (FR-022)

### Traceability Integrity

- [ ] All code files trace to tasks (FR-010)
- [ ] All tasks trace to spec requirements (FR-010)
- [ ] All spec requirements covered by tasks
- [ ] Traceability chain has no gaps

### Review Gate Passage

- [ ] Spec gate passed and documented (FR-011, FR-012)
- [ ] Plan gate passed and documented (FR-011, FR-012)
- [ ] Task gate passed and documented (FR-011, FR-012)
- [ ] Code gate passed and documented (FR-011, FR-012)

### Regeneration Compliance

- [ ] Code changes via regeneration, not patches (FR-015)
- [ ] Spec updated before regeneration when spec was wrong (FR-023)
- [ ] Regeneration history preserved in PHRs

### Task Management

- [ ] All tasks are atomic and testable (FR-017)
- [ ] Task splits follow naming convention (T005a, T005b) (FR-026)
- [ ] Subtasks maintain traceability to original (FR-027)

## Audit Strategy

### Audit Triggers

**Periodic Audits**:
- After each feature completion
- Before major releases
- Monthly compliance review

**Event-Driven Audits**:
- After emergency bypass usage
- When traceability gaps detected
- When gate failures occur

### Audit Procedure

1. **Artifact Inventory**: Verify all required artifacts exist
2. **Traceability Validation**: Run forward and backward traces
3. **Prompt Review**: Sample PHRs for quality and completeness
4. **Git History Analysis**: Verify Claude Code authorship
5. **Gate Documentation Review**: Verify all gates documented
6. **Emergency Bypass Review**: Verify retroactive documentation complete

### Audit Report Format

```markdown
# Workflow Compliance Audit

**Date**: 2026-01-30
**Auditor**: [Name]
**Scope**: [Feature(s) audited]

## Summary
- Total Features Audited: X
- Compliance Rate: Y%
- Critical Issues: Z

## Findings

### Compliant Areas
- [List areas passing all checks]

### Non-Compliant Areas
- [List violations with severity]

### Recommendations
- [Actions to improve compliance]

## Detailed Results
[Checklist results for each feature]
```

## Next Steps

1. **Run `/sp.tasks`** to generate task breakdown for implementing this workflow
2. **Create automation scripts** for gate validation
3. **Document workflow** in team onboarding materials
4. **Establish audit schedule** (monthly reviews)
5. **Train team** on prompt quality requirements
6. **Set up PHR templates** in `.specify/templates/`

## Notes

- This plan defines the workflow process, not application features
- Workflow applies to all features (001-todo-app, 003-clean-code, etc.)
- Hybrid gates balance automation with human judgment
- Emergency bypass provides pragmatic escape hatch while maintaining traceability
- Comprehensive PHR creation ensures complete audit trail
- Task splitting provides flexibility while preserving traceability
