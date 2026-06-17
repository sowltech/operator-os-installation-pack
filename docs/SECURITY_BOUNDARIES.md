# Security Boundaries

What this pack **is** and **is not** for, from a safety perspective.

## What CLIENT_OPERATOR promises

- The pack contains only generic templates, doctrine, and scripts.
- No real operator vault content is included.
- The validation scripts read files only; they never modify content.
- No external network calls are made by any script in this pack.

## What CLIENT_OPERATOR does not promise

- The pack is not a security product. It does not encrypt, sign, or audit
  client data. It is a knowledge + memory installation pattern.
- The pack does not authenticate or authorise any user. Access control to the
  client vault is the client's responsibility.
- The pack does not guarantee any specific level of context-savings. The
  measurement script reports the actual saving against the actual install.
- The pack does not provide legal, financial, medical, or regulatory advice.

## What the client must do

- Decide where to store the vault.
- Decide who has read and write access.
- Decide what files must never be uploaded to any third-party AI service.
- Maintain backups outside the vault location.
- Apply OS-level updates and disk encryption per the client's own policy.

## What the client must not do

- Do not store passwords, recovery phrases, government IDs, or unencrypted
  keys inside the vault. The vault is a knowledge layer, not a secrets layer.
- Do not paste highly confidential data into third-party AI services without
  explicit written approval from the data owner.
- Do not use this pack as a substitute for an independent security audit.

## Recommended contract clauses

When the install is delivered as a paid service, the contract should
include:

- Scope of work
- Data handling
- Client responsibility for source accuracy
- No guarantee of commercial outcome
- Backup responsibility
- Confidentiality (mutual)
- Payment terms
- Support period
- Change request fees

Specific contract drafting should be reviewed by counsel in the applicable
jurisdiction. This pack is not legal advice.

## Independent audit status

- This pack has **not** been independently security-audited.
- The validation scripts use the Python standard library only.
- The scripts have been static-checked but not fuzz-tested.
- Operators should review the scripts before running them against a client
  vault.

## Reporting issues

If you find a security defect in this pack, contact CLIENT_OPERATOR through
the channel agreed in your service contract. Do not file public issues for
sensitive findings.
