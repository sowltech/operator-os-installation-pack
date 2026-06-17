---
title: Full Stack Testing
slug: full-stack-testing
status: active
inputs:
  - target repo path
outputs:
  - pass/fail summary
---

# Full Stack Testing

## Purpose

Detect the available test runner in a repo and run it. Provide a uniform
exit code so callers can chain checks.

## Inputs

- target repo path

## Output standard

One line stating which runner was selected. The runner's normal output
follows. Exit 0 on pass, exit non-zero on failure.

## Guardrails

- Does not modify any file
- Does not install or upgrade dependencies
- Exits 1 if no runner is detected

## Success criteria

- Runner is selected correctly
- Exit code reflects underlying runner's verdict
