#!/usr/bin/env python3
"""Generate the player catalog JSON for one playlist folder.

Usage:
    make_catalog.py <playlist-folder> [--title <name>] [--filter album|artist]

Scans the folder (recursively, so album subfolders are supported) for .m4a
files named "Artist - Title.m4a", probes each with ffprobe for its duration,
and prints the catalog JSON consumed by templates/player-template.html.

- Album subfolders present  -> filterKey defaults to "album", each track's
  "album" is its subfolder name, and "file" is the path relative to the
  playlist folder.
- Flat folder               -> filterKey defaults to "artist", "album" is "".
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return round(float(out.stdout.strip()), 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--title", default=None)
    ap.add_argument("--filter", choices=["album", "artist"], default=None)
    args = ap.parse_args()

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1

    files = sorted(
        (p for p in root.rglob("*.m4a")),
        key=lambda p: tuple(part.casefold() for part in p.relative_to(root).parts),
    )
    if not files:
        print(f"no .m4a files under {root}", file=sys.stderr)
        return 1

    has_albums = any(len(p.relative_to(root).parts) > 1 for p in files)
    filter_key = args.filter or ("album" if has_albums else "artist")

    tracks = []
    for p in files:
        rel = p.relative_to(root)
        stem = p.stem
        if " - " in stem:
            artist, title = stem.split(" - ", 1)
        else:
            artist, title = "", stem
        tracks.append({
            "file": rel.as_posix(),
            "title": title.strip(),
            "artist": artist.strip(),
            "album": rel.parts[0] if len(rel.parts) > 1 else "",
            "duration": probe_duration(p),
        })

    catalog = {
        "title": args.title or root.name,
        "filterKey": filter_key,
        "tracks": tracks,
    }
    print(json.dumps(catalog, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
