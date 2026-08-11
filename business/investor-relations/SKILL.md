---
name: investor-relations
description: Use when preparing a fundraise data room, a board/investor update, or responding to investor due diligence — the structure that keeps financials, cap table, KPIs and forecast internally consistent, and keeps sensitive material from being over-shared. Not legal, tax or securities advice, and not a substitute for the company's own counsel on anything that touches an actual securities offering.
---

# investor-relations

Business layer (`business/README.md`). The recurring failure this block targets isn't missing
documents, it's **inconsistency between them**: a pitch deck's growth number that doesn't match the
financials, a cap table that wasn't updated after the last note converted. Due diligence exists
specifically to find that gap, and finding it costs credibility even when the underlying business is
fine.

**Not legal, tax or securities advice.** Which disclosures are required, how a round is legally
structured, and what an actual securities filing needs are questions for the company's counsel, not this
checklist.

## When
Preparing a data room ahead of a fundraise, sending a recurring investor/board update, or responding to
a due-diligence request from a prospective investor.

## Steps

### 1. Reconcile before anyone outside the company sees it
1. **The deck, the cap table, the actual financials, the forecast and the stated use of funds all have
   to agree with each other before outreach starts.** A diligence process exists to cross-check exactly
   these against each other — an inconsistency found by an investor reads as sloppiness at best,
   dishonesty at worst, regardless of which document was actually wrong.
2. **The cap table is current, not "current as of the last time someone updated it."** A conversion, an
   option grant, or a new note that hasn't been reflected yet is the single most common diligence
   surprise, and it's entirely avoidable.
3. **Financial statements and KPIs use the same definitions the deck uses.** The single-source-of-truth
   discipline `business/data-analytics` §5.3 states for a KPI applies directly here — a metric computed
   one way in the deck and another way in the financials is a credibility problem waiting to surface.

### 2. Scope what's shared, and when
1. **Build the data room before the raise starts**, not while already fielding requests — the handful
   of materials that build trust fastest (financials, KPIs, cap table, traction, use of proceeds) go in
   first.
2. **Don't expose the full room to a cold recipient.** Restrict the more sensitive material (customer
   contracts, detailed IP documentation, anything competitively sensitive) and release it as the
   relationship and interest level warrant, rather than by default.
3. **Match the depth of what's prepared to the round's actual stage** — a seed round's diligence doesn't
   need audit-ready GAAP statements and cohort-retention detail, and preparing Series-B-grade material
   for a seed conversation is effort spent in the wrong place.

### 3. Keep the relationship current after the raise
1. **A recurring update cadence, kept even when there's nothing dramatic to report.** Investor updates on
   a roughly monthly-to-quarterly rhythm, consistent whether the news is good or mixed, are what keeps a
   "still investigating"-style honest update (`business/incident-communication`'s same principle,
   applied here) from reading as evasive the one time things aren't going well.
2. **Bad news reaches investors before they'd hear it elsewhere.** The same posture
   `business/incident-communication` takes toward customers during an outage applies to investors during
   a real setback — silence gets filled with worse assumptions than the truth usually is.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a reconciled deck,
cap table, financials, forecast and use-of-funds before outreach, a data room scoped to the round's
actual stage with sensitive material gated rather than exposed by default, and a kept recurring update
cadence.

## Guardrails
- Never send a deck, financial statement or KPI report that hasn't been reconciled against the others.
- Never expose the full data room to a cold or early-stage recipient by default.
- Never let a cap table go stale — update it the moment something changes, not before the next round.
- Never decide alone what a securities offering legally requires — that's counsel's call.
- This block has no dedicated in-house fundraising/IR expertise behind it yet: a solid set of structural
  defaults, not proven doctrine, to be confronted with a real raise.

## Origin
Assembled from public sources, written without internal fundraising/investor-relations expertise. Data
room structure, stage-appropriate depth, reconciliation before outreach, and restricted-by-default
sensitive material: published startup-fundraising and due-diligence guidance. The cross-references to
`business/data-analytics`'s single-source-of-truth rule and `business/incident-communication`'s
honest-update posture are ours — this block is those same mechanisms applied to the investor
relationship specifically. Stamped 2026-08-11.
