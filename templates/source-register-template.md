# Source Register

Tracks every external source ingested into the knowledge layer. Lives at
`30_KNOWLEDGE/source-register.md`.

## Format

| Date ingested | Source title | Source location | Local path | Status | Notes |
|---|---|---|---|---|---|
| YYYY-MM-DD | example source | url, document title, or human source | `30_KNOWLEDGE/source-notes/<slug>.md` | active | initial intake |

## Status values

| Status | Meaning |
|---|---|
| active | the source is referenced from concept or workflow pages |
| dormant | the source has not been cited in 90 days |
| archived | the source has been moved out of the live knowledge layer |
| rejected | the source was reviewed and not adopted; kept for audit |

## Rules

1. **Append only.** Existing rows are never edited or deleted.
2. **Cite specifically.** A row without a clear source location and a
   local path cannot be reused.
3. **Status updates are new rows.** If a source moves from active to
   archived, write a new row recording the move; do not edit the original.

## Maintenance

A row marked dormant for 180 days is a candidate for archive. The audit
log records the move with action verb `WRITE VAULT` and a brief reason.
