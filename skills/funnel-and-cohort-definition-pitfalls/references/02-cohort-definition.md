# funnel-and-cohort-definition-pitfalls §2 — Cohort definition

A cohort table compares groups of users over the same number of periods. The pitfalls are in how the groups are
formed, what counts as retained, and how unequal rows are combined.

## 2.1 How cohorts are formed
1. **Choose the grouping rule to fit the question** (nimrodfisher): signup date as the default; first purchase
   date for commerce and marketplaces; the first activation event for products with a moment of first value;
   acquisition channel to compare channel quality; plan tier at signup; adoption of a specific feature to
   measure its impact; an assigned segment such as geography or account size.
2. **Write the rule down**, so that the same user lands in the same cohort for everyone reading the chart (own
   guidance).

## 2.2 The retention event
1. **Retention means different things in different products.** The source gives examples: a login or a core
   action for a consumer app, a repeat purchase within a number of days for commerce, seat or feature use for
   business software, creating a listing or making a sale for a marketplace, content consumed for some
   minimum time for a content product.
2. **Avoid events that say nothing about value** (source): a generic page view, browsing without buying, a
   passive single-sign-on login, creating an account only, opening an app with no engagement.
3. **Define "active" before the analysis, with the data team and at least one product stakeholder** (source). A
   wrong retention event produces correct-looking and misleading curves, so the event cannot be chosen after the
   curve is seen.
4. **Deduplicate to one signal per user per period.** If a user can generate many events a day, filtering to
   "any event" shows retention near 100 percent even for a product with problems. The source's fix is a single
   active or inactive signal per user per period.

## 2.3 Immature cohorts
1. **Recent cohorts have fewer periods of data.** The source's example: do not compare the twelfth-period
   retention of an old cohort with a recent one that only has three periods.
2. **Compare cohorts only at the same period number**, and mark which cells are incomplete (source).
3. **A key result that needs a period nobody has completed is not yet observable**; see `okr-scoring-pitfalls`
   for deferring such a score.

## 2.4 Averages and small cohorts
1. **An average across cohorts is dominated by the largest ones.** The source's advice is to report retention
   per cohort and not only the overall average. (The source labels this survivorship bias; the mechanism it
   describes is the weighting by cohort size.)
2. **A small cohort is noisy.** The source's example: a cohort of 20 showing 80 percent retention at period 6
   means 4 people were active. Set a minimum cohort size in advance and exclude or grey out cohorts below it,
   and show the count behind each rate. The source suggests a value of 100; that is its recommendation, no
   derivation is given, and it is not carried here.

## 2.5 Users and revenue
1. **User retention and revenue retention are different measures.** A retained user may spend less, and a churned
   user on an annual plan may still be recognised as revenue (source). Run them as separate analyses and label
   which one a table shows.
2. **Do not read one as the other**: a flat user curve says nothing about revenue, and the reverse (own
   guidance).

## 2.6 Reading shapes
1. **A pattern needs a cause before it is acted on.** The source lists common curve shapes (an early drop that
   flattens, a decline that never flattens, newer cohorts better or worse than older ones, a sudden step at a
   fixed period) and attaches an interpretation to each; those are the author's heuristics. Treat each as a
   hypothesis to test, for example by checking releases, acquisition mix or a contract or trial end date, with
   the tools in `metric-movement-diagnosis-pitfalls`.
