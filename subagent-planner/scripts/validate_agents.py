#!/usr/bin/env python3
"""Validate Codex custom agent TOML files created by subagent-planner."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tomllib
from collections.abc import Iterable


ALLOWED_MODEL = "gpt-5.5"
ALLOWED_REASONING_EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh"}
ALLOWED_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}
REQUIRED_STRING_FIELDS = ("name", "description", "developer_instructions")
NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
NICKNAME_RE = re.compile(r"^[A-Za-z0-9 _-]+$")


def iter_toml_files(paths: Iterable[pathlib.Path]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.toml")))
        elif path.is_file() and path.suffix == ".toml":
            files.append(path)
        else:
            raise ValueError(f"{path} is not a TOML file or directory")
    return files


def validate_file(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML: {exc}"]
    except OSError as exc:
        return [f"cannot read file: {exc}"]

    for field in REQUIRED_STRING_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"`{field}` must be a non-empty string")

    name = data.get("name")
    if isinstance(name, str) and not NAME_RE.fullmatch(name):
        errors.append("`name` must be snake_case, start with a letter, and use only lowercase letters, digits, and underscores")

    model = data.get("model")
    if model != ALLOWED_MODEL:
        errors.append(f"`model` must be {ALLOWED_MODEL!r}")

    effort = data.get("model_reasoning_effort")
    if effort not in ALLOWED_REASONING_EFFORTS:
        allowed = ", ".join(sorted(ALLOWED_REASONING_EFFORTS))
        errors.append(f"`model_reasoning_effort` must be one of: {allowed}")

    sandbox_mode = data.get("sandbox_mode")
    if sandbox_mode is not None and sandbox_mode not in ALLOWED_SANDBOX_MODES:
        allowed = ", ".join(sorted(ALLOWED_SANDBOX_MODES))
        errors.append(f"`sandbox_mode` must be one of: {allowed}")

    nicknames = data.get("nickname_candidates")
    if nicknames is not None:
        if not isinstance(nicknames, list) or not nicknames:
            errors.append("`nickname_candidates` must be a non-empty list when present")
        else:
            seen: set[str] = set()
            for nickname in nicknames:
                if not isinstance(nickname, str) or not nickname.strip():
                    errors.append("each nickname candidate must be a non-empty string")
                    continue
                if not NICKNAME_RE.fullmatch(nickname):
                    errors.append(f"nickname candidate {nickname!r} uses unsupported characters")
                if nickname in seen:
                    errors.append(f"duplicate nickname candidate: {nickname!r}")
                seen.add(nickname)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex custom agent TOML files.")
    parser.add_argument("paths", nargs="+", type=pathlib.Path, help="Agent TOML files or directories containing TOML files")
    args = parser.parse_args()

    try:
        files = iter_toml_files(args.paths)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not files:
        print("error: no TOML files found", file=sys.stderr)
        return 2

    failed = False
    for path in files:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"{path}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{path}: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
