# cli-tool-design-pitfalls: origin and source stamps

> Provenance of `skills/cli-tool-design-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of command-line tool design, never run: no tool was built or
tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| none | not applicable | Own guidance only. The review file listed a published command-line design guide and the awesome-copilot repository (MIT by the API); neither was opened: the guide's licence was not checked and clean room applies, and the repository was not needed for a stack-neutral topic |

## Removed
- Nothing was copied or paraphrased from a source; there is nothing to remove.

## Not verified
1. **Everything.** The points are conventions in common use (the separate output streams, exit-code semantics, no-colour handling, secrets in process lists); none was checked against a specification or a guide in this pass.
2. **Environment-variable and directory conventions** differ by platform and by tool ecosystem; re-read the platform's rules before fixing names.
3. **Publication.** A later pass may credit a creditable guide (CC BY or similar) once its licence file is read; until then the block claims no source.
4. **No command, flag or code was executed.**

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for internal build scripts, a swallowed environment error reported as success (§1.2.6), a path relative to the working directory and a missing prerequisite (§1.1.6), an unknown flag falling through to write mode (§2.1.8), the dry-run rule exempted for regenerated directories (§2.4.6), and the deprecation rule scoped to published interfaces. The status stays 🟡.

## Related blocks
`shell-scripting-conventions`, `bash-pitfalls-and-bats`, `mcp-server-design-pitfalls`, `api-design`,
`deprecation-migration`, `credential-lifecycle-pitfalls`.
