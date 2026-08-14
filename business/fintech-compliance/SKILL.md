---
name: fintech-compliance
description: Use when a feature touches payments, card data, a financial ledger, KYC onboarding or moving money between parties: regulatory scope, and the engineering invariants that keep it correct.
---

# fintech-compliance

Business layer (`business/README.md`). Money code fails differently from other code: a bug is a
support ticket, a financial bug is a discrepancy someone has to reconcile, sometimes a regulatory
finding. This block is `business/data-protection`'s sibling, aimed at payments/ledger/regulated-finance
work instead of personal data — same posture: route the legal question to the right person, and own the
engineering consequences ourselves.

**This is not legal, compliance or accounting advice.** Where a question has a regulatory answer —
whether a licence is needed, whether a customer needs enhanced due diligence, whether a specific flow
is in PCI DSS scope — the answer comes from compliance/legal, not from here.

## When
As soon as a feature: touches card data in any form, moves money between two parties (a customer and
the company, two customers, a customer and a third party), maintains a balance or a ledger, or onboards
a user for a regulated financial service (an account, a wallet, a payout).

## Steps

### 1. Route the regulatory questions before writing code
Take these to compliance/legal rather than guessing — same posture as `business/data-protection` §2:
- **Does this feature put us in PCI DSS scope?** Any flow where card data (the PAN, the CVV, the
  expiry) passes through, is stored by, or is transmitted by our own systems is in scope. The
  practically universal fix is to **never let card data touch our servers at all**: collect it directly
  into the payment processor's own hosted field/SDK, get back a token, and store and reuse only that
  token. A flow that routes card data through our backend "just to log it" or "just to validate the
  format" just put that backend in scope — that's a decision, not an implementation detail, and it goes
  to whoever owns PCI compliance before it ships.
- **Does onboarding this kind of user or this kind of flow trigger KYC/AML obligations?** Screening
  against sanctions lists (OFAC, UN, EU, national lists) at onboarding, and re-screening on a risk
  change, is a compliance program's call on *who* gets screened and *how strictly* — not a threshold to
  invent in the code. What the code has to provide is a hook where that screening can run, and a state
  the account can sit in while it's pending.
- **Does this need a money-services/e-money licence, or does it fit under someone else's?** Moving
  money between third parties is regulated in most jurisdictions; "we're just a technical intermediary"
  is a legal characterisation, not a fact you get to assume.

### 2. What the code has to provide: money handling
1. **Money is never a float.** Represent an amount as an integer minor-unit count (cents) or an exact
   decimal type, never a binary float — this is `skills/design-patterns` §4.5's Value Object entry
   applied at its highest-stakes case; a rounding error here isn't cosmetic, it's a discrepancy in a
   number someone has to reconcile.
2. **Every amount carries its currency**, and an operation across two amounts checks the currencies
   match before doing arithmetic on them — a silent add across currencies is a real, catchable bug
   class, not a hypothetical one.
3. **Rounding is a policy, applied once, at a named point** (e.g. half-up at the smallest currency
   unit), not wherever a division happens to land in the code. Two different rounding results for the
   same computation are how a ledger stops balancing.

### 3. What the code has to provide: the ledger
1. **A ledger is append-only.** No `UPDATE`, no `DELETE` on a posted entry — correcting a mistake is a
   new, explicit reversing entry, never an edit to history. The moment history can be silently changed,
   nobody can tell a bug from a cover-up, and reconciliation stops being possible.
2. **Every movement is (at least) two entries that net to zero** — a debit and a matching credit across
   two accounts, committed together or not at all. A balance is a *derived* read over the entries, never
   a separately-stored counter that can drift out of sync with what the entries actually say.
3. **The atomic unit of a financial write is the whole set of entries for one transaction.** Partially
   applying a multi-entry movement (crediting one side, failing before debiting the other) is a
   correctness bug regardless of how rare the failure window looks in testing.

### 4. What the code has to provide: payment operations
1. **Every request that can be retried (network blip, timeout, a user double-clicking pay) carries an
   idempotency key**, and the receiving side stores the result keyed on it — a retry with the same key
   returns the original result instead of charging twice. This applies to outgoing calls to a payment
   processor and, separately, to incoming ones.
2. **A webhook from a payment processor is verified before it's trusted** — its signature, against the
   raw request body, checked first, before any business logic runs on its payload.
3. **A webhook is deduplicated by the event's own id**, not by re-deriving "have I seen this before"
   from business state: insert the event id into a processed-events table under a unique constraint
   before doing any work; a unique-violation means it's already been handled, so skip. The common miss
   is idempotency on the *outgoing* call only — the incoming webhook handler needs its own, separately.
4. **A webhook handler re-fetches the authoritative state from the processor rather than trusting the
   payload alone** for anything a business decision depends on, and only applies a state transition if
   it's actually valid from where the record currently stands (no silently re-applying "paid" to an
   already-refunded order).
5. **Reconciliation is a designed-in job, not an afterthought**: something that periodically compares
   our ledger against the processor's own record of the same transactions and surfaces a mismatch —
   stuck-pending payments, a webhook that never arrived, a refund that didn't post — rather than relying
   on a customer to notice and complain first.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: the PCI-scope and
KYC/AML questions routed to compliance with their answers when they come back, amounts represented
without floats and currency-checked, the ledger append-only with entries that net to zero per
transaction, idempotency on both the outgoing call and the incoming webhook, and a reconciliation
mechanism named rather than assumed.

## Guardrails
- Never decide PCI DSS scope, licensing, or a KYC/AML threshold yourself — route it, the same way
  `business/data-protection` routes a lawful-basis question.
- Never let card data reach a server we control if a hosted-field/tokenisation alternative exists —
  that's the single biggest scope-reduction lever available, and skipping it is a decision someone
  senior should make knowingly, not a default.
- Never edit or delete a posted ledger entry. A correction is a new entry, always.
- Never represent money as a float, and never let an amount cross a currency boundary unchecked.
- Never add idempotency "later" — like `skills/background-jobs-conventions`, this is a design property,
  and retrofitting it means auditing every already-shipped call site for whether it was ever double-run.
- This block has no dedicated in-house fintech/compliance expertise behind it yet: a solid set of
  engineering defaults plus a routing checklist, not proven doctrine, to be confronted with a real
  regulated-payments engagement.

## Origin
Assembled from public sources, written without internal fintech/compliance expertise, the same honesty
posture as `business/data-protection`. PCI DSS scope and the tokenisation-as-scope-reduction mechanism:
published PCI compliance and tokenisation-vendor guidance. KYC/AML/sanctions-screening triggers
(onboarding screening, risk-driven re-screening, the OFAC/UN/EU list landscape): published AML/sanctions
compliance guides. Double-entry ledger invariants (append-only, no silent update/delete, balance as a
derived read, atomic multi-entry posting): published ledger-database design writing (Modern Treasury's
ledger engineering series, TigerBeetle's debit/credit documentation) aimed at engineers building
financial systems, not at accountants. Payment idempotency and webhook handling (idempotency keys on
outgoing calls, signature verification before trust, dedup by event id under a unique constraint,
re-fetching authoritative state rather than trusting the payload): published Stripe-style payment
integration practice, generalised beyond one named processor. The money-as-value-object point is not
new here — it cross-references `skills/design-patterns` §4.5, added 2026-08-11 from the real
`xefi-claude-skills` `design-patterns` plugin — this block is where its highest-stakes case gets spelled
out. Stamped 2026-08-11.
