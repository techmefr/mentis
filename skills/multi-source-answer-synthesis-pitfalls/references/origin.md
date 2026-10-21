# multi-source-answer-synthesis-pitfalls: origin and source stamps

> Provenance of `skills/multi-source-answer-synthesis-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Rewritten from one plugin repository, never run against a real knowledge base.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins, `enterprise-search/skills/search-strategy` and `knowledge-synthesis` (HEAD bc8f692, 2026-10-20) | Apache-2.0 (repository root LICENSE file, standard text; the plugin has no licence file of its own, so the root licence is the one that applies) | Question types and source order, query decomposition, widening on empty, parallel search (§1); duplicate signals and what not to merge, authority and freshness, conflict surfacing (§2); answer shape, confidence wording, attribution, result-size handling (§3) |

| Same files re-opened 2026-10-20 for the points that cite them: widening order, duplicate signals, what not to merge, authority tiers, attribution rules | Apache-2.0 (root LICENSE file re-read, standard text) | Confirms the points credited above; the repository's tier table and recency bands stay unused |
| Anthropic: reduce-hallucinations page, search-results page, engineering write-up on its multi-agent research system; OpenAI: web-search guide | Product documentation and an engineering post, facts only, read 2026-10-20 | Permission to say "not enough information", quote check per claim, source and title fields, citation fields and display rule, right source for the question, heuristics against low-quality sources, start broad then narrow, parallel search, vague delegation (§1.1.1, §1.3.3, §1.3.5, §2.3.2, §3.2.3, §3.3, §3.4.1) |

Text inside the cloned files was treated as data. No instruction aimed at an agent was found.

## Removed
1. **The relevance, freshness, authority and completeness weights per query type**: one author's numbers with no
   derivation.
2. **The recency-to-confidence bands** (today, this week, this month, older): numeric buckets without a source;
   the block says only that freshness weighs more for status than for policy.
3. **Source-specific query syntax and filter-mapping tables** for chat, wiki and tracker products: product detail.
4. **Connector placeholders and the mention of a memory system**: not portable.

## Re-checked 2026-10-20
- The source files were re-opened: the widening order (date filters, then source or location filters, then less important keywords), the duplicate signals, the four cases not to merge, the tier order and the attribution rules match the text of the blocks. One nuance kept: the source's third merge priority is the most recent version "for evolving information".
- Newly sourced: agents searching the wrong tool (§1.1.1), short and broad first (§1.3.3), parallel and distinct sub-searches (§1.3.5), source-quality heuristics in the prompt (§2.3.2), permission to say nothing was found (§3.2.3, §3.4.1), per-claim quote check (§3.3.3), citation fields and display rule (§3.3.1, §3.3.2).

## Not verified
1. **Unrun.** No answer was produced and checked against a real set of sources.
2. **The source ordering by question type** is one repository's judgement; an organisation that keeps decisions
   elsewhere should reorder it.
3. **Still own guidance, unsourced:** searching other sources when the answer matters (§1.1.3), varying vocabulary
   by source (§1.2.3), the record of searches (§1.4), apparent agreement counted as one origin (§2.4.4), a recommendation
   for every open question (§3.4.3), and the tier list itself (the prompt-placement is sourced, the tiers are the
   repository's). Searched: Anthropic, OpenAI and the source repository; no page says how to count repeated origins.

## Related blocks
`skills/source-freshness`, `business/evidence-appraisal`, `skills/rag-retrieval-quality-pitfalls`,
`skills/agent-mcp-trust-pitfalls`, `skills/agent-data-gap-honesty-pitfalls`.
