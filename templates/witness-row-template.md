# Audit Log Row Template

The audit log is a single Markdown file, `90_AUDIT/audit-log.md`. It is
**append-only**. Existing rows are never edited or deleted.

## Canonical shape

Every row uses exactly six pipe-separated cells:

```
| <row-number> | YYYY-MM-DD | <ACTION> | <target> | <details> | <outcome-marker> |
```

- **row-number**: a monotonically increasing integer starting at 1
- **YYYY-MM-DD**: today's date in ISO format
- **ACTION**: one of the canonical action verbs (see below)
- **target**: the file or folder path the action affected, in backticks
- **details**: a short prose description; must not contain a pipe character
- **outcome-marker**: one of `✅` `⚠️` `❌`

## Canonical action verbs

| Verb | When to use |
|---|---|
| CREATE FILE | A new file was added |
| EDIT FILE | An existing file was modified |
| WRITE VAULT | Multiple files were touched in one logical operation |
| DECISION | A decision artefact was added to the decisions folder |
| SESSION START | A working session began |
| SESSION END | A working session ended |
| RECONCILE | Working tree was brought back into a known state |
| APPROVE TOOL | A new tool was added to the allowlist |
| REVOKE TOOL | A tool was removed from the allowlist |
| BUILD CHECK | Validation scripts were run |

A row whose action verb is outside this set is rejected by the validator.

## Outcome markers

- `✅` — the action completed successfully
- `⚠️` — the action completed with a known issue or partial result
- `❌` — the action failed; the row records the failure for the audit
  trail

A row without one of these three markers is rejected by the validator.

## Example rows

```
| 1 | 2026-06-16 | SESSION START | `/path/to/client-vault/` | First install session for CLIENT_COMPANY | ✅ |
| 2 | 2026-06-16 | CREATE FILE | `00_INDEX/master-index.md` | Master index created from template | ✅ |
| 3 | 2026-06-16 | CREATE FILE | `00_INDEX/recall-map.md` | Recall map created with three initial task categories | ✅ |
| 4 | 2026-06-16 | BUILD CHECK | `90_AUDIT/audit-log.md` | Audit row validator ran across three rows; clean | ✅ |
| 5 | 2026-06-16 | SESSION END | `/path/to/client-vault/` | Day one install complete | ✅ |
```

## Rules

1. **Append only.** Never edit or delete a row that has already been
   written.
2. **Inner pipes are forbidden.** The pipe character is the cell separator.
   No pipe may appear inside a cell.
3. **Outcome marker required.** Every row ends with one of the three
   markers.
4. **Today's date only.** Backdating is forbidden. If you missed a row
   yesterday, write today's row noting the lapse.
5. **One row per operation.** Batch operations are recorded as one row
   with `WRITE VAULT` action.

## Validation

Run `scripts/check_audit_row.py --log 90_AUDIT/audit-log.md` after any
append. The validator checks shape, action verb, outcome marker, and
monotonic row numbers. A failure does not delete the bad row — the
operator must append a follow-up row recording the correction.
