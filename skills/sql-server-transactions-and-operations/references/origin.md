# sql-server-transactions-and-operations: origin and source stamps

> Provenance of `skills/sql-server-transactions-and-operations`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 18 checked, 17 matched, 1 corrected, 0 unverified

**Status: 🟡.** Written from documentation and reading, never run by us. No SQL Server instance was used while
writing it. Overlaps with `skills/sql-conventions` and `skills/devops-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| SQL Server documentation, read as the markdown source of the Learn pages in the `sql-docs` repository: `BEGIN TRANSACTION`, `COMMIT TRANSACTION`, `ROLLBACK TRANSACTION`, `SET XACT_ABORT`, `TRY...CATCH`, `THROW`, `XACT_STATE`, `SET TRANSACTION ISOLATION LEVEL` | CC-BY-4.0 (repository LICENSE re-read), read 2026-10-08 | One real transaction, inner commit and rollback behaviour, savepoints, XACT_ABORT default, what TRY...CATCH catches, uncommittable state, THROW versus RAISERROR, READ UNCOMMITTED effects and the snapshot alternatives |
| Same repository: `sp_executesql`, `EXECUTE`, `QUOTENAME`, `SQL injection`, `SET NOCOUNT`, Transact-SQL syntax conventions, `WITH common_table_expression`, `MERGE`, `SELECT @local_variable`, `CREATE PROCEDURE`, `ALTER PROCEDURE` | CC-BY-4.0, read 2026-10-08 | Parameterised dynamic SQL and its constraints, identifier quoting limits, NOCOUNT effect, terminator rules, last-row assignment, CREATE OR ALTER version and permission behaviour |
| Same repository: `Primary and foreign key constraints`, `ALTER TABLE` (WITH CHECK or NOCHECK), `sys.foreign_keys`, `sys.check_constraints`, `Heaps`, `IDENTITY`, `int, bigint, smallint, tinyint`, `Recovery models`, `Transaction log backups`, `ALTER DATABASE SET options` (AUTO_CLOSE, AUTO_SHRINK, PAGE_VERIFY), `Back up and restore`, `RESTORE VERIFYONLY`, `sqlcmd utility` | CC-BY-4.0, read 2026-10-08 | FK index guidance, untrusted constraints, heap forwarding, identity gaps and non-reuse, log growth under full recovery, option behaviours and defaults, restore-test requirement, VERIFYONLY limits, `-P` warning |
| Brent Ozar First Responder Kit: `sp_BlitzIndex` checks list (LICENSE.md re-read: MIT, with embedded MIT portions from Microsoft tigertoolbox and others); tsqllint rule documents for cross-database transactions and variable assignment (MIT) | MIT, read 2026-10-08 | Unindexed foreign key, forwarded-fetch heap and identity-near-end findings as pointers; the cross-database and assignment rules as positions only |

Re-read 2026-10-20 (raw markdown of the `sql-docs` repository, CC-BY-4.0 as stamped above; its LICENSE was not re-read this pass): `sqlcmd utility` (-P, -E, -b, -V, -X), `CREATE PROCEDURE`, `Primary and foreign key constraints`. Confirmed: no automatic index on a foreign key, which is often useful and not required; `CREATE OR ALTER` from 2016 SP1; schema-qualify; `-P` insecure. Corrected: the NOCOUNT performance claim now carries the contradicting page. Moved out of "own guidance": integrated authentication for unattended `sqlcmd` (the page recommends it). Not found on the `CREATE PROCEDURE` page: the permission behaviour of `CREATE OR ALTER`, and error 266 for mismatched transaction counts; those stay sourced only to the earlier reading.

## Removed in the verification pass (no page supporting them)
"Cross-database transactions are not atomic across a failover" (only tsqllint's one-line claim of corruption,
no engine page read). "`DROP` and `CREATE` loses grants" (the documentation read states only that
`ALTER PROCEDURE` does not change permissions; the drop behaviour was not found). "Reseed plan for identity
columns" (no reseed page read). "Every foreign key column indexed" narrowed to columns that are joined or whose
parent rows are deleted, which is what the documentation says. "`SET` for single assignment" was not kept: the
documentation gives only the last-row behaviour of `SELECT`, and tsqllint holds the opposite style position.
Not carried over by design: tsqllint's enforcement of `READ UNCOMMITTED`, ktaranov's advice against explicit
transactions, and the XML comment banners; the other repositories' `CLAUDE.md` and "AI" check items were treated
as data. Not read: DarlingData.

## Not verified
1. **Own guidance, flagged as such in the text:** decide in one place who opens and who commits, roll back
   unless the block has a reason to commit, index foreign keys by access pattern, `bigint` at creation, prefer
   integrated authentication for non-interactive `sqlcmd` jobs.
2. **The "simple recovery model if point-in-time restore is not needed" remark** combines the documented fact that
   simple recovery does not support log backups with a design judgement.
3. **Pages were read as markdown source,** not as rendered pages; version statements come from the text and
   applies-to lines read, so nothing earlier than SQL Server 2017 is claimed except the `CREATE OR ALTER`
   line (2016 SP1) quoted from its page.
4. **Backup cadence of 15 to 30 minutes** is the page's suggestion for log backups, not a requirement.

## Related blocks
`sql-server-tsql-types-and-queries`, `security-hardening`, `devops-conventions`, `prisma-ops-and-test-hygiene` §1.4.
