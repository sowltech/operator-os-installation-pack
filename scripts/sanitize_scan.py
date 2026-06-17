#!/usr/bin/env python3
"""Sanitisation scanner.

Walks the pack directory and reports every occurrence of a banned term in
file content. Fails (exit 1) if any term is found in a non-allowlisted file.

Read-only. Stdlib only. No external network. No file modification.

Allowlist:
  - This script (it must contain the term list by definition)
  - Any file matched by a pattern in `.scan-allowlist` at the pack root

Usage:
  python3 scripts/sanitize_scan.py [--root .] [--quiet]

Exit codes:
  0  no banned term found in scanned content
  1  one or more banned terms found
  2  pack root not found
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

SUBSTRING_BANNED: tuple[str, ...] = (
    # distinctive multi-word identifiers (substring-safe — low false positive risk)
    "Sirius Nexus",
    "Crown OS",
    "St Elmo",
    "sovereign-router",
    "ASTRALOCK Lite private",
    "NEXUS-PRIME",
    "WITNESS_MEMORY_LOG",
    "STACK_SKILL_TREE_MASTER",
    "09_Decisions",
    "00_HQ",
    "07_Agents",
    ".claude",
    "192.168.",
    "localhost:",
    "witness row",
    "commit hash",
    "repo hash",
)

WORD_BOUNDARY_BANNED: tuple[str, ...] = (
    # short / ambiguous tokens — require standalone match to avoid false positives
    # (e.g. "S T" inside "is to", "as the"; "Saint" inside "constraint")
    "Saint",
    "S T",
    "ORCA",
    "SHINOBI",
    "Phoenix",
    "qwen",
    "mistral",
    "hermes",
    "deepseek",
)


def _word_boundary_pattern(term: str) -> re.Pattern:
    # \b requires alphanumeric on one side; for terms with a space we anchor
    # surrounding characters as non-word so "S T" matches only as a token.
    escaped = re.escape(term)
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)


_WORD_BOUNDARY_PATTERNS: list[tuple[str, re.Pattern]] = [
    (t, _word_boundary_pattern(t)) for t in WORD_BOUNDARY_BANNED
]

TEXT_EXTENSIONS: frozenset[str] = frozenset(
    {".md", ".txt", ".py", ".sh", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg"}
)

DEFAULT_ALLOWLIST: tuple[str, ...] = (
    "scripts/sanitize_scan.py",  # contains the term list by definition
)


def load_allowlist(root: Path) -> list[str]:
    patterns = list(DEFAULT_ALLOWLIST)
    f = root / ".scan-allowlist"
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def is_allowlisted(rel_path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, p) for p in patterns)


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return list of (line_no, banned_term, line_excerpt) for hits in path."""
    hits: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return hits
    for lineno, line in enumerate(text.splitlines(), 1):
        lower = line.lower()
        excerpt_cache = None
        # substring-mode banned terms
        for term in SUBSTRING_BANNED:
            if term.lower() in lower:
                if excerpt_cache is None:
                    excerpt_cache = line.strip()
                    if len(excerpt_cache) > 80:
                        excerpt_cache = excerpt_cache[:77] + "..."
                hits.append((lineno, term, excerpt_cache))
        # word-boundary-mode banned terms
        for term, pattern in _WORD_BOUNDARY_PATTERNS:
            if pattern.search(line):
                if excerpt_cache is None:
                    excerpt_cache = line.strip()
                    if len(excerpt_cache) > 80:
                        excerpt_cache = excerpt_cache[:77] + "..."
                hits.append((lineno, term, excerpt_cache))
    return hits


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".", help="pack root path (default: cwd)")
    p.add_argument("--quiet", action="store_true", help="print only on failure")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"pack root not found: {root}", file=sys.stderr)
        return 2

    allowlist = load_allowlist(root)

    total_hits = 0
    files_scanned = 0
    files_with_hits: list[tuple[Path, list[tuple[int, str, str]]]] = []

    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = str(path.relative_to(root))
        if is_allowlisted(rel, allowlist):
            continue
        files_scanned += 1
        hits = scan_file(path)
        if hits:
            files_with_hits.append((path.relative_to(root), hits))
            total_hits += len(hits)

    if not args.quiet:
        total_terms = len(SUBSTRING_BANNED) + len(WORD_BOUNDARY_BANNED)
        print(f"[sanitize_scan] root: {root}")
        print(f"[sanitize_scan] files scanned: {files_scanned}")
        print(f"[sanitize_scan] allowlisted files: {len(allowlist)}")
        print(
            f"[sanitize_scan] banned terms: {total_terms} "
            f"({len(SUBSTRING_BANNED)} substring + "
            f"{len(WORD_BOUNDARY_BANNED)} word-boundary)"
        )

    if not files_with_hits:
        if not args.quiet:
            print("[ok] no banned terms found")
        return 0

    print(f"[FAIL] banned terms found in {len(files_with_hits)} file(s):", file=sys.stderr)
    for path, hits in files_with_hits:
        for lineno, term, excerpt in hits:
            print(f"  {path}:{lineno}: {term!r} -> {excerpt!r}", file=sys.stderr)
    print(f"[FAIL] total occurrences: {total_hits}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
