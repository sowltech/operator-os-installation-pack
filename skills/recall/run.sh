#!/usr/bin/env bash
# recall — plain-text recall against a vault.

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "usage: $0 <vault-root> <query-string>" >&2
    exit 1
fi

VAULT="$1"
QUERY="$2"

if [[ ! -d "$VAULT" ]]; then
    echo "vault root not found: $VAULT" >&2
    exit 1
fi

IGNORE_FILE="$VAULT/.recallignore"
EXCLUDES=()
if [[ -f "$IGNORE_FILE" ]]; then
    while IFS= read -r pattern; do
        [[ -z "$pattern" ]] && continue
        [[ "$pattern" =~ ^# ]] && continue
        EXCLUDES+=(--exclude-dir="$pattern")
    done < "$IGNORE_FILE"
fi

grep -rli "${EXCLUDES[@]}" --include='*.md' "$QUERY" "$VAULT" 2>/dev/null || true

exit 0
