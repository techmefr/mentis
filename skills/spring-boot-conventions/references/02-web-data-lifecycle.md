# § 2 — Errors, persistence settings, shutdown

> Section 2 of `skills/spring-boot-conventions`. Read it when an error body is produced, a datasource or JPA
> setting is touched, or the stop of the service matters. Read 2026-10-02 from the Spring Boot reference
> (4.2.0-SNAPSHOT): servlet web applications (error handling), working with SQL databases, graceful shutdown.
> The persistence rules that are not Boot-specific are in `skills/java-conventions`.

1. **Errors are produced in one place.** The default error mapping gives machine clients a JSON body with
   status and message and browsers a placeholder page. Domain failures are translated by exception-handler
   methods in an advice class, not by building responses in each controller (`skills/api-design` §5 for the
   shape).
2. **Switch on the problem-details format for APIs with outside consumers.** The framework supports the
   standard problem body, and Boot turns it on with one property (`spring.mvc.problemdetails.enabled`). Check
   the property name against the release in use.
3. **Errors handled inside a controller are not necessarily recorded by metrics and tracing.** If error rates
   matter, let the exception propagate to the advice, or record the observation where it is handled.
4. **A test with a mock web environment cannot prove a custom error page is rendered,** since error pages
   depend on the servlet container: use a running server for that one case.
5. **Turn off open-session-in-view explicitly** (`spring.jpa.open-in-view=false`). Boot registers it by
   default for web applications to allow lazy loading in views. Turning it off makes a lazy load outside a
   transaction fail in tests rather than quietly querying during view rendering in production.
6. **Do not let the ORM create the production schema.** The auto-DDL property takes values that create or
   drop tables (the documentation's own example is `create-drop`); keep those for throwaway test databases
   and run schema changes through a migration tool at deploy.
7. **The development console of the embedded database is never enabled in production.** The documentation
   names the H2 console explicitly; keep its property off outside a development profile.
8. **The lazy connection setting (`spring.datasource.connection-fetch=lazy`) fetches a pooled connection only
   when a statement actually runs,** so a transaction that finishes without touching the database holds no
   connection. Consider it when transactions often open before the data access.
9. **Graceful shutdown is on by default for the embedded servers; keep it,** and set the grace period
   (`spring.lifecycle.timeout-per-shutdown-phase`) below the platform's kill timeout. The server stops accepting
   new requests at the network layer and lets in-flight ones finish. An IDE stop that does not send a
   termination signal skips it, so do not conclude from a development run that the service drains.
