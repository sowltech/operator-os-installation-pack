# Governance Overview

The pack ships a small, durable governance pattern. It is **not** a workflow
engine, an approval system, or a SaaS — it is a written convention plus
templates that any organisation can adopt.

## The four primitives

| Primitive | Purpose | Lives in |
|---|---|---|
| Index | Tells the assistant what to load first | `00_INDEX/master-index.md` |
| Recall map | Tells the assistant which pages to load per task type | `00_INDEX/recall-map.md` |
| Decisions folder | Records every non-trivial choice the operator makes | `decisions/` |
| Audit log | Records every action against the vault, append-only | `90_AUDIT/audit-log.md` |

## The propose-vs-execute rule

A non-trivial action is **proposed before it is executed**.

| Step | What happens |
|---|---|
| Propose | The assistant or the operator describes the action, the affected files, the expected outcome |
| Pause | The proposal sits long enough for the operator to read it |
| Execute | The operator (or an explicit instruction from the operator) starts the action |
| Witness | A row is appended to the audit log describing what was actually done |

This rule is enforced by convention, not by code. The convention is durable
because every appended audit row creates a written record.

## Decision artefacts

Use `templates/decision-template.md`. Three things are recorded per
decision:

1. **What was decided.**
2. **Why.**
3. **What the instruction is.**

Each decision file lives in `decisions/<date> <slug>.md` with frontmatter
`type: decision`, `status: active | archived`, `updated: YYYY-MM-DD`.

A decision file is the **only** valid way to record a non-trivial choice.
Posts in chat, notes in a code comment, or verbal agreements are not
durable governance.

## The audit log

Use `templates/witness-row-template.md`. Each row has six pipe-separated
cells:

```
| <row-number> | YYYY-MM-DD | <ACTION> | <target> | <details> | <outcome-marker> |
```

`ACTION` is one of a small canonical set. `outcome-marker` is one of
`✅` (success), `⚠️` (warning / partial), `❌` (failure). The log is
**append-only**. Existing rows are never edited or deleted.

## Why this is enough

- The four primitives cover every observable operation against the vault.
- The conventions are written, not hidden in code.
- No external infrastructure is required — Markdown, a folder layout, and
  small Python validation scripts are sufficient.
- The pattern scales from one user to a small team without redesign.

## Routing classification

Before any non-trivial work, the operator classifies the task by **required
cognitive level** (see `00_INDEX/escalation-matrix.md`). The result is
written into the audit row's `details` cell.

## Where the pack stops

The pack does not include:

- Multi-tenant access control
- Cloud sync
- Real-time collaboration
- Identity management
- Compliance certification

For any of those, integrate the client's existing platform around the vault.
