# experiment-design-pitfalls §3 — Surprises, null results and the long term

Three readouts that need extra care: a result that looks too good, a result that says nothing, and a win
whose size is quoted for the whole product.

## 3.1 A result that is too good
1. **Treat it as a suspect before it is a win.** The RefoundAI summary of Kohavi's Twyman's law: a figure
   that looks unusually good is usually wrong, so hunt for a bug and replicate before celebrating (second-hand,
   paraphrased).
2. **Order of checks** in that summary: the sample ratio mismatch check first, the data pipeline second,
   replication third. Apply it in that order.
3. **Replicate a surprising result**, more than once if needed (same summary).
4. **Check the guardrails as hard as the primary metric**: a big lift with a quiet guardrail is the pattern
   the guardrails exist for (own guidance).

## 3.2 Negative and inconclusive results
1. **Report them honestly.** product-on-purpose's results checklist: negative or inconclusive results are
   reported as such, with confidence intervals, secondary and guardrail metrics and segment effects.
2. **Say which outcome it was**, using the win, loss and inconclusive definitions fixed in §1.1. An
   inconclusive test is a legitimate outcome, not a failed one.
3. **Write what was learned beyond the numbers** (product-on-purpose): surprising findings, open questions,
   implications for the hypothesis. Negative results are learnings.
4. **End with a decision**: ship, iterate or kill, with the reasoning and next steps (product-on-purpose).
   Not significant means no ship under §2.3; "iterate" needs a new hypothesis, not an extension.
5. **Keep the readout findable** so the same experiment is not repeated; the RefoundAI summary lists lost
   institutional memory among the common mistakes.

## 3.3 Long-term effects and whole-product impact
1. **A short test can show a pull-forward.** The RefoundAI summary recommends long-term holdouts, a small
   group kept on the old experience for months, to tell immediate gains from a real downstream effect, and
   to re-read old experiments later (second-hand; no figures carried).
2. **Whole-pie impact**: the total effect is the relative improvement multiplied by the share of users who
   actually see the change (same summary). A big lift on a rarely seen surface can matter less than a small
   lift on a surface everyone sees.
3. **State the share in the readout** when quoting a business impact, so the number is not read as a
   product-wide gain (own guidance, from point 2).
4. **Hierarchy of evidence** (same summary): anecdote, observational study, natural experiment, controlled
   experiment, repeated controlled experiments, from least to most trusted. A before and after comparison
   is not an experiment (own guidance).

## 3.4 Not every change needs a test
1. **The cost of testing counts.** The RefoundAI summary lists three reasons to skip a test: results would
   take too long, the downside risk is low, or the thing is new and has no control. For a new product it
   suggests independent success criteria instead (second-hand).
2. **Weigh the risk before testing**: can a negative impact be detected another way, and what will actually
   be done with the result? These are two of the summary's five risk questions. If nothing would change, do not run it (own guidance).
