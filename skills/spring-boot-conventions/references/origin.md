# spring-boot-conventions — origin and source stamps

> Provenance of `skills/spring-boot-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Spring Boot reference documentation (`spring-projects/spring-boot`, `documentation/`, version 4.2.0-SNAPSHOT): structuring your code, beans and dependency injection, externalized configuration, profiles, servlet web applications, working with SQL databases, graceful shutdown, actuator endpoints, testing | Apache-2.0 (repository `LICENSE.txt`, read) | §1 to §3. Rewrite with credit. |
| Spring Security reference documentation (`spring-projects/spring-security`, `docs/`): authorize HTTP requests, CSRF, CORS | Apache-2.0 (repository `LICENSE.txt`, read) | §3.4 to §3.6. |

**Read but not used for rules:** method security, OAuth2 resource-server and login chapters, data-access
chapters beyond the SQL page, observability and the Spring Framework reference were not read; no rule here is
claimed for them (so no rule on method-level authorization is given). Left out: reactive stack, native images,
container image building, Kotlin.

**Version stamp.** Documentation at Spring Boot 4.2.0-SNAPSHOT (a development snapshot, not a release). The
test annotations and several property names sit in modules that may differ in older lines; check each property
or annotation against the release in use. Expiry: when the project's Boot major changes
(`skills/source-freshness` §2.1) re-read §2 and §3 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against a
Spring Boot project.
