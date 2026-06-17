# Release Witness

A short, dated record of when this pack was assembled and what it contained
at that moment. Fill out before distribution.

## Release identity

- Pack name: Operator OS Installation Pack
- Version: 0.1.0
- Release date: YYYY-MM-DD
- Assembled by: CLIENT_OPERATOR
- Intended audience: paying clients commissioning an Operator OS Installation

## Pre-release checks

- [ ] `python3 scripts/sanitize_scan.py --root .` exited 0
- [ ] `python3 -m py_compile scripts/*.py` exited 0
- [ ] All Markdown files render in a standard previewer
- [ ] All shell scripts pass `bash -n`
- [ ] The demo vault skeleton round-trips through
      `python3 scripts/check_audit_row.py --log examples/demo-client-vault/90_AUDIT/audit-log.md`

## Contents at release

- 1 LICENSE (MIT)
- 1 README
- 5 docs in `docs/`
- 6 templates in `templates/`
- 5 skills in `skills/` (each with README + SKILL + run.sh)
- 3 scripts in `scripts/`
- 1 demo vault skeleton in `examples/demo-client-vault/`
- 3 audit registers in `audit/`

## What was excluded

See `audit/DO_NOT_SHIP_REGISTER.md`.

## What was sanitised

See `audit/SANITIZATION_REGISTER.md`.

## Distribution

- Recipient: <name of client>
- Method: <how the pack was delivered: zip, repo invite, secure share>
- Date: YYYY-MM-DD

## Post-release

If a defect is discovered after distribution, log it here:

| Date | Defect | Fixed in version | Recipients re-issued |
|---|---|---|---|
|  |  |  |  |

## Sign-off

- Operator signature: ____________________
- Date: ____________________
