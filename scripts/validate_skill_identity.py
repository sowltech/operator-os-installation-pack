#!/usr/bin/env python3
"""Validates identity and metadata for every skills/*/SKILL.md in this repo.

Genuine YAML frontmatter parsing (not regex). Checks apply to every skill
folder found under skills/, not just the two touched by any single PR, so
a cross-repo name/slug collision is caught regardless of which file was
most recently edited.

This does NOT prove skills are auto-discovered by Claude Code or any tool
— see docs/DELIVERY_SOP.md and README.md for the actual (manual, per-client
vault copy) install path. No .claude/skills/ mechanism exists in this repo.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("VALIDATION ERROR: PyYAML is required (`pip install pyyaml`). Refusing to fall back to regex parsing.", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_KEY_HINTS = ("key", "token", "secret", "password", "credential")
SECRET_VALUE_RE = re.compile(r"(sk-[a-zA-Z0-9]{10,}|ghp_[a-zA-Z0-9]{10,}|xoxb-[a-zA-Z0-9-]{10,})")


def _load_raw_frontmatter_keys(frontmatter_text: str) -> list[str]:
    """Returns every top-level key literally seen, in order, including
    duplicates — yaml.safe_load silently keeps only the last occurrence of a
    duplicate key, so this catches what safe_load would hide."""
    keys = []
    for line in frontmatter_text.splitlines():
        if line and not line.startswith((" ", "\t", "-")) and ":" in line:
            keys.append(line.split(":", 1)[0].strip())
    return keys


def validate_all_skills(skills_root: Path) -> list[str]:
    errors: list[str] = []
    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
    all_names: dict[str, Path] = {}
    all_slugs: dict[str, Path] = {}

    for skill_dir in skill_dirs:
        path = skill_dir / "SKILL.md"
        if not path.exists():
            errors.append(f"{skill_dir}: no SKILL.md found")
            continue

        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"{path}: missing YAML frontmatter block")
            continue
        frontmatter_text, body = match.group(1), match.group(2)

        raw_keys = _load_raw_frontmatter_keys(frontmatter_text)
        seen = set()
        for key in raw_keys:
            if key in seen:
                errors.append(f"{path}: duplicate frontmatter key '{key}'")
            seen.add(key)

        try:
            meta = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as exc:
            errors.append(f"{path}: invalid YAML frontmatter: {exc}")
            continue
        if not isinstance(meta, dict):
            errors.append(f"{path}: frontmatter did not parse to a mapping/object")
            continue

        if not body.strip():
            errors.append(f"{path}: no Markdown instruction body found after frontmatter")

        name = meta.get("name")
        slug = meta.get("slug")
        title = meta.get("title")
        status = meta.get("status")

        # name is optional in this repo's convention (3 of 6 skills predate
        # it), but if present it must be well-formed and unique.
        if name is not None:
            if not name:
                errors.append(f"{path}: 'name' present but empty")
            elif not KEBAB_CASE_RE.match(name):
                errors.append(f"{path}: name '{name}' is not safe lowercase kebab-case")
            elif name in all_names:
                errors.append(f"{path}: duplicate name '{name}' also used by {all_names[name]}")
            else:
                all_names[name] = path

        if meta.get("description") is not None and not meta.get("description"):
            errors.append(f"{path}: 'description' present but empty")

        if slug is not None:
            if not slug:
                errors.append(f"{path}: 'slug' present but empty")
            elif not KEBAB_CASE_RE.match(slug):
                errors.append(f"{path}: slug '{slug}' is not safe lowercase kebab-case")
            elif slug != skill_dir.name:
                errors.append(f"{path}: slug '{slug}' does not match its folder name '{skill_dir.name}'")
            elif slug in all_slugs:
                errors.append(f"{path}: duplicate slug '{slug}' also used by {all_slugs[slug]}")
            else:
                all_slugs[slug] = path

        if title is not None and not title:
            errors.append(f"{path}: 'title' present but empty")
        if status is not None and status not in ("active", "draft", "deprecated"):
            errors.append(f"{path}: status '{status}' is not one of active/draft/deprecated")

        for key, value in (meta.items() if isinstance(meta, dict) else []):
            if isinstance(value, str):
                if any(hint in key.lower() for hint in SECRET_KEY_HINTS):
                    errors.append(f"{path}: frontmatter key '{key}' looks secret-shaped; do not store real secrets in SKILL.md")
                if SECRET_VALUE_RE.search(value):
                    errors.append(f"{path}: frontmatter key '{key}' value matches a secret-shaped pattern")

    return errors


def main() -> int:
    errors = validate_all_skills(SKILLS_ROOT)
    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):", file=sys.stderr)
        for i, message in enumerate(errors, 1):
            print(f"  {i}. {message}", file=sys.stderr)
        return 1
    print(f"skill identity validation passed ({len(list(SKILLS_ROOT.iterdir()))} skill folders checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
