# elasticsearch-mapping-and-reindex-pitfalls §2 — Mapping explosion and storage bloat

Sources: the `elasticsearch-index-design` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/mapping-explosion.md`, `references/field-type-decisions.md`), read 2026-10-15. The source states compatibility with Elasticsearch 8.x or 9.x.

## 2.1 Unbounded field names
1. **A dynamic `object` over user-supplied key/value data with thousands of distinct keys makes every new key a new mapped field.** Cluster state and disk use grow without bound, queries slow down, and indexing can fail once the field limit is reached.
2. **Replace it with `flattened`.** The whole object becomes one field with limited sub-key indexing, which suits schema-less metadata used mostly for filtering (queries such as `labels.environment`).
3. **When `flattened` is not enough, the source offers three alternatives:** index only an allowlist of keys through an ingest pipeline when a known subset must be first-class fields; a separate labels index, joined or looked up at query time, for extreme cardinality; or `"dynamic": "strict"` on the parent object to reject documents with unknown keys instead of exploding silently.
4. **Audit the field count.** Read `GET /{index}/_mapping` and watch the total number of fields against `index.mapping.total_fields.limit`.

## 2.2 Storage-oriented choices
1. **`doc_values: false` on retrieve-only fields.** For a `keyword` field that is only returned from `_source` for display (the source's example is a `session_id`), disabling doc values saves disk on high-volume indices. Before disabling it, make sure the field is never used in a sort, an aggregation, a `terms` query, or as input of a runtime field that needs doc values, and that it is still returned from `_source`.
2. **Analysed-but-never-searched fields are bloat.** URLs, HTTP status codes, tags and identifiers that are only filtered or aggregated are `keyword`; the source's leaner choice for a status code is `keyword`, or `short` if it is numeric.
3. **Bounded precision metrics use `scaled_float`** rather than `float` or `double` when storage dominates (the source: durations with fixed precision, currency to cents with a scaling factor of 100).
4. **A keyword sub-field on a large analysed body needs `ignore_above`** (see §1.3).

## 2.3 Fixing it on a live index
1. **Mapping tweaks on existing fields that change the type, the structure or `doc_values` cannot be applied in place.** The source says they are rejected or leave data inconsistent.
2. **The sequence is a new index (for example `events-v2`), a reindex, then a check of the field count and the document count before cutover** (§3).

## 2.4 Checks (own guidance)
1. For every `object` that holds user-supplied keys, count the distinct keys seen in production; if the count is not bounded by design, it is `flattened`, an allowlist or strict.
2. Every `doc_values: false` has a written line saying which query paths were checked.
