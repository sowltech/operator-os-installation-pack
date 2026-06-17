# recall

A small generic helper that searches the configured vault for a query
string and prints matching file paths.

## What it does

- Performs a case-insensitive plain-text search across `.md` files
- Returns matching file paths, one per line
- Honours a `.recallignore` file at the vault root for excluded patterns

## What it does not do

- Does not call any external service
- Does not produce embeddings
- Does not rank by semantic similarity
- Does not modify any file

## Use

```
bash skills/recall/run.sh /path/to/client-vault "client onboarding"
```

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `vault root not found` | wrong path | check spelling, run from any directory using an absolute path |
| zero matches | query string not present | broaden query, or check `.recallignore` for over-exclusion |

## Performance

`grep -r` semantics. Linear in vault size. Acceptable for vaults under
about 50,000 files.
