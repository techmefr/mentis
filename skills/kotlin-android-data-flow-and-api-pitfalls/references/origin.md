# kotlin-android-data-flow-and-api-pitfalls: origin and source stamps

> Provenance of `skills/kotlin-android-data-flow-and-api-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading, never run by us. No Android project was built and no Kotlin was compiled
while writing it. This block is meant to be folded into the Kotlin language block when the extended language
blocks (the unmerged PR 118 branch) land; until then it stands alone and cites only blocks that exist on the
main branch.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Now in Android (commit a49ed25): `docs/ArchitectureLearningJourney.md`, `AGENTS.md` | Apache-2.0 (LICENSE re-read) | Part 1 rules |
| chrisbanes/skills (commit f8703a3): `skills/kotlin-api-design/SKILL.md` and its `functions.md`, `value-classes.md`, `multiplatform-boundaries.md` | Apache-2.0 (LICENSE re-read) | Part 2 rules |

## Removed in the verification pass (no page supporting them)
- "No Context in a view model", "navigation arguments are ids not objects", "one immutable UI state object per
  screen" and "a view model survives rotation": not in the files read (the guide has sealed state per feed, not a
  single object per screen); dropped.
- "Explicit API mode for libraries", "no default arguments across public binary API" and "extension functions
  for local convenience": the library-release skill of the same repository was not read; the extension rule
  here comes from the function-ownership reference instead.
- The architecture-samples repository (licence only): not read.
- The other nowinandroid documents (modularization journey, design file): not read.

## Not verified
1. **Own guidance:** none flagged; every point traces to a file above.
2. **The Now in Android guide is one reference app's design**, written by its maintainers, and says itself it
   differs from other architectures; its state flow, work scheduler and storage choices are not rules for every
   app.
3. **Kotlin language facts in part 2** (value class equality, boxing, serialisation encoding, extension
   precedence) are the skill's statements; no Kotlin documentation was read.
4. **The control-flow, Compose performance, state and component skills** the references link to were not read.
5. **Library names in the agent guide's test notes** are the project's choices; versions were not read.

## Related blocks
`android-edge-to-edge-insets`, `android-security-hardening`, `android-agp9-r8-gradle`.
