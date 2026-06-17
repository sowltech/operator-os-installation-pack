#!/usr/bin/env python3
"""Measure context savings of an index-first recall pattern.

Counts the words in every Markdown file under the vault root, then counts
the words in the selected file paths the assistant would actually load,
and reports the difference as a percentage saving.

Read-only. Stdlib only. No external network. No file modification.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"\b\w+\b")


def words(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    return len(WORD_RE.findall(text))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("vault", help="path to the vault root")
    p.add_argument(
        "selected",
        nargs="+",
        help="one or more files the assistant would actually load",
    )
    args = p.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        print(f"vault root not found: {vault}", file=sys.stderr)
        return 1

    all_md = list(vault.rglob("*.md"))
    whole = sum(words(f) for f in all_md)

    loaded_paths = [Path(s) for s in args.selected]
    missing = [str(p) for p in loaded_paths if not p.exists()]
    if missing:
        print(f"missing selected files: {missing}", file=sys.stderr)
        return 1

    loaded = sum(words(f) for f in loaded_paths)

    saving = ((whole - loaded) / whole * 100) if whole else 0.0

    print(f"Whole vault words: {whole:,}")
    print(f"Selected words:    {loaded:,}")
    print(f"Estimated saving:  {saving:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
