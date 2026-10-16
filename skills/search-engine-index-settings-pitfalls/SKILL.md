---
name: search-engine-index-settings-pitfalls
description: "Use when a Meilisearch index or a Redis Search index (FT.CREATE) is designed, changed, secured or debugged: which Meilisearch settings force a full reindex and why settings come before documents, searchable versus filterable attributes, payload size and memory, one index per language, joins instead of embedded objects, binary quantization, master key and API key roles, running as a non-root user; and for Redis Search the changes FT.ALTER cannot make and the alias swap, PREFIX and DIALECT 2, TAG versus TEXT, unescaped hyphens in tag values, sortable fields, vector settings matching the embedding model, and reading FT.INFO, FT.EXPLAIN and FT.PROFILE before changing a schema."
---

# search-engine-index-settings-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for two search engines that are easy to start and expensive to change.
The premise: **an index setting is a decision about stored data, not a runtime option, so the cost of
changing it is a rebuild, and the cost of a wrong query is an empty result that looks like a correct one**.
Elasticsearch mappings and reindexing are in `elasticsearch-mapping-and-reindex-pitfalls`; keeping an index in
step with the database is in `search-index-sync-pitfalls`; Redis connections, keys and cluster slots are in
`redis-client-and-cluster-pitfalls`, and Redis hardening and metrics in `redis-security-and-observability-pitfalls`.

## When
- A Meilisearch index is created, or a setting on a loaded index is about to change.
- Indexing is slow, or memory runs out during a large import.
- A Meilisearch instance is exposed, or a key is about to be put in a frontend.
- A Redis Search schema is created or has to change while the application runs.
- A Redis Search query returns nothing, or too slowly, or an index shows fewer documents than expected.

## Steps

**Read only the part the task meets.** They are independent; Meilisearch parts 1 and 2 come first on a new
instance.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Meilisearch indexing: settings that trigger a reindex, searchable attributes, payloads, index layout, joins, quantization, hardware | an index is created, loaded or changed | [`01-meilisearch-indexing.md`](./references/01-meilisearch-indexing.md) |
| 2 | Meilisearch keys and deployment: master key, search and admin keys, non-root user | an instance is deployed or a key leaves the server | [`02-meilisearch-keys-and-deployment.md`](./references/02-meilisearch-keys-and-deployment.md) |
| 3 | Redis Search: rebuilds and aliases, PREFIX and DIALECT, field types, tag escaping, query cost, vectors, diagnostics | an index schema or a query is written or fails | [`03-redis-search.md`](./references/03-redis-search.md) |

## Output / checkpoint
Each rule was exercised, not read off the page: a Meilisearch settings change was applied to a loaded index and
the resulting task was seen to reindex (1.1), the search key was used from a client and an attempt to write was
refused (2.2), a Redis Search schema change was done by building a second index, waiting for `percent_indexed`
to reach 1, and swapping the alias while queries kept working (3.1), and a tag value with a hyphen was run
through `FT.EXPLAIN` (3.3). A schema that was only read is not verified.

## Guardrails
- Never load documents into a Meilisearch index before its settings are set (1.1).
- Never leave every field searchable when only some are matched on (1.2).
- Never put the master key or an admin key in a frontend, and never search with the master key (2.2).
- Never run Meilisearch as root (2.3).
- Never drop and recreate a live Redis Search index to change its schema (3.1).
- Never query a Redis Search index by its versioned name from application code (3.1).
- Never leave a Redis Search call without DIALECT 2, or an index without a PREFIX (3.2).
- Never leave a hyphen unescaped inside a tag value (3.3).
- This block states documentation as of the commits in [`references/origin.md`](./references/origin.md);
  engine versions were not checked and nothing was run against either engine (🟡).

## Origin
Rewritten from the Meilisearch documentation (meilisearch/documentation, MIT) and the Redis, Inc. `redis-search`
agent skill (redis/agent-skills, MIT), read 2026-10-16. 🟡: never run by us; open points and own guidance are in
[`references/origin.md`](./references/origin.md).
