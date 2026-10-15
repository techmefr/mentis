---
name: elasticsearch-mapping-and-reindex-pitfalls
description: "Use when designing or changing an Elasticsearch index: explicit mappings and field types by access pattern, text with keyword sub-fields and ignore_above, mapping explosion and flattened, doc_values, moving to a new index with _reindex (destination setup, slices, throttling, ids, versions), and bulk loading typed documents."
---

# elasticsearch-mapping-and-reindex-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Elasticsearch traps that sit in the mapping and in the move
between indices. The premise: **the first document decides the types, a type cannot be changed afterwards, and
a copy that reports success can still be partial**. Query tuning, relevance and cluster triage are not covered
here. Application-side index synchronisation and outbox patterns are in `nestjs-integration-patterns` §5.

## When
- An index is created, or a mapping is reviewed for type, storage or query cost.
- A field type is wrong, or an object holds user-chosen keys.
- Documents are copied between indices or clusters, or a mapping change needs a new index.
- A CSV or JSON file is loaded through the bulk API.

## Steps

**Read only the section the task meets.** §3 follows from §1 and §2 when a type has to change.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Explicit mapping, type by access pattern, multi-fields, `ignore_above` | an index is created or a mapping reviewed | [`01-field-types.md`](./references/01-field-types.md) |
| 2 | Mapping explosion, `flattened`, `doc_values`, storage choices | a field holds free-form keys, or storage is high | [`02-mapping-explosion.md`](./references/02-mapping-explosion.md) |
| 3 | New index and `_reindex`: destination, tuning, overwrites, Serverless differences | a type changes, or documents move between indices | [`03-reindex.md`](./references/03-reindex.md) |
| 4 | Bulk loading: typed JSON, response errors, counts | a file is loaded with `_bulk` | [`04-bulk-loading.md`](./references/04-bulk-loading.md) |

## Output / checkpoint
For a mapping: each field's access pattern next to its type, and the mapping read back after creation. For a
reindex: the destination created beforehand, the source and destination counts compared, the replicas and
refresh interval restored. For a bulk load: the `errors` flag read, and the count compared with the input.

## Guardrails
- Never rely on dynamic mapping for a production index (§1.1).
- Never map a user-keyed object as a dynamic `object` (§2.1).
- Never reindex into a destination that was not created first (§3.2).
- Never use `slices=auto` on a remote reindex (§3.3).
- Never treat a bulk response as success without reading `errors` (§4.3).
- Never delete an index to fix its mapping without the owner's confirmation (§4.4).
- Versions: the sources state compatibility with Elasticsearch 8.x or 9.x; Serverless differs (§3.5).
  Nothing here was run against a cluster (🟡).

## Origin
Rewritten from the Elastic `elasticsearch-index-design`, `elasticsearch-reindex` and `elasticsearch-ingest`
agent skills (Apache-2.0, commit baa5111), read 2026-10-15. Open points and own guidance are in
[`references/origin.md`](./references/origin.md).
