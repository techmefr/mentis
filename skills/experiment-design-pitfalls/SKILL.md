---
name: experiment-design-pitfalls
description: "Use when an online controlled experiment (A/B test, split test) is designed, read out or reviewed: one pre-registered hypothesis, one primary metric, guardrails, minimum detectable effect, split and duration fixed before launch, sample size computed from a formula, analysing once instead of peeking, the sample ratio mismatch check, novelty effects, segments and multiple comparisons, results that look too good, negative and inconclusive results, long-term holdouts and whole-product impact."
---

# experiment-design-pitfalls

Not a step of the pipeline: a craft block for the A/B test, from the design card to the readout. The three
sections share one premise: **every decision taken after the data arrives (which metric, how long, which
segment, whether the split was fair) is a way to argue for the result you wanted**, so each is fixed or
checked before it can be abused. Tests of an idea at the discovery stage (interviews, prototypes) are in
`assumption-validation-pitfalls`; checking the numbers of any analysis is in `analysis-validation-pitfalls`.

## When
- Designing an A/B or split test: choosing metrics, sample size, duration, split, exclusions.
- Reading out a finished test, or reviewing someone else's readout before a ship decision.
- A result is "almost significant", looks too good, or someone wants to extend the test.
- A segment that "won" is proposed as the finding, or a lift is quoted as product-wide.

## Steps

**Read only the section the task meets.** §1 comes first when a test is not yet running; §2 and §3 are
independent of each other.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Design before launch: one hypothesis, primary metric, guardrails, MDE, split, duration, sample size, design card | a test is being planned or its design is reviewed | [`01-design-before-launch.md`](./references/01-design-before-launch.md) |
| 2 | Running and reading: analyse once, the SRM check, the primary result, guardrails, segments and multiple comparisons | results are about to be read or someone wants to peek or extend | [`02-running-and-reading.md`](./references/02-running-and-reading.md) |
| 3 | Surprises, null results, long-term effects: too-good results, honest negatives, holdouts, whole-pie impact, when not to test | a result is suspicious, flat or negative, or an impact number is being quoted | [`03-surprises-and-long-term.md`](./references/03-surprises-and-long-term.md) |

## Output / checkpoint
A design is done when someone who was not in the planning can answer from the card alone: what single
hypothesis is tested, which one metric decides, which guardrails block a ship, how many users per group and
why, how long it runs, and what counts as a win, a loss and an inconclusive result. A readout is done when it
states the SRM check, the interval of the primary metric, every guardrail, how many segments and metrics were
examined, and the decision with its reason. Read it once looking for a sentence that explains a choice made
after the fact (a metric, a segment, an extension) and for a lift quoted without the share of users who see
it. Nothing here was verified by running an experiment programme: the check is a read of the text.

## Guardrails
- Never read results before the sample ratio mismatch check; on a mismatch, do not interpret (§2.2).
- Never peek and stop, and never extend after a positive but non-significant result unless the design card
  said so. Sources differ on this and this block takes the analyse-once stance (§2.1).
- Never let a failed guardrail pass because the primary metric won (§1.1, §2.3).
- Never carry a sample-size rule of thumb; compute it from the formula and write the assumptions down (§1.2).
- Never present a segment found after the fact as the result; it is a new hypothesis (§2.4).
- Never treat a too-good result as a win before the bug hunt and a replication (§3.1).
- Thresholds in this block (0.05, 0.01, 80 percent power) are the sources' defaults, not laws; fix them in
  the design card (§1.1).

## Origin
Rewritten from nimrodfisher's data-analytics-skills (MIT), product-on-purpose's pm-skills (Apache-2.0),
anthropics' knowledge-work-plugins (Apache-2.0), phuryn's pm-skills (MIT) and, for principles only, RefoundAI's
lenny-skills (MIT), read 2026-10-16. Several are young 2026 repositories, one author's practice and not
consensus. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
