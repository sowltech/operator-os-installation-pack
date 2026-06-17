# Sanitisation Register

A record of what was sanitised when this pack was assembled. Read this
before you trust the pack to be client-safe.

## Methodology

Every text file under the pack root is scanned by `scripts/sanitize_scan.py`
against a fixed list of banned terms. The scan fails if any banned term
appears anywhere in the scanned content.

## Categories of sanitisation applied

### Identifiers replaced with placeholders

- Operator and company names were not included in source content.
  Where a placeholder was needed, `CLIENT_OPERATOR` and `CLIENT_COMPANY`
  were used.
- Internal product / system names were not included in source content.

### Vault paths replaced with placeholders

- All real vault paths were replaced with `/path/to/client-vault/` style
  placeholders.
- Internal folder names (numbered prefix folders for HQ, agents, decisions
  with specific numeric prefixes) are not used — generic equivalents like
  `decisions/` and `90_AUDIT/` were used instead.

### Network topology removed

- No specific IP address ranges, host names, or port numbers appear in
  shipped content.

### Model identifiers removed

- No specific LLM model names appear in shipped content.

### Wikilinks removed

- No `[[wikilinks]]` to internal pages are present in shipped content.
- Plain Markdown links use relative paths inside the demo vault example
  only.

### Tags removed

- No internal taxonomy tags appear in shipped content.

### Commercial intelligence removed

- No pricing tables, target client lists, revenue assumptions, launch
  timelines, or commercial roadmaps appear in shipped content.

### Code artefact references removed

- No specific repo names, commit identifiers, or release identifiers
  appear in shipped content.

### Internal log file names removed

- No reference to specific internal log file names appears in shipped
  content. The audit log in the demo vault is called `audit-log.md` and
  the retrieval log is called `retrieval-log.md`.

## Enforcement

The check is automated. To verify, run:

```
python3 scripts/sanitize_scan.py --root .
```

Exit 0 means the scan found nothing to flag. Exit 1 means a banned term
was found and must be removed before the pack can be shipped.

## Adding a banned term

Edit `scripts/sanitize_scan.py` and append to `BANNED_TERMS`. Re-run the
scan. The scan will pick up the new term on the next run.

## Adding an allowlist entry

If a file legitimately needs to mention a term that is otherwise banned
(for example, this register's own enforcement section), add a glob
pattern to `.scan-allowlist` at the pack root. The scanner skips matching
files.
