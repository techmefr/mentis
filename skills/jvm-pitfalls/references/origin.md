# jvm-pitfalls: origin and source stamps

> Provenance of `skills/jvm-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real Java project by us. No build was
run and no check was enabled while writing it.

**Fold-in note.** This block is meant to be folded into `java-conventions` (new references or an extended
Steps 1 and 3) when PR 118 lands and the Java blocks are consolidated. It is standalone only so that it does
not depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Error Prone bug-pattern pages, one per check (repository docs folder at the head of the main branch) | Apache-2.0 (COPYING read) | §1.1 to §1.3, §2.1, §2.2, §2.3: the behaviour each check describes and the fix it recommends |
| The NullAway README | MIT (LICENSE.txt read) | §3: non-null default, severity, annotated-package options, requirements, generated code, Android note |
| One MIT Java agent-skill repository, its concurrency-review skill | MIT (LICENSE read) | §2.3 point 1: handle the failure of a `CompletableFuture` with `exceptionally` or `handle` |

The Error Prone pages carry no version number; they were read from a shallow clone of the main branch.

## Rewrite notes
Each point names the check so that the build can enforce it; the prose is ours. The `compareTo` advice in
§1.1.1 and the "loop until the join succeeds" reading of `ThreadJoinLoop` in §2.2.3 go slightly beyond the
page text and are stated as such.

## Not verified
1. **Error Prone default severities** per check were not read; the pages describe the problem, not whether
   a check is an error or a warning by default. §1.4 and §2.4 say to set them to error explicitly.
2. **Version applicability.** The pages do not state the Java version a check needs; `java.time` (Java 8),
   `try-with-resources` and `addSuppressed` (Java 7) and the deprecation of `Class.newInstance` (Java 9)
   come from the pages' own mentions. Nothing here was run on a JDK.
3. **`BigDecimal.compareTo` ignoring scale** is from the JDK API, not from a page read here.
4. **NullAway requirements** (JDK 17, Error Prone 2.36.0) are from the README as of the date above and move
   with releases. The NullAway wiki (configuration, JSpecify mode) was not read.
5. **Dropped from the source list:** "ThreadLocal removed after use", "never lock on a string or `this`",
   "ThreadLocal in a static field only" beyond the static rule, and a Kotlin platform-type rule. None of
   them is stated on a page read, so none is written.
6. **Written by us, not sourced:** the checks lists in §1.4, §2.4 and §3.3, and the rule that the annotated
   set only grows.

## Related blocks
`java-conventions` (the general Java style this block extends), `testing-anti-patterns` (timing guesses in
concurrency tests), `security-hardening`.
