#!/usr/bin/env python3
"""Copy README screenshots into a repository-local githubreadme directory."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".webp",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "image"


def unique_destination(directory: Path, stem: str, suffix: str) -> Path:
    candidate = directory / f"{stem}{suffix}"
    index = 2
    while candidate.exists():
        candidate = directory / f"{stem}-{index}{suffix}"
        index += 1
    return candidate


def alt_text(path: Path) -> str:
    words = re.sub(r"[-_]+", " ", path.stem).strip()
    return words.title() if words else "Screenshot"


def stage_images(repo: Path, image_paths: list[Path], asset_dir_name: str) -> list[Path]:
    asset_dir = repo / asset_dir_name
    asset_dir.mkdir(parents=True, exist_ok=True)

    staged_paths: list[Path] = []
    for source in image_paths:
        if not source.is_file():
            raise FileNotFoundError(f"Image not found: {source}")

        suffix = source.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ValueError(f"Unsupported image extension for {source}. Supported: {supported}")

        destination = unique_destination(asset_dir, slugify(source.stem), suffix)
        shutil.copy2(source, destination)
        staged_paths.append(destination)

    return staged_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy README image assets into repo/githubreadme and print 480px image tags."
    )
    parser.add_argument("--repo", required=True, type=Path, help="Repository root.")
    parser.add_argument(
        "--images",
        required=True,
        nargs="+",
        type=Path,
        help="Image files to copy into the README asset directory.",
    )
    parser.add_argument(
        "--dir",
        default="githubreadme",
        help="Repository-relative asset directory name. Defaults to githubreadme.",
    )
    parser.add_argument(
        "--width",
        default=480,
        type=int,
        help="Rendered image width in pixels. Defaults to 480.",
    )
    args = parser.parse_args()
    if args.width <= 0:
        raise ValueError("--width must be a positive integer.")

    repo = args.repo.expanduser().resolve()
    if not repo.is_dir():
        raise NotADirectoryError(f"Repository root not found: {repo}")

    images = [image.expanduser().resolve() for image in args.images]
    staged = stage_images(repo, images, args.dir)

    for path in staged:
        relative = path.relative_to(repo).as_posix()
        print(f'<img src="{relative}" alt="{alt_text(path)}" width="{args.width}">')

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
