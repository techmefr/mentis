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
   the scattered calls with it, so the next developer cannot forget. The framework's documentation (12.x, read 2026-10-20) already offers a driver-neutral `whereLike`, case-insensitive by default, with a case-sensitive option that SQL Server does not support: prefer it to a hand-written helper where the installed version has it. The PostgreSQL manual states the case-insensitive operator is a PostgreSQL extension, depends on the active locale, and does not support nondeterministic collations; it says nothing about indexes (the lower-cased functional index and the case-insensitive text extension of the source stay the source's claim).
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
6. **Strings and numbers compare differently.** The query builder's documentation says MySQL and MariaDB convert a non-numeric string to zero in a string-to-number comparison, so a lookup by number can match a text value such as `aaa`; PostgreSQL does not coerce that way. Search for loose comparisons against mixed columns and for ids read from input.
7. **Upsert and insert-get-id have preconditions.** On PostgreSQL an upsert needs a primary or unique index on the key columns it names (MySQL ignores the argument and uses the table's own), and getting an inserted id expects an auto-increment column called `id` unless another name is passed. Review every `upsert` and `insertGetId`.
8. **Grouping exception.** A non-grouped column is accepted when the table's primary key is among the grouped columns; the strictness of point 4 then bites only for the columns of other tables and for non-key grouping (PostgreSQL manual, SELECT page).
9. **Truncation is not absolute.** An over-long value in a bounded text column errors, except that excess trailing spaces are silently cut, and an explicit cast to the length truncates without an error (PostgreSQL manual, character types). A migration that trims by cast hides the defect point 5 looks for.
10. **Raw expressions carry the injection warning in both engines.** The framework says it cannot guarantee a raw expression is injection-safe; bind values and never let input choose a column name (`skills/sql-conventions` §6.1).
11. **Checklist before the old database is deleted.** The source's items, restated: the migrations run clean
   on an empty PostgreSQL database; every raw SQL call is reviewed and ported; search and filter code
   ignores case where it should; every imported table's sequence is reset and one record per critical table
   was created without a duplicate-key error; boolean columns are cast and no raw comparison to `1` or `0`
   remains; reporting queries run; the full test suite passes against PostgreSQL and the real application
   was smoke-tested end to end; MySQL is kept live and revertible until confidence is established.
