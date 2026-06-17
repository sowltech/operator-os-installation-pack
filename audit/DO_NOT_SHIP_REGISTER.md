# Do-Not-Ship Register

Categories of asset that must never enter this pack. Every category here
is enforceable by either the sanitisation scanner or operator review.

## 1. Internal audit history

- Any real audit log from an existing operator vault
- Any retrieval log with real measurements
- Any session-start or session-end row with real timestamps

These contain operational intelligence by their nature.

## 2. Active decision artefacts

- Any decision artefact authored by the operator for their own business
- Any decision artefact about commercial strategy
- Any decision artefact about future product direction

The pack ships only the *template* for decisions, never any real
decision content.

## 3. Sovereign control surfaces

- Source code for any product the operator has built and not
  open-sourced
- Configuration files that pin specific operator infrastructure
- Skills that read operator financial data
- Skills that coordinate the operator's specific product loadout

## 4. Personal identifiers

- Operator name
- Operator company name
- Specific client names from prior engagements
- Personal email addresses

## 5. Network topology

- Specific IP addresses or address ranges
- Specific port numbers tied to the operator's local infrastructure
- Specific internal service endpoints

## 6. Model identifiers

- Specific LLM model names tied to the operator's specific loadout
- Specific prompt versions used internally

## 7. Commercial intelligence

- Operator pricing strategy
- Operator target client list
- Operator revenue assumptions
- Operator launch timelines
- Operator product roadmaps

## 8. Internal vault topology

- Real folder names tied to the operator's specific vault structure if
  they encode internal taxonomy
- Real file names that reveal internal organisation

## 9. Assistant configuration

- Operator's global assistant configuration files
- Operator's per-project assistant configuration files
- Memory stores from any assistant

## 10. Repository identifiers

- Specific repo names from the operator's GitHub or other host
- Specific commit identifiers
- Specific release identifiers

## Enforcement

- The scanner enforces categories 4, 5, 6, 7, 8, 9, and 10 by literal
  string match against banned terms.
- Categories 1, 2, and 3 are enforced by operator review during the
  assembly step. The audit log in this pack should always be a
  synthetic example.

## Recovery

If a banned item is discovered in the pack after assembly:

1. Remove the offending content.
2. Re-run the scanner.
3. Re-run the release witness.
4. Re-issue any client copies that were distributed before the fix.

The pack version number should increment on every fix.
