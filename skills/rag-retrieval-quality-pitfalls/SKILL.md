---
name: rag-retrieval-quality-pitfalls
description: "Use when an application answers from retrieved documents (RAG) and the answers are wrong, vague or unsupported, or when one is built or reviewed: how documents are split and indexed (chunk boundaries, metadata, stale or foreign-permission content, exact identifiers), how to evaluate retrieval separately from generation (reference sets by query type, recall and rank metrics, noise sensitivity), how to check grounding and citations at claim level, and the order in which to diagnose a bad answer (corpus, retrieval, ranking, context, generation) before changing anything."
---

# rag-retrieval-quality-pitfalls

A defensive block for the moment a retrieval-augmented answer is called "bad". The three sections share one
premise: **a wrong answer has five possible homes (the corpus, the retriever, the ranking, the prompt context,
the generation), and one end-to-end score cannot tell them apart; measure each stage before touching any**.
Measuring a prompt or model change in general is in `llm-eval-regression-pitfalls`; the untrusted text inside
retrieved documents is in `llm-app-prompt-injection-and-exfiltration-pitfalls`; the search engine side of
indexing is in `search-index-sync-pitfalls` and `elasticsearch-mapping-and-reindex-pitfalls`; accepting an AI
feature is in `ai-feature-acceptance-pitfalls`.

## When
- A RAG answer is wrong, says "not found" although the document exists, or states things no document says.
- Choosing how to split, index or search documents for a new assistant.
- Writing an evaluation for a retrieval pipeline, or a score moved and nobody knows which stage moved it.
- An answer cites a source and a reader cannot find the claim in it.

## Steps

**Read only the section the task meets.** They are independent, but §3.3 (diagnosis order) is the entry point
for any live complaint.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Splitting and indexing: boundaries, metadata, exact identifiers, staleness, who may see what | a corpus is chunked, re-indexed or searched | [`01-chunking-and-index.md`](./references/01-chunking-and-index.md) |
| 2 | Retrieval evaluation: reference sets by query type, recall, rank quality, noise, judge alignment | retrieval is measured or a retrieval change is judged | [`02-retrieval-evaluation.md`](./references/02-retrieval-evaluation.md) |
| 3 | Grounding, citations and failure diagnosis order | an answer is unsupported, a citation is checked, or a complaint arrives | [`03-grounding-and-diagnosis.md`](./references/03-grounding-and-diagnosis.md) |

## Output / checkpoint
Each failing question is filed under exactly one stage (corpus, retrieval, ranking, context, generation) with
the evidence that put it there (§3). Retrieval has its own numbers, reported apart from answer quality, on a
reference set that includes each query type the product receives (§2). Chunking, metadata and permission rules
are written down next to the index definition (§1). A change is judged by the metric of the stage it targets.

## Guardrails
- Never tune the prompt or swap the model before the failing question was placed in a stage (§3).
- Never publish one end-to-end score as the retrieval score (§2).
- Never accept a citation that was not checked against the cited passage (§3).
- Never index a document without carrying who may read it and when it was last true (§1).
- Never evaluate retrieval on questions all written from one chunk's wording (§2).
- Never let the model answer silently when nothing relevant was retrieved; return "not found" or ask (§3).
- This block is idea-level guidance from the sources in [`references/origin.md`](./references/origin.md), read on
  the date there. Nothing was run, and no metric was computed, while writing it. Numeric thresholds are not
  given because none was verified.

## Origin
Rewritten at idea level from the documentation of the Ragas evaluation library (Apache-2.0), read 2026-10-20,
and from craft knowledge marked "own guidance" in the references. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
