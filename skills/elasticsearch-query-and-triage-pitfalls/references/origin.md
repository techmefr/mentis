# elasticsearch-query-and-triage-pitfalls: origin and source stamps

> Provenance of `skills/elasticsearch-query-and-triage-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from skill documents, never run by us against an Elasticsearch cluster. No query was
profiled, no ruleset created and no allocation explained while writing it.

## Sources (all read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| elastic/agent-skills at commit baa5111 (2026-09-10): `skills/elasticsearch/elasticsearch-query-optimization/SKILL.md`, `references/query-optimization-reference.md` | Apache-2.0 (`LICENSE` re-read 2026-10-16, Apache License Version 2.0 text) | Profile-first diagnosis, collector signatures, `filter` against `must`, field types for `term`, leading wildcards and alternatives |
| elastic/agent-skills at baa5111: `skills/elasticsearch/elasticsearch-search-relevance/SKILL.md`, `references/multi-match-tuning.md`, `references/query-rules-reference.md` | Apache-2.0 (same file) | Choice between query rules and organic tuning, rule types, criteria, actions, `rule` query wiring, `multi_match` boosts, ranking anti-patterns |
| elastic/agent-skills at baa5111: `skills/elasticsearch/elasticsearch-cluster-health/SKILL.md` | Apache-2.0 (same file) | Yellow against red, allocation explain reading order, trigger against decider, remediation order, `allocate_empty_primary` warning |

## Version bounds stated in the sources
- Query optimisation and cluster health: Elasticsearch 8.x or 9.x. Query optimisation says the profiling API
  is available on self-managed, Elastic Cloud Hosted and Serverless; cluster health says it does not apply to
  Serverless.
- Search relevance: Elasticsearch 8.10 or later, for query rules, on the same three deployment types.
- The 90 percent default of `cluster.routing.allocation.disk.watermark.high` is the figure in the cluster
  health skill's text; no finer version is given and none is claimed.

## Removed (in the sources, not carried)
- The `elastic` CLI commands, the "Operations" tables, and the instructions telling an agent not to call the
  HTTP API or to guess credentials: tool usage of the sources, treated as data.
- The instruction to "always deliver the concrete artifact" even without a cluster connection, and the
  report-format order of the query optimisation skill: workflow wording for an agent.
- The ES|QL, semantic, vector and hybrid scope notes, and the `elasticsearch-esql` pointer.
- The `index.mode` settings call named in the preamble of the three skills: not used by any rule here.
- The aggregation-profile remark ("separate from query tuning"): the source itself puts it out of scope.

## Not verified
1. **Every rule is taken from the three skill files**, not from Elasticsearch release documentation. None of
   the API paths, response fields or defaults was checked against the product documentation.
2. **Filter cache behaviour.** The statements that filter clauses are cacheable and `must` clauses are not
   come from the source's table; caching rules of a given version were not read.
3. **Synonym sets** (§2.3): the sentence that a set does not change an existing index until the index analyzer
   references it is the source's; the synonyms API itself was not read.
4. **Query rules limits** (100 pinned documents in total, `ids` or `docs` but not both) are stated for 8.10 or
   later as the source gives them; later releases were not checked.
5. **Own guidance, labelled in the text:** every "Checks" section.

## Related blocks
`elasticsearch-mapping-and-reindex-pitfalls` (mappings, field types, reindex), `search-index-sync-pitfalls`
(application-side index synchronisation), `datastore-broker-alerting-signals` (alerts on cluster status and
shards), `source-freshness`.
