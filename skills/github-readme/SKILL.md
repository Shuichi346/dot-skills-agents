---
name: github-readme
description: Create or update polished English GitHub README.md files by analyzing a repository's source code, configuration, screenshots, and existing docs. Use when Codex is asked to draft repository documentation, explain what a library/app/tool does, write setup and usage instructions, add README screenshots, or organize GitHub README image assets in a githubreadme directory.
---

# GitHub README

## Workflow

1. Work from the repository root. Read project instructions first, then inspect the file tree, existing README files, package manifests, lockfiles, build scripts, examples, tests, and main entry points.
2. Infer the project purpose, audience, feature set, tech stack, setup commands, run commands, test commands, configuration, and license only from evidence in the repository or current official sources.
3. If screenshots or other images are attached or provided for README use, create `githubreadme/` in the repository root, copy the images there, and reference them from `README.md` with repository-relative links.
4. Write or update only the English `README.md` unless the user explicitly asks for another file. Do not output JSON.
5. Verify that local image links resolve and that all commands, paths, badges, and placeholders are intentional.

## Screenshot Assets

Use `scripts/stage_readme_images.py` when the user provides image file paths or local attachments that need to be copied into the repository:

```bash
python3 /Users/shuichi/.codex/skills/github-readme/scripts/stage_readme_images.py --repo /path/to/repo --images /path/to/screenshot.png /path/to/second.jpg
```

The script creates `githubreadme/`, copies supported image files with safe unique names, and prints README-ready image snippets with a fixed 480 pixel display width:

```markdown
<img src="githubreadme/screenshot.png" alt="Screenshot" width="480">
```

Place screenshots where they help readers understand the project: near the overview for app/product screenshots, in Usage for workflows, or in a UI section for tours and feature introductions. Use `<img>` tags with `width="480"` for screenshots, descriptive alt text, and concise captions. Do not add decorative images that do not explain the repository.

## README Structure

Start the file with this exact language switch table:

```markdown
<table>
  <thead>
    <tr>
      <th style="text-align:center"><a href="README_ja.md">日本語</a></th>
      <th style="text-align:center"><a href="README.md">English</a></th>
    </tr>
  </thead>
</table>
```

Then write a professional English README using the sections that fit the repository:

- Project title
- Badges, only when the values are known or can be safely derived
- One-paragraph overview explaining what the repository is and who it is for
- Screenshot or UI preview section, when image assets are available
- Features
- Tech stack
- Requirements
- Installation
- Usage
- Configuration or environment variables
- Development workflow
- Testing
- Project structure, only when it helps orientation
- Troubleshooting, only when repository evidence suggests common issues
- Roadmap, only when an existing roadmap or TODO source exists
- License

Add a table of contents when the README becomes long enough that navigation helps.

## Accuracy Rules

- Prefer exact commands from files such as `README.md`, `package.json`, `pyproject.toml`, `Makefile`, `justfile`, `Taskfile`, `Cargo.toml`, `Package.swift`, or CI workflows.
- Search the web for current official documentation when commands or behavior depend on a library, framework, API, or tool version that may have changed.
- Do not invent license terms, deployment targets, API keys, environment variable values, hosted URLs, maintainer names, support channels, or compatibility claims.
- Use placeholders for important missing facts, for example `[Add license information]`, `[Describe required environment variables]`, or `[Add deployment instructions]`.
- Keep the tone concrete and useful. Explain what the repository does before explaining how it is implemented.
- Make the README understandable to someone seeing the repository for the first time.
