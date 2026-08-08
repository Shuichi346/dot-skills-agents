# About Using Multi-Agent

Please proceed using the registered custom agents at '/Users/user_name/.codex/agents' as needed.

Main is responsible for requirements understanding, design, decision-making, and integration.
Use `explorer` for codebase investigation, `implementer` for implementation, `docs-researcher` for external specification research, `architect` for important design decisions, and `verifier` for independent verification after implementation.
Use `security-reviewer` only when security boundaries are involved, and `mechanic` only for simple repetitive tasks.

Independent read-heavy investigations may be parallelized as needed.
Do not run write agents concurrently; Main should integrate the results.
Do not spin up unnecessary subagents for small tasks.