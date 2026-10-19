# variance-analysis-pitfalls §1 — Decompose and bridge

> Section 1 of `skills/variance-analysis-pitfalls`. Read it when a gap is split into drivers or a waterfall is
> built. Sourced from the variance-analysis skill of anthropics' knowledge-work-plugins (commit `33eeda1`,
> `finance/skills/variance-analysis/SKILL.md`), sections on decomposition and on waterfall methodology, read
> 2026-10-16. The algebra below was checked by hand in this session. Sentences marked "own guidance" are ours.

1. **Start with volume and price.** For anything that is a price times a quantity (revenue, a purchased cost),
   the source splits the total variance (actual minus budget, or minus prior) into a volume effect, the
   change in quantity valued at the base price, and a price effect, the change in price applied to the actual
   quantity. Written out: volume effect is (actual quantity minus base quantity) times base price; price effect
   is (actual price minus base price) times actual quantity.
2. **Prove that the parts sum.** Adding the two gives actual price times actual quantity minus base price times
   base quantity, which is the total variance, so the check is exact when the order of valuation is as in point
   1. The source states the same check. Own guidance: put the check in the write-up as a line, and a gap
   between the parts and the total is a defect in the split, not a rounding remark.
3. **Keep the order of valuation fixed.** Valuing the quantity change at the actual price and the price
   change at the base quantity gives a different split of the same total. Own guidance: choose one
   convention, state it, and use it in every period.
4. **Extra effects need a formula that sums.** The source also splits rate, mix, headcount and timing effects
   (for blended margins, people costs and spend categories). Carry the idea, not its formulas as written:
   a headcount-times-base-average and a rate-times-base-headcount pair leaves out the interaction between the
   two changes, so the pair does not sum to the total unless that term is placed somewhere. Own guidance:
   write the interaction as its own line or assign it by a stated rule, and test the whole split on a small
   example where the answer is known before using it on real figures.
5. **Spend without a price and volume** can be split by nature instead: costs driven by headcount, by
   volume, discretionary, contractual or fixed, one-off, and timing between periods. Own guidance: the buckets
   must be exclusive, or an item is counted twice.
6. **A bridge reconciles.** The source gives the structure: a starting value, a list of signed drivers, an
   ending value, and the check that start plus the sum of the drivers equals the end. Complement the picture
   with a table showing each driver's amount, its share of the total variance and a running total. A share
   can exceed one hundred percent when drivers offset each other, which is normal.
7. **Few drivers, ordered, with the rest grouped.** The source suggests ordering from the largest positive to
   the largest negative or in the business sequence, grouping small items into an "other" line, and labelling
   each bar with its amount and a short description. It names five to eight drivers as its limit; treat that
   as a readability habit, not a rule, and never hide a material item inside "other".
8. **A text bridge is acceptable** when no chart is available, provided the same arithmetic check is shown.
9. **Where to look first.** The source orders investigation by largest absolute amount, then largest
   percentage, then a direction against the trend, then an item that was on track and no longer is, then a
   variance that grows each period. Own guidance: it is an order of attention, not a cut-off; the line at which
   a variance needs an explanation comes from your organisation, and the source's own percentage table is not
   carried.
