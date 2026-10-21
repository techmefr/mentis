# rag-retrieval-quality-pitfalls: origin and source stamps

> Provenance of `skills/rag-retrieval-quality-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from library documentation and craft knowledge, never run by us. No metric was computed
and no pipeline was built while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| vibrantlabsai/ragas (commit 298b682), LICENSE file read; docs pages for faithfulness, context precision, context recall, noise sensitivity and answer relevance, the testset generation concept page for RAG, the evaluate-and-improve-a-RAG-app guide and the align-an-LLM-judge guide | Apache-2.0 (LICENSE file) | Metric definitions at idea level, query types for test sets, splitter by document type, trace-driven failure analysis, retrieval as the bottleneck in the worked example, judge alignment |
| Anthropic: contextual retrieval article; search-results documentation page | Product documentation, no licence granted on the text; facts only, rewritten, read 2026-10-20 | Exact identifiers and hybrid search (§1.3.1), chunk count tested (§1.3.5), citation fields and block granularity (§1.2.1, §3.2.2, §3.2.3) |
| OpenAI: file-search guide (tools) and retrieval guide | Product documentation, facts only, read 2026-10-20 | Result-count trade-off (§1.3.5), score threshold (§3.1.4), citation fields (§1.2.1), results hidden unless requested (§3.3.1) |
| pgvector README (the LICENSE file read, PostgreSQL licence); Azure AI Search pages on vector query filters, security filters, chunking and creating a vector index; Amazon Bedrock knowledge-base pages on chunking and on query configuration | Documentation, facts only, read 2026-10-20 | Post-filtering leaves fewer results (§1.2.2, §1.3.6), per-document access filter (§1.2.3), table context and parent chunks (§1.1.3, §1.1.4), embedding space (§1.3.4), date filter example (§1.2.4) |

Ragas pages re-opened on 2026-10-20 for the points that cite them: faithfulness (the claim-share example), noise
sensitivity (relevant and irrelevant modes, lower is better) and context precision (the rank example).

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
2. **Still own guidance, not sourced:** the version half of §1.2.1, "check ten random chunks" style checks,
   the worst-questions habit (§2.2.4), one-stage-at-a-time changes (§2.4.1), "answer only from the documents is a
   request" (§3.1.5), cited versus retrieved sets (§3.2.4), showing source date (§3.2.5), model-written
   references being invented (§3.2.2, last sentence), and the checkpoint paragraph.
3. **Sourced on 2026-10-20 from product documentation** (figures re-checked on the page): filter-after-search
   and the 40-candidate default are the pgvector README at that date; filter modes and their default date are
   Azure AI Search; parent replacement and the 10,000-character table limit are Bedrock. Each is product
   specific and moves; re-read before relying. The Elasticsearch and Qdrant filtering pages were opened and
   did not state execution order, so they are not credited.
4. **Corrected:** the former wording implied one store behaviour; it now names which products document which.
5. **Other Ragas pages** (agent metrics, multi-turn, cost, prompt optimisation) were not read.

## Checked 2026-10-20
Credited from a page re-opened for the exact point: §1.1.2 to §1.1.4, §1.2.1 to §1.2.4, §1.3.1, §1.3.4, §1.3.5,
§1.3.6 (new), §2.2.2 (softened: the Ragas example shows the effect, the page states no general rule), §3.1.4,
§3.2.2, §3.2.3, §3.3.1. Searched and not found on the pages read: an embedding-model-change statement on the
OpenAI embeddings guide, a multi-tenant statement on the Pinecone filter page.

## Related blocks
`llm-eval-regression-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `search-index-sync-pitfalls`,
`elasticsearch-mapping-and-reindex-pitfalls`, `ai-feature-acceptance-pitfalls`, `agent-context-hygiene-pitfalls`.
