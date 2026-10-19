# jpa-hibernate-pitfalls: origin and source stamps

> Provenance of `skills/jpa-hibernate-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No entity was
mapped, no query counted and no application started while writing it.

**Fold-in note.** This block is meant to be folded into the persistence reference of `spring-boot-conventions`
when PR 118 lands (that block exists only on the unmerged branch). It is standalone only so that it does not
depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Hibernate ORM 7.4 user guide (single page): the performance chapter, the entity-mapping chapter (equals and hashCode, IDENTITY, bidirectional sync), the locking chapter, the query chapter (limits, bulk statements), the settings appendix | official docs, read 2026-10-08 | §1 and §2: eager default and its cost, parent-side one-to-one, Set versus bag, many-to-many, IDENTITY and batching, pooled optimizers, equals and hashCode failure modes, version column, fetch join limits, projections, pagination limit, bulk statements |
| The Spring Framework 7.0 reference page on `@Transactional` | official docs, read 2026-10-08 | §3.1: proxy mode, visibility, read-only, rollback rules |
| The Spring Boot 4.1 pages on SQL data initialisation, and the application-properties appendix | official docs, read 2026-10-08 | §3.2, §3.3: open-in-view default, ddl-auto defaults, single mechanism, Flyway and Liquibase behaviour |
| One MIT Java agent-skill repository, its JPA-patterns and concurrency-review skills | MIT (LICENSE read) | §1.1 point 6 (no cascade from a to-one), §1.3 point 5, §2.2 point 2 (entity graph, batch size), §3.2 point 2, the `@Async` self-invocation remark |

## Rewrite notes
Rules are re-explained principle first. Where the guide only describes a mechanism and the rule is our
inference (store an enum by name; set open-in-view off on purpose), the text says so or cites the practitioner
skill.

## Not verified
1. **`MultipleBagFetchException`** is not named in the guide pages read; §2.2 states only the Cartesian
   product advice the guide gives.
2. **Default `@Enumerated` type** and what Hibernate does with it was not read; §1.4 states the explicit rule.
3. **`hibernate.hbm2ddl.auto=validate`**: listed as supported by Spring Boot; what it checks was not read.
4. **Flyway and Liquibase specifics** (never edit an applied migration, locking when several replicas start,
   repeatable migrations) were not read from the tools' own documentation, and are not written.
5. **Dropped from the source list:** "`@Transactional` never around remote calls", "keyset pagination",
   "stable sort", "count queries separately", "never expose entities from controllers" (already
   `java-conventions` §4), "LazyInitializationException is fixed by the query, not by widening the session"
   beyond what the guide says in §2.3. No page read states them.
6. **Hibernate 7.4 behaviour** (limit with fetch joins) differs from earlier releases, as the guide says; a
   project on Hibernate 6 or earlier must check §2.2 point 3 against its own version.
7. **Spring Framework 6.0 and 6.2 version notes** (visibility, `rollbackOn`) are as the reference states them.
8. **Written by us, not sourced:** the checks lists, and the advice to assert statement counts for lists of
   one and many rows.

## Related blocks
`java-conventions` (§4: DTO at the edge, lazy by default, transactional at service level),
`testing-anti-patterns`, `security-hardening`, `background-jobs-conventions` (a job that runs twice).
