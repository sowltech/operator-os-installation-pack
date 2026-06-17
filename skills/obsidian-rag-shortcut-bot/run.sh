#!/usr/bin/env bash
# obsidian-rag-shortcut-bot
# Given a vault root and a task category, print the page paths to load.
# No external services. No file modifications. Stdlib only.

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "usage: $0 <vault-root> <task-category>" >&2
    exit 1
fi

VAULT="$1"
TASK="$2"
MAP="$VAULT/00_INDEX/recall-map.md"

if [[ ! -f "$MAP" ]]; then
    echo "recall-map.md not found at $MAP" >&2
    exit 2
fi

MATCH=$(awk -F'|' -v task="$TASK" '
    /^\|/ {
        c1 = $2
        gsub(/^[ \t]+|[ \t]+$/, "", c1)
        if (tolower(c1) == tolower(task)) {
            c2 = $3
            gsub(/^[ \t]+|[ \t]+$/, "", c2)
            print c2
            exit
        }
    }
' "$MAP")

if [[ -z "$MATCH" ]]; then
    echo "no match for task '$TASK' in $MAP" >&2
    exit 2
fi

printf '%s\n' "$MATCH" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
    | sed 's/^`//;s/`$//' \
    | awk 'NF > 0'

exit 0
