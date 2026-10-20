# pricing-and-packaging-pitfalls §5 — Willingness-to-pay research

A survey tells you what people say about prices. This section says which method answers which question and how
to read two of them without overclaiming. Method facts only; the way to run a live test is
`skills/experiment-design-pitfalls`.

## 5.1 The method follows the question
1. **A price range for something new:** a price-sensitivity survey of the Van Westendorp kind (§5.2).
2. **Demand at specific prices for an offer people already understand:** a stepped-price survey of the
   Gabor-Granger kind (§5.3).
3. **Trade-offs between features and price, and packaging:** a conjoint study or a best-worst ranking of
   features. Both need design skill and tooling; do not improvise either.
4. **Real purchase behaviour:** a price test on real traffic, last.
5. **A stated price is a statement, not a purchase.** Respondents overstate intent; the method pages say so.

## 5.2 Reading a price-sensitivity survey (four questions)
The four questions ask where a respondent finds the product too cheap to trust, a bargain, getting expensive
but still considered, and too expensive to consider.
1. **Validate before analysing.** One currency, one billing period, one product description for every
   respondent. Check each respondent's thresholds are in order (too cheap at or below bargain, at or below
   getting expensive, at or below too expensive). **Record exclusions and their number** instead of quietly
   editing an answer.
2. **Get the curve directions right.** At each candidate price, the two "cheap" curves (too cheap, bargain)
   count respondents whose threshold is at or above that price, so they fall as the price rises. The two
   "expensive" curves count respondents whose threshold is at or below it, so they rise. Using one rising
   cumulative on all four reverses the meaning of the cheap curves. Record how ties are counted.
3. **The named crossings are survey points.** They give a lower and an upper edge of an acceptable range and
   two interior points. The names ("optimal") are historical: they are not a revenue or profit optimum, and the
   method pages say the line-crossing reading has weak theoretical grounding.
4. **The base method predicts no demand.** It does not give purchase likelihood or volume. Extensions add
   purchase-intent questions at selected prices and apply discount factors because intent is overstated; they
   carry their own assumptions, state them if you use one.
5. **It leaves out competition, cost, margin and positioning.** Respondents judge one product with no set of
   alternatives; add the alternatives to the question or to the analysis.
6. **It fits a new-to-the-market product best.** For an established offer, a stepped-price or choice study
   fits better.
7. **Segment before reading.** Run it for the segment that would buy, not a panel of anyone.
8. **Report n per segment and the uncertainty around each crossing**, not one number. The sources gave
   minimum sample sizes that disagree and have no derivation; do not quote one.

## 5.3 Reading a stepped-price survey
In the usual form the researcher fixes a small set of prices, shows a respondent one of them chosen at
random, asks about purchase intent, and moves to the next higher price after a yes or a lower one after a
no. The answers become a demand curve and, with the price, a revenue curve.
1. **Randomise the first price shown.** A fixed first price anchors every answer after it.
2. **Use evenly spaced prices.** Uneven gaps distort the curve's shape, and the curve only exists at the
   prices you chose.
3. **Decide how respondents who say no at the lowest price are coded** (zero, or dropped) and write it down;
   the choice moves the curve.
4. **Stated intent over-reports purchase.** Read the curve as an upper bound on demand and a ranking of
   prices, not a forecast.
5. **It values one offer at a time.** It says nothing about which features belong in which plan.
6. **Run it after a range is known** (§5.2), so the steps sit where the answer is.

## 5.4 Validate with behaviour
A live price test follows `skills/experiment-design-pitfalls`: a hypothesis stated before launch, revenue per
visitor as the primary metric, guardrails on downgrades and retention, a fixed duration and, where
possible, a holdout. **Measure the long tail** (retention, downgrades, support load) for the customers who
bought at the tested price. Do not assume it.

## 5.5 What a study delivers
1. **A range and a shortlist of candidate prices**, with n per segment, the exclusions and the assumptions.
2. **Never "the price".** The person who owns pricing picks the number, with cost, competition and strategy in
   view.

**Never** let a crossing point or a revenue peak on a survey curve go into a plan as the price. It goes in as
a candidate to test.
