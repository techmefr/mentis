---
name: jpa-hibernate-pitfalls
description: "Use when a JPA or Hibernate entity, repository or query is written or reviewed, or a Spring service touches the database: association fetch types and N+1 queries, LazyInitializationException, fetch joins and pagination, DTO projections, equals and hashCode on entities, Set versus List for associations, bidirectional association sync, IDENTITY versus sequence ids and JDBC batching, enum mapping, optimistic locking with a version column, bulk updates that bypass the persistence context, where @Transactional works and where it does not, open-in-view, and who creates the schema (Hibernate DDL versus Flyway or Liquibase)."
---

# jpa-hibernate-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the layer between the entity model and the database. The three
sections share one premise: **the ORM hides the SQL, so every one of these is invisible in the Java and
only shows up as a count of statements, a wrong row, or an exception far from the cause**. The rule is
therefore to make the statements visible in a test. `java-conventions` §4 states the two Spring and JPA
rules that hold everywhere (a DTO at the API edge, lazy by default); this block adds the rest.

## When
- Writing or reviewing an entity, an association mapping, a repository method or a JPQL query.
- A page makes hundreds of queries, a `LazyInitializationException` appears, or an update is lost.
- An entity is put in a `Set` or used as a map key, or `equals` and `hashCode` are added to it.
- Adding `@Transactional`, deciding where a transaction starts, or changing who creates the schema.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Mapping: fetch type, collections, bidirectional sync, equals and hashCode, id generation and batching, enums, version column | an entity or association is written or changed | [`01-mapping.md`](./references/01-mapping.md) |
| 2 | Fetching and queries: N+1, fetch joins, LazyInitializationException, projections, pagination, bulk updates, counting statements in a test | a query is written, a page is slow, or an exception names a lazy association | [`02-fetching-and-queries.md`](./references/02-fetching-and-queries.md) |
| 3 | Transactions, sessions and schema: proxy limits, read-only, rollback rules, open-in-view, Hibernate DDL versus a migration tool | `@Transactional` is added, a request runs without a transaction, or the schema is created | [`03-transactions-and-schema.md`](./references/03-transactions-and-schema.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a test counted the SQL statements of the use case and the
count did not grow with the data (§2), a test put two instances for the same row into a `Set` the way the
code does and got one (§1.3), two sessions updating the same row did not both commit (§1.5), and the
service method that needs a transaction was called from outside its own class in a test and rolled back on
failure (§3). A mapping that was only read is not verified.

## Guardrails
- Never leave a `ToOne` association eager (§1.1).
- Never base `equals` and `hashCode` on a generated id that is read before it exists (§1.3).
- Never fetch-join two collections in one query (§2.2).
- Never expect `@Transactional` to apply to a call from the same object (§3.1).
- Never let Hibernate create the schema in a deployed environment that has a migration tool (§3.3).
- This block states Hibernate 7.4, Spring Framework 7.0 and Spring Boot 4.1 behaviour as of the documentation
  read on the date in [`references/origin.md`](./references/origin.md); fetching and pagination behaviour
  changed between Hibernate releases, so check a rule against the version in use. Nothing was run while
  writing it.
- Locking models beyond optimistic versioning, second-level caches and multi-tenancy are out of scope.

## Origin
Rewritten from the Hibernate ORM user guide (its performance chapter, the entity-mapping and query chapters),
the Spring Framework `@Transactional` reference, the Spring Boot data-initialisation pages and one MIT
JPA-patterns skill (read 2026-10-08). 🟡: never run by us; meant to be folded into the same-topic block
(`spring-boot-conventions`, a persistence reference) when PR 118 lands; open points are in
[`references/origin.md`](./references/origin.md).
