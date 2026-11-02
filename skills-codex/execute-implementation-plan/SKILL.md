---
name: execute-implementation-plan
description: Execute or resume an existing implementation plan such as PLANS.md, especially after interruption or handoff. Reconcile progress with actual state, complete the requested scope, and verify acceptance with bounded checks. Use for explicit plan-file execution; not new plan authoring or ordinary same-chat continuation.
---

# Execute Implementation Plan

Complete the requested plan using its design and acceptance criteria as the specification. Use the working tree, verification results, and observed external state as evidence of completed work. Preserve the full requested scope, including a deliberately requested MVP; do not substitute a smaller result for a difficult requirement.

## Load and reconcile

Read the entire user-named plan, or `PLANS.md` in the working directory, and applicable repository instructions before editing. Confirm that the plan matches the request and provides an executable design and observable acceptance conditions.

Resolve routine omissions from repository evidence. If the plan is missing or a material decision cannot be inferred safely, ask for the missing plan or decision without inventing scope. Continue independent authorized work when possible. Do not require the user to invoke another skill to fix a minor plan omission.

Find the authoritative tracker: normally `Progress Status` in the plan, or a separate tracker it identifies. If an older executable plan lacks one, add it before source work. If the plan must remain immutable or the user requests separate tracking, use `PROGRESS.md` beside it. Maintain exactly one authoritative checklist.

For same-chat continuation, inspect only what the next action needs. After interruption, compaction, or handoff:

- Inspect Git status, relevant changed files, and evidence for the next unmet requirements.
- Reconcile stale checkboxes against actual implementation and still-valid verification results. Treat summaries and legacy `Resume Here` notes as hints.
- Check whether pending external or non-idempotent operations already succeeded before retrying them.
- Resume the first unmet dependency-safe action; do not repeat completed work or audit the whole repository without a reason.

If side-effect state is uncertain, keep that operation pending and establish its state before retrying. Ask one focused question when available evidence cannot resolve the uncertainty.

## Execute through completion

When creating a macOS app, target Apple silicon only (`arm64`). Intel Macs are outside the supported scope: do not add `x86_64` builds, universal app distributions, Rosetta workflows, or Intel compatibility tests. Select arm64-compatible runtimes, native dependencies, helpers, and packaging settings. Include a bounded command-line architecture inspection of the built app and its bundled native components in the existing acceptance checks. The app must run natively on Apple silicon; report a dependency that requires Intel execution as a blocker. Do not turn a source-only fix in an existing project into an unrelated architecture migration.

Set `Current:` to the next dependency-safe item, implement it, obtain its acceptance evidence, and save progress. Repeat until the authorized scope and required verification are complete. Do not finish the turn merely because coding ended, a checklist phase changed, or a test unit passed.

User instructions take precedence over skill defaults. Respect user-requested phase stops, budgets, and permission limits. A legacy plan's blanket instruction to pause before all testing is a workflow default: when current user or higher-priority instructions authorize continuous execution, record that reporting change and continue. If no such direction supersedes an explicit stop in the plan, honor it. At a normal coding-to-testing transition, report progress and run the required checks without asking for renewed permission.

Preserve the user's product decisions and unrelated changes. Handle routine implementation details directly. Update the specification before changes that materially affect architecture, requirements, dependency order, acceptance criteria, or recovery; ground the revision in user direction or verified project evidence. Ask only for a material choice that remains unresolved. Record optional improvements as optional instead of adding them to required scope.

Incorporate new user corrections into the remaining work and invalidate affected evidence. Answer status or side questions briefly, then resume the original objective unless the user cancels or replaces it.

A plan step does not itself grant permission for an external write, destructive action, deployment, migration, purchase, commit, or push. Use authorization already established in context and obey applicable tool permissions. Before seeking new approval, complete the authorized preparation and make the pending action concrete and reviewable. Continue independent work while a dependent action is blocked.

## Keep progress reliable

- Use `[ ]` for pending, active, failed, or blocked work; `[x]` only for evidenced completion.
- `Current:` identifies the active item or exact blocker. `Next:` identifies the next dependency-safe action, or what would unblock it.
- After each implementation step or independent verification unit, update its checkbox and `Current:`/`Next:`, reconciling parent checkboxes if present, and save the tracker.
- Show the full checklist at the start, phase boundaries, and completion. For other work-unit updates, show changed checkbox lines plus `Current:` and `Next:`. Follow a user-requested shorter reporting format.
- Keep concise results, blockers, and necessary recovery facts. Keep raw logs and command-by-command history elsewhere. Do not duplicate narrative repository documentation.

Correct stale completion claims when evidence disagrees and briefly explain why. Source work can be complete while a separate verification item remains pending; neither means the overall task is complete.

## Verify the required behavior

Before verification, identify a finite set of required checks tied to the changed behavior and applicable repository requirements, with pass conditions and time limits. Reuse this set across continuation and handoff. Add a check only for an affected requirement, a concrete defect, or a relevant later change; curiosity, optional polish, and a desire for more confidence do not justify expanding the test scope. Once the set passes, stop verification and deliver the result.

Do not use computer-use features for testing or verification: no AI-driven screen observation and interactive clicking, typing, or navigation in a browser or native app (including CUA). Use terminal commands, APIs, logs, and deterministic automated tests instead. Existing scripted browser/UI tests may run through a test runner with finite limits; do not replace them with an interactive AI-operated UI session.

Follow the plan's acceptance conditions and repository checks with the smallest sufficient evidence. Prefer existing commands. Normally use static validation and build/type checking, a short realistic startup or critical-path smoke check, and only targeted tests needed to establish important remaining behavior. Combine overlapping checks and use focused tests during implementation when they directly prove an affected requirement.

