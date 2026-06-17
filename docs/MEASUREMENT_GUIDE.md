# Measurement Guide

How to measure the **context-savings** achieved by an index-first recall
pattern, against the *same* vault loaded whole.

## The hypothesis

If the assistant loads the entire vault for every task, it spends tokens
that do not contribute to the answer. If the assistant loads only the
index plus 1–5 targeted pages per task, the same answer is produced from
a dramatically smaller context window.

This guide tells the operator how to measure that gap honestly.

## The script

`scripts/measure_vault.py` is a small Python file that:

1. Counts the words in every Markdown file under the vault.
2. Counts the words in the selected file(s) the assistant would actually
   load for a given task.
3. Reports the difference as a percentage saving.

It uses only the Python standard library. It does not call any external
service. It does not modify any file.

## Usage

```
python3 scripts/measure_vault.py /path/to/client-vault \
    /path/to/client-vault/00_INDEX/master-index.md \
    /path/to/client-vault/00_INDEX/recall-map.md
```

Output looks like:

```
Whole vault words: 105,000
Selected words: 7,000
Estimated saving: 93.3%
```

## What the number means

- It is an **upper bound** on context savings. The real saving depends on
  the assistant's tokenisation, prompt overhead, and how the operator
  actually formulates queries.
- It is **not** a guarantee of cost savings in any specific assistant
  service.
- It is **valid for comparison** within a single install. Running the
  script before and after a vault re-organisation is a meaningful
  measurement of structural improvement.

## What the number does not mean

- It does not predict latency.
- It does not predict answer quality.
- It does not predict whether the assistant will recall the right page —
  that is a function of the `recall-map.md` quality.

## Recording results

Append a row to `90_AUDIT/retrieval-log.md` for each measurement:

```
| Date       | Task             | Pages loaded | Whole-vault words | Loaded words | Saving | Notes |
|------------|------------------|--------------|------------------:|-------------:|-------:|-------|
| YYYY-MM-DD | <example task>   | <list>       |           105,000 |        7,000 |  93.3% |       |
```

This row is **not** an audit row in the formal sense — it is a measurement
log. The format is intentionally similar so operators can read both with
the same eye.

## Cadence

- **Baseline**: run once at install (Phase 6 of `DELIVERY_SOP.md`).
- **Quarterly**: run again to check whether vault growth has affected the
  saving.
- **Ad-hoc**: run after any major restructure.

## Honesty

If the saving number drops below a previously recorded level, the operator
must record the drop, not hide it. The retrieval log is **append-only**
just like the audit log.
