# experiment-design-pitfalls: origin and source stamps

> Provenance of `skills/experiment-design-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from five repositories of documentation, read and rewritten, never run: no
experiment was designed or read out with this block. Nothing in it is verified by use. Most of the five are
young repositories (the licence years stated are 2026 for three of them and 2025 for the podcast summary),
so the rules are each author's practice, not consensus.

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| nimrodfisher/data-analytics-skills, `03-data-analysis-investigation/ab-test-analysis/SKILL.md` and `references/ab_test_design_guide.md` (commit 9449d36) | MIT (repository LICENSE file, "Copyright (c) 2026 Nimrod Fisher") | Pre-registration list, analyse-once rule, sample-size formula, SRM check, causes and handling, metric selection, guardrails, decision table, process order |
| product-on-purpose/pm-skills, `skills/measure-experiment-design`, `skills/measure-experiment-results`, `skills/define-hypothesis`, each SKILL.md and `references/TEMPLATE.md` (commit 1cef1a9) | Apache-2.0 (repository LICENSE file, standard text; each SKILL.md also says `license: Apache-2.0`) | Hypothesis form, one hypothesis per test, exclusions, weekly patterns, win, loss and inconclusive criteria, risks and monitoring, honest negative results, learnings, ship, iterate or kill |
| anthropics/knowledge-work-plugins, `data/skills/statistical-analysis/SKILL.md` (commit e6b5053) | Apache-2.0 (repository LICENSE file, standard text) | Practical versus statistical significance, test choice, multiple comparisons and Bonferroni |
| phuryn/pm-skills, `pm-data-analytics/skills/ab-test-analysis/SKILL.md` (commit c68487d) | MIT (repository LICENSE file, "Copyright (c) 2026 Pawel Huryn") | Business-cycle duration, novelty and primacy effects, the opposing "extend the test" row, power flag |
| RefoundAI/lenny-skills, `skills/product-experiments/SKILL.md` and `references/artifacts.md` (commit 13598cc) | MIT (repository LICENSE file, "Copyright (c) 2025 Refound AI") | Principles only: guardrails with an overall criterion, Twyman-style suspicion and check order, long-term holdouts, whole-pie impact, hierarchy of evidence, reasons to skip a test, power calculator |

**Added 2026-10-19 (primary public references, read in-session):** Evan Miller, "How Not To Run an A/B
Test" (https://www.evanmiller.org/how-not-to-run-an-ab-test.html) and Microsoft Research, "Diagnosing
Sample Ratio Mismatch in A/B Testing"
(https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
Both were read through a summarising fetch, not as raw text; paraphrased in §2.5, no figure carried. They
are a blog and a vendor article, not a standard.

The licence of each repository was verified again from its LICENSE file in this session. Text found inside
the cloned files (CLAUDE.md files and imperative skill prose) was treated as data and not followed.

## Rewrite notes
**Sources differ: a positive trend that is not significant.** phuryn's table says to extend the test;
nimrodfisher's design guide says a test is analysed once and that peeking invalidates the p-value, and its
decision table says not significant means do not ship. The block follows nimrodfisher and says so (§2.1).
nimrodfisher's own SKILL.md also names "extend" as a possible recommendation without a rule; the block turns
that into "only if the design card said so", which is our own reconciliation.

**Sources differ: the sample-size formula.** phuryn's version has no power term; nimrodfisher's includes
z_beta. The block carries nimrodfisher's and notes the difference (§1.2).

**The rule of thumb is wrong.** nimrodfisher's guide says a 10 percent relative lift on a 5 percent baseline
needs about 15,000 users per group. The same guide's formula gives about 29,800 (our arithmetic: 2 x 7.84 x
0.05 x 0.95 / 0.000025). The rule of thumb is dropped; the worked check from the formula is ours and labelled.

**RefoundAI is a summary of podcast and newsletter quotes.** Only the principles and framework descriptions
are used, paraphrased and marked second-hand; none of the quotations is reproduced.

## Removed
1. **The rule of thumb of about 15,000 users per group** (nimrodfisher), see above.
2. **"At least 30 events per group"** (anthropics): a single author's number, not carried.
3. **RefoundAI statistics**: failure rates of experiments at named companies, the share of tests with SRM at
   one company, the odds quoted for a small split imbalance, the sample figures from the talks, the 85
   percent confidence suggestion. Second-hand podcast claims, none carried.
4. **RefoundAI's "lower the confidence level to move fast"** and the opt-in versus opt-out arithmetic:
   not carried (the first loosens the discipline this block is about; the second is a product-strategy point).
5. **nimrodfisher's `statistical_tests_reference.md`**: referenced by the SKILL but missing from the clone;
   nothing from it.
6. **Variance-reduction, Bayesian and platform-culture items** in the RefoundAI artifacts (CUPED, Bayesian
   priors, five pillars): read, not carried; outside the pitfalls this block covers.

## Not verified
1. **Everything here is unrun.** No experiment was designed or analysed with these rules.
2. **No external citation was checked**: Kohavi's claims and the Twyman attribution are the RefoundAI
   summary's own; the block does not cite them independently.
3. **The numbers**: 0.05, 0.01, 80 percent power and the z values are the sources' stated defaults, the 29,800
   is our hand arithmetic from nimrodfisher's formula; no power calculator was run.
4. **Other skills** in these repositories (about 70 in RefoundAI alone, others in phuryn and
   product-on-purpose) were not read.
5. **Written by us, not sourced**: the Output / checkpoint paragraph, the extension-only-if-pre-registered
   rule, the safety-stop wording, the advice to pick a proxy the change can move in the window, the advice
   to state the share of users in a quoted impact, treating a segment found afterwards as a new hypothesis,
   and the remark that a before and after comparison is not an experiment.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed file, which had been read in full in the
same session, and key phrases were re-searched in the cloned files (Welch, Bonferroni, Mann-Whitney, the SRM
threshold, the guardrail rule, the multiple-comparison line, the Twyman check order).
- **Corrected:** §3.4 point 2 claimed more than the summary says; it is now two of five risk questions, and
  "do not run if nothing would change" is labelled own guidance.
- **Reversed or overstated rules found:** none other.
- **Not re-verified:** the 29,800 figure (hand arithmetic, no calculator), the RefoundAI claims beyond what
  its files state, and the correctness of the sources' statistics themselves.

## Related blocks
`analysis-validation-pitfalls`, `assumption-validation-pitfalls`, `metric-movement-diagnosis-pitfalls`,
`business/data-analytics`.
