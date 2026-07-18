---
name: operator-os-recall
description: Finds relevant approved vault material and returns bounded source-backed context for Operator OS tasks.
title: Recall
slug: recall
status: active
inputs:
  - vault root
  - query string
outputs:
  - list of matching file paths
---

# Recall

## Purpose

Plain-text recall of vault contents matching a query string. Acts as the
fallback when `obsidian-rag-shortcut-bot` cannot resolve a task category.

## Inputs

- vault root
- query string

## Output standard

- One file path per line on stdout
- Exit 0 even on zero matches; exit non-zero only on input errors

## Guardrails

- Read-only
- Respects `.recallignore` patterns at the vault root
- Stdlib + standard Unix tools only

## Success criteria

- Matches the same files a human running `grep -r` would find
- Does not return binary files or directory listings
- Is safe to invoke from other skills
