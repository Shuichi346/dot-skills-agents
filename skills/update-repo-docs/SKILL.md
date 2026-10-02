---
name: update-repo-docs
description: Maintain repository-local CHANGELOG.md, NOTES.md, and AGENTS.md after implementation work. Use to record material changes, engineering decisions, and durable project instructions, or create missing repo docs. Not for README authoring or global Codex configuration.
---

# Update Repo Docs

Maintain concise, factual documentation for maintainers and future coding agents. Write in English unless requested otherwise; use repository conventions for routine editorial decisions.

## Establish scope and evidence

- Use the user's target directory; otherwise use the repository or worktree root, or the working directory outside Git. Read applicable project instructions and target docs.
- A full update covers `CHANGELOG.md`, `NOTES.md`, and `AGENTS.md`. A request naming fewer files or prohibiting file creation takes precedence. Keep edits repository-local; changing shared files such as `~/.codex/AGENTS.md` requires an explicit request.
- Inspect relevant implementation, diffs, and verification results, including committed or uncommitted work as requested. Do not attribute unrelated local changes to this task.
- Separate implemented behavior and observed results from unresolved issues. Never invent impact or successful checks. Ask only when missing evidence materially affects scope or accuracy; otherwise complete the edits.

## Put information in the right document

### CHANGELOG.md

Record release- or milestone-level changes: user-visible behavior, public interfaces, configuration, migrations, and notable fixes. Use past tense and the existing format, adding `Unreleased` for unreleased work if needed. Do not assign release versions or dates without evidence. Omit routine cleanup and test-only changes unless their impact matters to users or maintainers.

### NOTES.md

Record issues, solutions, decisions, and unresolved limitations that prevent rediscovery. Use short past-tense entries explaining the outcome or rationale. Follow existing date conventions; otherwise use the actual current date as a `YYYY-MM-DD` heading. Avoid command transcripts and session logs.

### AGENTS.md

Record durable, repository-specific instructions in present tense or imperative voice, with actionable paths, commands, contracts, or constraints. Preserve existing rules and their scope. Do not promote one-time workarounds or unverified hypotheses into standing requirements, or duplicate global defaults and work history.

## Edit and finish

Preserve historical entries and document structure. Place additions according to the existing format; correct outdated current guidance only with supporting evidence. Repeat facts across documents only for distinct purposes. Leave existing files unchanged when there is nothing material to add.

For a full update, create missing target files unless the user's scope or applicable repository instructions restrict creation. Use minimal starter content: `# Changelog` with `## Unreleased`, `# Notes`, and `# AGENTS.md` with a short project-instructions introduction. Add dated headings and substantive entries only when there is information to record.

Review the final diff for factual support, duplicates, and unintended edits. Check referenced paths and commands against repository evidence, and run required documentation checks. Reuse available implementation test results; rerun code tests only if required or needed to verify an unresolved claim. Finish with a brief account of files changed, any starter-only files, and material verification limits.
