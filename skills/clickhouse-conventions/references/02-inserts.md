# clickhouse-conventions §2 — Inserts

Rules hold for the ClickHouse documentation current on 2026-10-08.

## 2.1 Batch on the client
1. **Every insert creates a part, so batch size is the main ingest lever.** The insert strategy page says the
   overhead is constant regardless of insert size, and recommends batches of at least 1,000 rows, ideally
   10,000 to 100,000.
2. **Keep the insert rate around one query per second.** The background merge of parts must keep up with the
   rate at which parts appear; many small inserts per second lead to poor query performance and the
   "too many parts" error.
3. **A retry is safe only with an identical batch.** The page says a retried insert must keep the same
   contents and order, so retry the stored batch, never a rebuilt one. The same page (re-read 2026-10-20)
   describes synchronous inserts on MergeTree engines as idempotent when retried this way, which is why a
   rebuilt or reordered batch loses that protection.
4. **Pre-sorting by the ordering key and a native input format help,** with compression, for large batches
   (the page's own advice).

## 2.2 Asynchronous inserts when the client cannot batch
1. **Use `async_insert = 1` with `wait_for_async_insert = 1`.** The server then buffers small inserts and
   writes them as larger parts, and acknowledges only after the flush reached storage. The documentation's strong
   recommendation is that exact pair.
2. **Avoid `wait_for_async_insert = 0` ("fire and forget").** The server acknowledges when the data is
   buffered, errors surface only in the server log and `system.asynchronous_inserts`, and a fast client can
   overload a server that needed to apply back-pressure.
3. **Know the flush conditions.** The buffer flushes at a size limit (default 100 MiB), a time limit (default
   200 ms, 1,000 ms on Cloud) or a query count (default 450). Data is not queryable until a flush.
4. **One bad row rejects the whole insert query's payload.** Parsing and type errors are found at flush time,
   and none of that query's data is written; with the default wait setting the error returns to the client.
