# api-change-classification-pitfalls §3 — Disagreements and the verdict

> Part 3 of `skills/api-change-classification-pitfalls`. Read it when a verdict is contested or must be acted
> on. Sources: Google AIP-180 and AIP-185 and the Microsoft Graph guidelines, all CC-BY-4.0, rewritten in our
> own words; points marked own guidance are ours.

## 3.1 Where the two sources disagree, and the reading this block takes
1. **Length or format of an opaque string.** AIP-180 says to treat an expected increase in a string's size as
   incompatible and not to change the set of valid resource names. The Graph guidance lists changing the length
   or format of opaque strings, such as resource identifiers, as non-breaking. **This block takes the stricter
   reading**: a change of length or format of an existing string is breaking. Reason: the AIP rationale is that
   consumers store such values in limited columns and in URLs, and a producer cannot know that nobody does. The
   Graph position is safe only if the contract said from its first release that the value is opaque and made no
   promise on length or format (own guidance on when the relaxation applies).
2. **Pagination.** Graph lists introducing server-side pagination to an existing collection as breaking; AIP
   shows the same mechanism as a trap in its default-behaviour rule but does not list it. Take the Graph
   reading: breaking.
3. **Performance.** Only the Graph guidance lists significant latency, rate-limit or concurrency changes as
   breaking. AIP's semantic rule covers visible behaviour. Take the Graph reading and fix the threshold in the
   contract (see part 2).
4. **Error codes.** Only the Graph guidance names top-level error codes. Take it: breaking.
5. **Where the sources are silent**, classify by the three kinds in part 1 and write the reasoning down. The
   sources both say their lists are indicative.

## 3.2 Stability level decides how much of this applies
1. **The strict rules apply to the stable surface.** AIP-180 refers to a stability level that may say
   otherwise, and AIP-185 separates stable from alpha and beta channels; the Graph guidance allows breaking
   changes on its beta endpoint with consideration of dependencies and customer impact.
2. **A pre-release surface must be labelled as one** before anyone depends on it (own guidance): without the
   label, consumers treat it as stable and the classification above applies to it.

## 3.3 What follows a "breaking" verdict
1. **Avoid it first.** Both sources prefer adding new things beside old ones. Graph's mechanism is a new
   uniquely named element, with the old one marked deprecated; where the original name is still the best, a
   version suffix on the old name can make the new one unique. See part 3 of `api-design` for the extension
   rule itself.
2. **If it cannot be avoided, version it.** AIP-185 requires a major version in the path and says an incompatible
   change follows AIP-180 and the stability-level rules; new major versions must not depend on the previous
   one. Older and newer versions must be usable at once within one client application for a reasonable
   transition, and the old one needs a well-communicated deprecation period before shutdown.
3. **The durations are one organisation's choice.** Graph requires supporting deprecated elements for at least
   36 months, or 24 months with demonstrated non-usage, for its stable surface; AIP-185 recommends 180 days of
   deprecation before removing beta functionality. Treat both as examples of writing a number down, not as
   figures to adopt. The deprecation procedure for your own contract is in `deprecation-migration`.
4. **Record the verdict where consumers read it** (own guidance): a breaking-change note that exists only in the
   pull request reaches nobody who needs it.
