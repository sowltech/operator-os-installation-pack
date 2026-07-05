#!/usr/bin/env bash
# Smoke test for token_economy_guard.sh — verifies trivial-skip, nudge, and headroom clause.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
H="$HERE/token_economy_guard.sh"
echo "1) trivial prompt (silent):"
printf '{"prompt":"hi"}' | bash "$H"; echo "   exit=$?"
echo "2) real prompt (nudge):"
printf '{"prompt":"refactor the module and add tests"}' | bash "$H"
echo "3) headroom clause (large fake transcript):"
TMP="$(mktemp)"; head -c 1200000 /dev/zero | tr '\0' 'x' > "$TMP"
printf '{"prompt":"build a service with tests","transcript_path":"%s"}' "$TMP" | bash "$H"
rm -f "$TMP"
echo "OK"
