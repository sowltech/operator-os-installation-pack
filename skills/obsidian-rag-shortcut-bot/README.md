# obsidian-rag-shortcut-bot

A small generic helper that turns a folder of Markdown notes into a recall
target an assistant can address quickly.

This skill is **drop-in**. It ships as a folder; the operator copies it
into the client vault under `skills/`.

## What it does

- Reads `00_INDEX/master-index.md` to learn the layout
- Reads `00_INDEX/recall-map.md` to learn task → page mappings
- Prints which 1–5 pages should be loaded for a given task type

It does **not** call any external service. It does not read any file
outside the configured vault root.

## Inputs

- A vault root path (positional argument or `--root`)
- A task category string (e.g. `sales-email`, `client-report`, `decision`)

## Outputs

- A list of file paths to load, on stdout
- Exit 0 on a clean match, exit 2 on no match found

## Use

```
bash skills/obsidian-rag-shortcut-bot/run.sh /path/to/client-vault sales-email
```

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `recall-map.md not found` | vault is not installed | run delivery SOP phase 3 |
| `no match for task <name>` | task not yet mapped | add a row to `recall-map.md` |
| stdout is empty | the matched row has empty page list | edit `recall-map.md` to cite pages |

## What it does not do

- Does not call any AI service.
- Does not parse natural language.
- Does not modify any file.
- Does not produce embeddings.

## Audit

Each run can optionally append a row to the audit log via the operator's
existing convention. See `templates/witness-row-template.md`.
