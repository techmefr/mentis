# search-index-sync-pitfalls §3 — Reimport, mapping configuration and data

Sources: the README of matchish/laravel-scout-elasticsearch at 78c788d (sections Features, Installation, Index settings and mappings, Zero downtime reimport) and the README of ankane/searchkick at 6050f50 (sections Deployment, Data Protection, Performance, Advanced Mapping, Reference), read 2026-10-16. Rules for field types and for moving documents between indices are in `elasticsearch-mapping-and-reindex-pitfalls` §1 and §3.

## 3.1 Zero-downtime reimport
1. **Both integrations build a new index and switch to it.** The Scout command `php artisan scout:import` creates a temporary index, imports all models into it, switches to it and removes the old one, so the existing search keeps working during the import in production. Searchkick's reindex builds a new index the same way.
2. **Searchkick can parallelise the rebuild.** `reindex` in the asynchronous mode returns the name of the new index (a timestamped name) and runs the import as background jobs; once they finish, the new index is promoted with `promote(index_name)`. The status can be tracked through Redis, and the `wait` option makes the call wait for completion. Concurrency is limited through the job framework (the source's example allows three jobs at once). Old indices are removed with `clean_indices`.
3. **A longer refresh interval during a parallel rebuild speeds it up, and must be restored.** The source passes `refresh_interval: "30s"` to the reindex, says it only makes a noticeable difference with parallel reindexing, and restores the mapping's value (1 second by default) at promotion with `update_refresh_interval: true`. The same rule on a plain Elasticsearch destination is in `elasticsearch-mapping-and-reindex-pitfalls` §3.2.
4. **Own guidance:** a release that changes the indexed data or the mapping runs the rebuild into a new index before traffic depends on it, and keeps the old index until the new one passes the checks at the end of this section.

## 3.2 Mappings and settings in configuration
1. **The Scout README says to define the mapping when the index is created, because an inappropriate preliminary definition and mapping may give wrong search results.** The config keys are `elasticsearch.indices.mappings.<index>` and `elasticsearch.indices.settings.<index>`, where `<index>` is what the model's `searchableAs` returns (the README's example is `products`), and `.default` in place of the name sets the fallback for every index. The config example is published with `php artisan vendor:publish --tag config`.
2. **Searchkick: a custom `mappings` option replaces the generated mapping, and then the searches must be custom as well.** The `merge_mappings: true` option keeps the mappings and settings Searchkick generates in addition to the custom ones.
3. **Own guidance:** keep these mappings in version control with the model, and review a mapping change as the reindex it will cause (`elasticsearch-mapping-and-reindex-pitfalls` §3.1).

## 3.3 Index only what you query
1. **Searchkick makes every string field searchable and filterable by default.** The `searchable` and `filterable` options restrict them, which speeds up indexing and reduces index size. Non-string fields are always filterable and must not be passed to `filterable`.
2. **Partial-word matching grows the index.** The source says the autocomplete options can increase the index size significantly, which is why they are declared per field.
3. **Searchkick indexes `BigDecimal` values as floats by default so they can be used for boosting.** Convert them to strings in the indexed data to keep full precision.

## 3.4 Data protection
1. **Encrypt data at rest and in transit, even inside your own network.** The source says this matters most when personal data of users goes to the search server, and notes that Bonsai, Elastic Cloud and Amazon OpenSearch Service support encryption at rest and HTTPS.
2. **The Scout README documents an environment switch that disables SSL verification** (`ELASTICSEARCH_SSL_VERIFICATION=false`). Own guidance: treat it as a local-development convenience, never as a production setting, since it removes the point of encrypting in transit.
3. **Own guidance:** the index is a copy of whatever the indexed data contains, so erasing or anonymising a person has to reach the index as well as the database. The README's `toSearchableArray` example returns the whole model array; for a model that holds personal data, return an explicit list of fields.

## 3.5 Checks (own guidance)
1. After a rebuild, the document count of the new index equals the number of records that should be indexed, and a known record from each model is found.
2. The refresh interval of the new index is back to its configured value before the switch.
3. The mapping lives in configuration next to the model, and the indexed data of each model with personal data is an explicit list of fields.
