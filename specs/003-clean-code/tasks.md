# Tasks: Clean Code Principles and Python Project Structure

**Input**: Design documents from `/specs/003-clean-code/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/ (complete), quickstart.md (complete)

**Tests**: Tests are NOT included in this task list (validation tools, not code testing)

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each clean code principle.

**Note**: This feature establishes CLEAN CODE STANDARDS through validation tools, documentation, and enforcement mechanisms - not application code.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Validation Tools**: `.specify/validation/` for automated checkers
- **Documentation**: `.specify/docs/clean-code/` for standards documentation
- **Checklists**: `.specify/checklists/` for review checklists
- **Examples**: `.specify/examples/` for code examples

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize clean code validation infrastructure and directory structure

- [ ] T001 Create clean code validation directory structure with .specify/validation/, .specify/docs/clean-code/, .specify/checklists/, and .specify/examples/ directories
- [ ] T002 [P] Create clean code standards overview in .specify/docs/clean-code/README.md explaining the 5-layer architecture, clean code principles, and validation approach

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core validation tools and documentation that MUST be complete before ANY user story validation can be implemented

**⚠️ CRITICAL**: No clean code validation can be performed until this phase is complete

- [ ] T003 [P] Create layer definition reference in .specify/docs/clean-code/layer-definitions.md documenting the 5 layers (CLI, Service, Domain, Storage, Utilities) with responsibilities, allowed dependencies, and forbidden dependencies
- [ ] T004 [P] Create clean code glossary in .specify/docs/clean-code/glossary.md defining terms like "single responsibility", "atomic function", "layer boundary", "dependency direction", and "circular import"

**Checkpoint**: Foundation ready - clean code validation implementation can now begin

---

## Phase 3: User Story 1 - Modular Layered Architecture (Priority: P1) 🎯 MVP

**Goal**: Enable teams to validate that codebase is organized into clear layers with single responsibilities and proper dependency direction

**Independent Test**: Verify that validation tools can check src/ directory structure, detect layer boundary violations, and validate dependency direction

**Spec Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-033, FR-034, FR-035, FR-036, FR-037, FR-038, FR-039, FR-040, FR-042

### Implementation for User Story 1

- [ ] T005 [P] [US1] Create directory structure validator script in .specify/validation/check_structure.py that verifies src/ contains cli/, services/, domain/, storage/, utilities/ subdirectories with __init__.py files
- [ ] T006 [P] [US1] Create dependency direction validator script in .specify/validation/check_dependencies.py that analyzes imports and validates CLI → Services → Domain, Services → Storage → Domain, all → Utilities dependency rules
- [ ] T007 [P] [US1] Create circular import detector script in .specify/validation/check_circular_imports.py that builds import graph and detects cycles
- [ ] T008 [US1] Create layer boundary validation guide in .specify/docs/clean-code/layer-boundaries.md explaining allowed and forbidden imports for each layer with examples (depends on T003)
- [ ] T009 [US1] Create architecture validation checklist in .specify/checklists/architecture-checklist.md with criteria for layer separation, dependency direction, and no circular imports (depends on T003)

**Checkpoint**: At this point, User Story 1 should be fully functional - teams can validate layered architecture with automated tools

---

## Phase 4: User Story 2 - Single Responsibility and Small Functions (Priority: P2)

**Goal**: Enable teams to validate that modules, classes, and functions have single responsibilities and stay small (≤25 lines)

**Independent Test**: Verify that validation tools can count function lines, detect multi-purpose functions, and validate nesting depth

**Spec Requirements**: FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-043

### Implementation for User Story 2

- [ ] T010 [P] [US2] Create function length validator script in .specify/validation/check_function_length.py that counts lines per function (excluding docstrings and comments), validates ≤25 lines, and detects documented exceptions
- [ ] T011 [P] [US2] Create nesting depth validator script in .specify/validation/check_nesting_depth.py that analyzes control flow and validates nesting depth ≤3 levels
- [ ] T012 [P] [US2] Create file length validator script in .specify/validation/check_file_length.py that validates files ≤300 lines
- [ ] T013 [US2] Create single responsibility guide in .specify/docs/clean-code/single-responsibility.md explaining how to identify single responsibility, when to split functions, and how to document exceptions (depends on T004)
- [ ] T014 [US2] Create function design checklist in .specify/checklists/function-design-checklist.md with criteria for function length, single responsibility, nesting depth, and explicit return values (depends on T004)
- [ ] T015 [US2] Create code examples in .specify/examples/single-responsibility-examples.py demonstrating good and bad examples of single responsibility, function length, and nesting depth

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - teams can validate architecture and function design

---

## Phase 5: User Story 3 - Explicit Naming and Type Hints (Priority: P3)

**Goal**: Enable teams to validate that functions, classes, and variables have descriptive names with complete type hints

**Independent Test**: Verify that validation tools can detect missing type hints, generic variable names, and naming convention violations

**Spec Requirements**: FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023

### Implementation for User Story 3

- [ ] T016 [P] [US3] Create type hint validator script in .specify/validation/check_type_hints.py that verifies all public functions have parameter and return type hints
- [ ] T017 [P] [US3] Create naming convention validator script in .specify/validation/check_naming.py that validates function names use verbs (snake_case), class names use nouns (PascalCase), constants use UPPER_SNAKE_CASE, and detects prohibited generic names (data, tmp, util, handle)
- [ ] T018 [US3] Create naming standards guide in .specify/docs/clean-code/naming-standards.md explaining verb-based function names, noun-based class names, descriptive variable names, and prohibited generic names with examples (depends on T004)
- [ ] T019 [US3] Create type hints guide in .specify/docs/clean-code/type-hints-guide.md explaining Python type hint syntax, when to use Optional, Union, and complex types, and benefits of type safety
- [ ] T020 [US3] Create naming and types checklist in .specify/checklists/naming-types-checklist.md with criteria for naming conventions, type hint completeness, and no generic names (depends on T004)
- [ ] T021 [US3] Create code examples in .specify/examples/naming-type-hints-examples.py demonstrating good and bad examples of naming conventions and type hints

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - teams can validate architecture, function design, and naming/types

---

## Phase 6: User Story 4 - Documentation and Dependency Management (Priority: P4)

**Goal**: Enable teams to validate that public functions have docstrings and dependencies follow proper direction rules

**Independent Test**: Verify that validation tools can detect missing docstrings, validate docstring format (Google style), and confirm dependency direction compliance

**Spec Requirements**: FR-024, FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-041

### Implementation for User Story 4

- [ ] T022 [P] [US4] Create docstring validator script in .specify/validation/check_docstrings.py that verifies all public functions and classes have Google-style docstrings with Args, Returns, and Raises sections
- [ ] T023 [P] [US4] Create import validator script in .specify/validation/check_imports.py that validates no wildcard imports (except utilities.constants), no unused imports, and imports organized (stdlib, third-party, local)
- [ ] T024 [US4] Create docstring standards guide in .specify/docs/clean-code/docstring-standards.md explaining Google-style docstring format, required sections (Args, Returns, Raises), and examples (depends on T004)
- [ ] T025 [US4] Create dependency management guide in .specify/docs/clean-code/dependency-management.md explaining dependency direction rules, how to avoid circular imports, and import organization best practices (depends on T003, T006)
- [ ] T026 [US4] Create documentation checklist in .specify/checklists/documentation-checklist.md with criteria for docstring presence, docstring format, and import organization (depends on T004)
- [ ] T027 [US4] Create code examples in .specify/examples/docstring-examples.py demonstrating good and bad examples of Google-style docstrings

**Checkpoint**: All user stories should now be independently functional - full clean code validation operational

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Integration, master validation script, and quality assurance

- [ ] T028 Create master validation runner script in .specify/validation/run_all_checks.py that executes all validation scripts (structure, dependencies, circular imports, function length, nesting depth, file length, type hints, naming, docstrings, imports) and generates comprehensive report
- [ ] T029 Create validation results template in .specify/validation/validation-report-template.md for documenting validation results with pass/fail counts, violations list, and remediation guidance
- [ ] T030 Create clean code quick reference in .specify/docs/clean-code/quick-reference.md with common validation commands, checklist locations, and troubleshooting tips
- [ ] T031 Validate all validation scripts work correctly by running them on sample code with known violations and verifying correct detection
- [ ] T032 Create clean code enforcement guide in .specify/docs/clean-code/enforcement-guide.md explaining when to run validations (pre-commit, PR review, CI/CD), how to interpret results, and remediation strategies

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but builds on architecture concepts
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1 and US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Extends US1 (dependency validation) but independently testable

### Within Each User Story

- Validation scripts before guides (guides explain what scripts check)
- Guides before checklists (checklists reference guides)
- Core validation before examples
- Story complete before moving to next priority

### Parallel Opportunities

- T002 can run in parallel with T001 (different files)
- T003 and T004 can run in parallel (different documentation)
- Within each user story, validation scripts can often run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch US1 tasks in parallel:
Task T005: "Create directory structure validator script..."
Task T006: "Create dependency direction validator script..."
Task T007: "Create circular import detector script..."
# Wait for T003 to complete (from Foundational), then:
Task T008: "Create layer boundary validation guide..." (depends on T003)
Task T009: "Create architecture validation checklist..." (depends on T003)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004) - CRITICAL
3. Complete Phase 3: User Story 1 (T005-T009)
4. **STOP and VALIDATE**: Test architecture validation tools on sample code
5. Demo clean code validation stage 1 (architecture validation)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T005-T009) → Test → Demo (MVP: Architecture validation!)
3. Add User Story 2 (T010-T015) → Test → Demo (Function design validation!)
4. Add User Story 3 (T016-T021) → Test → Demo (Naming and types validation!)
5. Add User Story 4 (T022-T027) → Test → Demo (Documentation validation!)
6. Each story adds validation capability without breaking previous checks

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T004)
2. Once Foundational is done:
   - Developer A: User Story 1 (T005-T009) - MUST complete first for MVP
   - After US1 complete, developers can work in parallel:
     - Developer A: User Story 2 (T010-T015)
     - Developer B: User Story 3 (T016-T021)
     - Developer C: User Story 4 (T022-T027)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 32

**By Phase**:
- Phase 1 (Setup): 2 tasks
- Phase 2 (Foundational): 2 tasks
- Phase 3 (User Story 1 - P1 MVP): 5 tasks
- Phase 4 (User Story 2 - P2): 6 tasks
- Phase 5 (User Story 3 - P3): 6 tasks
- Phase 6 (User Story 4 - P4): 6 tasks
- Phase 7 (Polish): 5 tasks

**Parallelizable Tasks**: 11 tasks marked with [P]

**MVP Scope**: Phases 1-3 (T001-T009) = 9 tasks

**Independent Test Criteria**:
- US1: Can validate layered architecture with automated tools
- US2: Can validate function design (length, responsibility, nesting)
- US3: Can validate naming conventions and type hints
- US4: Can validate documentation and dependency direction

**Artifact Types Created**:
- **Validation Scripts** (9 files): Python scripts for automated checking
- **Guides** (7 files): Documentation explaining clean code standards
- **Checklists** (4 files): Review checklists for manual validation
- **Examples** (3 files): Code examples demonstrating good/bad practices
- **Infrastructure** (3 files): Master runner, report template, quick reference

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This feature establishes CLEAN CODE VALIDATION through scripts and documentation, not application code
- All validation scripts should be Python-based for consistency
- Scripts should provide clear, actionable error messages
- Guides should explain WHY as well as HOW
- Examples should show both good and bad code
- Validation should be automatable for CI/CD integration
