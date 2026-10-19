# elasticsearch-mapping-and-reindex-pitfalls §1 — Explicit mappings and field types

Sources: the `elasticsearch-index-design` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/field-type-decisions.md`, `references/multi-field-patterns.md`), read 2026-10-15. The source states compatibility with Elasticsearch 8.x or 9.x, self-managed, Elastic Cloud Hosted and Elastic Cloud Serverless.

## 1.1 Define the mapping before the first document
1. **Create the index with its mapping (`PUT /{index}`) before any document is indexed.** With dynamic mapping the first document locks the types in: the source's examples are a numeric-looking string mapped as `text` and an ambiguous number mapped as `keyword`. Changing the type afterwards means a new index and a reindex (§3).
2. **Set `"dynamic": "strict"` on the root mapping** unless unknown fields are an explicit requirement. The source also names `false` as the alternative on the root or on sensitive objects.
3. **Gather the access pattern of every field first:** searched as full text, filtered by exact value, aggregated, sorted, or only returned in `_source`. The source treats missing access-pattern information as a blocker: do not guess, because a wrong type is expensive to fix at scale.
4. **On Serverless, omit shard and replica counts from the index creation; mappings stay explicit.** On self-managed and Elastic Cloud Hosted the source sets `number_of_shards` and `number_of_replicas` in the same request and states the chosen values.

## 1.2 Type by access pattern
1. **Full-text search only: `text`**, with no keyword sub-field.
2. **Exact filter, terms aggregation or sort only: `keyword`, not `text`.** This covers identifiers, enums, URLs, HTTP status codes and tags. A `text` field on a filter-only field wastes index space on analysed tokens, and aggregating or sorting it needs a `.keyword` sub-field or fielddata.
3. **Searched and also sorted or aggregated: `text` with a `keyword` multi-field**, searched on `name`, sorted and aggregated on `name.keyword`, with `ignore_above` 256 in the source's example. Only `text` breaks sort and aggregation; only `keyword` breaks relevance search.
4. **Decimals: `double`, `float` or `scaled_float`, never `text` or an integer type.** An integer type for prices with decimals loses precision. `scaled_float` with a `scaling_factor` of 10^n suits fixed precision (the source: currency to cents, latency to 0.01 ms) when storage matters at scale.
5. **Counters and true integers: `long` or `integer`. Timestamps: `date`, with ISO-8601 values. Flags: `boolean`**, and not `keyword` unless string semantics are wanted.
6. **A free-form key/value map with many distinct keys: `flattened`, not a dynamic `object`** (§2).
7. **Fixed-schema structured objects: `object`, or `nested` when independent queries on array elements are needed.**

## 1.3 Keyword sub-fields and `ignore_above`
1. **A keyword sub-field on a large analysed body without `ignore_above` indexes the whole raw string as one term.** The source lists two costs: a bloated terms dictionary and disk use, and document parsing exceptions when one term exceeds Lucene's term byte limit (about 32 KB in the file).
2. **Pick one fix by access pattern:** remove the sub-field when the body is only searched as text; add `ignore_above` (256 or the longest exact value you need to match) when an exact match is truly needed; or extract identifiers such as a request id or an error code into dedicated `keyword` fields at ingest.
3. **Add no sub-field that no query uses.** Each sub-field and each analysed form multiplies indexed data, so map only what the stated access patterns need.
4. **Multi-fields with different analyzers (`fields.en`, `fields.fr`) are the source's variant for language-specific search of one source value.**

## 1.4 Checks (own guidance)
1. For each field of a mapping under review, write its access pattern next to its type; a field with no pattern has no justified type.
2. After creating the index, read `GET /{index}/_mapping` and compare it with the intended mapping.
3. A `text` field with a `keyword` sub-field needs a reason in the form of a query that sorts or aggregates on it.
