---
name: marketing-claim-substantiation-pitfalls
description: "Use when marketing material (a landing page, deck, one-pager, battlecard, ad, email or case study) has to be checked claim by claim before it ships: extracting every disputable claim from every surface, a supported, thin or unsupported verdict with named proof, statistics checked against the cited source (context, paywalls, dead links, conflicting figures, single sources, sample, metric, period, recency), reuse of earlier verified claims, and sources and dates on internal numbers."
---

# marketing-claim-substantiation-pitfalls

Business layer (`business/README.md`), marketing. `business/product-marketing` §2 states the principle: a
claim about software is checkable, so check it. This block is the **verdict protocol and the statistic checks**
that make the principle something a reviewer can sign. Its premise: a claim survives because nobody searched
for its proof, so the work is a table, not a feeling.

Claim and advertising law differs by country and sector and was not verified here. This block names no
statute and no authority; regulated and comparative claims go to the person who owns legal or compliance.

## When
- Before publishing or sending a landing or pricing page, a deck, a one-pager, a battlecard, ads, an email
  sequence or a case study.
- After a repositioning, when old claims may still be live on other surfaces.
- A deck or an article carries statistics somebody must stand behind.
- A claim is about to be reused from an earlier piece.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Inventory and verdicts: extract claims, supported or thin or unsupported, fixes, legal flags, the report | a set of material needs a claim check | [`01-inventory-and-verdicts.md`](./references/01-inventory-and-verdicts.md) |
| 2 | Statistics and sources: number in context, paywall, dead link, conflicts, one source, definition, recency | a number or a quote is cited | [`02-statistics-and-sources.md`](./references/02-statistics-and-sources.md) |
| 3 | Reuse and internal material: re-verifying earlier claims, usage records, sourcing internal numbers | a claim is reused or a deck carries unsourced figures | [`03-reuse-and-internal-material.md`](./references/03-reuse-and-internal-material.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a claim table quoting each claim as written with its
surface, a verdict and the named proof or "none found", a fix per thin or unsupported claim, and a list of
claims flagged for legal or compliance sign-off. A claim without a named proof is removed or replaced by a
smaller claim the proof carries, then re-checked; it is never published on a hunch.

## Guardrails
- Never mark a claim supported without naming the proof (§1.2).
- Never soften a verdict to reassure the author, and never reword a claim into something the evidence
  cannot carry (§1.2).
- Never judge regulated or comparative claims yourself; flag them (§1.3).
- Never accept a statistic you cannot find in its source with the same context (§2.1).
- Never mark a paywalled or unreachable source verified without corroboration (§2.2).
- Never keep a number whose source link is dead (§2.2).
- Never treat a key claim with one source as verified; write down your own count (§2.3).
- Never reuse a verified claim without re-checking the source and the wording (§3.1).
- This block is a method written from small, young repositories and was never run on a real launch. Source
  status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from the claim-check skill of a small MIT product-marketing repository, the fact-checker agent and
a claim-library design spec of an MIT content pipeline, and the sourcing check of a young MIT positioning
skill, read 2026-10-15. 🟡: never run by us; the sources are young and unreviewed. Details in
[`references/origin.md`](./references/origin.md).
