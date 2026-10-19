---
name: agent-context-hygiene-pitfalls
description: "Use when an agent's results get worse as its context grows, or before a long-running agent's context is designed: the five degradation patterns (important text lost in the middle, poisoning by a wrong claim, distraction by irrelevant material, confusion between tasks, clash between contradicting sources), diagnosing them before blaming the model (variance, prompt quality, the cliff shape), recovering from poisoning by truncating, and the write, select, compress and isolate mitigations with compaction placed before the onset."
---

# agent-context-hygiene-pitfalls

A block for the moment an agent that worked at the start of a session starts to ignore, repeat or invent things
later in it. The two sections share one premise: **what sits in the context is input like any other, and
unverified input that stays in the context keeps being obeyed**. Isolating work in separate agents is in
`multi-agent-design-pitfalls`; fanning out is in `dispatch-parallel`; handing a session's state to the next one is
in `handoff`; measuring whether a change helped is in `llm-eval-regression-pitfalls`. Untrusted content as an
attack is in `agent-mcp-trust-pitfalls`; this block is about accidents of accumulation.

## When
- A long session degrades: instructions given earlier are ignored, a corrected error comes back, tools are
  called for the wrong task.
- Designing what a long-running agent loads, keeps and drops.
- Several retrieved or loaded sources disagree and the agent has to pick.
- Deciding when to compact, summarise or start over.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Patterns and diagnosis: the five degradation patterns, their symptoms, what to rule out first, why thresholds are not portable | a session misbehaves and the cause is not yet known | [`01-patterns-and-diagnosis.md`](./references/01-patterns-and-diagnosis.md) |
| 2 | Mitigation: write, select, compress, isolate, just-in-time loading, observation masking, where compaction triggers, finding the onset on your workload | a context strategy is being designed or changed | [`02-mitigation.md`](./references/02-mitigation.md) |

## Output / checkpoint
Before a session is called degraded, the same prompt was run at a small context and several times, so variance
and a bad prompt are ruled out (§1). The pattern was named, and the fix matches it: truncation for poisoning,
precedence for clash, segmentation for confusion, curation for distraction (§1, §2). Compaction triggers at a
point measured on this workload, before the failure, and summaries are treated as input that can poison (§2). A
context strategy that was never tested at growing sizes is not verified.

## Guardrails
- Never diagnose degradation from one bad run (§1).
- Never correct a poisoned context by adding corrections on top; remove the poison (§1).
- Never copy a published context threshold into a design; measure on your model and workload (§1, §2).
- Never let a model-written summary replace its source without keeping where each claim came from (§2).
- Never load everything that might be needed; leave it behind a retrieval step (§2).
- Restates one context-engineering skill collection as of the commit in [`references/origin.md`](./references/origin.md).
  Its research figures, thresholds and benchmark names were not verified and none is carried over. No
  agent was run while writing this.

## Origin
Rewritten from the context-degradation skill of a context-engineering collection (MIT), read 2026-10-16. 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
