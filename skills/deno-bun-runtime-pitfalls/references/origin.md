# deno-bun-runtime-pitfalls: origin and source stamps

> Provenance of `skills/deno-bun-runtime-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the claims checked against the Deno and Bun documentation on 2026-10-20. Never dogfooded; no Deno or Bun program was run while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Deno documentation: security and permissions, modules, Node and npm compatibility | MIT (`LICENSE` of the documentation repository read 2026-10-20); rewritten, nothing copied | Deny-by-default and scoping (§1.1), subprocess and native-library caveats (§1.1.4, §2.2.3), shared privilege (§1.1.3), pinned specifiers (§1.3.1), install scripts (§1.2.2), Node-API addons (§2.2.1) |
| Deno documentation (re-read 2026-10-20): `runtime/fundamentals/security.md`, `modules.md`, `node.md`, `configuration.md`, `runtime/reference/cli/compile.md`; the hosted supply-chain page | MIT, Copyright The Deno authors 2018-2024 (`LICENSE` of the docs repository read 2026-10-20) | Permission facts, prompts, revoke, versioned specifiers, scripts allow-list, Node-API, compile flags baked in, frozen lockfile advice |
| Bun documentation: lifecycle scripts, lockfile, Node compatibility | MIT for the Bun repository (`LICENSE.md` read 2026-10-20; the runtime statically links JavaScriptCore under LGPL-2 and other libraries under their own licences, the documentation text is not one of them); rewritten, nothing copied | Trusted-dependencies rule (§1.2.2), text lockfile and migration (§1.3.4), per-module compatibility states (§2.1.1) |

## Removed
- Flag spellings, command names, configuration keys, compatibility percentages, benchmark numbers and version numbers: not carried, on purpose.
- Framework-specific advice (web frameworks, ORMs) and the serverless platforms that host these runtimes: not covered.

## Not verified
1. **Checked:** Deno permission defaults, scoping, subprocess and native-library caveats, shared privilege; Bun and Deno install-script handling; Bun lockfile format and frozen mode; Deno versioned specifiers and import mapping; compatibility is partial per module on both; Deno Node-API addon support. **Also checked 2026-10-20:** Deno lockfile default, frozen option and disabling in the project file; Bun Node-API support (most addons, no limitations listed on the page); Deno frozen flag and CI recommendation; Bun frozen-install behaviour and that it is not on by default in CI; Bun default trusted list replacement rule; Bun per-module compatibility states with named stubs; Deno compile bakes in flags. **Corrected:** Bun's frozen install fails only when manifest and lockfile disagree on a package. **Unverified:** the Deno permission audit output (not on the security page), module-resolution differences, built-in tooling semantics, bundler and compile behaviour, benchmarks, shutdown and signal behaviour, container practice, support paths. Both runtimes release often: re-read before relying.
2. **Compatibility level of any specific library** is not claimed.
3. **Bun's missing permission model** is still the author's knowledge: none of the Bun pages read states it (the Node compatibility page read again 2026-10-20 does not mention permissions or signals); re-read in case it changed.

## Related blocks
`node-container-runtime`, `package-manager-supply-chain-pitfalls`, `monorepo-task-graph-and-cache-pitfalls`, `load-and-capacity-testing-pitfalls`, `source-freshness`.

Independent verification 2026-10-21: 33 checked, 33 matched, 0 corrected, 0 unverified
