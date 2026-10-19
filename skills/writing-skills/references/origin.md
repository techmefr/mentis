# writing-skills references: origin of points 11 to 38

> Provenance of `references/11-authoring-rules.md` (points 11 to 30 from the first table, 31 to 38 from the section at the end). Read it to trace a rule to its source, never to apply one.

**Status: 🟡.** Stated from documentation, not measured by us. Re-read in full on 2026-10-19 before writing:

| Source | Licence | What it gave |
|---|---|---|
| agentskills/agentskills `docs/skill-creation/best-practices.mdx` (commit 69ef37e) | `docs/` is CC BY 4.0, credited; wording is ours | Points 11 to 24: real expertise, trimming, coherent units, calibrating control, defaults, procedures, gotchas, templates, checklists, validation loops, plan-validate-execute, bundling scripts, refining from real runs |
| `docs/skill-creation/optimizing-descriptions.mdx` | CC BY 4.0 | Points 26 to 28 and 30: imperative phrasing, user intent, contexts without the domain name, concision, the one-step-task nuance |
| `docs/specification.mdx` | CC BY 4.0 | Points 25 and 29: what-and-when, the 1024-character limit |

## Not verified
1. Point 29: the 1024-character cap is the open specification's. The 1,536 figure in `SKILL.md` Step 3 is
   a platform listing limit that was not re-checked here.
2. No point was measured on our own blocks; "gotchas beat other content" is the guide's claim, restated, not a
   finding of ours.
3. The guide's `skill-creator` automation was not read and is not used (rule B).
4. Overlap with `SKILL.md` Steps 1 to 10 was checked by reading them, not by search: steps 7 and 8 (ordering,
   positive requirement) are untouched and no point restates them.

## Points 31 to 38

**Status: 🟡.** Re-read on 2026-10-19: `skills/productivity/writing-for-agents/SKILL.md` in full and `SKILL-MECHANICS.md` in full, from `mattpocock/skills` (MIT, 2026 Matt Pocock, licence file read again). Wording is ours.

| Source section | Points |
|---|---|
| Steps and completion criteria | 31 |
| Leading words (the negation passage) | 32 |
| Pruning (no-ops) | 33 |
| Context pointers | 34 |
| Pruning (environment as cache) | 35 |
| Pruning (relevance, sediment) | 36 |
| Pruning (single source of truth), information hierarchy (co-location, sprawl) | 37 |
| Leading words | 38 |

Not taken: the model-invoked against user-invoked choice, splitting by invocation and router skills from `SKILL-MECHANICS.md` (platform mechanics of one harness, Rule D, and `references/claude-code-platform.md` owns them); the "two loads" framing and the human as index (opinion about one author's workflow); the progressive-disclosure ladder (the router form of `CONVENTIONS.md` already does it).

## Not verified / open decision for the owner

1. **Positive steering against our guardrail style (point 32).** The source says a ban pulls the banned behaviour into context. Our template's `Guardrails` section and the default-equals-failure rule are phrased as prohibitions, and several hooks enforce prohibitions mechanically. The source itself keeps a prohibition for hard guardrails that cannot be phrased positively, which most of ours are. Not decided: whether to rewrite existing guardrails with a positive target beside each. Nothing was rewritten.
2. Point 33 overlaps point 12 by design; the source's claim that the no-op test is model-relative was not tested by us.
3. Point 38 (leading words) is the source's claim about pretraining and was not measured; the example words are the source's.
4. Nothing in points 31 to 38 was run against our own blocks, and `skill-trigger-evals` was not used to check point 34.

