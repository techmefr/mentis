# experiment-design-pitfalls §1 — Design before launch

A test designed after the data arrives is not a test. Everything below is written down before the first
user is assigned, because each item removes a way to argue for the result afterwards.

## 1.1 What is fixed in advance
1. **One hypothesis per experiment.** product-on-purpose's form is "We believe [change] for [users] will
   [outcome] as measured by [metric]"; if several things are being tested, run several experiments.
2. **One primary metric** decides the winner (nimrodfisher). It must be directly influenced by the change,
   measurable inside the test window and sensitive enough to show the minimum detectable effect. Secondary
   metrics give context; product-on-purpose suggests two or three.
3. **Guardrail metrics** that must not regress. nimrodfisher: a failed guardrail means do not ship, even if
   the primary metric wins. The RefoundAI summary of Kohavi's talk makes the reason concrete: a revenue
   number can often be raised by degrading the user experience, so the decision rests on an overall
   criterion that includes the guardrails (second-hand, paraphrased).
4. **Minimum detectable effect (MDE)**: the smallest lift that is practically significant (nimrodfisher).
5. **Split and exclusions.** Usually an even split; say why if it is not. Document who is excluded:
   product-on-purpose names employees, internal testers and users in conflicting experiments.
6. **Duration** comes from the power calculation and covers at least one full weekly cycle (nimrodfisher).
   product-on-purpose adds: do not stop mid-week when behaviour varies by day. phuryn asks for one to two
   full business cycles and enough time for novelty and primacy effects to wash out.
7. **Success criteria for win, loss and inconclusive**, defined before the test starts. product-on-purpose:
   this prevents post-hoc rationalisation and moving goalposts.
8. **Risks, monitoring and rollback criteria** (product-on-purpose): what will be watched during the run and
   what would end it early.

A card to fill before launch (shape from the sources, wording ours):

```
Hypothesis:        We believe ... for ... will ... as measured by ...
Primary metric:    definition | baseline | MDE (absolute)
Guardrails:        metric | what counts as a regression
Split / eligible:  ratio | who is in | who is excluded
Sample / duration: alpha | power | users per group | days (full weekly cycles)
Outcomes:          Win if ... | Lose if ... | Inconclusive if ...
Analysis date:     one look, on this date
```

## 1.2 Sample size
1. **Per group, for a rate** (nimrodfisher): n = 2 x (z_alpha/2 + z_beta)^2 x p x (1 - p) / MDE^2, where p
   is the baseline rate, MDE is absolute, z_alpha/2 is 1.96 for alpha 0.05 two-tailed and z_beta is 0.84 for
   80 percent power.
2. **Record the assumptions** next to the number: baseline, MDE, alpha, power (product-on-purpose asks for
   the calculation to be documented with its assumptions).
3. **Sources differ on the formula.** phuryn's version has no power term and asks to flag a test below 80
   percent power. This block uses the nimrodfisher form, which includes it.
4. **Compute, do not recall.** Worked check (our own arithmetic from the formula above): a 10 percent
   relative lift on a 5 percent baseline is 0.005 absolute, which gives about 29,800 users per group.
   The nimrodfisher guide prints a rule of thumb for the same case that is about half of this figure, so it
   contradicts its own formula; no rule-of-thumb count is carried here.
5. **Run the power check before launch.** The RefoundAI summary lists a power calculator for exactly this:
   expected traffic, acceptable runtime and minimum detectable impact, to avoid a month-long test that
   could never reach significance.
6. **When the sample cannot be reached in a reasonable time, say so.** The same summary treats "it will take
   too long to be actionable" as a reason to ship or decide on other evidence instead of testing (second-hand).

## 1.3 Choosing the metrics
1. **North star versus proxy.** If the north star metric needs weeks to move, use a leading proxy as the
   primary metric and keep the north star as a secondary signal (nimrodfisher).
2. **Pick a proxy that the change can move inside the window**, otherwise the test ends inconclusive for
   a reason decided at design time (own guidance, from point 2 of §1.1).
3. **Write the metric definition once** (numerator, denominator, filters, window) so that readout and
   design use the same number; see `analysis-validation-pitfalls` §2 for denominator mistakes.
