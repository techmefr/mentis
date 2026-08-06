# business: the second layer

> Blocks for the company's other functions — legal, UI/UX, marketing, sales, communication.
> Same template, **explicitly weaker contract**. Read this before adding one.

## Why this is a separate folder

The dev pipeline rests on two guarantees (`WORKFLOW.md` §3): **fresh context** and **default =
failure**. Both work because software produces citable artefacts. A test either passes or it doesn't.
A screenshot shows the button or it doesn't. `galadriel` can refuse a claim because there is
something to point at.

Most of these functions don't have that. There is no test suite for a positioning statement and no
`PASS` for a proposal. If those blocks sat in `skills/` alongside the rest, they'd inherit a
credibility they can't earn, and the words "verified" and "reviewed" would quietly come to mean two
different things in the same framework. Keeping them apart is what protects the dev core's claims from
being diluted by association.

## What a business block may and may not claim

| | `skills/` | `business/` |
|---|---|---|
| Fresh-context judge (`galadriel`) | yes | no |
| Evidence required before "done" | yes, cited | no, judgement instead |
| Gate that can block (`hooks/`) | yes | never |
| Checkpoint in the pipeline | yes | no |
| Maturity ceiling | 🟢 real production use | 🟡 at best, until a human with the actual expertise reviews it |

**A business block never gates anything.** It structures a decision and lists what's usually
forgotten. It does not certify. Anything it produces goes to a human who owns that function, and that
person's judgement outranks the block without discussion.

## Rules that still apply, unchanged

- **Rule B**: rewritten our way, `Origin` honest, no runtime dependency.
- **Rule C**: publishable. No client names, no contract terms, no internal pricing, no real campaign
  data. A block names a role and a situation, never a deal.
- **One block, one responsibility.**
- **No comments in produced code**, where a block touches code at all.

## The honesty rule specific to this layer

These blocks are written **without internal expertise in the function**. A block here is a structured
checklist assembled from public sources, not professional advice, and each one says so in its
`Origin`. Two consequences that are not negotiable:

- **Legal blocks are not legal advice.** They exist to stop an engineer walking into something
  obvious, and to make the question reach a lawyer earlier. Where a block's guidance would decide
  something contractual or regulatory, it says "ask", not "do".
- **A block in this folder that starts to sound authoritative is a bug.** The failure mode here isn't
  being incomplete, it's being confidently wrong in a domain where nobody in the loop can catch it.

## What's in here

| Block | Function |
|---|---|
| `data-protection` | legal |
| `licence-compliance` | legal |
| `legal-documents` | legal |
| `regulatory-watch` | legal |
| `ux-writing` | UI/UX |
| `interface-design` | UI/UX |
| `product-marketing` | marketing |
| `sales-support` | sales |
| `release-communication` | communication |
| `incident-communication` | communication |
| `internal-communication` | communication |
| `content-creation` | communication |
| `community-management` | communication |
| `product-ownership` | product |
| `social-publishing` | communication |

## Installing

Same as the dev blocks: copy the ones you want into the target repo's `.claude/skills/`. The folder
split is organisational, it isn't a different mechanism. See `skills/distributing-blocks`.
