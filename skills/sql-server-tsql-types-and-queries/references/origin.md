# sql-server-tsql-types-and-queries: origin and source stamps

> Provenance of `skills/sql-server-tsql-types-and-queries`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 14 checked, 14 matched, 0 corrected, 0 unverified

**Status: 🟡.** Written from documentation and reading, never run by us. No SQL Server instance was used while
writing it. Overlaps with `skills/sql-conventions` (2026-10-19); cross-referenced, not merged. SQL
Server has no coverage anywhere else in the repository.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| SQL Server documentation, read as the markdown source of the Learn pages in the `sql-docs` repository (checked-out HEAD, applies-to lines SQL Server 2017 and later): `datetime`, `datetime2`, `char and varchar`, `nchar and nvarchar`, `ntext, text, and image`, `money and smallmoney`, `ISNULL`, `COALESCE`, `GETDATE`, `SYSUTCDATETIME`, `+ (String Concatenation)`, `Data type precedence`, `Data type conversion` | CC-BY-4.0 (the repository LICENSE re-read), read 2026-10-08 | Date type rounding and recommendation, default lengths 1 and 30, byte versus byte-pair, `N` prefix, deprecated LOB types, money rounding, ISNULL truncation and nullability, COALESCE double evaluation, 8,000-byte concatenation truncation, precedence order |
| Same repository: `Scalar UDF inlining`, `table` data type, intelligent query processing details (table variable deferred compilation), `Statistics`, `Parameter Sensitive Plan optimization`, `Query processing architecture guide` (parameter sensitivity, local variables, RECOMPILE), `CREATE PROCEDURE` | CC-BY-4.0, read 2026-10-08 | Four reasons scalar UDFs are slow, inlining requirements and versions, table variable estimate and the 100-row caution, no statistics for multi-statement functions, sniffing scope, local-variable estimates, PSP version, schema-qualification reason |
| tsqllint rule documents: non-sargable, data-type-length, unicode-string, schema-qualify, set-variable, information-schema (LICENSE re-read, MIT) | MIT, read 2026-10-08 | Function-in-predicate, length and N-prefix rules; the information-schema and set-variable positions as style rules only |
| Brent Ozar First Responder Kit: `sp_BlitzCache` checks list and code, `sp_BlitzIndex` checks list (LICENSE.md re-read: MIT, with embedded MIT portions from Microsoft tigertoolbox and others) | MIT, read 2026-10-08 | Non-sargable and leading-wildcard check text, `PlanAffectingConvert` / `ConvertIssue` "Seek Plan" handling, scalar-function and multi-statement-function findings, parameter-sniffing variance check |

Re-read 2026-10-20 (raw markdown of the `sql-docs` repository, CC-BY-4.0 as stamped above): `Intelligent query processing details`, `Data type conversion`. Confirmed: table variable deferred compilation needs SQL Server 2019 and compatibility level 150, assumes one row otherwise, adds no column statistics, and its plan is built from the first execution's count and reused; scalar function inlining needs 2019 and level 150, on by default. The `Data type conversion` page says nothing about index seeks or cardinality, so the loss of a seek through an implicit conversion (the "Consequence" item below) stays unsourced by Microsoft pages: only an archived team blog post found by search (not read in full, no licence read) and third-party write-ups describe the plan warnings, and none is a source here.

Also read 2026-10-20 (same repository, same licence stamp): `int, bigint, smallint, and tinyint`, `datetime2`, `SQL Server index design guide`. Confirmed ranges and sizes; the `datetime2` page states no recommendation over `datetime` for new work (the recommendation in the first row came from the `datetime` page), documents that implicit conversion from `datetime` at compatibility level 130 and later accounts for fractional milliseconds, and says the type is not time-zone aware. The index design guide says nothing about functions in predicates, leading wildcards or implicit conversion in ordinary predicates (only an error for a conversion on the left side of a filtered index expression, with the advice to convert the right side), so the sargability items in "Not verified" remain supported only by the lint rule and the First Responder Kit. The parameter-sensitive plan page was not found at the path tried (not found).

## Removed in the verification pass (no page supporting them)
"Avoid query hints except `RECOMPILE` and `NOEXPAND`" (no page read on hints beyond `RECOMPILE`). "Parameter
sniffing is the first suspect for fast in SSMS, slow in the application" (the session-setting difference that
causes it was not read; rewritten to the documented variance check). Not carried over from the sources, by
design: tsqllint's rule that enforces `READ UNCOMMITTED`, its ban on `COUNT(*)`, ktaranov's advice against
explicit transactions and its XML comment banners, naming-by-prefix and keyword-capitalisation style rules, and
the "AI" check item and `CLAUDE.md` of the other repositories (treated as data). Not used because not read this
session: DarlingData, and the ktaranov style guide beyond its LICENSE.

## Not verified
1. **Own guidance, flagged as such in the text:** store UTC, start identity keys on `bigint`, prefer an inline
   table-valued function when the logic is one query, check generated parameter types of drivers and ORMs,
   `sys` views over `INFORMATION_SCHEMA` (a lint position, no reason in its rule document).
2. **Consequence of implicit conversion on index seeks:** the precedence page gives the conversion direction;
   the loss of a seek rests on the showplan warning handling in the First Responder Kit code, not on a
   Microsoft page.
3. **Sargability of functions and leading wildcards:** supported by the tsqllint rule and the First Responder
   Kit check text, not by a Microsoft page.
4. **Findings read as titles only:** forced serialisation from a scalar function in a computed column or check
   constraint, and the single-threaded modification note for table variables, come from the check lists and the
   kit's finding text.
5. **Pages were read as markdown source,** not as rendered pages; includes (version banners) were not expanded,
   so version statements come from the applies-to lines and the moniker ranges.

## Related blocks
`sql-server-transactions-and-operations`, `dotnet-aspnet-efcore-pitfalls` §3, `security-hardening`.
