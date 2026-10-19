---
name: ai-act-obligations-and-omnibus-status-pitfalls
description: "Use when an engineering or compliance owner prepares for Regulation (EU) 2024/1689 (AI Act): establishing which amending acts are in force and which application dates currently apply before relying on any date, the role question for counsel (provider, deployer, importer, distributor), risk-class triage (prohibited practices, high-risk, transparency duties, general-purpose models) and the inventory and records to keep. Not legal advice."
---

# ai-act-obligations-and-omnibus-status-pitfalls

A method block for the engineering and compliance side of a regulation whose application dates were staged in the
original text and then moved by an amending act. The risks are practical: a date quoted from memory or from a
proposal, a role assumed by engineering, an AI system that nobody classified, and a duty recorded nowhere. The texts
read are Regulation (EU) 2024/1689 (Articles 2, 3, 4, 5, 6, 25, 49, 50, 51, 53, 113 and Annex III as headed), the
Commission proposal COM(2025) 836 of 19.11.2025 (Digital Omnibus on AI), and the amending Regulation (EU) 2026/1744 of
8 July 2026 published on 24.07.2026. **Which role the organisation has, which class a system falls in, and how any
borderline case reads were not decided here and are for counsel.** This block is a working method, not legal advice,
and it does not replace a lawyer. Dating and sourcing a legal statement is in `business/regulatory-watch` and
`skills/source-freshness`.

## When
- Someone states an AI Act date, duty or fine from memory, or from news about "the omnibus".
- A feature uses, embeds or resells a model or AI system and someone asks whether the regulation applies.
- A product inventory, a risk register or a supplier review is built or changed in a possibly covered organisation.
- A system is about to be launched, renamed, rebranded, retrained for a new purpose, or sold to a new customer type.

## Steps

**Read only the part the task meets.** Part 1 before any date or duty is written down; the others as the work needs
them.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The staged dates, the proposal versus the act adopted, what was read and what to re-read | any date, deadline or "is it in force" is about to be stated or planned | [`01-status-and-dates.md`](./references/01-status-and-dates.md) |
| 2 | Scope and the role question (Articles 2, 3, 25), questions for counsel | someone asks whether the regulation applies or who bears a duty | [`02-scope-and-roles.md`](./references/02-scope-and-roles.md) |
| 3 | Risk-class triage (Articles 5, 6, 50, 51, 53) and what to inventory and record | systems are listed, classified, or a gap list is built | [`03-triage-and-inventory.md`](./references/03-triage-and-inventory.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). The output is a short readiness note: the status of the amending act and the
date it was read, the application dates relied on each marked "re-read before relying", the role question put to
counsel and its answer with date and name, the inventory of AI systems and models with owner, intended purpose and
class as provisionally triaged, the transparency and literacy measures with their evidence location, and the open
questions. **Not legal advice: the note is escalated to counsel before anyone relies on it.**

## Guardrails
- This block does not replace advice from a qualified lawyer; it never states that the organisation is, or is not, a
  provider or deployer, or that a system is or is not high-risk or prohibited. Not legal advice, escalate to counsel.
- Establish the current status of the amending acts from official sources read in the session before relying on any
  date; a proposal is not law, and a text adopted last month may itself have been amended since.
- Give a date only if it was read in the Official Journal text and mark it "re-read before relying".
- Never classify a borderline case; list it as an open question for counsel.
- Do not file, register or tell anyone a duty exists on the strength of this block.

## Origin
Regulation (EU) 2024/1689, COM(2025) 836 and Regulation (EU) 2026/1744 read 2026-10-19. Provenance, what was removed
and what was not verified are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
