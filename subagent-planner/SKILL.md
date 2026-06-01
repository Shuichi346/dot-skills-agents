---
name: subagent-planner
description: >-
  Plan and create Codex custom agent groups for a user-stated objective. Use when
  the user asks to design, create, generate, or configure subagents, custom
  agents, an agent group, an agent team, parallel worker roles, or reusable
  Codex agents for a task. The skill decides whether agents are warranted,
  chooses the optimal number and roles, writes agent TOML definitions when
  appropriate, and does not execute the underlying task itself. If agents are
  not warranted, respond exactly: "Agents are not needed for this task."
---

# Subagent Planner

## Objective

Create the smallest useful set of Codex custom agents for the user's stated objective. The work product is agent configuration, not execution of the user's underlying task.

Do not spawn agents, implement the requested feature, review the PR, run the research task, or otherwise complete the end goal. Only create the agents and a concise usage prompt for running them later.

## Workflow

1. Restate the user's objective internally as an agent-design problem.
2. Decide whether agents are warranted.
3. If agents are not warranted, respond exactly:

```text
Agents are not needed for this task.
```

4. If agents are warranted, choose the fewest roles that have distinct scopes and non-overlapping outputs.
5. Create one TOML file per custom agent.
6. Run `scripts/validate_agents.py` on the generated files when shell execution is available.
7. Respond with the created file paths, a short role summary, and a ready-to-use prompt for spawning the agents later.

## When Agents Are Warranted

Create agents only when at least one condition is clearly true:

- The task splits into independent non-trivial workstreams that can run in parallel.
- The task requires noisy read-heavy reconnaissance, log triage, test analysis, or document summarization that should stay out of the main context.
- The task benefits from isolated verification or second opinion, especially for correctness, security, migrations, release readiness, or high-risk changes.
- The task spans distinct toolchains or domains that need separate focused contexts.
- The user wants a reusable custom agent role with stable behavior across future runs.

Do not create agents for direct questions, simple commands, tiny single-file edits, ordinary linear bug fixes, small explanations, or cases where all proposed agents would duplicate the same work.

## Role And Count Rules

Prefer fewer agents. Use:

- `0` agents when the task is simple or linear.
- `1` agent only for a durable specialist role that is useful beyond the immediate request.
- `2-4` agents for most real groups.
- More than `4` agents only when each role has a genuinely independent evidence stream or deliverable.

Avoid generic "planner", "coder", and "reviewer" triples unless the user's objective actually needs all three. Prefer roles that describe the work boundary, such as `api_contract_reviewer`, `migration_auditor`, `docs_researcher`, `test_triage_worker`, or `frontend_accessibility_reviewer`.

## File Placement

Create project-scoped agents under `.codex/agents/` when the objective is tied to the current repository or workspace.

Create personal reusable agents under `~/.codex/agents/` only when the user explicitly asks for global agents or the objective is not project-specific.

If the target path is unclear and choosing wrong would create clutter, ask one focused question. If file writes are unavailable, provide complete TOML contents with intended paths instead.

Use file names like `<agent-name-with-hyphens>.toml`. Use `snake_case` for the TOML `name`.

## TOML Requirements

Every generated agent must include:

```toml
name = "agent_name"
description = "Human-facing guidance for when Codex should use this agent."
model = "gpt-5.5"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Define the role, boundaries, allowed actions, prohibited actions, and exact return shape.
"""
```

Use only `model = "gpt-5.5"`.

Use only these `model_reasoning_effort` values:

- `none`: purely mechanical formatting or extraction with no judgement.
- `minimal`: quick inventory, simple classification, or narrow fact collection.
- `low`: straightforward exploration or summarization where speed matters.
- `medium`: default for most specialist agents.
- `high`: complex review, debugging, security, architecture, migration, or edge-case analysis.
- `xhigh`: rare; use only for unusually hard, high-impact reasoning where latency is acceptable.

Set `sandbox_mode = "read-only"` for exploration, review, research, and verification agents. Use `workspace-write` only for agents that must edit files. Avoid write-capable agents in the same file areas unless their scopes are clearly disjoint.

## Developer Instruction Checklist

For each agent's `developer_instructions`:

- State the role in the first sentence.
- Define what the agent must inspect or produce.
- Define what the agent must not do.
- Give a concrete return format.
- Tell read-only agents not to modify files.
- Tell write-capable agents to keep changes scoped and report touched files.
- Keep instructions self-contained; do not depend on hidden context from the parent thread.

Read `references/subagent-authoring.md` only when you need TOML examples, role archetypes, or official-doc details.

## Validation

After creating or editing agent files, run:

```bash
python scripts/validate_agents.py <agent-file-or-directory>
```

Fix validation errors before finalizing. If validation cannot be run, state that clearly.

## Final Response

If no agents are created, output only the exact required sentence.

If agents are created, keep the final response concise:

- List the created agent files.
- Summarize each role in one line.
- State that the underlying task was not executed.
- Include a short prompt the user can use to spawn the group.
