# elasticsearch-mapping-and-reindex-pitfalls §4 — Bulk loading files

Sources: the `elasticsearch-ingest` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/mapping-design.md`, `references/troubleshooting.md`, `references/ndjson-bulk-format.md`), read 2026-10-15. The source states compatibility with Elasticsearch 8.x or 9.x.

## 4.1 Typed documents
1. **Create the index with an explicit mapping before the first bulk request whenever field types matter.** CSV cells arrive as strings, and dynamic mapping of strings often gives `text` with a `.keyword` sub-field, which breaks range queries, aggregations and date histograms.
2. **Send typed JSON in the bulk body:** numbers as JSON numbers, booleans as `true` and `false`, dates as ISO-8601 strings (`2023-01-15` or a full date-time). The source says values left as quoted strings are often mapped as text by dynamic mapping, and its troubleshooting page lists a string in a `long` field as a mapper parsing exception.
3. **Validate the header row of a CSV before converting it:** a typo in the first row becomes a field name.
4. **For an unknown JSON schema, bulk load a small sample, read `GET /{index}/_mapping` and adjust before loading the full file.**

## 4.2 Bulk format
1. **Each document is two lines: an action line (`{"index":{"_index":"..."}}`, with `_id` only when stable ids are required) and the document on the next line.** One JSON object per line, no pretty-printed JSON inside the bulk file.
2. **A JSON array is not a bulk body.** Loaded unchanged it becomes one document (or is rejected); emit one action and document pair per element, so that an array of four gives a count of four.
3. **Raw CSV text is not a bulk body either.** Convert each data row, skipping the header and empty trailing rows.
4. **Split large files into several bulk requests** (the source says commonly 500 to 5,000 documents each) and reduce the batch when documents are large.

## 4.3 Reading the response
1. **A response with `"errors": true` is a partial failure even when the call succeeded.** Read the `error` object of each item: a mapper parsing exception means a value does not fit the mapping, a rejected mapping update means a conflicting type on re-ingest, and a missing final source line means the action and source lines are not paired.
2. **Retry only the failed items after fixing the cause.**
3. **Compare `GET /{index}/_count` with the number of expected rows or elements.** The source's causes of a wrong count: an array indexed as one document (count 1), the header counted as a document or blank rows skipped (fewer or more), and a second load without `_id` (more than expected: duplicate `index` actions append new documents).
4. **When typed columns matter, read `GET /{index}/_mapping` again after the load** and confirm numeric, `date` and `boolean` types.

## 4.4 Wrong mapping already loaded
1. **A field already mapped as `text` cannot be turned into `long` in place.** The source recreates the index: delete it (with the owner's confirmation, since this destroys the data), create it again with the correct mapping, convert the source file to typed bulk lines and load again. Own guidance: for an index whose data cannot be reloaded from a file, use the new index and reindex path (§3) instead of deleting it.
