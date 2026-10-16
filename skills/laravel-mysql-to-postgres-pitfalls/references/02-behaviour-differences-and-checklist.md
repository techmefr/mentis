# laravel-mysql-to-postgres-pitfalls §2 — Behaviour that changes silently

> Part 2 of `skills/laravel-mysql-to-postgres-pitfalls`. Read it when application code or raw SQL is reviewed
> for the new driver. Sourced from `skills/laravel-mysql-to-postgres/SKILL.md` in `majdghithan/agent-skills`
> (commit `538264f`), read 2026-10-16. Sentences marked "own guidance" are ours; every other claim is the
> source's and was not run by us.

1. **Searches stop matching: PostgreSQL compares case-sensitively.** The source says MySQL's default collation
   ignores case and PostgreSQL does not, so a search written with a plain pattern match that found "iPhone" for
   "iphone" on MySQL silently returns nothing on PostgreSQL. Its remedy is the case-insensitive pattern
   operator, `ILIKE`, in the query builder's where clause; for heavy search, the `citext` extension or a
   functional index on the lower-cased column. It says to audit every product search, every find by email and
   every user-typed filter. Own guidance: write one scope or helper for "contains, ignoring case" and replace
   the scattered calls with it, so the next developer cannot forget.
2. **Zero and one are not true and false.** MySQL stores booleans as a small integer and PostgreSQL has a real
   boolean type. The source says casts hide most of this but raw comparisons break: a raw `where` clause
   comparing a boolean column to `1` fails with an error that no operator exists for boolean and integer. Its
   remedy is to let Eloquent and the `boolean` cast handle it, passing `true` or `false`, and to have no raw
   `= 1` or `= 0`.
3. **Raw SQL speaks MySQL.** Every `DB::raw`, `whereRaw` and `selectRaw` may use syntax PostgreSQL does not
   understand. The source's examples: `FIND_IN_SET()` and `GROUP_CONCAT()` become arrays and `string_agg()`,
   `DATE_FORMAT()` becomes `to_char()`, `RAND()` becomes `RANDOM()`, and backtick quoting of a name becomes
   double quotes. It says to search the application for those three calls before the cutover and review each
   hit by hand. Own guidance: keep the list of hits in the review, with the decision for each, and prefer a
   builder method that works on both drivers over a raw string when one exists.
4. **Grouping is strict.** The source says every non-aggregated column in a `SELECT` has to appear in `GROUP
   BY` on PostgreSQL, where MySQL guessed, and that reporting and dashboard queries hide this. Own guidance:
   run every report and dashboard query once against PostgreSQL with real-sized data before the cutover; a
   query that is never run in a test is found by a user.
5. **Nothing is silently truncated.** A string longer than its column raises an error instead of being
   trimmed, and a bad value in a `uuid` column raises instead of being stored. The source calls this
   PostgreSQL protecting your data, and says old code that relied on the trim now errors. Own guidance:
   search the import and the application for values that exceed a column's length, and decide on trimming in
   code on purpose.
6. **Checklist before the old database is deleted.** The source's items, restated: the migrations run clean
   on an empty PostgreSQL database; every raw SQL call is reviewed and ported; search and filter code
   ignores case where it should; every imported table's sequence is reset and one record per critical table
   was created without a duplicate-key error; boolean columns are cast and no raw comparison to `1` or `0`
   remains; reporting queries run; the full test suite passes against PostgreSQL and the real application
   was smoke-tested end to end; MySQL is kept live and revertible until confidence is established.