Do not write tests that merely mirror a reversible, low-impact edit. Do not add frameworks, broad fixtures, coverage targets, or test infrastructure without a concrete need. Once acceptance evidence passes, broaden or repeat checks only for new changes, failures, or unresolved requirements.

Use these local tool conventions when applicable and compatible with repository instructions:

- JavaScript/TypeScript: Prefer project-local `oxlint` and `typescript` through the existing package manager. Add an absent development tool only when needed for a required check or requested by the user, preserving the existing manifest/lockfile workflow. No global installs or transient auto-downloads.
- C-family: Resolve Homebrew LLVM with `brew --prefix llvm` and invoke tools from that prefix.
- Swift: Use toolchain `swift format` or `xcrun swift-format` and native build commands; do not install another formatter.
- Python: Use installed `ruff` and `ty` where applicable. Rust: Use rustup-managed `cargo check` or `rustc`.

If a check is inapplicable, record why and omit it rather than marking an unrun check complete. If equivalent current evidence establishes the same condition, record that basis. Required evidence that is unavailable remains pending with its prerequisite; do not weaken acceptance to declare success.

### Bound output and retries

Use quiet output or capture logs. Report concise success results and retrieve the smallest useful failure excerpt, expanding diagnostics only as needed. Give every check a finite execution time limit and bound its output; do not leave watch mode, polling, or a hung process running indefinitely. Split expensive checks into meaningful units and checkpoint each result; a unit boundary alone does not require yielding.

Apply a default limit of three executions per verification unit, including static checks, builds, smoke checks, and targeted tests: one initial execution plus two reruns after focused repairs. Count across source, configuration, fixture, or test edits and across interruptions. Honor stricter plan limits; a higher limit requires explicit user direction. Record attempts in the tracker only when needed to preserve the limit across a handoff or interruption.

Rerun an affected check after a focused repair while budget remains. If attempts are exhausted, the same failure recurs without a new diagnosis, or further work requires disproportionate infrastructure, leave that item unchecked with the diagnostic and next action. Continue independent in-scope work; if the blocker prevents all further progress, report the exact remaining requirement. Do not rename or subdivide a failed check, switch tools, or start a broader suite to reset its budget.

After a repair, invalidate the affected static/build checks and any behavioral evidence made stale, and rerun them only within the remaining attempt budget. Reuse passing evidence only while relevant source, configuration, dependencies, tests, and external inputs remain unchanged. Report unrelated failures without broadening the task unless they block required acceptance.

### Repeated failures and reasoning effort

For the same unresolved coding or bug-fix issue, use the existing bounded verification round (at most three executions, including the initial check and post-repair reruns), not an additional allowance of three repairs. If that round fails and diagnosis or repair strategy remains uncertain, stop retrying that issue and recommend that the user raise reasoning effort by one available level. Recommend this earlier if the same failure recurs without a new diagnosis; do not consume attempts merely to reach the limit. Missing permissions, credentials, dependencies, services, or other known external prerequisites need their specific remedy, not a reasoning-effort increase.

Explain the uncertainty without claiming a model limitation is proven. For example: 「The same issue has not been resolved within this attempt. It is possible that it cannot be resolved at the current reasoning level. Please increase the reasoning level by one step and instruct to continue the execution.」 Name the current and next levels only when reliably known; otherwise do not guess. Do not change settings or claim they changed yourself.

Save the diagnostic, attempted approaches, attempt count, and known effort level for resumption. Continue independent authorized work. Only after the user confirms a higher level and requests resumption may the same issue receive a new bounded round, normally at most three executions; retain the cumulative history. A new message or chat alone does not reset the budget. If still unresolved, recommend the next available higher level on the same basis. At the highest available level, or without a confirmed increase, report the blocker and a concrete next diagnostic rather than retrying indefinitely. This is a settings/resumption request, not a request for the user to test the unfinished deliverable.

## Preserve resumption evidence

For ordinary local edits and checks, Git and the working tree are usually sufficient. Add durable details when a handoff, material decision, or risky operation would otherwise be ambiguous: exact remaining action, blockers, attempts for an unfinished test unit, and necessary operation IDs or recovery conditions.

Before a non-idempotent operation, obtain the minimum appropriate duplicate-detection or recovery evidence, such as an idempotency key, migration/deployment ID, existence check, backup location, or rollback procedure. After an interruption, inspect that evidence before retrying. Never put credentials or raw sensitive output in the plan.

## Finish honestly

After implementation and the required automated checks are complete, include a short "Recommended operation checks (after completion)" list in the final response. Give concrete user actions and expected results for the changed behavior. Do not ask the user to operate or test the deliverable during production or make their response a prerequisite for completing the coding task. Keep these human checks outside the required implementation tracker; label them as recommendations that the agent has not performed, not as passed checks. If no meaningful human operation check applies, say so briefly. Report genuinely blocked automated checks honestly; do not use this handoff to conceal incomplete implementation.

Declare the coding task complete only when the requested implementation and required agent-run acceptance checks have current evidence. Human operation checks are post-completion recommendations, not coding completion gates. When reconciling a legacy plan, move user-operated checks into that separate recommendation list while retaining their original purpose; do not claim they were executed. Set the completed tracker to `Current: Complete` and `Next: None`, and show the final checklist with a concise account of delivered behavior, changed artifacts, and verification.

If a required item remains blocked or a user-requested stop is reached, save the actual state and exact next action; do not call the plan complete. If this skill itself requires a stop, identify this `SKILL.md` and quote the applicable instruction so the user can see why. Leave optional improvements clearly separate from required unfinished work.
