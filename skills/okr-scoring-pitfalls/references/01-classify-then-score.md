# okr-scoring-pitfalls §1 — Classify, then score

The convention follows the type of the objective, not the mood at grading time. Everything below is decided
from the original OKR set, before any final value is read.

## 1.1 Type first
1. **Five types** (product-on-purpose's enum): committed, aspirational, learning, operational health,
   compliance or safety. Carry the type from the original set; if the set did not state one, assign a default
   and say that it was assigned.
2. **Indicator class is a second, independent label**: leading, lagging, guardrail, health or evidence
   generation. The type decides the scoring convention; the class adds reporting rules on top. A guardrail is
   a class, not a type.
3. **Why the order matters**: the same 0.7 means success on an aspirational objective and a miss on a
   committed one, so a type chosen after seeing the number is a way to pick the verdict.

## 1.2 One convention per type (product-on-purpose)
| Type | How it is scored |
|---|---|
| aspirational | 0 to 1: (actual minus baseline) divided by (target minus baseline) |
| committed | pass or fail against the target; below the target is a miss that needs a postmortem |
| compliance or safety | binary, met or not met; no partial credit |
| operational health | pass, fail or drift within tolerance, against a threshold band |
| learning | validated, invalidated, partially validated or insufficient evidence; no number |

1. **The aspirational sweet spot** is stated by the source as 0.6 to 0.7, below 0.4 a miss, and a score above
   0.8 over several cycles a hint that the targets were set too low. The source attributes the convention to
   Doerr, Wodtke and others; that attribution was not checked here, so carry it as "per source" and let the
   team set its own band in advance.
2. **Never soften a committed miss.** Not hitting a committed target is a miss, not "ambitious failure", and
   effort does not turn it into a partial pass (product-on-purpose).
3. **Never read 0.7 as success** for committed, compliance or safety, or operational health; those aim at the
   full target or the band.
4. **Honest stretch is not punished** when the objective was disclosed as aspirational at writing time; a
   0.6 there is the designed result (product-on-purpose).

## 1.3 The guardrail rule
1. **A guardrail is scored by its own type and also reported alone.** It is never averaged into the primary
   objective score (product-on-purpose).
2. **A failed guardrail does not shrink because the primary key result went well**, whatever type the
   guardrail itself has.
3. **Do not force one number onto mixed types.** The source's template leads with a qualitative read and
   warns that a single average across different types means nothing; give the per-key-result scores and a
   sentence on what they do and do not mean.

## 1.4 Not observable yet, or only partly
1. **Not yet observable**: the key result's window ends after the cycle (a 90-day retention cohort is the
   source's example). Do not force a score; give an interim signal, a projected score with its confidence, and
   the date the final score becomes available (product-on-purpose).
2. **Not yet fully observable**: a committed or compliance key result with partial coverage. If the commitment
   named three audits and one is done, the one is a sub-signal and the key result is deferred; it is not a
   pass "on the part in scope" (product-on-purpose).
3. **Missing inputs get a marker, never a guess**: product-on-purpose names not-yet-observable,
   not-instrumented and not-supplied. A key result whose original definition is missing is not graded.
4. **The score is for the cycle, not for the future**: a single cycle's suggestive result is a reason for a
   second cycle of evidence, not proof (product-on-purpose).
