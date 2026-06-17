# Operator OS Installation Pack

A client-safe pack of generic templates, doctrine, validation scripts, skills,
and delivery checklists for installing a knowledge + decision + audit
operating system inside an existing organisation.

This pack contains **no proprietary operator content**. All content has been
sanitised to remove organisation names, vault paths, model identifiers,
network topology, internal product names, and commercial intelligence.

## What this pack is

A **drop-in toolkit** for delivering an *Operator OS Installation* — a
structured way to give a client:

- A bounded **knowledge layer** (vault structure, recall doctrine)
- A **memory layer** (append-only audit log with a canonical row shape)
- A **routing layer** (where each task is classified before work begins)
- A **governance layer** (a written decisions folder with a stable convention)
- A **skills layer** (small, composable, on-demand operator helpers)
- A **delivery + measurement layer** (install SOP and a context-savings script)

## What this pack is not

- Not a SaaS.
- Not a hosted product.
- Not a software framework.
- Not an LLM agent.
- Not a "brain" — it is a *pattern* for a knowledge OS, not a knowledge graph itself.

## Folder map

```
operator-os-installation-pack/
├── README.md                           ← this file
├── LICENSE                             ← MIT
├── docs/                               ← client-facing delivery docs
├── templates/                          ← copy-paste templates
├── skills/                             ← installable skill folders
├── scripts/                            ← validation + measurement tools
├── examples/demo-client-vault/         ← skeleton example install
└── audit/                              ← sanitisation register + release witness
```

## Install path

Follow `docs/DELIVERY_SOP.md`. The high level is:

1. Intake — `docs/CLIENT_ONBOARDING.md` collects scope.
2. Structure — copy `examples/demo-client-vault/` into the client environment.
3. Templates — install the six templates under `templates/` into the client's
   `00_INDEX/`, `decisions/`, `40_PROMPTS_SKILLS/`, and `90_AUDIT/` folders.
4. Skills — copy the five skill folders into the client's `skills/` directory.
5. Validate — run `scripts/check_audit_row.py` (the audit row validator) to
   prove the install is well-formed.
6. Measure — run `scripts/measure_vault.py` to record the context-savings
   baseline.
7. Handover — train the client per `docs/DELIVERY_SOP.md` phase 7.

## Boundaries

This pack includes **no real operator data**. It includes only generic
templates and reusable methods. Sanitisation history is in
`audit/SANITIZATION_REGISTER.md`. The list of artefact types deliberately
excluded is in `audit/DO_NOT_SHIP_REGISTER.md`.

## Licence

MIT. See `LICENSE`.
