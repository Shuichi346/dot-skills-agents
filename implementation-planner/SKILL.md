---
name: implementation-planner
description: Create precise, self-contained implementation plans for programming and software-engineering tasks, written for literal execution by AI coding agents such as Codex, Claude Code, Cursor Agent, or other LLM agents, and save the completed specification document as PLANS.md in the working directory. Use when the user asks for a plan, implementation plan, technical plan, project roadmap, task breakdown, phased execution plan, refactor plan, migration plan, or agent-ready specification before coding; includes mandatory clarification, research triggers, explicit agent roles, step dependencies, observable verification, phase gates, risk/recovery notes, and living-document progress sections.
---

# Implementation Planner

## Overview

Produce a specification document for an AI coding agent to execute. Do not implement code while using this skill unless the user separately asks for implementation after the plan.

Write as if the executing agent will follow the plan literally with no memory of the conversation. Eliminate ambiguity, use exact identifiers, and anchor verification on observable behavior.

## Required Output File

Save the completed plan as `PLANS.md` in the current working directory. A chat-only plan is incomplete unless the user explicitly requests chat output only.

If `PLANS.md` already exists, read it before writing:

- If it describes the same task, update it in place and preserve relevant living-document history.
- If it describes an unrelated task, ask before overwriting it.
- If the user explicitly asks for a new plan, replace the file with the new completed plan.

After saving, briefly report the absolute path to `PLANS.md` and whether any assumptions still need user review.

## Planning Workflow

### 1. Clarify Before Planning

Before writing a plan, classify the available information:

- **Explicit**: Stated by the user.
- **Inferable**: Reasonably deduced from the repository, task context, or conventional project structure.
- **Unknown**: Not stated, not inferable, and required for a correct plan.

Ask focused questions when an unknown would force a guess about any agent-executed detail, including:

- Functional behavior: inputs, outputs, edge cases, domain rules.
- Technical context: language, framework, runtime, package manager, project structure, existing conventions, shared utilities, database or ORM.
- Scope boundaries: new feature vs modification vs refactor, out-of-scope work, CI/CD expectations.
- Integration points: external APIs, authentication, authorization, permissions, latency, throughput, memory limits.
- Deployment: runtime environment, configuration, migrations, rollback needs.
- Agent environment: whether agents can run commands, whether they have full repository access, whether specialized agents will be used.

When asking questions:

- Group questions by category.
- Number every question.
- State why the answer matters.
- Include a default assumption only when it is safe to proceed if the user does not correct it.
- Stop after asking; do not produce a speculative plan.

Proceed directly to planning only when the request is complete enough, or when remaining unknowns can be listed as safe assumptions at the top of the plan.

### 2. Research When Accuracy Depends On It

Use web or documentation search before finalizing the plan when:

- The plan depends on a library API, CLI flag, framework behavior, or external service contract that is not already verified.
- The plan targets version-specific behavior or a modern toolchain whose behavior may have changed.
- A step would otherwise be Medium or High risk because of technical uncertainty that research can resolve.
- The technology is unfamiliar or niche.

Embed researched facts directly in the plan in your own words. Citations are useful provenance, but never make the executing agent follow external links to understand the plan.

### 3. Specify, Do Not Implement

The plan describes what to build and how it should behave. The executing agent writes the code.

Include:

- Exact file paths, module names, endpoint paths, component names, function names, and command names.
- Function signatures with complete type annotations when signatures matter.
- Type definitions, schemas, data structures, constants, configuration values, and environment variable names.
- Behavioral rules, concrete input/output examples, edge cases, error conditions, and failure modes.
- Algorithms in prose or pseudocode.
- Short code snippets only for non-obvious API usage, exact configuration, shell commands, or syntax that is easy to get wrong.

Do not include:

- Full function implementations.
- Full file contents for ordinary source files.
- Boilerplate the framework can generate or the executing agent can infer safely.
- Vague directives such as "handle errors appropriately", "add validation", or "follow best practices". Replace them with enumerated behaviors.

### 4. Assign Exactly One Agent Role Per Step

Use only these role names:

| Agent | Assign When |
|---|---|
| `coding-agent` | The step adds new behavior or writes new source code. |
| `refactoring-agent` | The step restructures existing code without changing external behavior. |
| `review-agent` | The step reviews code, checks plan compliance, performs static analysis, or runs verification. |
| `devops-agent` | The step changes build, CI/CD, deployment, environment, Docker, scripts, package management, or infrastructure. |
| `database-agent` | The step changes schema, migrations, seed data, queries, ORM configuration, or data-layer setup. |
| `documentation-agent` | The step creates or updates documentation rather than executable code. |
| `debug-agent` | The step diagnoses and fixes a specific known defect. |

If choosing between `coding-agent` and `refactoring-agent`, ask whether the step adds behavior. If yes, use `coding-agent`; if no, use `refactoring-agent`.

## Plan Structure

Scale the plan to the task:

- **Small task, about 1-5 steps**: Use Overview, Assumptions, Requirements, Steps, Verification, and Progress.
- **Medium task, about 5-15 steps**: Use the standard phased format with all living-document sections.
- **Large task, 15+ steps or major redesign**: Use the full phased format and add migration, rollback, performance, or security sections when relevant.

