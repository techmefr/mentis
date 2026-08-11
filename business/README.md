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

| Block | Function | When |
|---|---|---|
| `data-protection` | legal | a feature collects, stores, exports or shares personal data, or a new third party will receive it |
| `licence-compliance` | legal | adding a dependency, vendoring code, or shipping something that bundles third-party code |
| `legal-documents` | legal | before a first launch/public beta, charging, self-service signup, a new country, or a new subprocessor |
| `regulatory-watch` | legal | before writing a regulatory obligation into a document, plan or estimate; periodically as an audit |
| `ux-writing` | UI/UX | writing any text a user reads: labels, buttons, errors, empty states, emails |
| `interface-design` | UI/UX | designing or auditing a mockup, or deciding a UI element's shape before it's coded |
| `product-marketing` | marketing | before publishing a landing/pricing page, feature announcement, comparison, pitch, or case study |
| `sales-support` | sales | engineering is pulled into a proposal, scoping call, demo, or RFP response |
| `release-communication` | communication | a change ships that someone outside the team can notice |
| `incident-communication` | communication | something user-visible is broken or degraded in production |
| `internal-communication` | communication | announcing a decision, flagging a risk, asking for help, or handing off work |
| `content-creation` | communication | producing content for a public channel, starting from work actually done |
| `community-management` | communication | running the ongoing conversation on an account/community — replies, moderation, escalation |
| `product-ownership` | product | deciding what gets built and in what order, or writing/reviewing a story |
| `social-publishing` | communication | before publishing on any public social platform or account |
| `data-analytics` | BI / data | working against real data for reporting, dashboards, KPIs, or cross-source extraction |
| `fintech-compliance` | legal / finance | a feature touches payments, card data, a ledger, or onboards a user for a regulated financial service |
| `people-ops` | HR | hiring, onboarding a new employee, or offboarding someone leaving |
| `customer-success` | support / CS | setting up support triage/SLAs, or an ongoing account-health/churn process |
| `finance-ops` | finance | setting up or reviewing expense approval, invoicing/receivables, or budgeting |
| `vendor-management` | procurement | before signing/renewing a SaaS/vendor contract, or choosing between vendors |
| `learning-development` | HR | proposing, choosing, or reviewing a training/upskilling program |
| `sustainability-esg` | legal / comms | writing or reviewing a sustainability/ESG claim, report, or public commitment |
| `investor-relations` | finance | preparing a fundraise data room, a board update, or responding to due diligence |

## Installing

Same as the dev blocks: copy the ones you want into the target repo's `.claude/skills/`. The folder
split is organisational, it isn't a different mechanism. See `skills/distributing-blocks`.
