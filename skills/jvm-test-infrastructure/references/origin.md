# jvm-test-infrastructure: origin and source stamps

> Provenance of `skills/jvm-test-infrastructure`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real project by us. No container was
started and no Spring test was run while writing it.

**Fold-in note.** This block is meant to be folded into the tests reference of `spring-boot-conventions`
(Spring and Testcontainers parts) and into `java-conventions` (the Clock part) when PR 118 lands. It is
standalone only so that it does not depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Spring Boot 4.1 pages on testing Spring applications and on Testcontainers | official docs, read 2026-10-08 | §1.1 (data slices default to an embedded database, `Replace.NONE`), §1.2 (service connection, dynamic properties), §1.3 (lifecycle, imported containers), §2.1 (slices), the component-scan note |
| The Spring Framework 7.0 page on context caching | official docs, read 2026-10-08 | §2.2, §2.3: cache key, default maximum, forking, dirtying |
| The Testcontainers for Java documentation folder (index, databases module intro, features: networking, configuration, reuse; JUnit 5 and manual-lifecycle pages) | MIT (LICENSE read) | §1.1 reason to use a real engine, §1.2 mapped ports, §1.3 shared and singleton containers, §1 cleanup container and reuse |
| The Awaitility usage page | project documentation, read 2026-10-08 | §3.1: default timeout, polling options, assertions inside the poll, ignored exceptions, same-thread polling |
| The `java.time.Clock` API page (Java 21) | official docs, read 2026-10-08 | §3.2: purpose, injection, fixed and offset clocks |

## Rewrite notes
Rules are re-explained principle first. Package and annotation names are those of Spring Boot 4.1; the
Testcontainers documentation folder was read from a shallow clone of the main branch, so its version is the
repository head.

## Not verified
1. **Spring Boot 3 and earlier names:** `@MockBean`, `@DynamicPropertySource` placement, and the artifact for
   service connections differ from the 4.1 pages; nothing was read for earlier versions.
2. **Testcontainers module for a given engine** (class names, image defaults) was not read beyond the
   databases index; §1.1 point 3 (pin the image) is our advice.
3. **`@Testcontainers` and `@Container` usage with Kotlin** or with JUnit 4 was not covered.
4. **Awaitility version** and the Hamcrest dependency: the page read does not state them.
5. **Dropped from the source list:** "no mocking the class under test", "no verify-everything tests", "test
   names state behaviour" (not infrastructure; `testing-anti-patterns` covers mocking), "never disable the
   resource reaper" as an absolute (the documentation allows it where the environment cleans up),
   "avoid `@DirtiesContext` sprawl" is kept only as far as the framework page supports.
6. **Written by us, not sourced:** the checks lists, the awkward-instants list in §3.2, the test-only mutable
   clock in §3.2, and the advice to count contexts from the cache debug log (the log category itself is
   from the framework page).

## Related blocks
`testing-anti-patterns` (§1 to §3), `tdd`, `java-conventions`, `devops-conventions` (CI that runs a container
runtime).
