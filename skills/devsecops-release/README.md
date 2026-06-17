# devsecops-release

Generic release discipline helpers for a small codebase. Runs lint, tests,
and a pre-publish checklist. Refuses to advance if any check is missing.

## What it does

- Runs whatever lint / format / static check the target repo defines via
  a `Makefile` target named `lint`
- Runs whatever test target is named `test`
- Verifies a `CHANGELOG.md` exists and has been updated within N days
- Refuses to advance if the working tree is dirty

## What it does not do

- Does not build artefacts
- Does not push to any remote
- Does not modify any file
- Does not require any specific language toolchain

## Use

```
bash skills/devsecops-release/run.sh /path/to/target-repo
```

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `no Makefile target named 'lint'` | repo doesn't define one | add one, or pass `--skip-lint` |
| `working tree dirty` | uncommitted changes | commit or stash before release |
| `changelog stale` | last edit >30 days | update the changelog |
