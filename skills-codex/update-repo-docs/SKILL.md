---
name: update-repo-docs
description: Record completed coding work in repository-local CHANGELOG.md, NOTES.md, and AGENTS.md with minimal context use. Use after fixes, additions, changes, or removals to preserve outcomes and prevent regressions in later work. Not for README authoring or global Codex configuration.
---

# Update Repo Docs

Make a lightweight record immediately after coding so later work preserves fixes and intended behavior. Write in English unless requested otherwise.

## Use the current task's evidence

- Use the user's target directory; otherwise use the repository or worktree root, or the working directory outside Git. Follow applicable project instructions. Keep edits repository-local; shared files such as `~/.codex/AGENTS.md` require an explicit request.
- A full update considers `CHANGELOG.md`, `NOTES.md`, and `AGENTS.md`; narrower user scope takes precedence. Use completed work, decisions, and verification results already available in the conversation, including work already committed or pushed.
- Read only the insertion area and relevant existing sections needed to avoid duplicates or contradictions. Use targeted searches and bounded excerpts for long documents. Reuse instructions and evidence already loaded.
- Do not routinely inspect commit history, reread source code, or load entire logs and documents. If a material fact is missing, inspect only the smallest relevant diff or source excerpt. Investigate historical work only when requested. Do not reconstruct missing history or invent facts to fill an entry.

## Put information in the right document

### CHANGELOG.md — what changed

Record completed fixes, additions, behavior changes, and removals in past tense. Include meaningful interface, configuration, or migration changes; omit routine cleanup and test-only changes unless their impact matters.

Use `## YYYY-MM-DD` headings, newest first, with `### Fixed`, `### Added`, `### Changed`, and `### Removed` as needed. Use equivalent labels when writing in another language. Append same-day changes to the existing date and category; omit empty categories. Use the current date in the user's timezone for work just completed. For explicitly requested historical entries, use an evidenced date and ask if an essential date is unavailable.

Create new entries directly under date headings, without `Unreleased` or an assumed release version. Please retain existing past records as they are. If there are project-specific instructions, those instructions take precedence over this standard format.

### NOTES.md — why the implementation should be preserved

Keep concise technical handoff notes when they help prevent recurrence or accidental reversal: the cause, chosen solution and rationale, behavior that must remain intact, or an unresolved limitation. Include relevant code paths and existing regression-test references when already known and useful; do not force a template or investigate merely to fill fields.

Use dated entries following existing conventions, otherwise `YYYY-MM-DD`. Distinguish verified outcomes from unresolved issues. Do not repeat the changelog's change summary without adding useful reasoning or constraints, and avoid command transcripts or session logs.

### AGENTS.md — rules for future work

Record only durable, verified, repository-specific instructions in present tense or imperative voice, with actionable paths, commands, or contracts. Preserve existing rules and scope. Keep rationale in NOTES and reference the relevant section when useful. Do not turn every fix, one-time workaround, or hypothesis into a standing rule, or duplicate global defaults and work history.

## Edit and finish

An individual change need not produce entries in all three files. Keep each fact in the document serving its purpose; use short references instead of duplicated explanations. Update outdated current guidance only with supporting evidence, preserve history, and leave files unchanged when there is nothing material to add.

For a full update, create missing target files unless user scope or project instructions restrict creation. Use minimal starter headings: `# Changelog`, `# Notes`, and `# AGENTS.md` with a short project-instructions introduction. Add dated sections only when there is information to record.

Review only the documentation diff from this update for accuracy, duplication, and unintended edits. Reuse known path, command, and test evidence; verify only unresolved references and run required documentation checks. Do not rerun implementation tests merely to record the work. Finish briefly with files changed and material evidence limits.
