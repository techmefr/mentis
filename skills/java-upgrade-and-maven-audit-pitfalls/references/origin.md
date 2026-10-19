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
