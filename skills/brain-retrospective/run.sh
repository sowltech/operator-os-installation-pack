#!/usr/bin/env bash
# brain-retrospective — read-only audit log + decisions roll-up.

set -euo pipefail

ROOT="."
SINCE="14 days ago"
OUT=""

usage() {
    cat <<'EOF'
brain-retrospective — read-only audit log + decisions roll-up.

Usage:
  bash skills/brain-retrospective/run.sh [options]

Options:
  --root PATH    Vault root path. Default: current directory.
  --since DATE   Window start date string. Default: "14 days ago".
  --out FILE     Write report to FILE in addition to stdout.
  --help         Show this message.

Exit codes:
  0  Report produced.
  1  Vault root not found.
  2  Audit log missing.
  4  Window contains zero rows and zero decisions.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --root)  ROOT="$2";  shift 2 ;;
        --since) SINCE="$2"; shift 2 ;;
        --out)   OUT="$2";   shift 2 ;;
        --help|-h) usage; exit 0 ;;
        *) echo "unknown arg: $1" >&2; usage; exit 1 ;;
    esac
done

AUDIT="$ROOT/90_AUDIT/audit-log.md"
DECISIONS="$ROOT/decisions"
SOURCES="$ROOT/30_KNOWLEDGE/source-register.md"

[[ -d "$ROOT" ]]  || { echo "vault root not found: $ROOT" >&2; exit 1; }
[[ -f "$AUDIT" ]] || { echo "audit log missing: $AUDIT" >&2; exit 2; }

since_iso() {
    if date -d "$SINCE" +%Y-%m-%d >/dev/null 2>&1; then
        date -d "$SINCE" +%Y-%m-%d
    else
        python3 -c "
import datetime, re
m = re.match(r'(\d+)\s+days?\s+ago', '$SINCE'.strip())
n = int(m.group(1)) if m else 14
print((datetime.date.today() - datetime.timedelta(days=n)).isoformat())
"
    fi
}

SINCE_ISO=$(since_iso)
NOW_ISO=$(date +%Y-%m-%d)

_count_type() {
    awk -F'|' -v since="$SINCE_ISO" -v t="$1" '
        /^\| [0-9]+ \|/ {
            d=$3;  gsub(/^[ \t]+|[ \t]+$/, "", d)
            ty=$4; gsub(/^[ \t]+|[ \t]+$/, "", ty)
            if (d >= since && ty == t) c++
        }
        END { print c+0 }
    ' "$AUDIT"
}

audit_count=$(awk -F'|' -v since="$SINCE_ISO" '
    /^\| [0-9]+ \|/ {
        d=$3; gsub(/^[ \t]+|[ \t]+$/, "", d)
        if (d >= since) c++
    }
    END { print c+0 }
' "$AUDIT")

create_count=$(_count_type "CREATE FILE")
edit_count=$(_count_type "EDIT FILE")
write_count=$(_count_type "WRITE VAULT")
decision_count=$(_count_type "DECISION")
check_count=$(_count_type "BUILD CHECK")

active_decisions=0
if [[ -d "$DECISIONS" ]]; then
    active_decisions=$(grep -lE '^status:[[:space:]]*active' "$DECISIONS"/*.md 2>/dev/null | wc -l | tr -d ' ')
fi

source_total=0
if [[ -f "$SOURCES" ]]; then
    source_total=$(grep -cE '^\|' "$SOURCES" || true)
fi

if [[ "$audit_count" -eq 0 && "$active_decisions" -eq 0 ]]; then
    echo "no activity in window and no active decisions" >&2
    exit 4
fi

report() {
    cat <<EOF
# Retrospective — $NOW_ISO

## Window

- Start: $SINCE_ISO
- End:   $NOW_ISO
- Audit rows in window: $audit_count
- Active decisions:     $active_decisions
- Source register rows: $source_total

## Action verb breakdown

- CREATE FILE: $create_count
- EDIT FILE:   $edit_count
- WRITE VAULT: $write_count
- DECISION:    $decision_count
- BUILD CHECK: $check_count

## Active decisions

EOF
    if [[ -d "$DECISIONS" ]]; then
        grep -lE '^status:[[:space:]]*active' "$DECISIONS"/*.md 2>/dev/null | while read -r f; do
            echo "- \`$(basename "$f")\`"
        done
    fi
    if [[ "$active_decisions" -eq 0 ]]; then
        echo "(none active)"
    fi

    cat <<EOF

## Recommendations

(Generated heuristically from counts above. Each must be reviewed before
landing. Maximum five.)

EOF

    rec=0
    if [[ "$audit_count" -lt 3 ]]; then
        echo "$((rec+1)). [witness] Audit volume is low ($audit_count rows). Either widen the window with --since, or note the lapse."
        ((rec++))
    fi
    if [[ "$decision_count" -eq 0 && "$active_decisions" -gt 0 ]]; then
        echo "$((rec+1)). [decision] Active decisions exist but no DECISION rows landed in window — review whether any active decision needs updating."
        ((rec++))
    fi
    if [[ "$write_count" -gt 5 ]]; then
        echo "$((rec+1)). [archive] High write velocity ($write_count writes). Review whether any new pages duplicate existing concepts."
        ((rec++))
    fi
    if [[ "$rec" -eq 0 ]]; then
        echo "1. [witness] No anomalies. Append a session-end row noting the retrospective ran cleanly."
    fi

    cat <<EOF

---
This report was produced read-only. No file was modified. The operator
decides which recommendations land.
EOF
}

if [[ -n "$OUT" ]]; then
    mkdir -p "$(dirname "$OUT")"
    report | tee "$OUT"
else
    report
fi
exit 0
