# elasticsearch-query-and-triage-pitfalls §1 — Profile first, filter context, wildcards

Sources: the `elasticsearch-query-optimization` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/query-optimization-reference.md`), read 2026-10-16. The source states compatibility with Elasticsearch 8.x or 9.x, self-managed, Elastic Cloud Hosted and Elastic Cloud Serverless, and says the profiling API is available on all deployment types.

## 1.1 Profile before fixing
1. **Run the slow query unchanged with `"profile": true` on `_search`, then read `took` and `profile.shards[].searches[].query`.** Sort the child collectors by `time_in_nanos`: the collector with the highest time, summed across shards, is the target, and the others matter only once it is addressed.
2. **Do not propose more shards or more hardware while the profile names one clause.** The source's example is a `WildcardQuery` of about 3.8 seconds. Infrastructure changes need evidence that the query is already as cheap as it can be.
3. **Profiling has its own overhead.** Use it for the diagnosis and for the before and after comparison, not on every production request.
4. **Re-profile after the rewrite and compare.** Report an improvement only when the dominant collector changed or its `time_in_nanos` dropped materially; `took` alone does not confirm it.
5. **A slow query can still be a correct one.** A rewrite should return the same documents unless the report states the semantic trade-off (§1.3).

Signatures the source lists, read against the top collector:

| Profile signal | Typical cause | First fix |
|---|---|---|
| `WildcardQuery` with a high `next_doc` and a `*term*` pattern | leading or infix wildcard | `match` or `match_phrase`, a prefix query, or an n-gram field |
| several `TermQuery` in `must` next to one `MatchQuery` | exact filters are being scored | move the terms to `filter` |
| `MatchQuery` dominates after the filter fix | large candidate set or heavy analyzer | narrow with `filter`, check the analyzer |
| `BooleanQuery` with many `should` clauses | disjunction over many clauses | reduce the clauses, move constants to `filter` |

## 1.2 Filter context and field types
1. **Exact matches, ranges and other clauses that do not drive relevance go in `bool.filter`; only clauses that must affect `_score` stay in `must`.** Status, tenant id, service name and time ranges rarely belong in `must` when a text query ranks the results. Filter context skips scoring and can reuse the filter cache on repeated queries.
2. **Moving a required clause from `must` to `filter` keeps the same matching documents and changes only the score and the cost.** State that in the report: the remaining `must` clauses define the ranking.
3. **Check the mapping before moving or rewriting a clause.** `term` and `terms` belong on `keyword`, numeric or date fields; a `term` on analysed `text` is a common bug, and the fix is the right sub-field (the source's example is `service.keyword`) or a mapping change, said out loud and not made silently. `match` and `match_phrase` target `text`; `range` targets numeric, date or keyword fields, not `text`.
4. **Sub-field names differ between schemas** (`service` against `service.keyword`), so read `GET /{index}/_mapping` and take the names from it.

```json
{
  "query": {
    "bool": {
      "filter": [{ "term": { "status": "active" } }, { "term": { "tenant_id": "acme" } }],
      "must": [{ "match": { "description": "wireless keyboard" } }]
    }
  }
}
```

## 1.3 Leading wildcards
1. **A leading `*` cannot use the inverted index to narrow the term set.** The engine scans many terms and visits documents, which shows as a high `next_doc` in the profile. A trailing wildcard can sometimes use the term dictionary. A leading `*` stays a scan whatever the field type, and the source lists it among the common mistakes on high-cardinality fields.
2. **Pick the rewrite by what the user means:**

| Intent | Rewrite |
|---|---|
| full-text substring in log text | `match` or `match_phrase` on the analysed `text` field |
| literal substring on a keyword | a `wildcard`-typed field, or a reindex with an n-gram analyzer |
| prefix only | a `prefix` query on a `keyword`, or an edge n-gram at index time |
| fast prefix autocomplete | edge n-gram tokenizer at index time, then `match` or `prefix` |
| fast infix search at scale | n-gram analyzer (an index-time cost, `match` at query time) |

3. **Replacing `wildcard` `*foo*` with `match` can change which documents match.** Analysis tokenizes differently (`timeout` against `timeouts`), so say so and compare hit counts, or run `POST /{index}/_validate/query?explain=true` on the rewritten query.
4. **A `wildcard`-typed field is case-sensitive and still costly with a leading `*`**, though better than `text`.

## 1.4 Checks (own guidance)
1. The report quotes the top collector's `type`, `description` and `time_in_nanos` before and after.
2. Every field in a rewritten clause has its type confirmed from the mapping.
3. If the rewrite can change the result set, the report says so and shows the hit counts compared.
