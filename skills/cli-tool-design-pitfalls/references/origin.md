# cli-tool-design-pitfalls: origin and source stamps

> Provenance of `skills/cli-tool-design-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of command-line tool design, never run: no tool was built or
tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| no-color.org convention page | web page, facts only, nothing copied | Trigger is a non-empty variable, scope is tools that colour by default, flag and config override it (§1.4.2, §1.4.6) |
| freedesktop base-directory specification | specification, facts only, nothing copied | Four variable names, defaults, absolute-path requirement (§2.2.4) |
| cli-guidelines/cli-guidelines (published command-line guide) | CC BY-SA 4.0 (`LICENSE` read 2026-10-20) | Not opened: share-alike |

## Removed
- Nothing from the guide. The two convention pages were rewritten, no sentence copied.

## Not verified
1. **Everything except the colour variable and the base-directory defaults.** Streams, exit-code semantics, secrets in process lists, prompts and the rest are conventions in common use, still unsourced.
2. **Directory conventions** other than Linux's (macOS, Windows) were not read; re-read the platform's rules before fixing names.
3. **Guide.** No permissive command-line design guide found, searched: the guide's repository (CC BY-SA), convention pages.
4. **No command, flag or code was executed.**

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for internal build scripts, a swallowed environment error reported as success (§1.2.6), a path relative to the working directory and a missing prerequisite (§1.1.6), an unknown flag falling through to write mode (§2.1.8), the dry-run rule exempted for regenerated directories (§2.4.6), and the deprecation rule scoped to published interfaces. The status stays 🟡.

## Related blocks
`shell-scripting-conventions`, `bash-pitfalls-and-bats`, `mcp-server-design-pitfalls`, `api-design`,
`deprecation-migration`, `credential-lifecycle-pitfalls`.
