# Recall Map

Loaded **first** by any assistant working against this vault. Tells the
assistant which 1–5 pages to load for the task at hand.

## Rule

Never load the whole vault when this map can point at the exact pages.

## Map

| User task | Load these pages | Do not load | Output |
|---|---|---|---|
| Write a sales email | `10_CORE/offers.md`, `20_WORKFLOWS/sales-process.md` | raw source notes | email draft |
| Prepare a client report | `10_CORE/business-profile.md`, `20_WORKFLOWS/delivery-process.md`, the relevant project page | the whole vault | written report |
| Answer a business question | this file, then the exact topic page | unrelated folders | concise answer |
| Update an SOP | the target SOP page, `10_CORE/operating-rules.md` | all other workflows | revised SOP |
| Add a new decision | `decisions/.template.md` | unrelated folders | a new dated decision file |
| Run a retrospective | `90_AUDIT/audit-log.md` (last N entries), recent decision files | older history beyond the window | retrospective report |

## Add your own rows

For every recurring task the client does, add a row above. Two heuristics:

- If the task is performed at least once a week, it earns a row.
- If the task touches more than three files reliably, it earns a row to
  pin which three.

## Audit

Each time this map is materially changed, append a row to
`90_AUDIT/audit-log.md` with action verb `EDIT FILE` and the path of
this file in `target`.
