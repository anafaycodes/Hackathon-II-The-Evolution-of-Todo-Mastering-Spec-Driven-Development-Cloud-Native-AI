---
id: 5
title: Generate Task Breakdown for Dev Workflow
stage: tasks
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5
feature: 002-dev-workflow
branch: 002-dev-workflow
user: user
command: /sp.tasks
labels: ["task-generation", "workflow-implementation", "meta-feature", "documentation"]
links:
  spec: specs/002-dev-workflow/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-dev-workflow/tasks.md
tests:
  - None (workflow documentation - no tests)
---

## Prompt

/sp.tasks

Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts for 002-dev-workflow

## Response snapshot

Successfully generated comprehensive task breakdown for 002-dev-workflow (Spec-Driven Development Workflow).

**Tasks File**: `specs/002-dev-workflow/tasks.md`

**Total Tasks**: 30 tasks organized by workflow stage

**Task Distribution**:
- Phase 1 (Setup): 2 tasks - Workflow infrastructure and directory structure
- Phase 2 (Foundational): 2 tasks - Core templates (constitution, PHR) that block all workflow stages
- Phase 3 (User Story 1 - P1 MVP): 4 tasks - Constitution and Specification Creation
- Phase 4 (User Story 2 - P2): 6 tasks - Implementation Planning and Task Breakdown
- Phase 5 (User Story 3 - P3): 5 tasks - Claude Code Prompt-Driven Implementation
- Phase 6 (User Story 4 - P4): 6 tasks - Artifact Traceability and Review Gates
- Phase 7 (Polish): 5 tasks - Workflow validation and integration documentation

**Parallelizable Tasks**: 10 tasks marked with [P]

**MVP Scope**: Phases 1-3 (T001-T008) = 8 tasks for minimum viable workflow

**Meta-Feature Characteristics**:
- This feature implements the WORKFLOW ITSELF through templates, guides, and documentation
- No application code generated - all tasks create documentation artifacts
- Enables the spec-driven development process for all other features
- Self-referential: uses the workflow to implement the workflow

**User Story Organization**:
- US1 (P1): Constitution and spec creation capability
- US2 (P2): Planning and task breakdown capability
- US3 (P3): Code generation and PHR capture capability
- US4 (P4): Traceability and gate validation capability

**Artifact Types Created**:
- **Templates** (8 files): constitution, spec, plan, tasks, PHR, review gate checklist, ADR, workflow validation
- **Guides** (11 files): constitution creation, spec creation, planning, task breakdown, prompt writing, code generation, regeneration, PHR creation, emergency bypass, gate enforcement, audit process
- **Checklists** (4 files): spec validation, plan validation, task validation, workflow validation
- **Infrastructure** (2 files): README, directory structure

**Key Design Decisions Applied**:
- Hybrid gate enforcement (automated + manual review)
- Emergency bypass with retroactive documentation
- PHRs for all Claude Code interactions (comprehensive audit trail)
- Task splitting allowed with subtask naming (T005a, T005b)
- Regeneration over patching (update spec if spec wrong, refine prompt if code wrong)

**Independent Test Criteria**:
- US1: Verify constitution.md and spec.md can be created using templates and guides
- US2: Verify plan.md and tasks.md can be created with architecture decisions and atomic tasks
- US3: Verify code can be generated via prompts with PHR capture in history/prompts/
- US4: Verify code artifacts can be traced back through task → plan → spec chain

**Execution Strategy**:
- MVP First: Complete Phases 1-3 for constitution and spec creation capability
- Incremental Delivery: Add one workflow stage at a time, validate independently
- Parallel Team: After Foundational phase, multiple workflow stages can be documented in parallel

**Format Compliance**:
- All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- Task IDs sequential (T001-T030)
- [P] markers for parallelizable tasks (10 tasks)
- [US1]-[US4] labels for user story tasks
- Exact file paths included in all descriptions

## Outcome

- ✅ Impact: Complete task breakdown created with 30 tasks organized by workflow stage. Each stage is independently implementable through documentation and templates. MVP scope clearly defined (8 tasks for constitution and spec creation). Meta-feature structure enables the workflow to govern itself.
- 🧪 Tests: None (workflow documentation - validation through usage, not automated tests)
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: Execute tasks sequentially starting with T001 (directory structure). Use /sp.implement to execute all tasks, or execute individual tasks via Claude Code prompts. After US1 complete, validate constitution and spec creation process before proceeding to US2-US4.
- 🧠 Reflection: Task breakdown successfully maps workflow stages to documentation tasks. Foundational phase (core templates) correctly identified as blocking all workflow stages. Each user story phase creates complete documentation for one workflow stage. MVP scope (US1) enables basic constitution and spec creation. Meta-feature nature requires careful attention to self-consistency - the workflow documentation must follow the workflow it defines.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully
- Graders run and results (PASS/FAIL): Format compliance: PASS (all tasks follow checklist format), User story organization: PASS (each workflow stage independently documentable), Dependency ordering: PASS (foundational templates block workflow stages), MVP identification: PASS (US1 clearly marked as MVP), Meta-feature handling: PASS (tasks create documentation, not code)
- Prompt variant (if applicable): Standard /sp.tasks workflow adapted for meta-feature (workflow implementation through documentation)
- Next experiment (smallest change to try): Monitor task execution to validate that documentation tasks are sufficiently detailed. Verify that templates include enough examples and guides provide enough context for teams to follow the workflow without additional clarification.
