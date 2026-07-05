#!/usr/bin/env bash
# token_economy_guard.sh — always-run token-discipline + headroom nudge for LLM coding agents.
#
# Register on the agent's UserPromptSubmit hook. Stdout is injected into context, so keep it tiny:
# one compact line, plus a headroom clause only when live context is getting large.
#
#   - Cheap: local-model reachability cached; headroom = one grep + wc; never blocks.
#   - Local-model-aware: route out when a local model is up, else apply in-session discipline.
#   - Headroom-aware: warns to tighten / checkpoint before the window forces a summarize.
#   - Silent on trivial prompts. Never errors (always exit 0).

set -uo pipefail

# Point this at YOUR local model host's tags/health endpoint. Probe the model, not a proxy.
LOCAL_LLM_URL="${LOCAL_LLM_URL:-http://127.0.0.1:11434/api/tags}"
CACHE="${TOKEN_ECONOMY_CACHE:-$HOME/.cache/token_economy_local_status}"
TTL="${TOKEN_ECONOMY_TTL:-120}"
WARN_KB="${TOKEN_ECONOMY_HEADROOM_WARN_KB:-500}"
CRIT_KB="${TOKEN_ECONOMY_HEADROOM_CRIT_KB:-1000}"

mkdir -p "$(dirname "$CACHE")" 2>/dev/null || true

PAYLOAD=""
[ -t 0 ] || PAYLOAD="$(cat 2>/dev/null || true)"

PROMPT="${CLAUDE_HOOK_PROMPT:-}"
if [ -z "$PROMPT" ] && [ -n "$PAYLOAD" ]; then
  PROMPT=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("prompt",""))
except Exception: print("")' 2>/dev/null || echo "")
fi
[ "${#PROMPT}" -lt 12 ] && exit 0

# cached local-model reachability
status="DOWN"; now=$(date +%s); mtime=0
[ -f "$CACHE" ] && mtime=$(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE" 2>/dev/null || echo 0)
if [ -f "$CACHE" ] && [ $((now - mtime)) -lt "$TTL" ]; then
  status=$(cat "$CACHE" 2>/dev/null || echo DOWN)
else
  if curl -s --max-time 1 "$LOCAL_LLM_URL" >/dev/null 2>&1; then status="UP"; else status="DOWN"; fi
  printf '%s' "$status" > "$CACHE" 2>/dev/null || true
fi

# context headroom: bytes since last compaction boundary (approx live context)
headroom=""; transcript=""
if [ -n "$PAYLOAD" ]; then
  transcript=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("transcript_path",""))
except Exception: print("")' 2>/dev/null || echo "")
fi
if [ -n "$transcript" ] && [ -f "$transcript" ]; then
  boundary=$(grep -nE '"isCompactSummary":[[:space:]]*true|"type":[[:space:]]*"summary"' "$transcript" 2>/dev/null | tail -1 | cut -d: -f1)
  if [ -n "$boundary" ]; then live_bytes=$(tail -n +"$boundary" "$transcript" 2>/dev/null | wc -c | tr -d ' ')
  else live_bytes=$(wc -c < "$transcript" 2>/dev/null | tr -d ' '); fi
  live_kb=$(( ${live_bytes:-0} / 1024 ))
  if [ "$live_kb" -ge "$CRIT_KB" ]; then
    headroom=" | headroom LOW (~${live_kb}KB live) — checkpoint NOW: one audit entry + a compact handoff, then offload noisy work to a sub-agent."
  elif [ "$live_kb" -ge "$WARN_KB" ]; then
    headroom=" | headroom tightening (~${live_kb}KB live) — stop re-reading, summarize, prefer sub-agents for noisy fan-out."
  fi
fi

if [ "$status" = "UP" ]; then
  echo "[token-economy] local model UP — route mechanical steps out, keep synthesis here. Read narrow, truncate output, batch calls, one audit pass.${headroom}"
else
  echo "[token-economy] local model DOWN — apply in-session discipline: read only needed lines, truncate noisy output, batch calls, validate once, one audit entry.${headroom}"
fi
exit 0
