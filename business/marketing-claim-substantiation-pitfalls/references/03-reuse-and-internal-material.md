# marketing-claim-substantiation-pitfalls §3 — Reuse and internal material

Claims outlive the check that approved them. This section covers the second use of a verified claim and
the numbers that live in internal decks, where nobody is reading a footnote.

## 3.1 Reuse is a cheap re-verification, never a skipped one
1. **A claim verified before can be re-checked quickly, not trusted blindly.** ContentForge's design spec
   for a per-brand claim library states the rule: reuse means cheap re-verification, never skipped
   verification. A hit still gets its source checked for liveness and its wording compared verbatim
   before it enters the new piece.
2. **A miss or an aged hit goes through full verification.** The store makes the work faster; it must not
   make it weaker.
3. **Give claim types different lifetimes.** The spec's own example is a short life for market numbers, a
   longer one for study findings, and for evergreen facts no expiry but a liveness check on the source.
   The figures it uses (90, 365 and 180 days) are its design choices and are not carried; write yours.
4. **That spec is a design pass the authors deliberately did not build**, and was not run. Treat the
   ideas as untested.

## 3.2 Know where each claim is used
1. **Record which published pieces use which claim.** The same spec does so with usage events, so that a
   retracted source gives a list of pieces to fix by scanning rather than searching.
2. **When a source is retracted or a figure changes, fix every piece on the list**, and re-check the ones
   that used it. Own guidance: a spreadsheet with claim, source, date checked and pieces is enough.

## 3.3 Internal material
1. **Every statistic carries a source and a date**, in internal decks and one-pagers too (chrisrodde
   positioning skill, audit check on sourcing and its standing guardrails).
2. **Internal estimates are labelled as estimates**, so that nobody repeats them as findings.
3. **Where a number has no source, look for a credible published substitute before deleting it.** The
   same skill gives two reasons the gap matters: a buyer who checks finds nothing, and a salesperson
   cannot defend the figure in the room. Own guidance: if no substitute exists, the number goes (§1.2).
4. **A stat that collapses under a buyer's question costs more than it gained** (same skill). Own
   guidance: ask the question a sceptical buyer would ask of each number before it ships.

## 3.4 When the claim is part of a repositioning
1. **Check old material before checking the new.** After a change of message, the old claim can
   still sit on pages and in decks, at a different strength. That is the job of
   `business/messaging-audit-pitfalls` §1 and §2; run the inventory and the checks there, and bring the
   claims back here.
