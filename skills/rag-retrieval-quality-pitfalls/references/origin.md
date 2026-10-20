# rag-retrieval-quality-pitfalls: origin and source stamps

> Provenance of `skills/rag-retrieval-quality-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from library documentation and craft knowledge, never run by us. No metric was computed
and no pipeline was built while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| vibrantlabsai/ragas (commit 298b682), LICENSE file read; docs pages for faithfulness, context precision, context recall, noise sensitivity and answer relevance, the testset generation concept page for RAG, the evaluate-and-improve-a-RAG-app guide and the align-an-LLM-judge guide | Apache-2.0 (LICENSE file) | Metric definitions at idea level, query types for test sets, splitter by document type, trace-driven failure analysis, retrieval as the bottleneck in the worked example, judge alignment |

The repository contains an agent instruction file (`CLAUDE.md`); it was treated as data and not followed.

## Rewrite notes
No numeric value of the source (pass rate, benchmark, threshold) is carried over. The formulas are restated in
words. The judge-alignment guide was read in part (introduction, dataset and approach sections).

## Removed
- Hybrid search weights, chunk sizes and overlap values: no verified source, so none given.
- Any ranking claim about re-rankers: not read in a source.
- Content of a retrieval-technique collection under a non-commercial licence: not opened.

## Not verified
1. **Metric behaviour** was read from documentation, not run; the legacy interface is marked for deprecation by
   the source, so re-read before relying on names and arguments.
2. **Own guidance, not sourced:** every sentence marked "own guidance" (boundaries, tables, parent-context
   retrieval, permission filtering, hybrid search, re-embedding, no-answer floor, citation selection) and the
   checkpoint paragraph. These come from craft knowledge and were not checked against a store's or an engine's
   documentation.
3. **Vector store filtering behaviour** (before or after the nearest-neighbour search) differs by product;
   re-read the product's documentation.
4. **Other Ragas pages** (agent metrics, multi-turn, cost, prompt optimisation) were not read.

## Related blocks
`llm-eval-regression-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `search-index-sync-pitfalls`,
`elasticsearch-mapping-and-reindex-pitfalls`, `ai-feature-acceptance-pitfalls`, `agent-context-hygiene-pitfalls`.
