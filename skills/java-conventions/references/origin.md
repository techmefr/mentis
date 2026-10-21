# java-conventions — origin and source stamps

> Provenance of `skills/java-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule. The earlier provenance (Effective Java,
> two MIT-licensed skill repositories) is in the Origin section of `SKILL.md`.

**Status: 🟡.** No Java project was built or run for this pass.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Facts were re-read from the JDK source tree (the javadoc of the classes cited), the Spring Framework and Spring Boot reference sources, the Jakarta Persistence API source and the Maven Surefire page. Nothing was compiled or run. Effective Java is a book and was not available; the points that rest only on it are listed as unverified.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| JDK source tree: Optional, Object, Enum, ExecutorService, AutoCloseable, ConcurrentHashMap, Record (javadoc) | GPL-2.0 with the Classpath exception (LICENSE of the openjdk/jdk repository read 2026-10-20), facts only | Optional intent note, hashCode contract, ordinal note, shutdown advice, try-with-resources note, concurrent retrievals, records since 16 |
| Spring Framework reference sources (dependency injection, declarative transactions, propagation, rollback rules) and the Transactional annotation javadoc | Apache-2.0 (LICENSE.txt of spring-framework read 2026-10-20) | constructor injection advice, participating transactions, rollback-only and the unexpected rollback exception, requires-new connection and pool warning, proxy interception, read-only hint, default rollback on unchecked only |
| Spring Boot reference source: external configuration | Apache-2.0 (LICENSE.txt of spring-boot read 2026-10-20) | record binding, validation of configuration properties, duration units |
| Jakarta Persistence API source: ManyToOne, OneToMany, Enumerated | Eclipse Distribution License 1.0 / EPL-2.0 (LICENSE.md read 2026-10-20) | fetch defaults and the lazy hint, ordinal default for enums |
| Apache Maven Surefire plugin documentation: inclusions and exclusions | Apache-2.0 (Maven licence file read 2026-10-20) | default test class name patterns |

### Verified in this pass
1. 1.1 (records exist since 16 and have private final fields per component); 1.5 (equals and hashCode contract).
2. 2.3 (try-with-resources for resources that hold handles); 3.1 (concurrent map); 3.3 (an unused executor service should be shut down).
3. 4.1 (the Spring team advocates constructor injection); 4.5, 4.7, 4.8 against the pages named above; 5.4 against Surefire.

### Corrected in this pass
1. 1.3: the JDK note says Optional is primarily a return type; it does not forbid parameters or fields, so the ban is now labelled as the book's convention.
2. 4.4: under the Jakarta Persistence API many-to-one defaults to EAGER and LAZY is a hint; the rule is now stated as "declare LAZY explicitly", with the default noted.
3. 4.5, 4.7, 4.8 and 5.4: extended with the ordinal default, the default rollback rule, the pool sizing advice, the milliseconds default and the Surefire patterns.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.2, 1.4, 1.6: Effective Java items and own guidance, no permissive page read.
2. 2.1, 2.2 (checked versus unchecked is a convention; the javadoc only defines the checked category), 3.2, 4.2, 4.3, 4.6, 5.1, 5.2, 5.3: not located on the pages read.
3. Spring Boot 3 specifics: the pages read are from a newer line than the one the block targets; version in the build file decides.
4. Nothing was compiled.

### Tally
Points 24. Sourced 10, corrected 2, still unverified 12.

Independent verification 2026-10-21: 18 checked, 17 matched, 1 corrected, 0 unverified (Optional, hashCode, Enum.ordinal, ExecutorService, Surefire patterns, Spring rollback, participation, requires-new and self-invocation rules, Jakarta Persistence fetch defaults and the lazy hint, Boot duration and record binding; corrected: Jakarta Persistence 3.2 infers the string form of an enum that declares a string value field, the ordinal default holds otherwise). Spring pages read were the current line (Framework 7.0.9), the block targets Boot 3: check the version in the build file.
