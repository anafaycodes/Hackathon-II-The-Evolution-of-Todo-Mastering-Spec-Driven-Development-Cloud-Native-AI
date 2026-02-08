# Tasks: Spec-Driven Development Workflow

**Input**: Design documents from `/specs/002-dev-workflow/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: Tests are NOT included in this task list (process validation, not code testing)

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each workflow stage.

**Note**: This feature implements the WORKFLOW ITSELF through templates, documentation, and validation tools - not application code.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Templates**: `.specify/templates/` for reusable templates
- **Documentation**: `.specify/docs/` for workflow documentation
- **Scripts**: `.specify/scripts/` for automation tools
- **Memory**: `.specify/memory/` for constitution and persistent artifacts

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize workflow infrastructure and directory structure

- [ ] T001 Create workflow directory structure with .specify/templates/, .specify/docs/, .specify/scripts/, .specify/memory/, specs/, and history/ directories
- [ ] T002 [P] Create README.md in .specify/ explaining workflow structure and purpose

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core templates and documentation that MUST be complete before ANY user story workflow can be implemented

**⚠️ CRITICAL**: No workflow stage can be executed until this phase is complete

- [ ] T003 [P] Create constitution template in .specify/templates/constitution-template.md with sections for principles, constraints, quality standards, and governance rules
- [ ] T004 [P] Create PHR template in .specify/templates/phr-template.prompt.md with YAML frontmatter for metadata and sections for prompt text, response, outcome, and evaluation

**Checkpoint**: Foundation ready - workflow stage implementation can now begin

---

## Phase 3: User Story 1 - Constitution and Specification Creation (Priority: P1) 🎯 MVP

**Goal**: Enable teams to establish project principles and create detailed specifications before any code is written

**Independent Test**: Verify that constitution.md can be created with complete principles, and that spec.md files can be created with user stories, requirements, and success criteria before any implementation planning

**Spec Requirements**: FR-001, FR-002, FR-016

### Implementation for User Story 1

- [ ] T005 [P] [US1] Create spec template in .specify/templates/spec-template.md with sections for clarifications, user scenarios, requirements, success criteria, constraints, and out-of-scope items
- [ ] T006 [P] [US1] Create constitution creation guide in .specify/docs/constitution-guide.md explaining how to define principles, establish constraints, and document governance rules
- [ ] T007 [US1] Create spec creation guide in .specify/docs/spec-guide.md explaining how to write user stories with priorities, define requirements, establish success criteria, and avoid implementation details (depends on T005)
- [ ] T008 [US1] Create spec validation checklist in .specify/templates/spec-validation-checklist.md with criteria for testable requirements, no implementation details, unique feature branches, and complete acceptance scenarios (depends on T005)

**Checkpoint**: At this point, User Story 1 should be fully functional - teams can create constitutions and specifications following templates and guides

---

## Phase 4: User Story 2 - Implementation Planning and Task Breakdown (Priority: P2)

**Goal**: Enable teams to create detailed implementation plans and atomic task lists from specifications

**Independent Test**: Verify that plan.md files can be created with architecture decisions and module structure, and tasks.md files can be created with atomic, testable tasks that reference spec requirements

**Spec Requirements**: FR-003, FR-004, FR-017, FR-025, FR-026, FR-027

### Implementation for User Story 2

- [ ] T009 [P] [US2] Create plan template in .specify/templates/plan-template.md with sections for summary, architecture sketch, technical context, design decisions, and task decomposition strategy
- [ ] T010 [P] [US2] Create tasks template in .specify/templates/tasks-template.md with phase structure (Setup, Foundational, User Stories, Polish), task format guidelines, and dependency documentation
- [ ] T011 [US2] Create planning guide in .specify/docs/planning-guide.md explaining how to make architecture decisions, define module structure, and map requirements to implementation (depends on T009)
- [ ] T012 [US2] Create task breakdown guide in .specify/docs/task-breakdown-guide.md explaining how to create atomic tasks, assign task IDs, map tasks to spec requirements, define dependencies, and handle task splitting (depends on T010)
- [ ] T013 [US2] Create plan validation checklist in .specify/templates/plan-validation-checklist.md with criteria for architecture decisions documented, module structure defined, and all spec requirements mapped (depends on T009)
- [ ] T014 [US2] Create task validation checklist in .specify/templates/task-validation-checklist.md with criteria for atomic tasks, unique IDs, spec requirement references, and clear acceptance criteria (depends on T010)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - teams can create constitutions, specs, plans, and task breakdowns

---

## Phase 5: User Story 3 - Claude Code Prompt-Driven Implementation (Priority: P3)

**Goal**: Enable teams to generate all code exclusively through Claude Code prompts that reference specs and tasks

**Independent Test**: Verify that code files have corresponding prompts in history/prompts/, and that no manual edits exist (via git history analysis showing only Claude Code commits)

**Spec Requirements**: FR-005, FR-006, FR-007, FR-008, FR-009, FR-015, FR-018, FR-020, FR-022, FR-023, FR-024

### Implementation for User Story 3

- [ ] T015 [P] [US3] Create prompt writing guide in .specify/docs/prompt-guide.md explaining how to reference task IDs and spec sections, include acceptance criteria, request full file outputs, and ensure deterministic prompts
- [ ] T016 [P] [US3] Create code generation guide in .specify/docs/code-generation-guide.md explaining Claude Code usage, prompt execution, output capture, and commit practices
- [ ] T017 [US3] Create regeneration guide in .specify/docs/regeneration-guide.md explaining when to regenerate vs patch, how to refine prompts, when to update specs, and how to maintain traceability (depends on T015, T016)
- [ ] T018 [US3] Create PHR creation guide in .specify/docs/phr-guide.md explaining PHR structure, when to create PHRs (all Claude Code interactions), how to route PHRs to correct directories, and how to fill metadata (depends on T004)
- [ ] T019 [US3] Create emergency bypass documentation in .specify/docs/emergency-bypass.md explaining bypass criteria, retroactive documentation requirements, and compliance restoration process

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - teams can execute the full workflow from constitution to code generation

---

## Phase 6: User Story 4 - Artifact Traceability and Review Gates (Priority: P4)

**Goal**: Enable teams to map every code artifact back to specs, plans, and tasks through review gates

**Independent Test**: Select any code file and trace it back through task ID → plan section → spec requirement, and verify that all review gates have documented pass/fail results

**Spec Requirements**: FR-010, FR-011, FR-012, FR-013, FR-014, FR-019, FR-021

### Implementation for User Story 4

- [ ] T020 [P] [US4] Create traceability validation guide in .specify/docs/traceability-guide.md explaining how to map code → task → plan → spec, how to validate traceability chains, and how to audit for gaps
- [ ] T021 [P] [US4] Create review gate checklist template in .specify/templates/review-gate-checklist.md with sections for each workflow stage (spec, plan, task, code) and hybrid validation criteria (automated + manual)
- [ ] T022 [US4] Create gate enforcement guide in .specify/docs/gate-enforcement-guide.md explaining hybrid approach (automated for objective criteria, manual for subjective), gate pass/fail documentation, and remediation process (depends on T021)
- [ ] T023 [US4] Create audit process documentation in .specify/docs/audit-process.md explaining how to perform traceability audits, validate no manual code edits, check PHR completeness, and verify gate compliance (depends on T020)
- [ ] T024 [US4] Create ADR template in .specify/templates/adr-template.md with sections for decision context, options considered, selected option, tradeoffs, and rationale
- [ ] T025 [US4] Create ADR creation guide in .specify/docs/adr-guide.md explaining when to create ADRs (architecturally significant decisions), how to document decisions, and how to link ADRs to specs/plans (depends on T024)

**Checkpoint**: All user stories should now be independently functional - full workflow with traceability and gates operational

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Workflow validation, integration documentation, and quality assurance

- [ ] T026 Create workflow overview documentation in .specify/docs/workflow-overview.md explaining the complete workflow from constitution to code, stage dependencies, and best practices
- [ ] T027 Create quick reference guide in .specify/docs/quick-reference.md with common commands, template locations, and troubleshooting tips
- [ ] T028 Validate all templates are complete and internally consistent (no placeholder text, all sections defined, examples provided)
- [ ] T029 Validate all guides reference correct template paths and follow consistent structure
- [ ] T030 Create workflow validation checklist in .specify/templates/workflow-validation-checklist.md for verifying complete workflow implementation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1 and US2 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Validates US1-US3 but independently testable

### Within Each User Story

- Templates before guides (guides reference templates)
- Guides before checklists (checklists validate guides)
- Core documentation before integration documentation
- Story complete before moving to next priority

### Parallel Opportunities

- T002 can run in parallel with T001 (different files)
- T003 and T004 can run in parallel (different templates)
- Within each user story, templates and guides can often run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch US1 tasks in parallel:
Task T005: "Create spec template in .specify/templates/spec-template.md..."
Task T006: "Create constitution creation guide in .specify/docs/constitution-guide.md..."
# Wait for T005 to complete, then:
Task T007: "Create spec creation guide in .specify/docs/spec-guide.md..." (depends on T005)
Task T008: "Create spec validation checklist..." (depends on T005)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004) - CRITICAL
3. Complete Phase 3: User Story 1 (T005-T008)
4. **STOP and VALIDATE**: Test constitution and spec creation process
5. Demo workflow stage 1 (constitution and spec creation)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T005-T008) → Test → Demo (MVP: Constitution and Spec creation!)
3. Add User Story 2 (T009-T014) → Test → Demo (Now with planning and tasks!)
4. Add User Story 3 (T015-T019) → Test → Demo (Now with code generation!)
5. Add User Story 4 (T020-T025) → Test → Demo (Full workflow with traceability!)
6. Each story adds workflow capability without breaking previous stages

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T004)
2. Once Foundational is done:
   - Developer A: User Story 1 (T005-T008) - MUST complete first for MVP
   - After US1 complete, developers can work in parallel:
     - Developer A: User Story 2 (T009-T014)
     - Developer B: User Story 3 (T015-T019)
     - Developer C: User Story 4 (T020-T025)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 30

**By Phase**:
- Phase 1 (Setup): 2 tasks
- Phase 2 (Foundational): 2 tasks
- Phase 3 (User Story 1 - P1 MVP): 4 tasks
- Phase 4 (User Story 2 - P2): 6 tasks
- Phase 5 (User Story 3 - P3): 5 tasks
- Phase 6 (User Story 4 - P4): 6 tasks
- Phase 7 (Polish): 5 tasks

**Parallelizable Tasks**: 10 tasks marked with [P]

**MVP Scope**: Phases 1-3 (T001-T008) = 8 tasks

**Independent Test Criteria**:
- US1: Can create constitution and specs with templates and guides
- US2: Can create plans and tasks with templates and guides
- US3: Can generate code via prompts with PHR capture
- US4: Can trace artifacts and validate gates

**Artifact Types Created**:
- Templates: 8 files (.md templates for constitution, spec, plan, tasks, PHR, checklist, ADR, validation)
- Guides: 11 files (documentation for each workflow stage)
- Checklists: 4 files (validation criteria for specs, plans, tasks, workflow)
- Infrastructure: 2 files (README, directory structure)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This feature implements the WORKFLOW through documentation and templates, not application code
- All tasks create documentation, templates, or guides - no code generation
- Focus on clear, actionable documentation that teams can follow
- Templates should include examples and placeholder text
- Guides should explain WHY as well as HOW
- Validation checklists should have objective, measurable criteria
