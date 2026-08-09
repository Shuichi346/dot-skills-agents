# About Using Multi-Agent

If necessary, please proceed using the custom agents registered in /Users/user-name/.codex/agents.

## Main Agent
**main**: Responsible for orchestration. Handles requirements understanding, design, decision-making, and integration.

### Sub-Agents
- **explorer**: Used for codebase investigation
- **implementer**: Used for implementation tasks
- **docs-researcher**: Used for researching external specifications
- **architect**: Used when critical design decisions are required
- **verifier**: Used for independent verification after implementation
- **security-reviewer**: Used only when security boundaries are involved
- **mechanic**: Used only for simple, repetitive tasks

## Operational Rules
- Independent investigations (read-focused tasks) can be executed in parallel as needed
- Simultaneous execution of write-based agents is prohibited. The main agent integrates the results.
- Do not launch unnecessary sub-agents for small-scale tasks