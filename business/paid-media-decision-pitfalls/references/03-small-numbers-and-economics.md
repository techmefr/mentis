# paid-media-decision-pitfalls §3 — Small numbers and economics

Most false findings in a small account are sample-size errors that look like insight. Doubt runs both ways:
one conversion on one click proves no more than no conversion in five clicks disproves. This section is the
arithmetic to run before calling spend wasted, and it ends in a refusal to carry a universal kill rule.
Every formula below was recomputed in this session (see the check lines).

## 3.1 No conversions in N clicks rules out only high rates
1. **The statement.** If a term got N clicks and no conversion, you can rule out only conversion rates above a
   bound. At 95 percent confidence the bound is the rate p at which a run of N clicks with no conversion would
   happen one time in twenty, that is `(1 - p)^N = 0.05`, so `p = 1 - 0.05^(1/N)`. The 95 percent level is a
   convention used here to show the size of the effect; the level that suits a real decision is for someone
   who owns the statistics.
2. **The table** (computed, not quoted):

| Clicks, no conversion | Rates ruled out at or above | What you can honestly say |
|---|---|---|
| 5 | 45 percent (45.07) | nothing; no conversion is the expected outcome |
| 10 | 26 percent (25.89) | still nothing useful |
| 30 | 9.5 percent | you may begin to doubt a strong rate |
| 50 | 5.8 percent | meaningful only where a high rate was plausible |
| 100 | 3.0 percent (2.95) | evidence against any rate above that |

   Check: `1 - 0.05^(1/N)` gives 45.07, 25.89, 9.50, 5.82 and 2.95 percent for N = 5, 10, 30, 50 and 100. The
   source's own table rounds the middle rows to 10, 6 and 3 percent; the rule of thumb "3 divided by N" is
   close for large N (3.0 percent at N = 100) and loose for small N (60 percent at N = 5, against 45).
3. **One conversion on one click is noise too.** A single early success does not show that a term works.

## 3.2 Break-even before "wasted"
1. **Compute the conversion rate the spend would have to reach to be worth keeping.** Cost per result equals
   cost per click divided by conversion rate, so the rate that exactly meets a target cost per result is
   `break-even conversion rate = cost per click / target cost per result`.
2. **Worked example.** At a click cost of 2.00 and a target of 40.00 per result, break-even is 2.00 / 40.00 =
   0.05, that is 5 percent. Ruling out 5 percent at 95 percent confidence needs the smallest N with
   `0.05^(1/N) >= 0.95`, which is 59 clicks (check: 0.95^59 = 0.0485, below 0.05, and 0.95^58 = 0.0510,
   above). Below 59 clicks with no conversion, this term has not been shown to miss the target.
3. **If the plausible rate for that traffic is below the break-even rate, the term is not failing, it is
   unmeasured.** Say so. If the plausible rate is well above it, a long run of clicks without a conversion is
   worth a look sooner.
4. **Give the date by which a readable sample exists, or say it never will.** At the same example, 59 clicks
   at five clicks a month takes about 12 months (59 / 5 = 11.8). "Let it run" is an honest answer only with a
   date you will actually know by. Sometimes the honest answer is that this term cannot be judged and its
   budget belongs elsewhere or the term belongs inside a broader group.
5. **Derive targets from deal arithmetic, not from a benchmark.** A target cost per result comes from what a
   result is worth to the business (value, margin, how often a lead becomes a customer). When the source of
   that number is missing, write MISSING (§1.3) and do not borrow a platform's average.

## 3.3 No fixed kill rule, and no summed windows
1. **A cost spike is a question, not a verdict.** Doubling on a handful of conversions, with a conversion lag
   still filling in, is noise until sample size, lag and learning state are checked (§2.3, §2.4). Never pause
   an ad on a fixed multiple of the target.
2. **If someone asks for a kill rule, build it from the account.** Show what the proposed rule would have
   stopped over the last months and whether those would have been the right stops, given the lag. A rule
   that nobody tested against history is a mood with a number in it. A repeatable rule is better than a mood;
   a rule copied from another account's thresholds is neither.
3. **Never replace a producer without a staged replacement** and never judge the replacement on its first few
   days (§2.3).
4. **Do not apply one budget-to-cost ratio across objectives.** Awareness, lead generation and purchase
   campaigns have different economics; a single ratio is a defect of the review, not of the campaigns.
5. **Do not sum conversions built on different windows or definitions.** Show them side by side with each
   window named (`business/ad-measurement-pitfalls` §3).
