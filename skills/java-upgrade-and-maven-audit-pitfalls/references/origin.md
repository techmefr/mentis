# java-upgrade-and-maven-audit-pitfalls: origin and source stamps

> Provenance of `skills/java-upgrade-and-maven-audit-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading, never run by us. No build, upgrade or audit was run while writing it. Overlaps with `skills/java-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| claude-code-java (commit 0d98fe9): `skills/java-migration/SKILL.md` | MIT (LICENSE re-read) | Part 1 rules |
| claude-code-java: `skills/maven-dependency-audit/SKILL.md` | MIT | Part 2 rules |

## Removed in the verification pass (no page supporting them)
- "Fix deprecation warnings first", "run the full suite on the new JDK in CI before switching production" and
  "replace removed APIs in a single commit": none is stated in the skill; the CI point is kept once as flagged
  own guidance (1.6), the other two dropped.
- "No version ranges", "dependency convergence enforced" and "exclude transitive logging implementations to keep a
  single binding": not in the audit skill (it has a single exclusion example for a legacy logging artifact);
  the exclusion rule is written from that example only.
- The OpenRewrite Spring recipes (reported by the review as Moderne Source Available, not checked here):
  idea-only; mentioned as a tool the user may install, never copied.
- The REST API guideline extras, architecture review checklist and Java code review checklist (other skills of
  the same repository): not read for this block, listed as not done.

## Not verified
1. **Own guidance, flagged as such in the text:** the CI run on the target JDK (1.6).
2. **JDK release facts** (removed modules, the 25 changes, the encoding default, the compatibility table) are the
   skill's statements; no JDK release note was read, and the table is a snapshot that ages.
3. **Severity bands and timings** are the skill's own policy, not a standard.
4. **The scan plug-in, the versions plug-in and the analysis plug-in goal names** were not checked against the
   plug-ins' current documentation.
5. **Gradle**: the skill shows only one toolchain snippet; Gradle dependency auditing is not covered.
6. **Spring Boot 4**: the skill mentions a 3 to 4 path in its trigger text but gives no rules; not covered.

## Related blocks
`java-conventions`, `deprecation-migration`, `ci-workflow-hardening`.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The JDK enhancement proposal pages named below, the Maven dependency mechanism guide and plugin goal pages, the Versions plugin goal pages, the dependency-check Maven usage page and the scoring specification were re-opened. The JEP pages carry an Oracle copyright with no open licence stated on the page; they are official release documents and were used for facts only, in own words. No JDK release note or compatibility table was read for the claims left unverified.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| JEP 320 (remove Java EE and CORBA modules), JEP 403 (strong encapsulation), JEP 400 (UTF-8 by default), JEP 421 (deprecate finalization), JEP 451 (prepare to disallow dynamic agent loading), JEP 471 (deprecate Unsafe memory access), JEP 486 (permanently disable the security manager), JEP 503 (remove 32-bit x86 port) | openjdk.org pages, copyright holder Oracle, no open licence stated; facts only | release numbers and exact effect of each change |
| Apache Maven: introduction to the dependency mechanism; dependency plugin tree and analyze goal pages | Apache-2.0 (Maven LICENSE read 2026-10-20) | nearest-definition mediation, dependency management, exclusions, includes filter, used-undeclared and unused-declared analysis |
| Versions Maven plugin 2.23.0: display-dependency-updates, display-plugin-updates, use-latest-releases, commit, revert | Apache-2.0 (LICENSE.txt of the mojohaus/versions repository read 2026-10-20) | update reports for dependencies and plugins, replacement by latest releases, backup commit and revert |
| OWASP dependency-check Maven plugin usage page | Apache-2.0 (LICENSE.txt read 2026-10-20) | HTML report from a check goal, bound to the verify phase, first run downloads the vulnerability database |
| FIRST Common Vulnerability Scoring System 3.1 specification | FIRST licenses it freely for public use with conditions (stated on the page) | qualitative rating bands |

### Verified in this pass
1. 1.2 item 1 (JEP 320), item 2 (JEP 403 and the opening flag), item 3 (JEPs 421 and 400); 1.4 item 1 (opening flag) and item 3 (the 17 symptom is an inaccessible-object exception).
2. 2.1 item 3 (plugin updates report); 2.2 item 2 (bands); 2.3 items 2 and 3 (includes filter; analyze categories); 2.4 items 1, 2 and 3 (dependency management, exclusion, latest-releases with commit and revert).

### Corrected in this pass
1. 1.2 item 4: the security manager is disabled but its API is retained; the Unsafe memory-access methods are deprecated for removal, not removed; only the 32-bit x86 port is removed; dynamic agent loading only warns from 21. Text rewritten with release numbers.
2. 2.3 item 1: Maven picks the nearest definition, not the newest; added, since "omitted for conflict" can hide a fixed version.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.1 (the long-term-support path 8, 11, 17, 21, 25) and the compatibility table: no release roadmap page read.
2. 1.2 item 2 (preview features changing syntax), 1.3, 1.4 item 2, 1.5 (Spring Boot 3 needs Java 17 and Jakarta EE 9; the current Boot reference source gives Java 17 as the floor but says nothing on Jakarta), 1.6: not located on a permissive page.
3. 2.1 items 1 and 2, 2.2 item 1 and 3 (the second scan option), 2.5: the skill's own process.
4. "omitted for conflict" and "omitted for duplicate" labels: the tree goal page read documents the verbose option only, not the labels.
5. Nothing was run.

### Tally
Points 30. Sourced 12, corrected 2, still unverified 16.
