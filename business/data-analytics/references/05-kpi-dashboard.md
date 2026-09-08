# § 5 — KPI and dashboard discipline

> Section 5 of `business/data-analytics`. Read it when a metric or a dashboard is proposed, defined or
> reviewed. Points 1 to 3 are cited from this block's guardrails and from three business blocks.

1. **Every KPI gets a written definition before it goes on a dashboard**: the exact formula (numerator,
   denominator, filters), the table(s)/logic it's computed from, an owner, a target or acceptable range,
   and how often it refreshes. A number on a dashboard with none of that is a number nobody can defend
   when it's questioned. The moment it is questioned is the moment it matters — a figure that decides
   something gets challenged by whoever the decision goes against, and an undefended number loses that
   argument regardless of whether it was right.
2. **Run the decision test on a proposed metric**: what specific action changes based on this number
   moving? If the honest answer is "nothing, it's just interesting," it's a vanity metric — raw page
   views, follower counts, total signups with no context. It doesn't belong on a decision-making
   dashboard; a rate, a ratio, or a trend usually carries the same information in an actionable form
   (page views → conversion rate by source; signups → activation rate).
3. **One metric, one definition, one place it's computed** — the single-source-of-truth rule. The same
   name ("revenue", "active customer") computed two different ways in two dashboards is worse than an
   admittedly-imperfect metric everyone agrees on: it produces a real argument about whose number is
   right when both are technically defensible from their own definition.
4. **A dashboard that shows more than can be read at a glance defeats its own purpose.** Cognitive-load
   research on this is consistent: people track a handful of things at once reliably, not thirty. A
   handful of well-defined KPIs beats a wall of tiles; anything else belongs one click deeper, not on
   the first screen.
5. **A metric with no target is a metric nobody can read.** A number on its own says nothing about
   whether today is good; the target, the range or the comparison is what turns it into information. The
   observable consequence of omitting it is a dashboard people stop opening, because every visit
   requires asking someone whether the figure is normal.
6. **A metric that can be moved without moving the thing it measures will be.** Any figure someone is
   accountable for becomes a target, and the cheapest way to move a proxy is usually not the work it
   stands for — closing tickets faster by closing them unresolved, raising an average by excluding the
   hard cases. Naming that exposure when the metric is defined is part of defining it; pairing it with a
   counter-metric is the usual fix.
7. **State the metric's direction and its owner in the definition.** Whether up is good is not always
   obvious from a name, and a metric with no owner has nobody to ask when it breaks — so it stays broken
   and visible, which teaches every reader to discount the whole dashboard.
8. **A dashboard shows its own freshness, or its numbers are assumed live.** Readers date a figure by
   when they looked at it. A tile fed by a nightly load, or one whose last refresh failed, is
   indistinguishable from a current one, so the visible timestamp is not decoration — it is the
   difference between a stale number being noticed and a stale number being acted on.
9. **A KPI's definition changing is an event, not an edit.** Recomputing history under a new definition
   makes an old trend disagree with every report and screenshot taken before it; leaving history under
   the old one puts a discontinuity in the series. Either is defensible and neither is silent: mark the
   change on the series with its date, and say which of the two was done.
10. **A drill-down that does not reconcile with its tile is worse than no drill-down.** The detail
    behind a KPI is the first thing a challenged number gets checked against, so a total that does not
    match the sum of its rows — a different filter, a different grain (§2.7), a deduplication applied at
    one level only — destroys confidence in the tile that was correct. Reconciling the two is part of
    building the drill-down, not a follow-up.
11. **A KPI on a dashboard is a claim someone will repeat outside it.** The figure ends up in a
    steering deck, a board pack or a customer-facing summary, detached from the filters and the
    freshness that qualified it — which is why the definition (point 1) and the filters (§4.4) have to
    travel with the number rather than living beside it on the screen.
