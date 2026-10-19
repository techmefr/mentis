# prisma-ops-and-test-hygiene: origin and source stamps

> Provenance of `skills/prisma-ops-and-test-hygiene`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Prisma documentation: connection pool, logging, the version 7 upgrade guide, the migration pages | official docs | Pool defaults per major, driver adapter pool options, middleware removal and extensions, removed flags and settings, the version 8 migration workflow note |
| One MIT agent-skill for Prisma migration review (copyright line blank in the licence file) | MIT | The migration risk list, rename and required-column behaviour, expand and contract, foreign key indexes, concurrent index builds, the pre-apply checklist |
| One MIT JavaScript testing-practices repository | MIT | The five outcomes, property-based and mutation testing, no sleeping, realistic data, behaviour over internals |
| The Node.js API documentation: events and net pages | MIT | Listener order, error event without a listener, port 0 assignment |

The share-alike Node best-practice repository and the other ideas-only repositories were used for no phrasing.

## Not verified
1. **Prisma version boundaries.** Pool defaults, the removal of `$use`, `$on('query')` and the removed flags
   are from the version 7 upgrade and logging pages; behaviour on version 6 and earlier was not checked
   except the version 6 pool default. Prisma ORM 8 documents a TypeScript-based migration workflow that was
   not worked through; section 1.4 is for the SQL-file workflow and says so.
2. **Rename, required-column and enum behaviour** (§1.4.1 to 1.4.3) come from the migration-review skill; the
   migration documentation page fetched returned newer-major content and did not confirm them.
3. **fast-check default run count** (100) is from a comment in the testing source, not from the library's
   documentation; seed and path replay is described from general knowledge of the library, not read.
4. **Stryker** is described from its public documentation page, not run.
5. **Written by us:** the connection budget
   arithmetic, and all verification lists.

## Related blocks
`testing-anti-patterns`, `nestjs-di-traps`, `nestjs-reliability`, `nestjs-node-conventions`,
`devops-conventions`.
