---
name: elasticsearch-query-and-triage-pitfalls
description: "Use when a slow Elasticsearch search is diagnosed or rewritten (profile first, filter against must, term on text fields, leading wildcards), when a document must be pinned or a ranking tuned (query rules, multi_match and field boosts), or when a cluster is yellow or red (unassigned shards, allocation explain, deciders, allocate_empty_primary)."
---

# elasticsearch-query-and-triage-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Elasticsearch traps that sit in the query, in the choice of a
relevance lever, and in reading a non-green cluster. The premise: **a slow or badly ranked search has a
named cause, and the fix that does not name it (more shards, a bigger boost, a forced reroute) costs more
than the problem**. Mappings and moving documents between indices are in
`elasticsearch-mapping-and-reindex-pitfalls`; application-side index synchronisation is in
`search-index-sync-pitfalls`.

## When
- A search is slow, or a query is about to be rewritten for speed.
- A document must come first for a query, or ranking on free text is poor.
- A cluster reports yellow or red, shards are unassigned, or an operator asks what to do about it.

## Steps

**Read only the section the task meets.** §1 and §2 follow from the mapping (`elasticsearch-mapping-and-reindex-pitfalls`
§1): a rewrite is only valid for the field types the mapping really has.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Profile first, `filter` against `must`, `term` and field types, leading wildcards | a search is slow or a query rewritten | [`01-query-tuning.md`](./references/01-query-tuning.md) |
| 2 | Pinning with query rules, organic ranking with `multi_match`, ranking anti-patterns | a result must rank first, or ranking is weak | [`02-relevance-levers.md`](./references/02-relevance-levers.md) |
| 3 | Yellow against red, allocation explain, trigger against cause, last-resort reroute | the cluster is not green | [`03-cluster-triage.md`](./references/03-cluster-triage.md) |

## Output / checkpoint
For a query: the profile quoted before and after, the field types confirmed from the mapping, the semantic
caveat stated if the rewrite can change which documents match. For a relevance change: the same query run
before and after with the top hits compared. For a triage: the status, the one index it is localised to, the
decider named, the data-loss statement, and no write performed.

## Guardrails
- Never propose more shards or hardware while the profile names a clause (§1.1).
- Never leave an exact-match clause in `must` when a text clause drives relevance (§1.2).
- Never simulate a pin with a boost, `function_score` or a sort (§2.1).
- Never expect a ruleset to pin anything until the search carries a `rule` query (§2.2).
- Never run `allocate_empty_primary` as a first or casual fix: it permanently loses the shard (§3.3).
- Rules are stated for Elasticsearch 8.x or 9.x; query rules need 8.10 or later; triage does not apply to
  Serverless (§3). Nothing here was run against a cluster (🟡).

## Origin
Rewritten from the Elastic `elasticsearch-query-optimization`, `elasticsearch-search-relevance` and
`elasticsearch-cluster-health` agent skills (Apache-2.0, commit baa5111), read 2026-10-16. Open points and own
guidance are in [`references/origin.md`](./references/origin.md).
