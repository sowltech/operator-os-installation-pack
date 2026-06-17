# full-stack-testing

Generic test enforcement helper for a small codebase. Invokes whatever
test runner the target repo defines and prints a structured pass/fail
summary.

## What it does

- Detects which test runner is available (pytest, npm test, cargo test,
  go test, make test)
- Runs it
- Prints exit status and a short summary

## What it does not do

- Does not write tests
- Does not modify any file
- Does not install dependencies

## Use

```
bash skills/full-stack-testing/run.sh /path/to/target-repo
```

## Order of discovery

1. `make test` if `Makefile` has a `test:` target
2. `pytest` if a `tests/` folder exists
3. `npm test` if a `package.json` exists
4. `cargo test` if a `Cargo.toml` exists
5. `go test ./...` if a `go.mod` exists

The first match wins. The runner that wins is reported on stdout.
