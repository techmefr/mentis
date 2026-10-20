# deno-bun-runtime-pitfalls: origin and source stamps

> Provenance of `skills/deno-bun-runtime-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge. Never dogfooded; no Deno or Bun program was run while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None opened. The review found no creditable source for this gap | n/a | Nothing taken |

## Removed
- Flag spellings, command names, configuration keys, compatibility percentages, benchmark numbers and version numbers: not carried, on purpose.
- Framework-specific advice (web frameworks, ORMs) and the serverless platforms that host these runtimes: not covered.

## Not verified
1. **Every runtime behaviour** (permission scopes, default install-script handling, lockfile format and enforcement, native-addon support, shutdown behaviour) is general knowledge and was not checked against current documentation or run. Both runtimes release often: re-read before relying.
2. **Compatibility level of any specific library** is not claimed.
3. **Bun's missing permission model** is stated as of the author's knowledge; re-read in case it changed.

## Related blocks
`node-container-runtime`, `package-manager-supply-chain-pitfalls`, `monorepo-task-graph-and-cache-pitfalls`, `load-and-capacity-testing-pitfalls`, `source-freshness`.
