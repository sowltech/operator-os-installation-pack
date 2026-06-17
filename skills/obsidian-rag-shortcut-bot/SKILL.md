---
title: Obsidian RAG Shortcut Bot
slug: obsidian-rag-shortcut-bot
status: active
inputs:
  - vault root path
  - task category string
outputs:
  - list of page paths to load
---

# Obsidian RAG Shortcut Bot

## Purpose

Turn the operator's recall map into a one-shot lookup: given a task
category, return the file paths the assistant should load.

## Inputs

| Name | Type | Required |
|---|---|---|
| vault root | path | yes |
| task category | string | yes |

## Retrieval protocol

1. Verify `<vault-root>/00_INDEX/recall-map.md` exists.
2. Find the row whose first cell matches the task category.
3. Print the page list from the second cell.
4. Exit 0 on success, exit 2 if no match.

## Output standard

- One path per line on stdout.
- No prose, no logging, no warnings on the happy path.
- All warnings on stderr.

## Guardrails

- Do not read any file outside the configured vault root.
- Do not modify any file.
- Do not call any external service.
- Do not embed, hash, or summarise content.

## Success criteria

- Match returns the expected pages.
- Empty match exits with a clear stderr message.
- The skill is safe to run in a loop.
