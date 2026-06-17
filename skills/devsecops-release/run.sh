#!/usr/bin/env bash
# devsecops-release — lint + test + clean tree + fresh changelog.

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <repo-path>" >&2
    exit 1
fi

REPO="$1"
cd "$REPO" || { echo "repo not found: $REPO" >&2; exit 1; }

SKIPS=()
if [[ -f .devsecops-skip ]]; then
    while IFS= read -r s; do SKIPS+=("$s"); done < .devsecops-skip
fi

is_skipped() {
    local k="$1"
    for s in "${SKIPS[@]:-}"; do
        [[ "$s" == "$k" ]] && return 0
    done
    return 1
}

fail=0

if is_skipped lint; then
    echo "[skip] lint"
else
    if grep -qE '^lint:' Makefile 2>/dev/null; then
        if make lint >/dev/null 2>&1; then echo "[ok] lint"; else echo "[FAIL] lint"; fail=1; fi
    else
        echo "[FAIL] no Makefile target named 'lint'"
        fail=1
    fi
fi

if is_skipped test; then
    echo "[skip] test"
else
    if grep -qE '^test:' Makefile 2>/dev/null; then
        if make test >/dev/null 2>&1; then echo "[ok] test"; else echo "[FAIL] test"; fail=1; fi
    else
        echo "[FAIL] no Makefile target named 'test'"
        fail=1
    fi
fi

if is_skipped tree; then
    echo "[skip] tree"
else
    if [[ -z "$(git status --short 2>/dev/null)" ]]; then echo "[ok] working tree clean"; else echo "[FAIL] working tree dirty"; fail=1; fi
fi

if is_skipped changelog; then
    echo "[skip] changelog"
else
    if [[ -f CHANGELOG.md ]]; then
        if find CHANGELOG.md -mtime -30 | grep -q . 2>/dev/null; then
            echo "[ok] changelog fresh"
        else
            echo "[FAIL] changelog stale (>30 days)"
            fail=1
        fi
    else
        echo "[FAIL] no CHANGELOG.md"
        fail=1
    fi
fi

exit "$fail"
