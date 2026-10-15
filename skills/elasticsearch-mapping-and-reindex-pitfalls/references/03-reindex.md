# elasticsearch-mapping-and-reindex-pitfalls §3 — Changing a type: new index and reindex

Sources: the `elasticsearch-reindex` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/tuning.md`, `references/troubleshooting.md`, `references/api-reference.md`) and `elasticsearch-index-design` (`SKILL.md`, `references/field-type-decisions.md`), read 2026-10-15. Both reindex and design skills state compatibility with Elasticsearch 8.x or 9.x, and the reindex skill distinguishes self-managed and Elastic Cloud Hosted from Serverless (§3.5).

## 3.1 The sequence
1. **A field type cannot be changed in place.** Create a new index (versioned name such as `events-v2`) with the corrected mapping, copy the documents with `POST /_reindex`, verify with `GET /{new}/_count` (compared with the source count) and `GET /{new}/_mapping`, then cut reads and writes over with an alias swap or an application configuration change.
2. **Consider the alternatives before reindexing:** runtime fields fix a type mismatch or add a computed field without reindexing when the stored values need not change; aliases redirect queries transparently and combine with a reindex for zero-downtime mapping changes; snapshot and restore (self-managed and Elastic Cloud Hosted) moves a whole index faster when nothing is transformed.
3. **Do not use `_split`, `_shrink` or snapshot and restore for a filtered subset copy or a plain document migration:** they solve other problems.

## 3.2 Preparing the destination
1. **`_reindex` does not copy mappings, shard counts or analyzers.** Create the destination first, with explicit settings and mappings derived from the source mapping. Relying on auto-creation with dynamic mapping causes partial failures or silent type coercion.
2. **During the copy, set `number_of_replicas: 0` and `refresh_interval: "-1"` on the destination for write throughput, and restore the production values with `PUT /{dest}/_settings` afterwards** (on Serverless only the refresh interval is yours to set).
3. **For a data stream destination, create an index template with `data_stream: {}` and the data stream first, and set `dest.op_type` to `"create"`:** data streams are append-only.
4. **Keep timestamp fields.** If `source._source` restricts the copied fields, list every timestamp field: omitting it drops the values and can break time-based queries, data stream routing and retention. A script must not remove or overwrite them unless that is the intent. Data streams route documents by `@timestamp`.

## 3.3 Running the copy
1. **Submit with `wait_for_completion=false` for anything that may take more than a few seconds.** The response is a task id; poll `GET /_tasks/{task_id}` until `completed` is true, then read `status.total`, `status.created` and `response.failures`. The reindex keeps running when a client socket times out (the source's example is Kibana Dev Tools).
2. **Throttle with `requests_per_second`,** and change it on a running task with `POST /_reindex/{task_id}/_rethrottle?requests_per_second=N`.
3. **`slices=auto` is for a local reindex only.** The source states that a remote reindex does not support slicing; partition by query (date ranges, term filters) across parallel requests instead.
4. **A remote reindex needs the remote host on the `reindex.remote.whitelist` allowlist of the coordinating nodes** (self-managed and Elastic Cloud Hosted). Its coordinating node holds a 100 MB on-heap buffer per request, so keep `source.size` times the average document size comfortably below it (the source suggests 50 to 80 MB) to avoid `OutOfMemoryError`. The default `source.size` is 1000; the source starts at 500 for remote.
5. **Test with `max_docs` first** at two or three `source.size` values, compare throughput, then run the full copy with the best value.
6. **When retrying a partly completed reindex, set `conflicts` to `"proceed"`.** The default `"abort"` stops at the first version conflict.
7. **Raise `scroll` when the scroll context is lost on a slow cluster:** the default keep-alive is 5 minutes and the source's example uses `scroll=2h`.

## 3.4 Overwrites
1. **Several sources into one destination overwrite each other when their documents share an `_id`.** The count is then lower than the sum of the sources. Make the id unique by adding the source index name with a script, or use `op_type: "create"` with `conflicts: "proceed"` to keep the first written version.
2. **To stop an older copy from replacing a newer document, set `dest.version_type` to `"external"`.** Elasticsearch then keeps the source version and rejects older writes. The source gives cross-cluster synchronisation as the case.
3. **Mapping conflicts give a partial reindex.** Documents whose values do not fit the destination mapping fail while the rest succeed; read `failures` in the task response. On self-managed, debug logging of `TransportShardBulkAction` shows the exact field. Fix the destination mapping, delete the partially filled index and run again.

## 3.5 Deployment differences
1. **Read `GET /` first and check `build_flavor` and `version.number`.** The source's table: on Serverless the shard and replica counts are managed (omit them at creation), `PUT /_cluster/settings` is blocked, `_cat/count` is unavailable (use `GET /{index}/_count`), tasks can only be fetched by id (no listing or cancelling), `_split` and `_shrink` are not available, and remote reindex is limited to Elastic Cloud Hosted sources and is a technical preview.

## 3.6 Checks (own guidance)
1. The destination was created by hand, and its mapping was read back before the copy started.
2. The destination count equals the source count after the copy; a lower count points at overwritten ids (§3.4) or at failures.
3. The replicas and the refresh interval are back to their production values before the alias moves.
