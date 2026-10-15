# search-index-sync-pitfalls §1 — Sync strategy and what the index does not follow

Sources: the README of ankane/searchkick at 6050f50 (sections Indexing, Strategies, Associations, Default Scopes, To Reindex or Not to Reindex, Queuing, Partial Reindexing, Synonyms, Reference) and the README of matchish/laravel-scout-elasticsearch at 78c788d (section Eager load), read 2026-10-16. Searchkick 6 works with Elasticsearch 8 and 9 and OpenSearch 2 and 3 as its README states. The index-is-derived-data rules, the outbox and the lag metric are in `nestjs-integration-patterns` §5.

## 1.1 Choose the strategy on purpose
1. **Searchkick names four ways to keep the index in step.** Inline (the default): on every insert, update or delete of a record. Asynchronous: background jobs, on a queue named `searchkick`. Queuing: push the ids of records to update onto a queue and reindex in batches in the background, which the source calls more performant than the asynchronous way, since that one updates records individually. Manual: callbacks off, and the caller reindexes a record or a relation.
2. **Own guidance, inferred from the source's wording:** the source recommends background jobs "for better performance", so with inline sync the index write belongs to the same flow as the record write, and the latency and failures of the search server reach the caller. Make the choice knowingly, and when the search server must not affect a write, use the asynchronous or the queuing mode and the outbox of `nestjs-integration-patterns` §5.
3. **The queuing mode needs a Redis connection, which the source recommends wrapping in a connection pool, a background job that processes the queue, and a length check on the queue.** Own guidance: that length is a lag signal to watch (`nestjs-integration-patterns` §5.4, point 5).
4. **Bulk work has two switches.** Wrapping the updates in the bulk callbacks block sends them as a batch; wrapping them in the callbacks-off block skips index updates entirely, and the mode can also be overridden on one call (inline, asynchronous or queue). Own guidance: whatever ran under the callbacks-off block is not in the index, so follow it with a reindex of the affected records.
5. **The Scout driver README describes no strategy choice.** How Scout itself synchronises and queues is documented on laravel.com, which was not read for this block.

## 1.2 What the index does not follow
1. **Data is not synced when an association changes.** A child record needs an explicit callback that reindexes its parent, and the source adds it as an `after_commit` on the child:

```ruby
class Image < ApplicationRecord
  belongs_to :product

  after_commit :reindex_product

  def reindex_product
    product.reindex
  end
end
```

2. **By default every record is indexed; a `should_index?` method decides which ones.** A record that a default scope or a soft delete hides from normal queries must also be excluded here: the source's example pairs a default scope on `deleted_at` being null with a `should_index?` returning the same test. The option `unscope: true` is the opposite choice, to index and search the filtered records too.
3. **Own guidance:** list each way a record can change without its own save (a child, a soft delete, a bulk update, a callbacks-off section) and name the reindex path that covers it.

## 1.3 When to reindex
1. **Reindex when you install or upgrade the library, when the indexed-data method changes, and when the options that shape the index change. Not when the application starts.**
2. **An interrupted reindex can be resumed** (the source's `resume: true`), so a large rebuild does not restart from zero.
3. **A new search server needs a full reindex after deployment**, which the source shows as a rake task for all models on every hosting variant it lists.
4. **Static synonyms in the model need a reindex when they change.** The source's alternative is a synonym file on the search server, reloaded without a reindex; its example reload call is `Product.search_index.reload_synonyms`.
5. **Scout:** the indexed data is whatever `toSearchableArray` returns, so a change to that method is a change to the indexed data and needs a reimport (§3.1).

## 1.4 Import cost and partial updates
1. **Searchkick imports in batches with `find_in_batches` (1000 per batch by default, `batch_size` changes it); eager-load associations with the `search_import` scope** so the import does not issue a query per record.
2. **Scout eager-loads on import through a global scope.** Bind a custom `ImportSourceFactory` in the service provider's `register` method and add the scope that calls `with` on the relation. Separately, `toSearchableArray` can call `loadMissing` so the relation is always loaded when the model is saved.
3. **Reindex only the attributes that changed.** Split the indexed data into separate methods (the source's example keeps price data in its own method) and call `reindex` with that method's name: less time generating the data and less network traffic. `ignore_missing: true` ignores errors for documents that do not exist yet.
4. **Reindex conditionally.** The source's `callback_options` takes an `if:` method that reads `previous_changes`, so an update to an attribute that is not indexed does not trigger an index write.

## 1.5 Checks (own guidance)
1. The strategy is written down next to the model, with the reason for it.
2. Every association whose data is indexed in the parent has a reindex callback, and every default scope or soft delete has a matching `should_index?`.
3. After a change to the indexed-data method, a reindex of the whole index is in the release steps.
