---
name: finance-ops
description: Use when setting up or reviewing the company's own financial operations (expense approval, invoicing, budgeting). Building a payment or ledger product is business/fintech-compliance.
---

# finance-ops

Business layer (`business/README.md`). Distinct from `business/fintech-compliance`: that block is
engineering invariants for a *product* that moves other people's money (a ledger, a payment flow); this
one is the structural discipline around the company's *own* financial operations — who can approve
what, how invoicing gets chased, how a budget gets tracked. Same honesty posture as the rest of this
layer: not accounting or tax advice.

## When
Setting up or reviewing who can approve an expense or a payment, how invoices/receivables are tracked,
or how spend against a budget is monitored.

## Steps

### 1. Separation of duties: the core control
1. **The person who requests or benefits from a spend never also approves it.** This is the single
   highest-value control against both error and fraud — not because any specific person is suspected,
   but because a control that depends on one person's honesty rather than on a structural check is a
   control that fails exactly when honesty does.
2. **The person who approves a transaction is not the same person who reconciles or reviews it
   afterwards.** Approval and review are two different checks; collapsing them into one person removes
   the second check entirely.
3. **A small team can't fully separate duties, and that's expected — use compensating controls instead
   of pretending the separation exists.** A founder/owner personally reviewing bank and card statements
   monthly, requiring a second signature above a stated amount, or rotating who handles a given process
   periodically all substitute for headcount the team doesn't have. Don't skip the control because the
   textbook version needs more people than exist.
4. **Detection is faster with the control in place than a post-hoc audit relies on**: organisations with
   real separation-of-duties controls catch discrepancies materially faster than those without, which
   directly caps how large a problem gets before it's noticed.

### 2. Invoicing and receivables
1. **An invoice has a stated due date and payment terms from the moment it's sent**, not an implicit
   "whenever." Ambiguity here is what turns into a slow-payer problem later.
2. **Overdue receivables are tracked and chased on a schedule**, not noticed when cashflow gets tight.
   A simple aging view (current / 30 / 60 / 90+ days overdue) surfaces the problem while it's still
   small.
3. **A recurring late payer is a decision to make explicitly** (stricter terms, upfront deposit,
   involving someone senior) rather than an accepted pattern nobody has actually decided to accept.

### 3. Budgeting and spend visibility
1. **A budget is a tracked commitment, not a document written once and revisited at year-end.** Spend
   against it reviewed on a cadence (monthly is common) catches an overrun early enough to act on it,
   rather than as a year-end surprise.
2. **Every recurring spend (subscriptions, contracts) has a named owner** who can say why it exists and
   whether it's still needed — an unowned recurring charge is how a company keeps paying for a tool
   nobody uses.
3. **A one-off spend above a stated threshold gets the same "requester ≠ approver" check as routine
   expenses** — a threshold exists precisely so a large exception doesn't slip through because it felt
   too unusual for the normal process to apply.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a stated separation
between who requests/benefits from a spend and who approves it (or a named compensating control where
headcount doesn't allow real separation), an aging view of receivables reviewed on a schedule, and a
named owner per recurring spend with budget tracked against actuals on a cadence.

## Guardrails
- Never let the same person both request/benefit from and approve the same transaction, without an
  explicit compensating control replacing that check.
- Never let an overdue invoice go unchased until cashflow makes it urgent — track on a schedule, not on
  pressure.
- Never leave a recurring subscription/contract with no named owner.
- This block has no dedicated in-house finance/accounting expertise behind it yet: a solid set of
  structural defaults, not proven doctrine, and not accounting or tax advice — a real bookkeeper or
  controller's judgement outranks it without discussion.

## Origin
Assembled from public sources, written without internal finance/accounting expertise. Separation of
duties (requester ≠ approver ≠ reviewer, compensating controls for small teams, faster fraud detection
with the control in place): published internal-controls guidance aimed at small businesses and
nonprofits, where the headcount-constrained case is explicitly addressed rather than assumed away.
Invoicing/receivables aging and budget-as-tracked-commitment: general financial-operations practice,
generalised rather than tied to one accounting platform. Stamped 2026-08-11.
