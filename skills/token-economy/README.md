# Token Economy — always-on token discipline for LLM coding agents

A drop-in skill + hook that makes an LLM coding agent spend the fewest tokens per task without
losing its audit trail. Two parts:

- **`SKILL.md`** — the always-apply protocol: scope-before-reading, locate-first, batch, truncate
  output, reuse canonical artifacts, single audit pass, plus a **context-headroom** policy.
- **`token_economy_guard.sh`** — an always-run hook. On every non-trivial prompt it injects one
  compact line reminding the agent to (a) route mechanical steps to a local model when one is up,
  or apply in-session discipline when not, and (b) checkpoint before the context window forces a
  lossy summarize.

## Install

1. Copy `token_economy_guard.sh` into your agent's hooks directory and make it executable.
2. Register it on the agent's `UserPromptSubmit` event.
3. (Optional) point it at your local model: `export LOCAL_LLM_URL=http://127.0.0.1:11434/api/tags`.
4. Add `SKILL.md` to your agent's skills so the full protocol is available on demand.

## Configuration (env)

| Variable | Default | Meaning |
|---|---|---|
| `LOCAL_LLM_URL` | `http://127.0.0.1:11434/api/tags` | Local model endpoint to probe (probe the model, not a proxy) |
| `TOKEN_ECONOMY_TTL` | `120` | Seconds to cache the reachability probe |
| `TOKEN_ECONOMY_HEADROOM_WARN_KB` | `500` | Live-context KB at which to start tightening |
| `TOKEN_ECONOMY_HEADROOM_CRIT_KB` | `1000` | Live-context KB at which to checkpoint |

## Design notes

- The hook carries **no doctrine body** — it points at the skill so the canonical text is never
  duplicated.
- Headroom is measured as **bytes since the last compaction boundary** in the transcript, not raw
  transcript size (which is cumulative and keeps growing after every compaction).
- Fail-safe: the hook never blocks a prompt and always exits 0.

MIT licensed. Part of the Operator OS Installation Pack.
