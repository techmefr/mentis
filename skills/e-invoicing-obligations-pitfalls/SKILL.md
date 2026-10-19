---
name: e-invoicing-obligations-pitfalls
description: "Use when engineers and a finance or compliance owner have to prepare for structured electronic invoicing in the EU: inventorying invoice flows, formats, platforms and archiving, reading the EU-level rules of Directive (EU) 2025/516 (VAT in the digital age), finding what the national authority currently requires, asking the accounting adviser the right questions, and keeping a dated record of the format and platform decision and its test."
---

# e-invoicing-obligations-pitfalls

A defensive block for the engineering and finance side of structured e-invoicing: what to inventory, what to ask,
which records to keep, what to escalate. The failures are mechanical: "we send PDFs by email" is assumed to be
an electronic invoice, the EU text is taken for the national rule, a national date from a blog is built into a
roadmap, a platform is chosen without a test record, and nobody owns the question. The legal text read for this
block is Council Directive (EU) 2025/516 of 11 March 2025 (its invoicing and digital reporting amendments to
Directive 2006/112/EC, its transposition and application dates) and, as an example of the national layer, one
page of the French tax administration. Which duty applies to a company, from which date, in which format and
through which platform, is decided by the national authority and the accounting or tax adviser, not by this
block. Related blocks: `business/finance-ops` for the finance function, `business/regulatory-watch` for dating
and sourcing a legal statement, `business/fintech-compliance` for regulated payment businesses,
`skills/source-freshness` for re-reading sources. This block is a working method, not tax or legal advice.

## When
- A company issues or receives invoices and hears that structured electronic invoicing or digital reporting is coming.
- A product generates invoices for customers (billing feature, marketplace, platform) in an EU country.
- An accountant, a customer or a tax authority sends a notice about a format, a platform or a date.
- A tool, ERP or billing vendor is chosen or changed and invoices flow through it.

## Steps

**Read only the part the task meets.** Part 1 first when the flows are not yet listed.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Inventory and the EU-level text: flows, formats, platforms, archiving, what the Directive says, what it leaves to Member States | the picture of invoice flows is missing, or someone quotes "the EU rule" | [`01-inventory-and-eu-level-text.md`](./references/01-inventory-and-eu-level-text.md) |
| 2 | The national-implementation trap: finding the current official page, dating it, one French example | a date, a mandate or a platform duty is about to enter a plan | [`02-national-layer-and-dated-reading.md`](./references/02-national-layer-and-dated-reading.md) |
| 3 | Adviser questions, decision record, test, escalation | a format or platform is chosen, tested or changed, or a question must go to the adviser | [`03-adviser-decision-record-escalation.md`](./references/03-adviser-decision-record-escalation.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For each company or product under review: the flow inventory (B2B, B2C,
B2G, cross-border, reverse-charge, self-billing) with volumes and owners, the format and platform per flow, the
archiving location, the national authority page read with URL and date, the statements taken from it marked
"re-read before relying", the questions put to the adviser with their answers and dates, and the decision record
with the test evidence. Anything legal is a question with an owner, not a conclusion.

## Guardrails
- Not tax or legal advice. This block does not replace the accountant, the tax adviser or the national authority;
  escalate every applicability, date, exemption and format question to them.
- Never state a duty or a date without having read the sentence it comes from, in the current official source, and
  marking it "re-read before relying" with the read date.
- Never present the EU Directive as the national rule: it sets a frame and leaves options to Member States (part 1).
- Never take a national date from memory, a vendor page or a forum; read the authority's own page (part 2).
- Never restate the paid standard text from memory: name EN 16931, check its availability, and have the vendor or
  adviser state which syntaxes are accepted (part 1).
- Never paste real invoices, customer data or tax identifiers into a prompt, ticket or fixture; use invented ones.
- Never decide alone that a flow is out of scope or that a platform choice is compliant (part 3).

## Origin
Legal statements from Directive (EU) 2025/516 read on EUR-Lex 2026-10-19 and from one national authority page read
the same day; the rest is our own guidance, flagged as such. Provenance, what was removed and what was not verified
are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
