# saas-metric-definition-pitfalls §1 — Revenue and retention

> Part 1 of `skills/saas-metric-definition-pitfalls`. Read it when a recurring-revenue or retention figure is
> defined or checked. Every formula is the source's (nimrodfisher, one file of metric definitions); points
> marked own guidance are ours.

## 1.1 Recurring revenue
1. **MRR is the predictable monthly revenue from active subscriptions.** The source excludes one-time fees,
   professional services and usage overages unless they are contracted. Write the exclusion list beside the
   figure: it is the first thing two reports disagree on.
2. **MRR has four components**: new (customers acquired this month), expansion (upgrades, added seats, upsells
   to existing customers), contraction (downgrades by existing customers) and churned (customers who
   cancelled). A movement reported without its component is a movement nobody can act on.
3. **ARR is MRR times 12.** The source calls it a forward-looking annualised run rate, explicitly not a
   trailing twelve-month total. A sum of the last twelve months of revenue is a different quantity; give it
   its own name (own guidance on naming).
4. **ACV is total contract value divided by contract length in years**, used to compare deal sizes. It is a
   per-contract figure, not a recurring-revenue figure (own guidance: do not add ACVs and call the sum ARR
   without checking each contract's term and what the contract value includes).

## 1.2 Churn: customers or revenue
1. **Logo churn rate (monthly)** is churned customers divided by customers at the start of the month. It
   counts every customer the same, whatever its size.
2. **Revenue churn rate (monthly)** is churned MRR divided by MRR at the start of the month. It weights churn
   by customer value.
3. **The two can move in opposite directions** (own guidance): losing many small customers raises logo churn
   and barely moves revenue churn; losing one large customer does the reverse. Quote which one, and when the
   decision is about money, say why the other was not used.
4. **Both denominators are the start of the month.** Customers or MRR acquired during the month are not in
   the base (the formulas as written have no new-customer term).

## 1.3 Net and gross revenue retention
1. **Net revenue retention (NRR)** is starting MRR plus expansion minus contraction minus churned, divided by
   starting MRR. Above 100 percent, revenue from existing customers is growing even with no new customers
   (source).
2. **Gross revenue retention (GRR)** is starting MRR minus contraction minus churned, divided by starting MRR.
   Expansion is excluded, so the source states its upper bound is 100 percent and says it measures the pure
   downside.
3. **A GRR above 100 percent is a bug in the calculation**, not a good result (own guidance, a consequence of
   the bound): expansion leaked in, or the cohort in the numerator is not the cohort in the denominator.
4. **NRR and GRR use the same starting cohort.** New MRR appears in neither formula; adding it turns the
   figure into something that is no longer retention (own guidance, read from the formulas).
5. **Say which one is quoted.** "Retention" with no qualifier is NRR to one reader and GRR to another, and the
   two differ exactly by expansion.
