# jpa-hibernate-pitfalls §3 — Transactions, sessions and schema

Spring Framework 7.0 and Spring Boot 4.1 documentation unless another source is named. The placement of
`@Transactional` at service level is in `java-conventions` §4; this section covers where it silently does
nothing, and the two places a session or a schema gets created without anyone deciding.

## 3.1 Where @Transactional does nothing
1. **A call from inside the same object is not intercepted.** In the default proxy mode only external calls
   that arrive through the proxy start a transaction; a method calling another method of the same object does
   not, even if the target is annotated. Move the transactional method to another bean, or use AspectJ mode
   when the design really needs self-invocation.
2. **Visibility depends on the proxy type.** Since Spring Framework 6.0, class-based proxies honour
   `public`, `protected` and package-visible methods; interface-based proxies only honour public methods
   declared on the interface. The `@Async` annotation has the same self-invocation limit, per a concurrency
   skill reviewed for this block.
3. **A checked exception does not roll back by default.** Only `RuntimeException` and `Error` do. Since
   Spring Framework 6.2 you can switch the default globally with
   `@EnableTransactionManagement(rollbackOn = ALL_EXCEPTIONS)`, which the reference recommends unless you
   rely on commit-on-business-exception behaviour; it is the safer choice in Kotlin code, where checked
   exceptions are not enforced. Otherwise name the exceptions with `rollbackFor`.
4. **`readOnly = true` is a hint on the transaction,** and the reference says it applies only to the
   propagation values `REQUIRED` and `REQUIRES_NEW`. Put it on query-only service methods; do not treat it
   as a guard against writes.

## 3.2 Open session in view
1. **Know whether it is on.** The Spring Boot property `spring.jpa.open-in-view` defaults to `true`: it
   registers an interceptor that binds a persistence context to the thread for the whole request.
2. **What that hides.** Lazy associations load in the controller or during serialisation, outside any
   service transaction, so a missing fetch shows up as extra statements and not as an exception. A
   JPA-patterns skill warns that it can mask N+1 problems.
3. **Decide on purpose.** Set it to `false` and load what each response needs inside the service
   (§2.2, §2.4); then a forgotten fetch becomes a `LazyInitializationException` in a test instead of a
   slow page in production. If you keep it on, keep the statement count assertion of §2.1 on every endpoint.

## 3.3 Who creates the schema
1. **Use one mechanism.** The Spring Boot data-initialisation page recommends a single mechanism for schema
   generation. When a migration tool (Flyway or Liquibase) is present, use it alone; combining it with the
   basic `schema.sql` and `data.sql` scripts is not recommended and its support is slated for removal.
2. **Know the Hibernate default.** `spring.jpa.hibernate.ddl-auto` is `create-drop` when an embedded
   database is detected and no migration tool is present, and `none` otherwise. Moving from an in-memory test
   database to a real one therefore changes who creates the tables; set the value explicitly in every
   profile. `validate` is among the supported values; what it checks was not read for this block.
3. **Migrations run at startup by default** once the Flyway or Liquibase module is on the classpath, and
   Liquibase also runs before tests. You cannot use two different ways to initialise the database
   (for example a migration tool at startup and Hibernate in tests); test against the schema you deploy.

## 3.4 Checks
- A test calls the transactional method from another bean and from the same one: only the first rolls back.
- With open-in-view off, every controller test that returns an entity graph still passes.
- Start the application against an empty database and against the previous release's schema: both succeed.
- `ddl-auto` is visible and explicit in each profile's configuration.
