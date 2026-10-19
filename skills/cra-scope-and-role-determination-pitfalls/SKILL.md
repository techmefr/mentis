---
name: cra-scope-and-role-determination-pitfalls
description: "Use when engineers and a compliance owner must work out whether and how Regulation (EU) 2024/2847 (Cyber Resilience Act) applies to a product: the product-with-digital-elements definition and exclusions, the manufacturer, importer, distributor and open-source steward roles, open-source and non-commercial supply, the class question, what to inventory (products, components, SBOM, support period), what to record and what to escalate. Not legal advice."
---

# cra-scope-and-role-determination-pitfalls

A method block for the question that comes before every Cyber Resilience Act task: does the Regulation apply to
this product, and in what role are we. The failures are mechanical: scope decided per company instead of per
product, "free, so out", a rebrand that quietly makes the reseller a manufacturer, open-source dependencies absent
from the inventory, a support period nobody decided. The text read is Articles 2, 3, 4, 7, 8, 13 and 18 to 25 of
Regulation (EU) 2024/2847 as published; every duty is stated only after reading its article and is marked
re-read before relying. The annexes, the application dates (Article 71) and national rules were not read. The
reporting duty is in `skills/cra-exploited-vulnerability-clock`. This block does not replace a lawyer and never
concludes that something is or is not in scope.

## When
- A product is about to launch, be rebranded, resold, integrated or published as open source.
- Someone asks "does the CRA apply to us" or states a role or a duty from memory.
- A product register, SBOM practice or support-period policy is designed.

## Steps

**Read only the part the task meets.** Part 1 first.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Product definition, connection, intended purpose, on the market, exclusions, substantial modification | a scope question is asked | [`01-does-it-apply.md`](./references/01-does-it-apply.md) |
| 2 | Manufacturer, importer, distributor, authorised representative, role changes, chain evidence | we ship, resell, rebrand or modify | [`02-economic-operator-roles.md`](./references/02-economic-operator-roles.md) |
| 3 | Open-source consumption and publication, steward flag, non-commercial supply, class question | open source is involved or the category is asked | [`03-open-source-and-class.md`](./references/03-open-source-and-class.md) |
| 4 | Register fields, components and SBOM, support-period decision, re-run triggers, escalation package | the determination becomes a register | [`04-inventory-record-escalate.md`](./references/04-inventory-record-escalate.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). The output is a per-product determination note: product, facts
gathered, definitions and exclusions considered with the sentence read and the read date, role per flow, open
questions, class candidate, register entry, and counsel's answer with name and date once received. Evidence is
a register row traced to the article sentences. Every output ends with: not legal advice, escalate to counsel.

## Guardrails
- Not legal advice. This block does not replace a qualified lawyer; escalate to counsel before any scope, role
  or class conclusion is recorded as settled.
- Never state a duty without having read its article in the current text; mark it re-read before relying.
- Never state a date or deadline from memory; Article 71 is read only when cited, and counsel confirms.
- Never reason from the company: scope and role are per product and per flow (parts 1, 2).
- Never treat "free of charge" or "open source" as an exemption by itself (part 3).
- Annexes, harmonised standards, national authorities and amendments were not read: say so.
- Do not paste confidential contracts or customer data into a prompt or ticket.

## Origin
Articles of Regulation (EU) 2024/2847 on EUR-Lex, read 2026-10-19, restated in our words; the per-product
register and escalation package are our own guidance. Provenance, removals and unverified points:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
