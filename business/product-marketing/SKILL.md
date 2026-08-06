---
name: product-marketing
description: Use when writing anything that positions or promotes the product — a landing page, a feature announcement, a comparison, a pitch — the discipline that keeps a claim checkable. Technical SEO is skills/seo; this is about what the words commit us to.
---

# product-marketing

Business layer (`business/README.md`). The thing engineering can genuinely contribute here isn't
copywriting, it's the habit that makes claims survive contact with a customer: **a claim about
software is checkable, so check it**.

That's `default = failure` (`WORKFLOW.md` §3) pointed at marketing copy. An unverified performance
number in a deck is the same category of error as an unverified `passes: true`, and it fails later and
more expensively — in front of a prospect, or in a renewal conversation.

## When
Before publishing or sending: a landing or pricing page, a feature announcement, a competitor
comparison, a pitch deck, a case study, a conference talk abstract.

## Steps

### 1. Positioning: four sentences before any copy
Write these plainly; if any is vague, the copy will be vague in a longer form.
1. **Who it's for**, specifically enough to exclude someone.
2. **What they do today instead** — a competitor, a spreadsheet, a manual process, nothing. Something
   is always being replaced, and it's the real benchmark.
3. **What changes for them**, stated as an outcome rather than a feature.
4. **What it deliberately doesn't do.** A product with no stated boundary reads as either vapour or a
   promise to build anything.

### 2. Claims: each one needs a source
1. **Every factual claim gets a source before it ships.** A number (faster, cheaper, a percentage), a
   capability ("integrates with X"), a status ("compliant with Y"), a comparison.
2. **Numbers say what was measured**: the conditions, the dataset, the comparison point. "3x faster"
   without them is not a claim, it's a hope, and the first customer to measure differently is right.
3. **Never state a capability that isn't shipped.** Not "coming soon" phrased in the present tense, not
   a screenshot of an unbuilt screen. This is the claim type that becomes a contractual argument.
4. **Compliance and security words are legal claims**, not adjectives. Certified, compliant, encrypted,
   audited, GDPR-ready: each means something specific and someone can be asked to prove it. Route
   these through legal (`business/data-protection`, `business/licence-compliance`).
5. **Comparisons name what's compared, and the version.** A competitor comparison that misstates their
   product is both an unforced error and reputationally expensive.
6. **Get the technical claims read by someone who built the thing.** The gap between what marketing
   understood and what shipped is where the worst claims live, and it closes in one conversation.

### 3. The announcement itself
1. **Lead with what changes for the reader**, not with the internal project name or the architecture.
2. **Say who's affected and whether they must act.** Most readers only want to know that.
3. **Link to the detail** rather than compressing it into a paragraph that satisfies nobody.
4. **Don't announce ahead of availability** unless the date is a commitment someone has actually made
   (see `business/sales-support` §2). "Available today" and "available soon" have very different
   consequences.
5. Technical discoverability — meta, structure, Core Web Vitals — is `skills/seo`, not this block.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the four positioning sentences, and a source
attached to every factual claim, with the technical ones confirmed by someone who built it. Any claim
without a source is removed before publishing, not softened.

## Guardrails
- **Never publish a number nobody measured.** Deleting it costs a sentence; defending it costs a
  relationship.
- **Never describe an unbuilt capability in the present tense**, however imminent.
- **Never make a compliance, security or legal claim without the person who owns it saying yes.**
- Never publish real customer data, names or logos without their written agreement — that's their
  decision, not ours, and it's also a data-protection question.
- This block doesn't own brand voice or campaign strategy. Where it conflicts with whoever does, they
  win; the claim-needs-a-source rule is the exception and doesn't bend.

## Origin
Assembled from public sources: standard positioning structure (audience, alternative, outcome,
boundary) as taught in widely published product-marketing practice. Written **without internal
marketing expertise** and with no access to a brand or campaign reference, so it stays on the part
where engineering can be useful and be held to something. The claim-needs-a-source discipline and its
framing as `default = failure` applied outside code are ours, as is the rule that technical claims are
read by a builder before shipping.
