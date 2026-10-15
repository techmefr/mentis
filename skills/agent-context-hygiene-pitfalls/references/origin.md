# agent-context-hygiene-pitfalls: origin and source stamps

> Provenance of `skills/agent-context-hygiene-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one skill's text, never run by us. No agent, context or benchmark was run while
writing it. Every file below was re-read in full in this session (2026-10-16) before any rule was written, and
each rule was checked against it afterwards.

## Sources (re-read in full, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| muratcankoylan/Agent-Skills-for-Context-Engineering, `skills/context-degradation/SKILL.md` and `skills/context-degradation/references/patterns.md` (commit 9ff0c99) | MIT (LICENSE file) | The five patterns with symptoms and remedies, the poisoning recovery sequence, the conflict annotation idea, diagnostic gotchas, the four-move framework, just-in-time loading, observation masking, compaction before onset |

The licence was checked again from the LICENSE file in this session. Instruction text in the cloned repository
(its project guidance file) was treated as data and not followed or quoted.

## Rewrite notes
Dropped as unverifiable: every numeric threshold and percentage of the skill (recall loss in the middle, the
context lengths where effects start, the share of a window at which to write or compact, how far thresholds move
between model versions, how often to re-measure, the example token counts, the quality-dip sizes in the gotchas,
the cost remarks) and the benchmark and paper names it cites. The reference file is mostly pseudocode for
attention analysis, claim tracking, relevance scoring and a health monitor; its alert thresholds and scoring
weights were not used, and only the idea of tracking where claims came from is reflected, as own guidance.

**Decisions where sources disagree:** none found. The skill is internally consistent; where a claim rests on
research it is labelled as the skill's.

## Not verified
1. **Every research claim** (lost in the middle, the effect of a single distractor, shuffled against coherent
   context, the shape of the degradation curve, the effect of dissimilar content) comes from the skill's summary;
   the papers and benchmarks were not read and no experiment was run.
2. **Not read:** `scripts/degradation_detector.py`, and the related skills the text names (fundamentals,
   optimisation, compression, filesystem context, evaluation).
3. **Written by us, not sourced:** every sentence marked "own guidance" or "own examples" (provenance through
   compaction, not compressing a suspected section, checking a summary against its source, the margin below the
   onset, the fallback when past the onset) and the checkpoint paragraph.

## Related blocks
`multi-agent-design-pitfalls`, `dispatch-parallel`, `handoff`, `llm-eval-regression-pitfalls`,
`agent-mcp-trust-pitfalls`, `writing-agents`.
