---
name: token-economy
description: Always-apply token discipline for LLM coding agents. Keeps context small, batches work, avoids re-reads, truncates tool output, and manages context-window headroom so every task spends the fewest tokens without losing the audit trail. Local-model-aware (route mechanical steps to a local LLM when available, apply in-session discipline when not).
---

# Token Economy — Always-Apply Discipline

The goal is not terseness for its own sake. It is to spend the fewest tokens while keeping the
agent aligned to a single source of truth and preserving the audit trail.

## The 7-point protocol (apply every non-trivial task)

1. **Scope before reading.** State the smallest set of files/lines the task needs; read only those.
2. **Locate first, full-read second.** Search/grep to find, then read the top match with an
   explicit line range — not the whole file.
3. **Batch independent work.** Group independent tool calls into one step; group edit + validate +
   log into one bounded pass. One verification pass, not per-step re-checks.
4. **Truncate tool output at the source.** Pipe noisy commands through `head`/`cut`/`tail`/`grep -c`.
   Never let a large dump land in context.
5. **Reuse canonical artifacts.** Cite the existing doc/summary/log entry instead of restating it.
6. **Do not re-derive settled facts.** If it is already in the conversation or a project doc,
   reference it — do not re-read or re-explain.
7. **Single audit pass.** Append one audit entry per bounded unit of work, not one per sub-step.

## Local-model routing (optional)

- **Local model available** (`$LOCAL_LLM_URL` reachable): push mechanical sub-steps (scans, greps,
  status loops, simple classification) to the local model; keep synthesis in the premium session.
- **Local model unavailable:** do not wait on routing. Apply the protocol in-session — because the
  mechanical work now runs in the premium session, discipline matters more, not less.

Probe the compute endpoint itself, not a router/proxy in front of it — a proxy can report healthy
while the model host is down.

## Context headroom (act before the window forces a summarize)

Headroom is the margin before the harness must auto-summarize (a silent, lossy compaction).

- **Green:** work normally.
- **Tightening:** stop re-reading, summarize findings, prefer sub-agents for noisy fan-out.
- **Low:** checkpoint now — one audit entry + a compact handoff (state + next action) so a
  summarize loses nothing, then offload remaining noisy work to a sub-agent or fresh session.

Measure **live** context (bytes since the last compaction boundary in the transcript), not raw
transcript size — the transcript is cumulative and keeps growing after every compaction.

## Finish self-check

- [ ] Read only what was needed (line ranges, not whole files)?
- [ ] Truncated every noisy command?
- [ ] Batched independent calls and validated once?
- [ ] One audit entry?
- [ ] Cited canonical docs instead of restating them?
- [ ] Headroom checked; checkpointed if low?
