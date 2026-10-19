# dotnet-testcontainers-and-time-seam-pitfalls: origin and source stamps

> Provenance of `skills/dotnet-testcontainers-and-time-seam-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No container was started and no test
was run while writing it. Overlaps with `skills/dotnet-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Testcontainers for .NET (commit 84f485c): `docs/api/best_practices.md`, `resource_reaper.md`, `resource_reuse.md`, `wait_strategies.md`, `docs/test_frameworks/xunit_net.md` | MIT (LICENSE re-read) | Part 1 rules |
| dotnet/skills (commit 6364668): `testability-obstacle` skill | MIT (LICENSE re-read) | Part 2 rules |

## Removed in the verification pass (no page supporting them)
- The Guidelines-style rules 1615 and 1618 (CC BY-SA collection of guidelines): idea-only, never opened; the
  "no production code in assertions" rule is written as own guidance (2.4 point 1).
- A rule that the reaper must never be disabled on any machine: narrowed to the documentation's own exception for
  environments that clean up themselves.

## Not verified
1. **Own guidance, flagged as such in the text:** the literal-expectation rule (2.4 point 1).
2. **The reaper image digest and the private-registry copy procedure** were read but are release-specific; check
   the current page before using them.
3. **Reuse behaviour** is described by the documentation as experimental; the hashed fields listed there may
   have changed.
4. **Fixture scope per assembly** depends on the xUnit.net version and an extension named on the page; not
   checked.
5. **`FakeTimeProvider` and the `PeriodicTimer` overload** availability by target framework is the skill's wording
   ("where the target framework provides it"); not checked against the API documentation.
6. **The skill is written for agent migration tasks**; the numeric details (which operations count as ambient)
   are its own scope choices.

## Related blocks
`testing-anti-patterns`, `dotnet-conventions`, `dotnet-msbuild-and-nuget-publish-pitfalls`.
