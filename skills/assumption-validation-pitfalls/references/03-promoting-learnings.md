# assumption-validation-pitfalls §3 — Promoting a finding to a learning

One test result is one story. A learning stated as a rule has to survive being retold, being checked in other
contexts and being contradicted. This section is the bar for promoting a finding, and the way to keep what
disagrees with it.

## 3.1 Three tiers
1. **Individual results** stay as they are, one hypothesis file each, loaded on demand (shinpr
   product-principles calls this tier 3).
2. **Learnings for one opportunity** sit with that opportunity and load when it is worked on (tier 2).
3. **Product-level principles** are distilled, always in view, and recorded with the conditions where they hold
   (tier 1).
4. **Promotion is proposed by an independent pass.** The source's distiller reads the artifacts directly in a
   separate context, so one narrative does not anchor the result (shinpr knowledge-distiller). The tool names
   and file layout are the source's and are not carried.

## 3.2 What counts as enough
1. **A single observation, or the same observation told several times, stays at the lowest tier**
   (knowledge-distiller).
2. **Independent evidence.** Promotion needs evidence that is independent and decision-relevant; its strength
   matters more than a count (shinpr).
3. **Context coverage.** The evidence must cover the segments or conditions the learning names. A deliberately
   segment-specific learning can stay at the opportunity level without research in unrelated segments.
4. **Actionable and not contradicted.** A product-level rule must influence future decisions and have its
   contradictions resolved or explicitly conditioned; an opportunity-level learning must be strong enough to
   change that opportunity's decision (knowledge-distiller).

## 3.3 Keep contradictions
1. **Do not average away conflicting evidence.** Record it as a conditional statement: under condition A,
   X holds; under condition B, the opposite does (shinpr).
2. **A contradiction becomes a discovery target only when resolving it can change a current decision**
   (knowledge-distiller).
3. **Learnings are stated within their conditions.** Treat a principle as established only inside the contexts
   where its evidence was recorded (product-principles).

## 3.4 Freshness
1. **Tag a promoted learning with the date it was last validated** (shinpr).
2. **Re-check when the governing conditions changed**, or when the old evidence cannot support a decision that
   is being made now, not merely because a timer elapsed.
3. **Traceability from hypothesis to decision**: hypothesis, validation, user story, requirements document,
   implementation and test stay linked (product-principles), so a result can be traced to what it changed.

A learning record (fields from the source, layout ours):

```
Learning:             one statement, within its conditions
Supporting results:   hypothesis ids | segments or contexts covered
Contradictions:       under condition A ... | under condition B ...
Tier:                 result | opportunity | product-level
Last validated:       date
```
