# architecture-fitness-functions-pitfalls: origin and source stamps

> Provenance of `skills/architecture-fitness-functions-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one tool's documentation and own craft knowledge, never run on a
real codebase by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TNG/ArchUnit, docs/userguide: Getting Started, What to Check, Ideas and Concepts, The Lang API, The Library API, JUnit Support (LICENSE file read: Apache License 2.0) | Apache-2.0 | Kinds of checks (package, class, containment, inheritance, annotation); ready-made layered, onion, slices and module rules and general coding rules; rule descriptions in failure messages; importing a chosen set with options; freezing existing violations with a store and its creation, update and refreeze settings; ignore patterns matched on messages; architecture metrics |

Credit as the licence requires: ArchUnit, TNG Technology Consulting GmbH, Apache License 2.0
(https://github.com/TNG/ArchUnit). The text was rewritten, not reproduced; no endorsement by the authors is
implied.

## Removed
1. **All code samples, class and method names beyond the few that anchor a fact** (the freeze wrapper, the
   ignore-patterns file): they are the tool's API, not the method, and may change.
2. **The named metric authors and the formulas**: read the tool's documentation for the definition.
3. **Property names and default values** except where the point is a behaviour (a store may be forbidden from
   being created or updated, refreezing exists).
4. **The evolutionary-architecture book and its definition** were not read; the term "fitness function" is used
   from general knowledge only.

## Not verified
1. §1 points 1, 2, 5 to 7 and 9, §2 points 2 to 4, 6 to 8, and §3 points 1 to 3, 5 to 9 are own guidance (or own
   extensions of a documented behaviour) and are marked in the text.
2. Empty selection: the current guide (read 2026-10-20) says the tool fails by default, with a global and a per-rule override; the version that introduced it is not stated, so test it on a pinned older version.
3. The matching behaviour for frozen violations was re-read 2026-10-20 (line numbers ignored by default; store creation off and update on by default; refreeze off by default) and matches the block; the effect of caching was taken as stated and not run.
4. The ArchUnit documentation was read at the repository's default branch on 2026-10-20; a project's pinned
   version may differ.
5. No tool was installed or run in writing this block.

## Related blocks
`skills/php-architecture-test-pitfalls`, `skills/no-catch-all-layer`, `skills/archi`, `skills/documentation-adr`,
`skills/safe-refactor`, `skills/slo-design`, `skills/load-and-capacity-testing-pitfalls`, `skills/source-freshness`.
