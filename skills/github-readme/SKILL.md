---
name: github-readme
description: Create or update a GitHub repository's README from source code and project documentation, including setup, usage, and supplied screenshot assets. Use for README authoring or edits, not general code explanations or unrelated documentation.
---

# GitHub README

Produce a reader-ready README that explains the project and gives a practical path to using it. Default to English `README.md`; follow the user's requested language, file, and format when specified.

## Scope and evidence

- Read project instructions. For a focused edit, inspect the relevant content; for a full README, start with existing docs, manifests, scripts, and entry points. Follow examples, tests, or CI as needed to establish reader-facing facts.
- Complete the edit using evidence and reasonable editorial choices. Ask only when an unresolved choice materially changes the deliverable and cannot be inferred.
- Preserve useful existing content and user edits. Limit changes to the requested README and necessary supplied image assets unless the user requests more.
- Derive commands, requirements, configuration, and capabilities from the implementation. Resolve stale docs against scripts and source. Check official documentation for uncertain version-specific behavior, respecting pinned versions.
- Do not invent project facts, including license, compatibility, services, or released features. Omit unsupported optional sections; state essential missing information plainly. Reserve editorial placeholders for requested templates or drafts.

## Writing and layout

Lead with the title, purpose, and audience. Include requirements, installation, and a concrete usage example where applicable. Add other sections only when supported and useful. Prefer one documented setup path unless the project requires multiple workflows.

Use plain language, descriptive headings, and concise prose. Use lists, tables, and a table of contents when they help readers. Avoid promotional claims and filler sections. Include badges only with verified targets and values.

For a new README or full refresh, use this language switch at the top when `README_ja.md` exists; otherwise omit the switch. Preserve existing working language navigation. A focused edit need not alter it, and adding navigation does not require creating a translation.

```html
<table>
  <thead>
    <tr>
      <th style="text-align:center"><a href="README_ja.md">日本語</a></th>
      <th style="text-align:center"><a href="README.md">English</a></th>
    </tr>
  </thead>
</table>
```

## Screenshot assets

Reuse suitable repository images. For supplied local images that need copying, use [scripts/stage_readme_images.py](scripts/stage_readme_images.py), resolving its path from this skill directory:

```bash
python3 /path/to/github-readme/scripts/stage_readme_images.py --repo /path/to/repo --images "/path/to/App Preview.png"
```

The helper copies images into `githubreadme/` with unique filenames and prints repository-relative `<img>` tags. Default to 480 pixels wide; use `--width` for a requested size. Keep any custom `--dir` inside the repository. Reuse staged files on subsequent edits.

Inspect images before describing them. Place them near relevant content, with descriptive alt text and useful captions. If an attachment is inaccessible, complete the text and report the missing asset without inventing a path.

## Verification and delivery

Review the diff, local links and images, heading anchors, and command consistency. Run relevant documentation checks or a bounded example when useful and feasible. Prose or image-only edits do not by themselves require an application build, a full test suite, or new tests. Distinguish source-checked commands from executed commands.

Finish after the edit and relevant checks. Briefly report changed files, validation, and unresolved facts or assets; repeat the README only if requested.
