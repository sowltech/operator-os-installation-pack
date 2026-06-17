# Retrieval Log

Records every measurement of context savings produced by
`scripts/measure_vault.py`.

The log is **append-only**. Historical rows are never edited or deleted.

## Format

| Date | Task | Pages loaded | Whole-vault words | Loaded words | Saving | Notes |
|---|---|---:|---:|---:|---:|---|
| YYYY-MM-DD | example task | `master-index.md`, `recall-map.md` | 105,000 | 7,000 | 93.3% | baseline at install |

## Rules

1. **One row per measurement.** Do not batch.
2. **Today's date only.** Do not backdate.
3. **Cite the pages loaded.** "Loaded words" without "pages loaded" is
   meaningless.
4. **Note context.** The Notes column should record whether this was a
   baseline, a quarterly check, or an ad-hoc measurement, and any change
   in vault size since the last row.

## Cadence

- Baseline at install.
- Quarterly.
- Ad-hoc after any major restructure.

## Honesty

If a measurement shows a worse result than a previous row, record it.
The log is the audit trail of the vault's structural health, not a
marketing surface.
