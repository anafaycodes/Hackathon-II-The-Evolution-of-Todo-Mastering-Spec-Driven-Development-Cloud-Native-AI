---
id: 4
title: Generate Workflow Requirements Quality Checklist
stage: misc
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5
feature: 002-dev-workflow
branch: 002-dev-workflow
user: user
command: /sp.checklist
labels: ["workflow-requirements", "checklist", "validation", "pre-adoption-review"]
links:
  spec: specs/002-dev-workflow/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-dev-workflow/checklists/workflow-requirements.md
tests:
  - None (checklist generation - no tests)
---

## Prompt

/sp.checklist

Generate a custom checklist for the current feature based on user requirements for 002-dev-workflow

## Response snapshot

Successfully generated comprehensive requirements quality checklist for 002-dev-workflow (Spec-Driven Development Workflow).

**Checklist Details**:
- **File**: `specs/002-dev-workflow/checklists/workflow-requirements.md`
- **Total Items**: 165 checklist items
- **Traceability Coverage**: 132 items with spec references (80.0%)

**Focus Areas** (user-selected):
1. Workflow Stage Requirements (stage ordering, gates, transitions) - 42 items
2. Traceability Requirements (mapping, documentation, audit) - 38 items
3. Prompt & PHR Requirements (structure, creation, storage) - 40 items
4. Exception Handling Requirements (bypass, splitting, updates) - 45 items

**Usage Context**: Pre-adoption review (validate workflow before rollout)

**Depth Level**: Standard (primary flows + common exceptions)

**Checklist Structure**:
1. **Requirement Completeness** (58 items) - Are all necessary workflow requirements documented?
2. **Requirement Clarity** (42 items) - Are workflow requirements specific and unambiguous?
3. **Requirement Consistency** (28 items) - Do workflow requirements align without conflicts?
4. **Acceptance Criteria Quality** - Are success criteria measurable?
5. **Scenario Coverage** (25 items) - Are all workflow flows/cases addressed?
6. **Edge Case Coverage** (12 items) - Are workflow boundary conditions defined?
7. **Non-Functional Requirements** - Process performance, usability, reliability, scalability
8. **Dependencies & Assumptions** - Are they documented and validated?
9. **Ambiguities & Conflicts** - What needs clarification in workflow?

**Key Checklist Characteristics**:
- Tests workflow requirements quality, NOT workflow implementation
- Question format: "Are [workflow requirements] defined/specified/documented?"
- Focus on completeness, clarity, consistency, measurability, coverage
- References spec sections for traceability
- Identifies gaps, ambiguities, and conflicts in workflow requirements

**Sample Items**:
- "Are stage entry criteria specified for each workflow stage? [Gap]"
- "Is 'hybrid gate enforcement' clearly defined with automation vs manual boundaries? [Ambiguity, Spec §FR-021]"
- "Are traceability mapping requirements complete (code → task → plan → spec)? [Completeness, Spec §FR-010]"
- "Is 'significant prompt' defined with specific criteria? [Clarity, Spec §FR-024]"
- "Are emergency bypass trigger criteria defined? [Completeness, Spec §FR-022]"
- "Are requirements defined for recovering from spec-code mismatches? [Coverage, Spec Clarifications]"

**Quality Dimension Distribution**:
- Completeness: 58 items (35.2%)
- Clarity: 42 items (25.5%)
- Consistency: 28 items (17.0%)
- Coverage: 25 items (15.2%)
- Edge Cases: 12 items (7.3%)

**Recommended Review Order**:
1. Requirement Completeness (identify workflow gaps)
2. Requirement Clarity (resolve process ambiguities)
3. Scenario Coverage (ensure all flows covered)
4. Requirement Consistency (align workflow requirements)
5. Exception Handling Coverage (validate bypass, splitting, updates)
6. Acceptance Criteria Quality (ensure measurability)

## Outcome

- ✅ Impact: Comprehensive workflow requirements quality checklist created with 165 items covering workflow stages, traceability, prompts/PHRs, and exception handling. Checklist enables pre-adoption review to identify gaps, ambiguities, and conflicts in workflow spec before team rollout.
- 🧪 Tests: None (checklist is for testing workflow requirements quality, not workflow implementation)
- 📁 Files: 1 file created (workflow-requirements.md)
- 🔁 Next prompts: Use checklist during pre-adoption review to validate workflow requirements completeness and clarity. Address identified gaps and ambiguities by updating spec.md. Consider pilot testing workflow with small feature to validate requirements in practice.
- 🧠 Reflection: Checklist successfully focuses on workflow requirements quality (completeness, clarity, consistency) rather than workflow execution verification. High traceability coverage (80.0%) enables efficient spec review. Standard depth level provides good balance between thoroughness and practicality for pre-adoption review context. Exception handling coverage (45 items) addresses critical workflow edge cases like emergency bypass and task splitting.

## Evaluation notes (flywheel)

- Failure modes observed: None - checklist generation completed successfully
- Graders run and results (PASS/FAIL): Requirements focus: PASS (all items test workflow requirements, not implementation), Traceability: PASS (80.0% coverage meets 80% minimum), Coverage: PASS (all 4 focus areas addressed with balanced distribution), Depth: PASS (standard depth with exception handling included)
- Prompt variant (if applicable): Standard /sp.checklist workflow with clarifying questions for focus areas, usage context, and depth level
- Next experiment (smallest change to try): Monitor checklist usage during pre-adoption review to identify if any critical workflow requirement quality dimensions are missing. Consider adding items for workflow tooling requirements (automation, validation scripts) if team needs them.
