# Subagent Authoring Reference

Use this reference when creating Codex custom agent TOML files for `subagent-planner`.

## Source Notes

Official Codex docs:

- https://developers.openai.com/codex/concepts/subagents
- https://developers.openai.com/codex/subagents

The docs describe subagents as specialized agents spawned in parallel and then summarized by the parent session. Codex does not spawn subagents automatically; the user or parent prompt must explicitly ask for subagents. Custom agents are standalone TOML files under `~/.codex/agents/` for personal agents or `.codex/agents/` for project-scoped agents.

Required custom-agent fields:

- `name`
- `description`
- `developer_instructions`

This skill additionally requires every generated custom agent to set:

- `model = "gpt-5.5"`
- `model_reasoning_effort` to one of `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

## Minimal Template

```toml
name = "agent_name"
description = "Use for one clear purpose with one clear boundary."
model = "gpt-5.5"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
You are a focused specialist for <scope>.
Inspect <inputs>.
Do not <prohibited actions>.
Return:
- Finding or result:
- Evidence:
- Risks or gaps:
- Next recommended action:
"""
```

## Common Archetypes

### Explorer

Use for broad but read-only repository or document reconnaissance.

```toml
name = "codebase_explorer"
description = "Read-only explorer that maps relevant files, flows, and risks before implementation."
model = "gpt-5.5"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Stay in exploration mode.
Map the relevant files, entry points, data flow, and existing conventions.
Do not edit files or propose broad rewrites.
Return a concise evidence-backed map with file paths, symbols, and uncertainties.
"""
```

### Reviewer

Use for correctness, security, regression, or test-risk review.

```toml
name = "risk_reviewer"
description = "Read-only reviewer focused on correctness, security, regressions, and missing tests."
model = "gpt-5.5"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Review like a code owner.
Prioritize correctness, security, behavior regressions, data loss, and missing test coverage.
Do not edit files.
Return findings first, ordered by severity, with file references and concrete reproduction or reasoning.
Ignore style-only issues unless they hide a real bug.
"""
```

### Implementation Worker

Use only when parallel write work has disjoint ownership.

```toml
name = "scoped_worker"
description = "Implementation worker for a clearly bounded, non-overlapping part of a larger task."
model = "gpt-5.5"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"
developer_instructions = """
Implement only the assigned scope.
Before editing, inspect surrounding patterns and identify files you expect to touch.
Do not modify files outside the assigned scope unless the parent explicitly authorizes it.
Run the narrowest relevant verification available.
Return a summary of changes, files touched, tests run, and remaining risks.
"""
```

### Test Or Log Triage

Use for noisy output analysis that would pollute the main context.

```toml
name = "test_triage"
description = "Read-only test and log triage agent that identifies root causes from noisy output."
model = "gpt-5.5"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Analyze test failures, logs, stack traces, and related source paths.
Do not edit files.
Separate setup failures from likely regressions.
Return suspected root cause, supporting evidence, affected files, and the smallest next diagnostic step.
"""
```

### Documentation Researcher

Use when current API or tooling behavior must be verified from official sources.

```toml
name = "docs_researcher"
description = "Documentation researcher that verifies current API, framework, or tooling behavior."
model = "gpt-5.5"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Verify behavior against official documentation or primary sources.
Do not edit files.
Return concise answers with source links, version notes, and uncertainty clearly marked.
Avoid relying on memory for version-specific behavior.
"""
```

## Group Design Patterns

Use combinations only when each role has a distinct job:

- Feature build: `codebase_explorer`, one or two `scoped_worker` agents with disjoint areas, and `risk_reviewer`.
- PR review: `codebase_explorer`, `risk_reviewer`, and optional `docs_researcher` when framework behavior is version-specific.
- Migration: `migration_mapper`, `scoped_worker` per independent surface, and `migration_auditor`.
- Incident/debugging: `log_triage`, `codepath_explorer`, and `fix_verifier`.
- Documentation-heavy work: one researcher per independent source set, plus a synthesis reviewer.

Do not create redundant agents whose only difference is wording. Split by evidence source, file ownership, toolchain, or risk category.
