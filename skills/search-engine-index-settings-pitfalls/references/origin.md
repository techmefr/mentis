# search-engine-index-settings-pitfalls: origin and source stamps

> Provenance of `skills/search-engine-index-settings-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and skill files, never run by us: no Meilisearch instance or Redis
server was started, no index created and no query run while writing it. Every file below was opened in full on
2026-10-16 before a rule was taken from it (the deployment page only in its first 150 lines, see below), and
each repository's licence file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| meilisearch/documentation (commit `944814e`), `capabilities/indexing/advanced/indexing_best_practices.mdx` | MIT (LICENSE file: MIT licence text, copyright Meili SAS 2019-2025) | The reindex list, searchable attributes, payloads, index layout, joins, quantization, hardware |
| the same repository, `resources/self_hosting/security/basic_security.mdx` | MIT | Master key, the four default keys, which key goes to a frontend |
| the same repository, `resources/self_hosting/deployment/running_production.mdx`, lines 1 to 150 (steps 1 to 4) | MIT | System user, directories and modes, configuration file, service file |
| redis/agent-skills (commit `a84871d`), `skills/redis-search/SKILL.md` | MIT (LICENSE file: MIT licence text, copyright Redis, Inc. 2026; frontmatter `license: MIT`) | PREFIX, dialect, tag versus text, vector settings, the alias operation |
| the same repository, `skills/redis-search/references/index-management.md`, `query-optimization.md`, `dialect.md`, `debugging.md` | MIT | The rebuild table, the cheap-query levers, dialect behaviour, FT.INFO fields and the hyphen example |

The Meilisearch pages come from a documentation repository whose licence file is the repository's MIT text;
no separate licence for the documentation content is stated, so the pages were rewritten, not copied. The
code samples in the Redis files were not carried; client mirrors (Python and Java) were left out.

The redis/docs repository (CC BY-NC-SA 4.0) and valkey-io/valkey-doc (CC BY-SA 4.0) are idea-only for this
programme and were not read for this block.

## Version bounds stated in the sources
1. Meilisearch: none beyond the pinned commit; the reindex list and the default key set are those of that
   commit. The page says the payload default is 100 MB and configurable.
2. Redis: dialect 2 is the only supported value from Redis 8; Redis 7 and the module still honour dialect 1
   (the source's statement). The hybrid command that needs Redis 8.4 was not taken.

## Removed in the verification pass
1. **The second half of the deployment page** (reverse proxy and HTTPS steps, by their headings) was not read,
   so nothing about proxying or TLS is stated.
2. **The master key length "at least 16 bytes"** was kept as the page states it; its example commands and the
   generated sample key were not carried.
3. **The remaining Redis Search references** (hybrid search, aggregation, RAG, HNSW tuning, text tokenisation,
   JSON indexing, client pages) were not read in full; only the five files in the table are used.
4. **"Search keys with admin power on a public page"** (from the brief) is stated as the page's rule that admin
   keys must not be on a public frontend; nothing stronger.
5. **Line comments** in the source examples were not carried; the repository forbids them.
6. **The `redis-search` skill's claim that a tag is about ten times faster than text** is kept and attributed
   to the source in the text; it was not measured.

## Not verified
1. **Nothing was run.** Every behaviour is the sources' claim.
2. **Conflict inside the Redis source:** a dimension mismatch is said to produce silent garbage in the skill
   overview and an initialisation error in the debugging file; the text says so and tells the reader to test.
3. **Meilisearch settings per release** beyond the commit were not checked; new settings added later are not
   in the reindex list.
4. **Which Redis versions ship which commands** (beyond the dialect statement) was not checked.
5. **Written by us, not sourced:** the ranking-rule remark and the copy-first advice for a settings change
   (1.1), reading the key from a secret store, scoped keys with
   an expiry and the key checks (2), the reasoning behind PREFIX, the check-at-creation rule for vectors,
   the failure-count-first remark, and every checks section.

## Related blocks
`elasticsearch-mapping-and-reindex-pitfalls`, `search-index-sync-pitfalls`, `redis-client-and-cluster-pitfalls`,
`redis-security-and-observability-pitfalls`, `security-hardening`, `source-freshness`.
