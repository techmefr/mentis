# jpa-hibernate-pitfalls §2 — Fetching and queries

The Hibernate performance chapter opens its fetching section with one sentence worth keeping: fetching too
much data is the number one performance issue for most Jakarta Persistence applications. Everything below
is a way to fetch exactly what a use case needs, and to notice when it does not. Hibernate 7.4 unless
another source is named.

## 2.1 Make the statements visible
1. **Count the SQL statements of a use case in a test.** The guide recommends a data-source proxy (it names
   datasource-proxy and p6spy) because it lets an integration test assert the number of executed statements
   and fail when an N+1 appears. Plain statement logging is fine to look at but cannot fail a build.
2. **Assert the count for a list of one and a list of many.** An N+1 is a count that grows with the data;
   two sizes in one test show it.
3. **Know the two sources of N+1.** An eager association whose join fetch a query forgot triggers a secondary
   statement per row (§1.1); a lazy collection touched in a loop does the same on first access. The fix is in
   the query that loads the data, not in the loop.

## 2.2 Fetch joins and pagination
1. **A `JOIN FETCH` is right for `ToOne` associations and for at most one collection.** Fetching several
   collections in one query produces a Cartesian product. For more than one collection, the guide says to use
   secondary queries, triggered by navigating the lazy association or by calling `Hibernate.initialize`.
2. **Alternatives to a fetch join** for the same job, from a JPA-patterns skill and the settings appendix: an
   entity graph (declarative; Spring Data accepts it on a repository method), or batch fetching (`@BatchSize`,
   or the setting `hibernate.default_batch_fetch_size`), which loads lazy associations for several parents
   in one statement. Whichever you choose, check it with the count from §2.1.
3. **Pagination combined with a fetch join to a collection is the case to check first.** Before Hibernate 7.4
   a limit did not work well with a many-valued fetch join. From 7.4 it is fixed on databases that support
   limits and offsets inside subqueries; on the others Hibernate loads every matching row and applies the
   limit in memory, which the guide says has terrible performance characteristics. A setting makes such a
   query throw instead (`hibernate.query.fail_on_pagination_over_collection_fetch`); turn it on in tests.

## 2.3 LazyInitializationException
1. **Fetch what is needed before the persistence context closes.** The guide says this is the best way to
   deal with the exception, and that there are good and bad ways: the good one is the query or fetch
   join of §2.2, the bad ones keep a session open longer than the unit of work (§3.2).
2. **A DTO or a projection built inside the transaction cannot throw it.** Map to the response shape in the
   service, while the session is open (see the projections rule below).

## 2.4 Projections for reads
1. **Entity queries are for entities you will modify.** They are useful because of dirty checking. For a
   read-only transaction the guide says to fetch DTO projections: select only the columns the use case
   needs, and the persistence context has nothing extra to manage.
2. **Use a record or an interface projection** with a constructor expression or the repository's projection
   support, rather than loading the entity and copying a few fields.

## 2.5 Bulk update and delete
1. **A bulk `update` or `delete` statement bypasses the persistence context.** The guide states that its
   effect is not reflected in the persistence context or in entities already in memory, and the application
   must keep them in sync (clear the context or reload after the statement).
2. **It does not increment the version column** unless you write `update versioned`; see `01-mapping.md`
   §1.5.

## 2.6 Checks
- A statement-count assertion on the busiest list endpoint, run with 1 and with 20 rows.
- A query that fetches a collection and pages: run it on the production database engine, since whether the
  limit is applied in the database depends on what the engine supports.
- Search for a repository method returning an entity that a controller maps field by field.