For medium and large plans, use this structure:

```markdown
**Implementation Plan: [Feature or Project Name]**

**Overview:**
[2-3 sentences. State the user-visible outcome and how to see it working.]

**Stated Assumptions:**
1. [Assumption not explicitly confirmed by the user.]

**Requirements:**
1. [Verifiable pass/fail condition, preferably observable behavior.]

**Tech Stack and Conventions:**
[Language, framework, runtime, package manager, file naming, module patterns, known repository conventions.]

**Boundaries:**
✅ Always:
- [Actions agents can take without asking.]

⚠️ Ask First:
- [Actions requiring human confirmation.]

🚫 Never:
- [Hard stops.]

**Architecture Changes:**
[Affected components, exact paths, before/after structure, or target directory tree.]

**Agent Summary:**
| Agent | Step Count | Phases Involved |
|---|---:|---|
| `coding-agent` | N | 1, 2 |

**Implementation Steps:**
[Phased steps, each phase ending with a Phase Gate.]

**Risks and Mitigations:**
1. Risk: [Concrete risk.]
   Mitigation: [Concrete mitigation tied to a step.]

**Success Criteria:**
- [ ] [Observable final condition.]

**Progress:**
- [ ] Step 1.1: [Status detail.]

**Decision Log:**
- Decision: [Initial planning decision or "None yet".]
  Rationale: [Why.]
  Date: [YYYY-MM-DD or "Not started".]

**Surprises & Discoveries:**
- [None yet.]

**Outcomes & Retrospective:**
- [Not started.]
```

## Step Requirements

Every implementation step must include these fields:

- **Step ID**: Unique and dependency-addressable, such as `1.1`, `1.2`, or `2.G`.
- **Agent**: Exactly one role from the allowed role list.
- **Location**: Exact file path, module, service, component, endpoint, or repository area.
- **Action**: Literal instruction the assigned agent can execute.
- **Details**: Specifications needed to write correct code: signatures, types, data shapes, behavioral rules, examples, edge cases, pseudocode, and configuration.
- **Dependencies**: Step IDs that must be complete first, or `None`.
- **Verification**: Exact checks to perform and expected results.
- **Complexity**: `Low`, `Medium`, or `High`.
- **Risk**: `Low`, `Medium`, or `High`; explain any Medium or High rating.
- **Idempotence & Recovery**: Required for Medium or High risk, and required for destructive work regardless of risk.

Verification must include at least one observable behavior check unless the step is purely structural. Build, lint, or typecheck commands are useful baselines, but they are insufficient for user-visible behavior. Prefer checks such as:

- Run a named test file and confirm a specific case passes.
- Send a request to an endpoint and confirm status code and body.
- Run a CLI command and confirm exact stdout, stderr, and exit code.
- Interact with a UI path and confirm visible state.
- Confirm a migration creates, updates, or rolls back a specific schema state.

## Phase Gates

Every phase must end with a Phase Gate step:

- Use Step ID `N.G`.
- Assign `Agent: review-agent`.
- Depend on all steps in that phase.
- Run exact build, lint, typecheck, test, or migration commands appropriate to the stack.
- Include at least one observable behavior check demonstrating the phase purpose, unless the phase is purely structural.
- State expected results with pass/fail precision.

Each completed phase must leave the system buildable and in a coherent state.

## Risk and Recovery Rules

For any Medium or High risk step:

- State whether the step is safely re-runnable after partial failure.
- If safely re-runnable, explain why, such as idempotent file generation, `CREATE TABLE IF NOT EXISTS`, or atomic temp-file rename.
- If not safely re-runnable, specify exact rollback or retry steps.

For destructive operations, schema migrations, file deletions, deployments, or data rewrites:

- Include a rollback path even if the risk is rated Low.
- State exact files, commands, migration identifiers, backups, or deployment targets involved.
- Mark operations that require human confirmation under `⚠️ Ask First`.

## Living Document Rules

Include these sections in every medium or large plan and instruct the executing agent to update them as work proceeds:

- **Progress**: Checkbox list for every step and phase gate. Completed entries must include UTC timestamps, such as `(2026-05-01 14:30Z)`.
- **Decision Log**: Non-trivial decisions, deviations from the plan, scope changes, and the rationale for each.
- **Surprises & Discoveries**: Unexpected behavior, bugs, library quirks, evidence, and short log excerpts.
- **Outcomes & Retrospective**: Milestone and final notes comparing actual outcome against the plan Overview.

When revising a plan mid-execution, update Requirements, Steps, Progress, and Decision Log consistently.

## Quality Bar

Before delivering the plan, check that:

- The completed plan has been saved to `PLANS.md` in the current working directory.
- Every requirement maps to at least one step and one success criterion.
- Every step has exact dependencies and no forward dependency references.
- Every step has one agent role and one concern.
- No step combines coding and review, or feature work and refactoring.
- Verification includes observable behavior wherever behavior changes.
- External facts needed by the executing agent are embedded in the plan.
- File paths, function names, endpoints, commands, and data structures are exact where known.
- Assumptions are explicitly listed and safe for the user to correct.
- The plan is self-contained and does not rely on "as discussed above" or external documents for required facts.
