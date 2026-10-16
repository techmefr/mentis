# laravel-mysql-to-postgres-pitfalls: origin and source stamps

> Provenance of `skills/laravel-mysql-to-postgres-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one skill file, never run by us: no application was moved, no
migration run on PostgreSQL, no statement executed. The file was re-read on 2026-10-16 before a rule was taken
from it, each rule was checked against it in a final pass, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| `majdghithan/agent-skills` (commit `538264f`), `skills/laravel-mysql-to-postgres/SKILL.md` | MIT (LICENSE file: MIT licence text, copyright 2026 Majd Ghithan) | The empty-database test, the two data-move options, the sequence trap and its remedy, case sensitivity and its remedies, boolean comparisons, MySQL-only functions and quoting, strict grouping, no silent truncation, the verification checklist |

No code is copied; the SQL function names and the operator names are product names and are restated as such.
Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **The section "Why bother"** (indexed JSON columns, integrity, planning as data grows): marketing for the
   move, not a rule.
2. **The three links in the source's last section** (a cloud vendor's migration guide, a blog post about moving
   with the query builder, the loader tool's site): not opened, so nothing is taken from them.
3. **Tool versions and flags for the loader tool:** the source gives none and none are stated.

## Not verified
1. **Everything is the source's claim.** The case-insensitive pattern operator, the extension and the index
   option, the boolean error, the sequence behaviour, the function mapping, grouping strictness and the absence
   of truncation were not run against a database, and the PostgreSQL manual was not read.
2. **Own guidance, flagged in the text:** the CI job (part 1, point 1), the rollback preparation (point 2),
   rehearsing on a copy and comparing counts (point 3), generating reset statements from the catalogue
   (point 4), listing the places before the rehearsal (point 5), the shared case-insensitive helper, keeping
   the list of raw-SQL decisions, running the reports at real size and searching for over-long values
   (part 2, points 1, 3, 4 and 5).
3. **MariaDB** is named in the description because the source's title says "MySQL/MariaDB"; no MariaDB-specific
   behaviour was read.
4. **Laravel versions:** the source states none; nothing here is tied to a framework release.

## Related blocks
`skills/mysql-pitfalls`, `skills/laravel-conventions`, `skills/search-index-sync-pitfalls`.
Fold into the same-topic block when #118 lands.
