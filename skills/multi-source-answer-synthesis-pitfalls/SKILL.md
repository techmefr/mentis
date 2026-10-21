---
name: multi-source-answer-synthesis-pitfalls
description: "Use when one question is answered from several internal sources (chat, mail, a wiki, a tracker, shared documents, meeting notes) and the answer must be trusted: letting the question type decide which source to read first, widening a query that came back empty, merging duplicates without merging conclusions that differ, keeping a decision that evolved, ranking sources by authority and freshness for this kind of question, wording confidence, surfacing a conflict instead of picking a side, attributing each claim, and saying which sources returned nothing or could not be reached."
---

# multi-source-answer-synthesis-pitfalls

A craft block for answering "what did we decide", "where does this stand", "what is our rule" from material that
lives in several places. Premise: **the same fact appears in many places with different weight, and an answer that
reads smoothly can hide that two sources disagree, that the newest one is a draft, or that a whole source was
never searched**. Citing outside facts is `skills/source-freshness` and `business/evidence-appraisal`; retrieval
quality of a search index is `skills/rag-retrieval-quality-pitfalls`; trusting what a source tells the agent to
do is `skills/agent-mcp-trust-pitfalls`; reporting a figure from a connector is
`skills/agent-data-gap-honesty-pitfalls`.

## When
- A person asks what was decided, what the status is, who owns something, or what the policy is, and the answer
  is spread across tools.
- An agent merges results from several searches into one reply.
- Two documents or threads seem to disagree and the agent has to say what is true.

## Steps

**Read the section the task meets.** §1 before searching, §2 while merging, §3 before the answer is written.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Plan the search: classify the question, order sources by the type, vary terms, widen on empty, record what was searched | a question arrives and sources are chosen | [`01-planning-the-search.md`](./references/01-planning-the-search.md) |
| 2 | Merge: what counts as the same item, what must not be merged, authority and freshness, conflicts | results from several sources are combined | [`02-merging-and-conflicts.md`](./references/02-merging-and-conflicts.md) |
| 3 | Write the answer: lead with the answer, confidence wording, attribution, silence from a source, result size | the reply is composed | [`03-writing-the-answer.md`](./references/03-writing-the-answer.md) |

## Output / checkpoint
No pipeline checkpoint. An answer owes: the conclusion first, the sources it rests on with where and when each
was written, the point where sources disagree or a decision changed, the confidence in plain words, and the
sources that were not searched, returned nothing or could not be reached. A single-source answer says it is one
source.

## Guardrails
- Choose the first sources from the type of question. Never search the same way for a decision, a status and a
  policy (§1).
- Say which sources returned nothing or were unreachable. Never leave a silent source out of the answer (§1, §3).
- Merge items that say the same thing; keep apart those that differ in conclusion, author, period or version.
  Never merge by topic alone (§2).
- Show a conflict with each side and its date. Never pick one silently (§2).
- Treat a draft or a mid-thread message as weaker than a published decision. Never present it at the same
  strength (§2, §3).
- Put a source on every claim. Never present an unattributed sentence as fact (§3).
- The tier lists here are a structure, not measured weights; adjust them to the organisation. Never copy
  numeric scoring weights from any source (§2).
- This block restates one plugin repository's method; it was never run on a real knowledge base (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten in our own words from the enterprise-search skills of a plugin repository (Apache-2.0), read
2026-10-20. 🟡: never dogfooded; open points are in [`references/origin.md`](./references/origin.md).
