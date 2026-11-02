---
name: implementation-planner
description: Create or revise a durable implementation plan such as PLANS.md for a substantial software change, with an executable design, dependency-ordered steps, acceptance evidence, and live progress. Use for a requested plan file or agent-ready specification; not ordinary same-chat planning or source implementation.
---

# Implementation Planner

Write a self-contained plan that another coding agent can implement and resume without rediscovering the user's intended result. Plan the complete requested scope, including an MVP when explicitly requested; never shrink required behavior to make implementation easier.

This skill authors the plan. Do not edit product source or begin implementation as part of planning. If the user also requested implementation, finish and save the plan, then continue with that authorized work; planning does not create an additional approval gate.

## Establish the contract

Read applicable repository instructions, any existing target plan, and the source, tests, configuration, and current changes relevant to the task. Resolve knowable paths, interfaces, commands, and constraints from evidence. Research version-specific or uncertain dependencies in official documentation; include the execution-relevant facts and their source links in the plan.

Separate explicit requirements, supported inferences, and material unknowns. Choose routine details from repository conventions. Ask a focused question only when an unresolved choice would materially change behavior, architecture, compatibility, data handling, operations, or acceptance. Continue independent planning work while awaiting an answer; do not silently settle the dependent decision.

Define the user-visible outcome, scope boundaries, relevant failure behavior, and observable completion conditions. Include operating qualities such as performance, privacy, accessibility, or recovery when the requested product needs them. Do not invent enterprise requirements or defer necessary behavior as future polish.

User instructions take precedence over skill defaults. Carry forward the user's decisions and existing authorization. Separate work that can proceed from any action requiring new permission; a plan cannot grant that permission. Do not prescribe additional confirmation for already authorized actions.

## Write the executable design

When creating a macOS app, target Apple silicon only (`arm64`). Intel Macs are outside the supported scope: do not add `x86_64` builds, universal app distributions, Rosetta workflows, or Intel compatibility tests. Select arm64-compatible runtimes, native dependencies, helpers, and packaging settings. Include a bounded command-line architecture inspection of the built app and its bundled native components in the existing acceptance checks. The app must run natively on Apple silicon; report a dependency that requires Intel execution as a blocker. Do not turn a source-only fix in an existing project into an unrelated architecture migration.

Carry this macOS architecture requirement into the saved plan when applicable.

Use one coherent solution. Explain the components, interfaces, data flow, state, and important errors or edge cases that determine implementation. Give exact paths and identifiers where verified; distinguish proposed locations from existing ones. Avoid speculative function-level detail the executor can decide safely.

Assign stable implementation IDs such as `I1`, `I2`. For each step include:

- **Outcome and location:** The concrete result and affected files, modules, or services.
- **Action:** Required behavior and the design decisions needed to implement it.
- **Dependencies:** Earlier IDs or `None`.
- **Acceptance evidence:** A command, observation, or artifact inspection and its expected result.
- **Risk and recovery, when relevant:** How to detect partial success and recover from migration, destructive work, or external side effects.

Sequence steps by dependency. Phases describe construction order and meaningful checkpoints; they do not change the final scope. Use specialized agents only when authorized and independent roles would improve accuracy or coverage. A plan does not need fictional agent assignments.

## Design proportionate verification

Write a finite verification list tied to the changed behavior and applicable repository requirements. State that the executor stops testing when this list passes. Add checks during execution only for an affected requirement, a concrete defect, or a relevant later change, not for optional polish or more confidence.

Do not use computer-use features for testing or verification: no AI-driven screen observation and interactive clicking, typing, or navigation in a browser or native app (including CUA). Use terminal commands, APIs, logs, and deterministic automated tests instead. Existing scripted browser/UI tests may run through a test runner with finite limits; do not replace them with an interactive AI-operated UI session.

Carry these testing restrictions and the post-completion handoff below into the saved plan so an executor does not need this skill to follow them.

Map required behavior to sufficient evidence. Prefer existing project commands and checks. Normally progress from static validation and build/type checking to a short realistic startup or critical-path smoke check, then only targeted tests needed for behavior those checks cannot establish. Combine overlapping checks. Focused tests may be part of an implementation step when they directly prove that step's behavior.

For every required agent-run check, state its command or non-interactive evidence source, expected result, prerequisites, and finite execution time limit. Put human operation flows in a separate post-completion recommendation section, outside required acceptance gates and progress checkboxes. Distinguish commands discovered in the repository from proposed ones. Explain inapplicable tiers rather than creating permanently pending checkboxes. Do not require new test files, frameworks, coverage targets, or wrapper infrastructure without a concrete verification need.

Use these local tool conventions when applicable and compatible with repository instructions:

- JavaScript/TypeScript: Prefer project-local `oxlint` and `typescript`, invoked through the existing package manager. Add an absent development tool only when needed for a required check or requested by the user; use the existing manifest and lockfile. No global installs or transient auto-downloads.
- C-family: Use Homebrew LLVM through the prefix resolved by `brew --prefix llvm`.
- Swift: Use toolchain `swift format` or `xcrun swift-format` and native build commands; do not install another formatter.
- Python: Use installed `ruff` and `ty` where applicable. Rust: Use rustup-managed `cargo check` or `rustc`.

