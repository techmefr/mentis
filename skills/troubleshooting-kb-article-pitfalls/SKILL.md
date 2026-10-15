---
name: troubleshooting-kb-article-pitfalls
description: "Use when troubleshooting pages, error references or a knowledge base are written from support history: choosing which failures deserve a page from clustered evidence, gating each cluster on document versus fix, choosing the entry shape, the entry anatomy (message verbatim, applies to, cause, branched fix, confirm it worked, still stuck), verifying before publishing, making the page findable by the error string, capturing knowledge during resolution, generating the error catalog from one source, and keeping pages current."
---

# troubleshooting-kb-article-pitfalls

The premise: **a troubleshooting page is a stopgap for a failure the product could stop causing, and it is only
worth publishing when it comes from evidence, was verified, and ends with the reader unblocked**. Pages written
from imagination document failures nobody has while the real ones stay unwritten; unverified fixes cost more
trust than a gap.

This block is about the pages. One incoming report is `bug-triage`; documentation structure and decisions are
`documentation-adr`; wording of the interface itself is `business/ux-writing`.

## When
- Turning tickets, issues and error telemetry into troubleshooting or error-reference pages.
- Reviewing a help centre or known-issues list that nobody finds, or whose fixes no longer work.
- Deciding whether a recurring support question deserves a page or a product change.
- Setting up how support captures knowledge as it resolves cases.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Evidence, clustering, regression versus page, the document-versus-fix gate | deciding what to write | [`01-evidence-and-gate.md`](./references/01-evidence-and-gate.md) |
| 2 | Entry shapes, the six parts, writing rules | an entry is being drafted | [`02-entry-shape-and-writing.md`](./references/02-entry-shape-and-writing.md) |
| 3 | Verification before publishing, findability, stable anchors, customer data | an entry is about to be published or cannot be found | [`03-verify-and-findable.md`](./references/03-verify-and-findable.md) |
| 4 | Capture during resolution, one-source catalog, stamps and retirement, measuring, escape hatch | the practice around the pages is being set up | [`04-capture-catalog-maintain.md`](./references/04-capture-catalog-maintain.md) |

## Output / checkpoint
A ranked list of clusters with the decision for each (page, product fix, macro, regression report), entries in
the six-part shape, and for each entry a record of the version it was reproduced on and the post-fix signal, or
the explicit note that it was not reproduced. An entry without that record is a draft.

## Guardrails
- Never write a page from a failure nobody reported or measured (§1.1).
- Never write ten pages for ten tickets with one cause (§1.2).
- Never write a page for a cluster that appeared right after a release; report the regression (§1.3).
- Never let a page be the permanent answer for a failure the product could stop emitting (§1.4).
- Never call a fix "simple", "easy" or "just" (§2.3).
- Never publish a fix that was not run as written from the reader's starting state (§3.1).
- Never rename an error identifier or its anchor (§3.3).
- Never publish a real token, address or customer identifier in an example (§3.4).
- Never leave a "contact support" line that points at a channel nobody watches (§4.5).
- The source behind this block names published frameworks (knowledge-centred service and others) that were not
  read here; this block carries none of their text and cites them only as the source does. Its figures and
  second-hand statistics are not carried.

## Origin
Rewritten from the developer-troubleshooting-docs skill and its signal-mining reference in Samuel Berthe's
developer-relations-skills (MIT), read 2026-10-15. Details, removed content and open points are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
