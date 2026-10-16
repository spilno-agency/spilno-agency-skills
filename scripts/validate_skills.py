#!/usr/bin/env python3
"""Validate every skill folder: SKILL.md exists, frontmatter is well-formed,
`name` matches the folder, and no agency brand is hardcoded in the algorithm."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", "scripts"}
FORBIDDEN = [re.compile(r"Spilno Agency", re.I), re.compile(r"mcp__[0-9a-f]{8}-")]
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def validate_skill(folder: Path) -> list[str]:
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return [f"{folder.name}: missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return [f"{folder.name}: SKILL.md has no YAML frontmatter"]
    meta = match.group(1)
    errors = []
    name = re.search(r"^name:\s*(\S+)\s*$", meta, re.M)
    if not name or name.group(1) != folder.name:
        errors.append(f"{folder.name}: frontmatter `name` must equal folder name")
    if not re.search(r"^description:\s*\S", meta, re.M):
        errors.append(f"{folder.name}: frontmatter `description` is empty")
    for pattern in FORBIDDEN:
        if pattern.search(text):
            errors.append(f"{folder.name}: hardcoded value matches /{pattern.pattern}/ — use a placeholder")
    return errors


def main() -> int:
    folders = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in SKIP_DIRS)
    errors = [e for folder in folders for e in validate_skill(folder)]
    for error in errors:
        print(f"::error::{error}")
    print(f"Checked {len(folders)} skill(s), {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