Plan finite time and output budgets for all checks, concise success summaries, and focused failure diagnostics. Apply a default budget of one initial execution plus two post-repair reruns per verification unit, including static checks, builds, smoke checks, and targeted tests, across edits and interruptions. The user may explicitly change this budget; use a stricter limit where cost or side effects require it. Stop retrying when the limit is reached or the same failure recurs without a new diagnosis, record the blocker, and continue independent in-scope work. Do not reset the budget by renaming or subdividing a failed check, switching tools, or broadening the suite. Do not plan open-ended repair loops, watch sessions, or additional checks after sufficient acceptance evidence passes.

Split expensive verification into meaningful units. Coding-to-testing transitions are progress checkpoints by default: update status and continue authorized verification. Include a return-to-user boundary only when the user requested staged execution, an applicable instruction requires it, or the next action needs permission or unavailable input. Record the reason for any required stop so the executor can distinguish it from a routine checkpoint.

### Repeated failures and reasoning effort

For the same unresolved coding or bug-fix issue, use the existing bounded verification round (at most three executions, including the initial check and post-repair reruns), not an additional allowance of three repairs. If that round fails and diagnosis or repair strategy remains uncertain, stop retrying that issue and recommend that the user raise reasoning effort by one available level. Recommend this earlier if the same failure recurs without a new diagnosis; do not consume attempts merely to reach the limit. Missing permissions, credentials, dependencies, services, or other known external prerequisites need their specific remedy, not a reasoning-effort increase.

Explain the uncertainty without claiming a model limitation is proven. For example: 「The same issue has not been resolved within this attempt. It is possible that it cannot be resolved at the current reasoning level. Please increase the reasoning level by one step and instruct to continue the execution.」 Name the current and next levels only when reliably known; otherwise do not guess. Do not change settings or claim they changed yourself.

Save the diagnostic, attempted approaches, attempt count, and known effort level for resumption. Continue independent authorized work. Only after the user confirms a higher level and requests resumption may the same issue receive a new bounded round, normally at most three executions; retain the cumulative history. A new message or chat alone does not reset the budget. If still unresolved, recommend the next available higher level on the same basis. At the highest available level, or without a confirmed increase, report the blocker and a concrete next diagnostic rather than retrying indefinitely. This is a settings/resumption request, not a request for the user to test the unfinished deliverable.

Include this escalation and resumption rule in the saved plan so the executor can apply it without loading this skill.

### Post-completion handoff

Include the following executor instruction in the plan; authoring the plan alone does not mean implementation is complete:

After implementation and the required automated checks are complete, include a short "Recommended operation checks (after completion)" list in the final response. Give concrete user actions and expected results for the changed behavior. Do not ask the user to operate or test the deliverable during production or make their response a prerequisite for completing the coding task. Keep these human checks outside the required implementation tracker; label them as recommendations that the agent has not performed, not as passed checks. If no meaningful human operation check applies, say so briefly. Report genuinely blocked automated checks honestly; do not use this handoff to conceal incomplete implementation.

## Save one authoritative tracker

Save `PLANS.md` in the working directory unless the user chose another path or chat-only output. Update an existing plan for the same task in place, preserving valid decisions and completion evidence. Ask before replacing an unrelated plan.

By default, put `## Progress Status` immediately after the title. If the user requests separate tracking or the plan must remain immutable, use `PROGRESS.md` beside it and identify that file as authoritative. Keep checkbox state in exactly one file.

The tracker contains meaningful planning milestones, each implementation ID, and applicable verification units. Use `[ ]` for pending, active, failed, or blocked work and `[x]` only for evidenced completion. Include `Current:` for the active item or blocker and `Next:` for the next dependency-safe action. Avoid redundant parent checkboxes unless grouping materially helps.

Mark only planning actually completed as done when delivering a new plan; future implementation and verification stay unchecked. When revising an existing plan, retain or correct completed items using current evidence. Set `Current:` and `Next:` accordingly.

Specify that the executor saves the tracker after each implementation step or independent verification unit. At the start, phase boundaries, and completion, show the full checklist; ordinary updates show only changed checkbox lines with `Current:` and `Next:`. Follow a user-requested shorter reporting format. Keep logs and command-by-command history out of the tracker.

## Plan shape and handoff

Use only sections with material content. A typical plan contains:

1. Progress Status.
2. Outcome, requirements, and scope boundaries.
3. Current system evidence and relevant assumptions.
4. Architecture and design.
5. Implementation sequence with stable IDs and dependencies.
6. Final verification with observable pass conditions and budgets.
7. Recommended human operation checks after completion, with actions and expected results.
8. Material decisions, permission boundaries, and recovery details.

Check that every required behavior maps to implementation and acceptance evidence, dependencies are executable, and no unknown decision is disguised as a fact. Keep the specification stable during execution; change it when user direction or verified evidence requires a material revision. Routine progress updates do not change product scope.

Add resumption details only when interruption or side effects require facts beyond the working tree: the remaining action, blockers, and necessary operation identifiers or safe-retry conditions. Leave narrative history and durable repository rules to repository documentation; do not invoke another documentation skill automatically.

Report the saved plan and tracker paths, the checklist, the next action, and any material unresolved assumption concisely. Do not require `$execute-implementation-plan` for ordinary continuation in the same chat; it is useful for explicit plan-file execution or later resumption.
