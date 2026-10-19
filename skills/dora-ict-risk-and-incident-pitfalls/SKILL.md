---
name: dora-ict-risk-and-incident-pitfalls
description: "Use when engineers or a compliance owner at a financial entity, or at a supplier of ICT services to one, have to prepare for Regulation (EU) 2022/2554 (DORA): deciding whether the entity is in scope, inventorying ICT assets and dependencies, wiring incident detection, classification and reporting records, keeping the register of information on ICT third-party arrangements, and checking the contract provisions with ICT providers."
---

# dora-ict-risk-and-incident-pitfalls

A defensive block for the engineering side of the digital operational resilience regulation: what to
inventory, which records to prepare, what to escalate. The failures are mechanical: the scope question is
assumed instead of asked, the asset inventory is a spreadsheet nobody updates, incidents are logged without the
fields a classification needs, the register of information lists vendors but not functions, and a contract
is signed without the clauses the text lists. The only legal text read for this block is Regulation (EU)
2022/2554 as published in the Official Journal, Articles 2 to 6, 8 to 14, 17 to 20, 28 to 30.
application date. Whether an entity is in scope, which duty applies to it, which incident is "major", and any
deadline or threshold set by technical standards, are decisions of counsel or the entity's compliance
function. Related blocks: `business/fintech-compliance` for the wider sector, `business/vendor-management` for
the generic vendor lifecycle, `business/regulatory-watch` for dating and sourcing a legal statement. This
block is a working method for qualified people, not legal advice.

## When
- A company supplies software or hosting to a bank, payment firm, insurer or similar entity and receives DORA
  questions or contract clauses.
- A financial entity starts an inventory, an incident process, a register or a contract review for DORA.
- An incident happened and someone asks whether and what to report.
- A vendor is about to be onboarded for a service a financial entity depends on.

## Steps

**Read only the part the task meets.** Part 1 first when nobody has settled whether the entity is in scope.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Scope question and ICT risk-management framework: who is in scope, proportionality, governance, inventory, change, detection, continuity, backup, learning | scope is unclear, or a framework duty is mapped to engineering work | [`01-scope-and-ict-risk-framework.md`](./references/01-scope-and-ict-risk-framework.md) |
| 2 | Incident management and reporting: recording, classification criteria, notification stages, client information, outsourcing the reporting | an incident process is built, tested or an incident is under way | [`02-incident-management-and-reporting.md`](./references/02-incident-management-and-reporting.md) |
| 3 | Third-party risk: register of information, pre-contract checks, contract provisions, exit, concentration | a vendor is onboarded, a register is built, or a contract is reviewed | [`03-register-and-contract-provisions.md`](./references/03-register-and-contract-provisions.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For each entity, system or contract under review: the scope question
asked with its owner (counsel or compliance function), the inventory of functions, assets and providers with
a last-updated date, the incident record fields available against the classification criteria read, the
register rows with the critical-or-important flag decided by a named person, and the contract checklist with
a present or missing mark per clause. Everything marked "not legal advice, escalate to counsel or the
compliance function" is a question with an owner, not a conclusion.

## Guardrails
- Not legal advice. This block does not replace a lawyer or the entity's compliance function; escalate to
  counsel or the compliance function every scope, applicability and "is it major" question.
- Never state a duty without having read the article it comes from (parts 1 to 3 cite them).
- Never give a deadline, a threshold or a template layout from memory: the reporting time limits, the
  materiality thresholds and the register templates are set by technical standards that were not read; look
  them up in the current text and ask the compliance function.
- Never decide alone that a function is critical or important, or that an incident is major (parts 2 and 3).
- Never paste client data, incident evidence or a real contract into a prompt, ticket or fixture.
- A supplier never assumes the regulation does not concern it because it is not itself listed: its client's
  duties reach it through the contract (part 3).

## Origin
Legal statements from Regulation (EU) 2022/2554, read on EUR-Lex 2026-10-19; the rest is our own guidance,
flagged as such. The full provenance, what was removed and what was not verified are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
