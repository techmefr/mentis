# search-engine-index-settings-pitfalls §1 — Meilisearch indexing

Sources: the Meilisearch documentation of meilisearch/documentation at 944814e, page `capabilities/indexing/advanced/indexing_best_practices.mdx`, read 2026-10-16. The page names no engine version; the list of settings that cause a reindex is the page's list at that commit.

## 1.1 Settings first, documents second
1. **Create the index, set its settings, and only then add documents.** Changing some settings makes the engine reindex every document in the index, which is slow on a large dataset.
2. **The settings that trigger a full reindex** are: searchable attributes, filterable attributes, sortable attributes, stop words, synonyms, typo tolerance, embedder configuration, the dictionary, proximity precision, separator tokens and non-separator tokens.
3. **Changing displayed attributes or ranking rules does not.** Own guidance: that makes ranking rules the safe knob for relevancy experiments on a loaded index, and the first list the place to look before editing a setting in production.
4. **A settings change on a live index is a data migration:** schedule it, expect the index to be busy, and test the new settings on a copy first (own guidance).

## 1.2 Searchable, filterable and sortable are different jobs
1. **Every field is searchable by default.** The fewer fields the engine has to index for matching, the faster indexing is, and the better the relevancy and the smaller the disk use, so list only the fields a user's query words should match.
2. **A field needed only to filter or to sort is not searchable.** The page names numeric and boolean fields as the usual case; remove them from the searchable list and keep them in the filterable or sortable one.
3. **A field that is in none of the four lists** (searchable, filterable, sortable, displayed) **may as well be removed from the document.** Smaller documents are processed faster. The page also suggests compressing the request body with brotli, deflate or gzip.

## 1.3 Payload size
1. **Send fewer, larger batches.** The page's example: adding 100,000 documents in two batches of 50,000 beats four of 25,000.
2. **A large payload costs memory,** and the instance may crash if the machine does not have it. The default maximum payload is 100 MB and is configurable; raise it only with the machine's memory in view.

## 1.4 What goes in an index, and how many
1. **Meilisearch is not the main database.** It is built for retrieval; the more documents, the slower indexing and search. Index only what a search should return.
2. **Use one index per language** for a multilingual dataset.
3. **Do not create more indexes than needed.** The page links it to how the engine manages address space and leaves "too many" to the setup: reduce the count if multi-index searches degrade.
4. **Keep related objects out of each document.** The page's example is a deals index where each deal would embed its full company: store the company identifier and hydrate it through a join at search time. It lists smaller indexes, faster indexing, one place to update company data, and filtering by related data without copying it; its figure of 20 to 50 percent smaller indexes is its own estimate.

## 1.5 Machine and vectors
1. **Remove any cap on input and output operations.** The page names the credit-based limits of a cloud block-storage service as a severe slowdown for indexing.
2. **Use solid-state storage and avoid spinning disks.** Indexing is memory-hungry and multi-threaded; the page says more processor cores help more than more memory.
3. **Binary quantization is irreversible.** For AI-powered search, it stores each vector dimension in one bit, lowers semantic relevancy and speeds indexing; once enabled, the original vector values are discarded, and the only way back is to re-vectorise the whole index into a new embedder. The page says it works best on datasets above one million documents with models above 1,400 dimensions.
4. **Keep the engine updated.** The page says each release brings indexing improvements (own guidance: read the release notes before a production upgrade, since settings lists are version-bound).

## 1.6 Checks (own guidance)
1. Create the index, apply settings, load documents, then change one setting from the reindex list and confirm the resulting task reindexes; change a ranking rule and confirm it does not.
2. List the fields used in filters and sorts and confirm none of them is searchable unless users type words that should match it.
3. Compare the import time of the same data in two batch sizes before fixing a batch size.
