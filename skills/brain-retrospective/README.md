# brain-retrospective

On-demand retrospective for the operator. Reads the audit log, the
decisions folder, and the source register, and emits a structured
Markdown report.

## What it reads

| Source | Default path |
|---|---|
| Audit log | `<vault>/90_AUDIT/audit-log.md` |
| Decisions | `<vault>/decisions/` |
| Source register | `<vault>/30_KNOWLEDGE/source-register.md` |
| Retrieval log | `<vault>/90_AUDIT/retrieval-log.md` |

All paths can be overridden via flags.

## What it does

- Counts rows in the audit log inside the configured window
- Reports the action-verb breakdown
- Lists active decisions and any with activation criteria
- Reports source-register status counts
- Emits up to five tagged recommendations

## What it does not do

- Does not modify any file
- Does not run on a schedule
- Does not call any AI service
- Does not collect metrics into a database

## Use

```
bash skills/brain-retrospective/run.sh \
    --root /path/to/client-vault \
    --since "14 days ago"
```

## Output sections

1. Window
2. Audit activity
3. Action verb breakdown
4. Active decisions
5. Source register summary
6. Recommendations (max 5, each tagged `[concept] [witness] [decision] [archive]`)

## Cadence

Operator-triggered. Run after a release, at end-of-week, after a routing
override, or whenever the operator types the retrospective command.
**No cron. No background process.**
