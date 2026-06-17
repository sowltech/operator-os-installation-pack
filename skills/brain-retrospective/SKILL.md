---
title: Brain Retrospective
slug: brain-retrospective
status: active
inputs:
  - vault root
  - window string (e.g. "14 days ago")
outputs:
  - markdown report on stdout
---

# Brain Retrospective

## Purpose

Produce a read-only Markdown retrospective from the audit log, decisions
folder, and source register inside a vault. The operator reviews the
report and decides which recommendations land.

## Inputs

| Flag | Type | Default |
|---|---|---|
| `--root` | path | `.` |
| `--since` | date string | `14 days ago` |
| `--out` | path | stdout |

## Output standard

Markdown report. Stable section headers:

- Window
- Audit activity
- Action verb breakdown
- Active decisions
- Source register summary
- Recommendations

## Guardrails

- Read-only
- Does not call any AI service
- Does not modify files
- Exits 4 if the window contains zero audit rows and zero decision files

## Success criteria

- Output is well-formed Markdown
- Counts match a manual grep
- Recommendations cite evidence by path or row number
