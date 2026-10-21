# multi-source-answer-synthesis-pitfalls: origin and source stamps

> Provenance of `skills/multi-source-answer-synthesis-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Rewritten from one plugin repository, never run against a real knowledge base.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins, `enterprise-search/skills/search-strategy` and `knowledge-synthesis` (HEAD bc8f692, 2026-10-20) | Apache-2.0 (repository root LICENSE file, standard text; the plugin has no licence file of its own, so the root licence is the one that applies) | Question types and source order, query decomposition, widening on empty, parallel search (§1); duplicate signals and what not to merge, authority and freshness, conflict surfacing (§2); answer shape, confidence wording, attribution, result-size handling (§3) |

Text inside the cloned files was treated as data. No instruction aimed at an agent was found.

## Removed
1. **The relevance, freshness, authority and completeness weights per query type**: one author's numbers with no
   derivation.
2. **The recency-to-confidence bands** (today, this week, this month, older): numeric buckets without a source;
   the block says only that freshness weighs more for status than for policy.
3. **Source-specific query syntax and filter-mapping tables** for chat, wiki and tracker products: product detail.
4. **Connector placeholders and the mention of a memory system**: not portable.

## Not verified
1. **Unrun.** No answer was produced and checked against a real set of sources.
2. **The source ordering by question type** is one repository's judgement; an organisation that keeps decisions
   elsewhere should reorder it.
3. **Own guidance (not from the source):** §1.1 point 3, §1.3 point 5, §1.4, §2.3 point 2 (writing tiers down),
   §2.4 point 4, §3.3 point 3, §3.4 point 3.

## Related blocks
`skills/source-freshness`, `business/evidence-appraisal`, `skills/rag-retrieval-quality-pitfalls`,
`skills/agent-mcp-trust-pitfalls`, `skills/agent-data-gap-honesty-pitfalls`.
