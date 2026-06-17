# Example Skill — Recall First

## Purpose

Demonstrate the recall-first pattern as an installable skill.

## Inputs

- the user's task
- master index
- recall map
- the relevant target pages only

## Retrieval protocol

1. Read `00_INDEX/master-index.md`.
2. Identify the task category.
3. Use `00_INDEX/recall-map.md` to choose pages.
4. Load no more than five pages unless the task is explicitly an audit.
5. Summarise the loaded context before execution.
6. Produce the requested output.
7. Append an audit row if the vault state changed.

## Output standard

- Clear answer first
- Evidence from loaded pages only
- Action steps
- Files changed, if applicable
- Risks or missing data

## Guardrails

- Do not invent missing facts.
- Do not load unrelated folders.
- Do not overwrite existing pages without an audit row noting the change.
