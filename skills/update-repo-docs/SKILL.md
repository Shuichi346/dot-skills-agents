---
name: update-repo-docs
description: Update or create repository-local CHANGELOG.md, NOTES.md, and AGENTS.md after programming work. Use when Codex needs to keep working-directory documentation current, create missing repo docs, record issues or decisions, add future agent instructions, or document release-level changes without touching codex-wide shared files.
---

# Update Repo Docs

## Overview

Keep repository-local `CHANGELOG.md`, `NOTES.md`, and `AGENTS.md` present and useful after implementation work. Write only material information, in English, with enough context for another agent to understand later.

## Scope

- Target the current working directory or detected repository root.
- Update only repository-local files such as `<repo>/CHANGELOG.md`, `<repo>/NOTES.md`, and `<repo>/AGENTS.md`.
- Do not edit codex-wide shared files such as `~/.codex/AGENTS.md` unless the user explicitly asks.
- If `CHANGELOG.md`, `NOTES.md`, or `AGENTS.md` is missing from the repository root, create it with minimal starter structure.
- Do not invent entries just because a file was created.

## Workflow

1. Inspect the completed work, relevant diffs, test results, and existing docs.
2. Ensure `CHANGELOG.md`, `NOTES.md`, and `AGENTS.md` exist in the repository root.
3. Preserve the existing document style and headings when they are clear.
4. Decide whether each file has something useful to record. Skip content changes that would only add filler.
5. Add concise entries near the top of each file unless the file's format requires otherwise.
6. Re-read the edited files and remove duplicate, stale, or overly detailed text.

## Starter Structures

When creating missing files, keep the initial content small:

```markdown
# Changelog

## Unreleased
```

```markdown
# Notes

## YYYY-MM-DD
```

```markdown
# AGENTS.md

Project instructions for coding agents working in this repository.
```

Add bullets under these headings only when there is material information to record.

## Document Roles

### `NOTES.md`

Use for chronological work notes: issues encountered, solutions applied, and decisions made.

- Write in past tense.
- Include the date when the file already uses dates, or add a simple `YYYY-MM-DD` heading.
- Keep entries short: one issue, solution, or decision per bullet.
- Prefer facts that prevent rediscovery over step-by-step work logs.

### `AGENTS.md`

Use for rules that future agents should follow in this repository.

- Write in present tense or imperative voice.
- Add rules only when the work revealed a durable convention, prohibited action, or recurrence-prevention rule.
- Preserve existing project instructions and avoid duplicating global Codex defaults.
- Keep rules actionable: mention file paths, commands, data contracts, or constraints when relevant.

### `CHANGELOG.md`

Use for release-level or milestone-level change history.

- Follow the existing changelog format if one exists.
- Add to `Unreleased` when present; otherwise add a small top section such as `## Unreleased`.
- Write completed changes in past tense.
- Include user-visible behavior, public interfaces, configuration changes, migrations, and notable fixes.
- Skip routine refactors, minor internal cleanup, and test-only changes unless they matter to users or maintainers.

## Quality Bar

- Be concise; avoid bloating context for future agents.
- Do not invent releases, dates, or impact.
- Do not repeat the same fact across all three files unless each audience needs it.
- When files were missing but there is nothing material to record, create the files with starter structure and mention that no substantive entries were added.
