# Escalation Matrix

A small, durable taxonomy for deciding **what cognitive level a task
requires** before work begins. Used to keep simple tasks small and to
lift complex tasks to the right altitude.

## Cognitive levels

| Level | Question | Use for |
|---|---|---|
| 1 | What should be said? | Writing, content, formatting |
| 2 | What information is required? | Research, retrieval, intake |
| 3 | What must persist? | Notes, decisions, audit rows |
| 4 | What capabilities are required? | Tool selection, skill choice |
| 5 | What sequence creates the outcome? | SOPs, workflows |
| 6 | How should knowledge be organised? | Taxonomies, recall maps |
| 7 | What reality governs this task? | Businesses, ecosystems, markets |
| 8 | How should intelligence itself be structured? | Planning, governance design |
| 9 | How does this improve itself? | Retrospectives, feedback loops |
| 10 | How do multiple intelligences cooperate? | Human + AI collaboration patterns |

Use the **minimum** level that still satisfies the task. Most tasks live
at levels 1–3.

## Triggers

| Trigger | Lifts to |
|---|---|
| The task requires more than three distinct operations | 4–5 |
| The task touches two or more business domains | 6–7 |
| The task references two or more named projects | 7 |
| The outcome is referenced by an open commitment more than seven days in the future | 5–6 |
| The decision requires written approval, not just acknowledgement | 8 |
| The change modifies a foundational rule or convention | 8 |
| The result must persist across future sessions | at least 3 |
| The task is a meta-review of past work | 9 |
| The task involves the operator plus more than one assistant plus shared infrastructure | 10 |

## Demotions

Demote (stay at a lower level) when:

- A trigger fires but the work fits inside an existing template, SOP, or
  doctrine page.
- A trigger fires but only one component has unresolved questions —
  handle the single component at its native level.
- A trigger fires but the change is purely cosmetic.
- The operator describes the task as quick or small and no complexity
  trigger contradicts that.

## How this connects to routing

After classification, the operator chooses the runtime route:

| Level | Suggested execution surface |
|---|---|
| 1–2 | A fast assistant, locally if available |
| 3–5 | A general-purpose assistant, locally if available |
| 6–7 | A reasoning-capable assistant, possibly remote |
| 8–10 | The most capable assistant available, with explicit operator approval |

The runtime choice is recorded in the audit log row's `details` cell.

## Evidence sources

Triggers are evaluated against the four primitives of the vault:

| Primitive | Purpose |
|---|---|
| Audit log | Past work and decisions, with row numbers |
| Decisions folder | Active and archived decisions |
| Open commitments folder | Anything referenced as a future obligation |
| Project records folder | Active project state |

No separate escalation log is required. The audit log is the trail.
