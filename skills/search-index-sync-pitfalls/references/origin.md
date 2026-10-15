# search-index-sync-pitfalls: origin and source stamps

> Provenance of `skills/search-index-sync-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from two library READMEs, never run by us. No Rails or Laravel application, no
Searchkick, no Scout driver and no search server was started while writing it.

## Sources (read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| ankane/searchkick at commit 6050f50: `README.md` (2,348 lines, all read; the sections used are Indexing, Strategies, Associations, Default Scopes, To Reindex or Not to Reindex, Synonyms, Testing, Deployment, Data Protection, Performance, Queuing, Partial Reindexing, Advanced Mapping, Multi Search, Scroll API, Deep Paging, Reference, Gotchas) | MIT, Copyright (c) 2013-2026 Andrew Kane (`LICENSE.txt` re-read 2026-10-16) | Four sync strategies, association and default-scope gaps, reindex triggers, partial and conditional reindex, parallel rebuild and promotion, test practice, 10,000 cap, one shard, multi-search errors, encryption |
| matchish/laravel-scout-elasticsearch at commit 78c788d: `README.md` (322 lines, all read; the sections used are Features, Installation, Index settings and mappings, Eager load, Zero downtime reimport, Search, Conditions, Pagination) | MIT, licence text without a copyright line (`LICENSE.md` re-read 2026-10-16) | Per-index mapping and settings keys, eager loading on import, zero-downtime reimport command, `query_string` default, conditions, pagination precedence, SSL verification switch |

The `laravel/scout` README (a pointer to the Laravel documentation) and the Laravel documentation itself were
not read for this block. Searchkick's `CHANGELOG.md`, `lib/` and `test/` directories and the Scout driver's
`src/`, `docs/` and `config/` were not opened; only the two READMEs are relied on.

## Version bounds stated in the sources
- Searchkick: the README says the latest version works with Elasticsearch 8 and 9 and OpenSearch 2 and 3, and
  names version 5.5.2 for Elasticsearch 7 and OpenSearch 1. It announces 6.0 as recent and describes a new query
  builder in the Upgrading section.
- Scout driver: the README lists Elasticsearch 8.0 or later with ElasticsearchDSL 8.0.0 or later, 7.0 or later
  with 3.0.0 or later, and 6.0 up to but not including 7.0 with an earlier DSL; PHP 8.0 or later and Laravel
  8.0.0 or later; Laravel Scout 10.x.
- The parallel import of the Scout driver is described there as an alpha version; it is not used here.

## Removed (in the sources, not carried)
- Everything on relevance features (stemming, synonyms at search time, misspellings, personalisation,
  conversions, autocomplete tuning, highlights, geo, nearest-neighbour, semantic and hybrid search): the index
  synchronisation question does not depend on them.
- The cloud-specific deployment recipes (Heroku add-ons, credentials embedded in URLs): hosting detail. The
  README's URL form with a user and password is not carried.
- The Rails controller, JavaScript and test-helper code: replaced by prose, and the one kept sample
  (reindexing a parent from a child) is rewritten without comments.
- The Scout driver's multiple-model search and working-with-results sections (its returned-fields option is
  kept as one line in §2.5).

## Not verified
1. **Scout's own synchronisation and queue behaviour** is documented on laravel.com and was not read; §1.1
   describes only what the Searchkick README states and says so for Scout.
2. **The query handling of the Scout driver (§2.5) is an inference.** The README states that a query passed to
   `search` is built as a `query_string` query. That user text is then read as query syntax, and that a
   callback with a structured query avoids it, is our reading of that statement; the driver's source was not
   opened and nothing was run.
3. **Searchkick defaults** (batch size 1000, refresh interval 1 second, queue name `searchkick`, the 10,000
   cap) are as the README states them for the stamped commit.
4. **Elasticsearch behaviour** (up to a second of delay, the 10,000 cap, `track_total_hits`) is the READMEs'
   description, not checked against Elasticsearch release documentation.
5. **Own guidance, labelled in the text:** the latency reading of the inline strategy (§1.1), the reindex after
   a callbacks-off section, the mapping in version control, the one-shard ranking tests, the filters-in-conditions
   rule, treating the SSL switch as development only, the erasure path and the explicit field list for personal
   data, and every "Checks" section.

## Related blocks
`nestjs-integration-patterns` (§5: index as derived data, outbox, idempotent indexing, lag),
`elasticsearch-mapping-and-reindex-pitfalls` (field types, moving documents between indices),
`elasticsearch-query-and-triage-pitfalls` (query tuning, cluster triage), `source-freshness`.
