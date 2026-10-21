# spring-boot-conventions — origin and source stamps

> Provenance of `skills/spring-boot-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Spring Boot reference documentation (`spring-projects/spring-boot`, `documentation/`, version 4.2.0-SNAPSHOT): structuring your code, beans and dependency injection, externalized configuration, profiles, servlet web applications, working with SQL databases, graceful shutdown, actuator endpoints, testing | Apache-2.0 (repository `LICENSE.txt`, read) | §1 to §3. Rewrite with credit. |
| Spring Security reference documentation (`spring-projects/spring-security`, `docs/`): authorize HTTP requests, CSRF, CORS | Apache-2.0 (repository `LICENSE.txt`, read) | §3.4 to §3.6. |

**Verification pass 2026-10-20.** Re-opened the published Spring Boot reference at 4.1.1 (the stable release that
day; the repository `LICENSE.txt` of Apache-2.0 re-read is the one credited, the site pages were read for facts)
and the Spring Security reference at 7.1.1: structuring your code, beans and dependency injection, externalized
configuration (both halves), profiles, servlet web applications, SQL databases, graceful shutdown, actuator
endpoints, testing Spring Boot applications (both halves), authorize HTTP requests, CSRF, CORS. Confirmed:
§1.1 to §1.8 (kebab-case placeholders, constructor binding with records and the `-parameters` flag, validation
with `@Validated` and `@Valid` on nested objects, override order and last-profile-wins, the active-profile
property valid only in non-profile-specific documents), §2.1, §2.2 (with the Framework 6.0 origin of the
format), §2.4 to §2.8, §3.1 to §3.4, §3.7 to §3.9, §3.11, §3.12. Corrected: §2.3 (the reference says web
observations and metrics, not tracing), §2.9 (network-layer refusal is described only for Tomcat, Jetty and
Reactor Netty), §3.5 (disable CSRF for a backend with no browser traffic), §3.6 (a
`UrlBasedCorsConfigurationSource` bean plus enabling CORS in the chain). Flagged as our reasoning where the pages
say nothing: field injection (§1.2), the kill-timeout relation and the shutdown default (§2.9), the
production-engine advice for data tests (§3.10; the page shows the annotation and states that data tests roll
back, and its embedded-database replacement is implied rather than stated). The version stamp above is
superseded for the pages read: 4.1.1, not a snapshot, and the property names used in the block are the ones
those pages show.

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

Independent verification 2026-10-21: 14 checked, 14 matched, 0 corrected, 0 unverified. Checked against the documentation tree at main (4.2 snapshot): exposure and sanitisation defaults, shutdown access, open-in-view, connection-fetch, problem details, H2 console, graceful shutdown, profiles and slices
