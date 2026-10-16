# search-engine-index-settings-pitfalls §3 — Redis Search

Sources: the `redis-search` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/index-management.md`, `references/query-optimization.md`, `references/dialect.md`, `references/debugging.md`), read 2026-10-16. The files tie dialect behaviour to Redis 8 and to the older module; anything else about versions is not stated.

## 3.1 A schema change is a new index
1. **The in-place command can only add a field.** Removing a field, changing a field's type, changing a sort, no-stemming, weight or phonetic option, changing the key prefix, and changing the language, stop words or the no-fields and no-offsets options all need a rebuild. So does growing past the number of text fields the index was created for; set that limit up front on an index expected to grow.
2. **Rebuild behind an alias:** create the new index under a new name next to the old one, wait until `FT.INFO` shows `percent_indexed` at 1, point the alias at the new index with one atomic update, then drop the old one.
3. **Create the alias at the start and make application code query the alias,** never a versioned index name. The source's bad example is an application that queries the versioned index directly: there is then no painless way to roll forward.
4. **Never drop the live index and recreate it under traffic;** queries during the rebuild return errors.
5. **Dropping an index with the delete-documents option deletes every indexed document,** not only the index. Use the plain drop when the data must stay (the source labels the plain form non-blocking).

## 3.2 Always a prefix, always dialect 2
1. **Give every index a key prefix.** The source says to always set it. Own reasoning: without one the index is not tied to a named family of keys.
2. **Two indexes with overlapping prefixes** can index the same key twice, which the source lists as the cause of the 'Document is already in index' error after a JSON write; keep prefixes disjoint.
3. **Pass dialect 2 on every search, aggregate and hybrid call.** From Redis 8 it is the only supported value and the older ones are removed; vector query syntax and parameter placeholders need it.
4. **On Redis 7 or the older module, dialect 1 is still honoured,** and some older clients pin it; a vector query sent without the dialect then fails to parse. If one code base targets both, set the dialect explicitly so behaviour is the same on each.

## 3.3 Field types and tag values
1. **Use a tag field for categories, statuses and identifiers, not a text field "because it is a string."** Text is tokenised and stemmed and is for full-text search; the source calls the text-for-category choice the classic mistake and says a tag is roughly ten times faster for exact-match filtering (its figure, not measured here).
2. **Escape every hyphen inside a tag value in a query,** as well as dots and other punctuation. An unescaped hyphen is read as a negation: the source shows the explain output for a brand named with a hyphen parsed as the first word AND NOT the second word. The query then runs without error and returns nothing, or the wrong thing.
3. **Numeric fields serve range filters and sorting;** a document whose numeric field holds a non-number is not indexed, and shows up in the failure count (3.5).
4. **A vector field has three settings that must match the embedding model exactly:** the dimension count, the element type, and the distance metric (cosine for normalised text embeddings, inner product for un-normalised, Euclidean for raw). The source says a dimension mismatch gives silent garbage in one place and a vector index initialisation error in another; check it at index creation, with a test query, and do not wait to see which.

## 3.4 Queries that stay cheap
1. **Narrow first with tag and numeric predicates,** which cost less than text scoring and cut the candidate set. The source's vector example pre-filters with tag and numeric clauses before the nearest-neighbour step, and says not to fetch widely and filter in the client.
2. **Sort only on fields declared sortable.** Sorting a non-sortable field falls back to a row-by-row sort over the page.
3. **Keep the page small:** a small limit, a field list that returns only what the caller uses (or keys only), and no wildcard scans over the whole index. The source says raising the limit to a thousand is fine and a hundred thousand hurts.
4. **Avoid deep offsets.** The server scans and sorts offset plus page size rows; use a server-side cursor on aggregate queries for long result sets.
5. **Profile instead of guessing:** the profile command reports time per stage; the explain command shows how the query was parsed, including stemming expansion.

## 3.5 Read the diagnostics before changing the schema
1. **Three commands cover most of it:** explain for how a query was parsed, profile for where time goes, and `FT.INFO` for the index itself.
2. **In `FT.INFO`, check these first:** the indexed document count against what is expected; the indexing-failure count, which a type mismatch on a numeric field or a bad vector blob will raise (inspect one failing document); whether indexing is still running and the percent indexed, which must be complete before benchmarking or swapping an alias; and the inverted-index size, which is large when text fields are over-indexed.
3. **The source's wrong reflex:** adding sortable to every field, or re-creating the index, before reading these.
4. **Own guidance:** an index that is missing documents is a failure-count question first and a schema question second.

## 3.6 Checks (own guidance)
1. Run the explain command on a query with a hyphenated tag value, unescaped and escaped, and compare.
2. Rebuild an index behind an alias while a loop queries the alias and confirm no query errors.
3. Compare the document count and the failure count after a bulk load, before and after any schema edit.
