# dotnet-msbuild-and-nuget-publish-pitfalls: origin and source stamps

> Provenance of `skills/dotnet-msbuild-and-nuget-publish-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading, never run by us. Nothing was built, packed or published while writing it.
This block is meant to be folded into the same-topic .NET block when the extended language blocks (the unmerged
PR 118 branch) land; until then it stands alone and cites only blocks that exist on the main branch.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| dotnet/skills (commit 6364668): `msbuild-antipatterns` skill and its references (entries 01 to 23, PrivateAssets list, quick-reference checklist) | MIT (LICENSE re-read) | Part 1 and part 2 rules |
| dotnet/skills: `dotnet-aot-compat` skill (critical rules and checklist) | MIT | IL warning rules |
| dotnet/skills: `nuget-trusted-publishing` skill and `publish-workflow.md` template | MIT | Trusted publishing rules and troubleshooting |
| dotnet/skills: `convert-to-cpm` skill (description and mode section only) | MIT | Only the fact that Central Package Management is the fix for version drift |

## Removed in the verification pass (no page supporting them)
- Pinning the SDK with `global.json` and a roll-forward policy, committing lock files, `.slnx` for new
  solutions, keeping the NuGet audit on, deterministic CI builds and flagging `NoWarn` or
  `TreatWarningsAsErrors=false` as slop: the review attributed them to a hygiene repository that could not be
  cloned (not found) and to files of the dotnet/skills repository that were not read for these rules. Not
  written.
- "Suppressions at the narrowest scope with a written justification": not found in the files read; the one
  suppression rule read is the IL one, which says never.
- The API shape extras (exception handler logging, no Swashbuckle, validation on a later release, enums as
  strings): not in the files read for this block.

## Not verified
1. **Own guidance, flagged as such in the text:** the evaluation-based check for a duplicate instance (part 2),
   the review ordering (part 1).
2. **The catalogue is one team's guidance**, written for agent use; facts about MSBuild behaviour (instance
   identity, evaluation order, path normalisation) were not re-checked against the MSBuild documentation.
3. **The Central Package Management conversion procedure** was not read beyond its description.
4. **The skill that compares evaluations for a clash** was not read.
5. **The nuget.org policy fields and the one-hour and seven-day figures** are the skill's statements, not checked
   against the nuget.org documentation page it links.
6. **Trusted publishing for hosts other than GitHub Actions** is not covered by the source.
7. **The AOT skill's procedure beyond the critical rules** (polyfills, per-feature recipes) was not read.

## Related blocks
`dotnet-conventions`, `ci-workflow-hardening`, `dotnet-testcontainers-and-time-seam-pitfalls`.
