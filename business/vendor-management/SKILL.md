---
name: vendor-management
description: Use before signing or renewing a SaaS or vendor contract, or when choosing between vendors: security and compliance review before signing, and renewal tracking.
---

# vendor-management

Business layer (`business/README.md`). A vendor decision made on price and feature fit alone, with the
security/compliance review happening (if at all) after the contract is signed, is the recurring failure
mode this block exists to prevent — by the time an issue surfaces, the leverage to walk away is gone.

## When
Choosing between vendors for a new SaaS/service purchase, before signing any contract that grants a
third party access to company or customer data or systems, and on every contract renewal.

## Steps

### 1. Assess before signing, not after
1. **The security/compliance review happens during selection, before the contract is signed** — built
   into the procurement workflow itself, not as a follow-up once the team is already relying on the
   tool. A review that starts after rollout has no real leverage: the vendor already has the business.
2. **Tier the depth of review to what the vendor actually touches.** A vendor with no access to customer
   data or critical systems needs a light check; one that will hold personal data (cross-reference
   `business/data-protection` §4 on third parties) or sit in a critical path needs a real one —
   security documentation, relevant certifications, how they handle access control, encryption,
   incident response and business continuity.
3. **A vendor holding an open-source-licensed component as part of what they ship is still a
   `business/licence-compliance` question** — vendor risk and licence risk are reviewed together, not
   as two separate processes that each assume the other caught it.
4. **Document the decision**, not just the outcome: what was reviewed, what was flagged, what was
   accepted as a residual risk and by whom. A decision nobody can reconstruct six months later can't be
   re-evaluated when circumstances change.

### 2. Track the relationship after signing
1. **Every vendor contract has a named owner and a renewal date tracked somewhere that gets checked**,
   not discovered when a card is charged for a service nobody remembers still being used. An
   auto-renewing contract with no owner is a recurring spend nobody has actually decided to keep (this
   is the same failure `business/finance-ops` §3.2 names for recurring spend generally — a vendor
   contract is that failure's most common shape).
2. **Re-review triggers on more than the calendar**: a scope expansion (the vendor now gets more access
   or more data than originally scoped), a vendor security incident, or a change of ownership/control
   at the vendor all warrant a fresh look, not just the renewal date.
3. **A high-risk vendor gets a shorter re-review cycle than a low-risk one** — risk tiering from
   selection (§1.2) should keep applying after signing, not just at the point of the initial decision.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a documented
security/compliance review completed before signing, scoped to what the vendor actually touches, a named
owner and tracked renewal date per contract, and a re-review triggered by scope change or incident, not
only by the calendar.

## Guardrails
- Never let a vendor review happen only after the team is already dependent on the tool — the leverage
  to walk away is what a pre-signing review protects.
- Never leave a contract auto-renewing with no named owner tracking it.
- Never assume a vendor's licence/open-source obligations were someone else's problem to have checked —
  cross-reference `business/licence-compliance`.
- Never treat a vendor handling personal data as a pure procurement decision — `business/data-protection`
  §4's third-party questions (data processing agreement, hosting location) apply.
- This block has no dedicated in-house procurement/vendor-risk expertise behind it yet: a solid set of
  structural defaults, not proven doctrine, to be confronted with a real vendor-selection cycle.

## Origin
Assembled from public sources, written without internal procurement/vendor-risk expertise. Pre-signing
review built into procurement, risk-tiering by data/access scope, documented decisions including
accepted residual risk, and re-review triggered by scope change/incident/ownership change rather than
only the calendar: published SaaS/third-party vendor-risk-assessment guidance. The cross-references to
`business/licence-compliance` and `business/data-protection` are ours — neither of those blocks names the
broader vendor-selection process they each assume happens somewhere, and this is where it lives.
Stamped 2026-08-11.
