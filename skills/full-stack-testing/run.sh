#!/usr/bin/env bash
# full-stack-testing — detect a test runner and run it.

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <repo-path>" >&2
    exit 1
fi

REPO="$1"
cd "$REPO" || { echo "repo not found: $REPO" >&2; exit 1; }

if grep -qE '^test:' Makefile 2>/dev/null; then
    echo "[runner] make test"
    exec make test
fi

if [[ -d tests ]] && command -v pytest >/dev/null 2>&1; then
    echo "[runner] pytest"
    exec pytest
fi

if [[ -f package.json ]] && command -v npm >/dev/null 2>&1; then
    echo "[runner] npm test"
    exec npm test
fi

if [[ -f Cargo.toml ]] && command -v cargo >/dev/null 2>&1; then
    echo "[runner] cargo test"
    exec cargo test
fi

if [[ -f go.mod ]] && command -v go >/dev/null 2>&1; then
    echo "[runner] go test ./..."
    exec go test ./...
fi

echo "[FAIL] no test runner detected" >&2
exit 1
