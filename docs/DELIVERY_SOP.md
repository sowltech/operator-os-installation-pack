# Delivery SOP — Operator OS Installation

A repeatable, generic install procedure for a knowledge + memory + governance
operating system inside a client environment.

## Phases

| Phase | Action | Done when |
|---|---|---|
| 1 | Intake | Scope written and counter-signed using `docs/CLIENT_ONBOARDING.md` |
| 2 | Structure | Vault folders created from `examples/demo-client-vault/` |
| 3 | Templates | Six templates from `templates/` placed into the client vault |
| 4 | Skills | Five skill folders from `skills/` copied into the client vault |
| 5 | Validate | `scripts/check_audit_row.py` passes against the empty audit log |
| 6 | Measure | `scripts/measure_vault.py` records the context-savings baseline |
| 7 | Handover | Client completes one live task end-to-end |

## Phase 1 — Intake

Use `docs/CLIENT_ONBOARDING.md`. Do not skip sections. Sign-off is required
before any folder is created on the client machine.

## Phase 2 — Structure

Copy the `examples/demo-client-vault/` folder into the client's chosen
location (`/path/to/client-vault/`). Verify the folder tree matches.

## Phase 3 — Templates

For each of the six templates under `templates/`:

| Template | Install location inside client vault |
|---|---|
| `recall-map-template.md` | `00_INDEX/recall-map.md` |
| `retrieval-log-template.md` | `90_AUDIT/retrieval-log.md` |
| `source-register-template.md` | `30_KNOWLEDGE/source-register.md` |
| `decision-template.md` | `decisions/.template.md` |
| `witness-row-template.md` | `90_AUDIT/audit-log.md` (header only) |
| `escalation-matrix-template.md` | `00_INDEX/escalation-matrix.md` |

## Phase 4 — Skills

Copy each of the five skill folders from `skills/` into the client vault's
`skills/` directory. Verify each skill's `run.sh` is executable.

## Phase 5 — Validate

```
python3 scripts/check_audit_row.py --log /path/to/client-vault/90_AUDIT/audit-log.md
```

Expect: zero rows in window. Exit 0. (A fresh install has no audit rows; the
validator should not fail on an empty log.)

## Phase 6 — Measure

```
python3 scripts/measure_vault.py /path/to/client-vault \
    /path/to/client-vault/00_INDEX/recall-map.md
```

This produces the baseline saving percentage. Record it in
`90_AUDIT/retrieval-log.md` row 1.

## Phase 7 — Handover

- Walk the client through `00_INDEX/recall-map.md`.
- Show them how to run one skill from `skills/`.
- Show them how to append a row to `90_AUDIT/audit-log.md` using the
  template in `templates/witness-row-template.md`.
- Show them how to author one decision file using
  `templates/decision-template.md`.
- Schedule the first retrospective using `skills/brain-retrospective/`.

## Handover checklist

- [ ] Vault opens cleanly
- [ ] `00_INDEX/master-index.md` lists all installed pages
- [ ] `00_INDEX/recall-map.md` maps tasks to pages
- [ ] At least three workflows captured (the three the client identified
      in onboarding §3)
- [ ] At least three skills installed
- [ ] Context-savings baseline recorded
- [ ] Client has a one-page start guide
- [ ] Client understands what must never be uploaded to external AI
- [ ] Backup / export plan agreed in writing
