---
name: search-index-sync-pitfalls
description: "Use when an application framework keeps a search index (Elasticsearch or OpenSearch) in step with its database through a Rails or Laravel integration: choosing the sync strategy, related records and soft deletes, partial reindex, eventual consistency in tests, the 10,000 result cap, user text passed as query syntax, zero-downtime reimport, per-index mapping configuration and encryption of personal data."
---

# search-index-sync-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the traps that the framework search integrations leave to the
caller. The premise: **the integration keeps the index in step for the record you save, and for nothing
else**: not for a changed parent, not for a record hidden by a scope, not for a mapping you changed, and not
immediately. The core rules (the index is derived data, write through an outbox, index idempotently, watch
the lag) are in `nestjs-integration-patterns` §5; this block adds only what the two integrations below say on
top of them, and is not specific to NestJS.

## When
- A model is made searchable, or the data sent to the index is changed.
- A record can change without its own save (a child, a soft delete, a bulk update).
- Search results are tested, paged, or built from user text.
- The index is rebuilt in production, or personal data goes to the search server.

## Steps

**Read only the section the task meets.** The sources are Searchkick (Rails) and the Laravel Scout
Elasticsearch driver by matchish; where a rule is stated for one of them it says which.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Sync strategy, related records, default scopes, when to reindex, partial and conditional reindex | a model is indexed or its indexed data changes | [`01-sync-strategy.md`](./references/01-sync-strategy.md) |
| 2 | Eventual consistency, one shard in tests, the 10,000 cap, user text as query syntax, multi-search errors | results are tested, paged, or built from input | [`02-consistency-and-queries.md`](./references/02-consistency-and-queries.md) |
| 3 | Zero-downtime reimport, mappings in configuration, searchable fields, encryption | the index is rebuilt or configured, or data is sensitive | [`03-reimport-and-data.md`](./references/03-reimport-and-data.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the sync strategy is named, every
way a record can change without its own save has a reindex path, the tests refresh where they need it, no
raw user text reaches the query syntax unintended, and a rebuild goes through a new index and a switch.

## Guardrails
- Never assume a child change reaches the parent document (§1.2).
- Never rely on a default scope or a soft delete to keep a record out of the index (§1.2).
- Never test a search right after a write without a refresh (§2.1).
- Never pass raw user text to the default Scout search without knowing it is parsed as query syntax (§2.5).
- Never rebuild a production index in place (§3.1).
- Rules are stated for Searchkick 6 (Elasticsearch 8 and 9, OpenSearch 2 and 3) and for the Scout driver with
  Elasticsearch 8 or later; nothing here was run (🟡).

## Origin
Rewritten from the READMEs of ankane/searchkick (MIT, commit 6050f50) and matchish/laravel-scout-elasticsearch
(MIT, commit 78c788d), read 2026-10-16. Version-bound facts, the inference on Scout's query handling and own
guidance are in [`references/origin.md`](./references/origin.md).
