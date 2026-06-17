---
title: DevSecOps Release
slug: devsecops-release
status: active
inputs:
  - target repo path
outputs:
  - structured pass/fail report
---

# DevSecOps Release

## Purpose

Refuse to release until the standard discipline checks pass. Lint, test,
clean tree, fresh changelog.

## Inputs

- target repo path

## Output standard

One line per check, prefixed `[ok]` or `[FAIL]`. Exit 0 on all pass, exit 1
on any failure.

## Guardrails

- Read-only against the repo
- Does not push, tag, or modify
- Honours `.devsecops-skip` file for explicit per-check skip

## Success criteria

- All four checks pass
- Output is machine-parseable
