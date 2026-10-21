# offline-first-sync-and-conflict-pitfalls: origin and source stamps

> Provenance of `skills/offline-first-sync-and-conflict-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from project documentation and craft knowledge. No sync service was
installed or run and no client was built while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| electric-sql/electric at commit 3f9809f, `website/docs/sync/guides/` (writes, shapes, security, troubleshooting; auth and postgres-permissions seen only by title), LICENSE file read | Apache-2.0 (LICENSE file) | Four write patterns and their trade-offs, synced versus local state, shape definition limits, public-by-default endpoint, proxy authorisation, transport pitfalls |

The repository holds agent instruction files and a `.claude` folder; they were not opened and nothing in them was
followed.

## Left out on purpose
- yjs/yjs: the licence field of the GitHub API was "no assertion"; the repository was not opened.
- automerge/automerge: LICENSE file read (MIT, Copyright (c) 2019-2021 the Automerge contributors); its documentation
  was not used, so no text or structure of it is in this block.
- rocicorp/mono: LICENSE file read (Apache-2.0); not used (docs not read).
- Electric's streams, agents and integration documentation, benchmarks and the product comparison page.
- All code samples, configuration names, ports and version-specific API names.

## Not verified
1. **Statements about Electric** (shapes single-table and immutable, filter restrictions, public by default, cache
   headers and request sharing) are the documentation's at the commit; the product changes quickly, so re-read
   before relying on them.
2. **Convergent data types, tombstone lifetime, clock handling and ordering** (§2) are craft knowledge, not read
   in a source.
3. **Platform storage eviction and browser connection limits** are general knowledge; re-read the platform
   documentation for the targets you support.
4. **Own guidance** is marked in the text, and every "Checks" and test list is own guidance.

## Related blocks
`kotlin-android-data-flow-and-api-pitfalls`, `rich-text-editor-pitfalls`, `kanban-board-ui-pitfalls`,
`nestjs-reliability`, `laravel-idempotent-jobs`, `field-and-row-permission-ui-api-pitfalls`,
`flutter-four-async-states`, `source-freshness`.
