# search-index-sync-pitfalls §2 — Consistency, scores, paging and query input

Sources: the README of ankane/searchkick at 6050f50 (sections Testing, Deep Paging, Scroll API, Multi Search, Gotchas) and the README of matchish/laravel-scout-elasticsearch at 78c788d (sections Search, Conditions, Pagination), read 2026-10-16. The Scout README lists Elasticsearch 8.0 or later with ElasticsearchDSL 8.0.0 or later, and older pairings for Elasticsearch 7 and 6.

## 2.1 Eventual consistency
1. **Elasticsearch and OpenSearch are eventually consistent.** The source says a change can take up to a second to show in search, and that an explicit `refresh` of the index makes it visible immediately.
2. **Refresh where a test or a flow needs to read its own write, and nowhere else.** The source's tests call the index refresh right after creating the record; its factory trait reindexes the record with `refresh: true`. Own guidance: a flow that needs read-your-write in production is a reason to read the record from the database, which the search server is not the source of truth for (`nestjs-integration-patterns` §5.4, point 4).
3. **Keep the sync callbacks off in tests that do not search.** The source disables them for performance and enables them in the tests that need the index.
4. **Parallel test workers need separate indices.** The source sets an index suffix per worker (`Searchkick.index_suffix = worker`) and reindexes the models in each worker's setup.

## 2.2 Scores on a tiny index
1. **Scores can be wrong when the index holds few documents spread over several shards.** The source ties this to the distributed nature of the engine and gives a single shard (`number_of_shards: 1`) as the fix, which Searchkick sets by default in the test environment. Own guidance: a ranking test builds its index with one shard and does not extrapolate to a production index with many.

## 2.3 Paging
1. **Paging is capped at the first 10,000 results, and the total count is capped with it.** The source does not recommend lifting the cap (its `deep_paging: true` option exists for those who really need all results). For an accurate total only, it passes `track_total_hits: true` in the body options.
2. **The scroll API is for processing large amounts of data, not for real-time user requests**, and the source clears the scroll when it has finished a manual loop.
3. **Scout: builder pagination takes precedence over `take()` and the `from` option.** The source's example sets both and still returns the first 50 results, ignoring the offset.

## 2.4 Multi-search failures
1. **A multi-search does not raise errors the way a single search does.** The source says to call the `error` method on each query to check it. Own guidance: a batch of searches is read query by query, and an empty list is not proof that the query succeeded.

## 2.5 User text, query syntax and returned fields
1. **The Scout driver turns the text passed to `search` into a `query_string` query**, which the README shows with field names and AND and OR operators inside the string.
2. **Inference from that README statement, not stated by it and not run:** user-typed text passed straight to `search` is parsed as that query syntax and not as plain words. The README does not say how to neutralise it. The route it does describe for anything beyond the default is a callback that receives the client and the query builder; building a structured query there, with the user text as a plain value, keeps the user's input from being read as syntax.
3. **Scout accepts only three conditions on `where`-style calls:** equality, `whereIn` and `whereNotIn`, with no operators. Elasticsearch term objects such as a range query can be passed as the value of `where`, and a range-only search calls `search()` with an empty argument.
4. **Own guidance:** a search that mixes user text with required filters keeps the filters in conditions (`where`) and only the words in the text, so a user cannot widen the filter through the text.
5. **Fields that must not appear in a result are limited with the `source` option** (the README's `->options(['source' => [...]])`), since indexed models can hold fields that should not be returned.

## 2.6 Checks (own guidance)
1. Every test that searches right after a write refreshes the index, and tests that do not search run with the callbacks off.
2. Ranking tests use one shard.
3. Pages beyond 10,000 results are either not offered or use a different mechanism, and totals that must be exact use `track_total_hits`.
4. The place where user text reaches the engine is identified, and the choice between syntax and plain words is written down.
