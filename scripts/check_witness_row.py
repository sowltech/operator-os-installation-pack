#!/usr/bin/env python3
"""Audit log row validator.

Validates rows in an append-only audit log. Each row must have the canonical
six-cell shape:

    | <row-number> | YYYY-MM-DD | <ACTION> | <target> | <details> | <outcome> |

The validator checks:

- Six cells exactly (no extra pipes inside cells)
- Monotonically increasing row numbers
- ISO date format
- Canonical action verb
- Outcome marker present

Read-only. Does not modify the log. Exits 0 on a clean log, non-zero on
any defect found.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

CANONICAL_ACTIONS = {
    "CREATE FILE",
    "EDIT FILE",
    "WRITE VAULT",
    "DECISION",
    "SESSION START",
    "SESSION END",
    "RECONCILE",
    "APPROVE TOOL",
    "REVOKE TOOL",
    "BUILD CHECK",
}

OUTCOME_MARKERS = {"✅", "⚠️", "❌"}  # check, warning sign + VS-16, cross

ROW_PATTERN = re.compile(r"^\|\s*\d+\s*\|")


def parse_row(line: str):
    """Return cells list or None if the line is not a row."""
    if not ROW_PATTERN.match(line):
        return None
    if not line.rstrip().endswith("|"):
        return None
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    cells = [c.strip() for c in inner.split("|")]
    return cells


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"audit log not found: {path}"]
    issues: list[str] = []
    prev_n = 0
    rows = 0
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        cells = parse_row(raw)
        if cells is None:
            continue
        rows += 1
        if len(cells) != 6:
            issues.append(
                f"line {lineno}: expected 6 cells, got {len(cells)} — "
                f"inner pipes are forbidden"
            )
            continue
        # row number
        try:
            n = int(cells[0])
        except ValueError:
            issues.append(f"line {lineno}: row number {cells[0]!r} is not an integer")
            continue
        if n <= prev_n:
            issues.append(
                f"line {lineno}: row number {n} is not greater than previous {prev_n}"
            )
        prev_n = n
        # date
        try:
            datetime.date.fromisoformat(cells[1])
        except ValueError:
            issues.append(f"line {lineno}: date {cells[1]!r} is not ISO format")
        # action verb
        if cells[2] not in CANONICAL_ACTIONS:
            issues.append(
                f"line {lineno}: action {cells[2]!r} not in canonical set "
                f"({sorted(CANONICAL_ACTIONS)})"
            )
        # target — must not be empty
        if not cells[3]:
            issues.append(f"line {lineno}: target cell is empty")
        # details — must not be empty
        if not cells[4]:
            issues.append(f"line {lineno}: details cell is empty")
        # outcome marker — at least one of the three present in the cell
        if not any(marker in cells[5] for marker in OUTCOME_MARKERS):
            issues.append(
                f"line {lineno}: outcome cell {cells[5]!r} missing one of "
                f"the required markers (check / warning / cross)"
            )
    if rows == 0 and not issues:
        # empty audit log is valid (fresh install)
        return []
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log", required=True, help="path to the audit log file")
    args = p.parse_args()
    issues = validate(Path(args.log))
    if issues:
        print("audit log validation FAILED:", file=sys.stderr)
        for msg in issues:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    print(f"[ok] audit log clean: {args.log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
