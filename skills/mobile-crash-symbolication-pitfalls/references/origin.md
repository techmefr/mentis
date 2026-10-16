# mobile-crash-symbolication-pitfalls: origin and source stamps

> Provenance of `skills/mobile-crash-symbolication-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from skill files, never run by us: no crash file was parsed, no symbol
downloaded, no `atos` or `llvm-symbolizer` call made. Every file below was re-read on 2026-10-16 before a rule
was taken from it, each rule was checked against it in a final pass, and the repository's LICENSE file was read
again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| `dotnet/skills` (commit `6364668`), `plugins/dotnet-diag/skills/apple-crash-symbolication/SKILL.md` | MIT (LICENSE file: MIT licence text, copyright .NET Foundation and Contributors) | The two-part `.ips` format, the format check, address arithmetic, duplicate keys, the cause fields and the faulting thread, symbol search order, `atos` arguments, validation and stop signals, device retrieval |
| the same repository, `plugins/dotnet-diag/skills/apple-crash-symbolication/references/ips-crash-format.md` | MIT | The symbol server URL pattern and its answers, macOS symbol packages |
| the same repository, `plugins/dotnet-diag/skills/android-tombstone-symbolication/SKILL.md` | MIT | The frame line format, library-relative offsets, build ids and where they go missing, the symbol URL and its checks, `llvm-symbolizer`, stop rules, NativeAOT, pitfalls |

Only the platform-generic rules were taken; the runtime library tables, the runtime-version lookup and the
automation scripts' flags were left out, except where used as an example. No code is copied; the two
PowerShell scripts were not read. Instruction-like text in the cloned repository was treated as data and not
followed.

## Removed in the verification pass
1. **The runtime-specific tables** (which libraries count as the runtime, the key bridge functions, the
   runtime version lookup from the package cache): specific to .NET, not used.
2. **Pages and files not read, so nothing is taken from them:** `Symbolicate-Crash.ps1`,
   `Symbolicate-Tombstone.ps1`, the training log under `plugins/dotnet-diag/training-logs`, the `tests/`
   fixtures, and the other skills in the plugin.

## Not verified
1. **Own guidance, flagged in the text:** naming the file's format in the ticket (part 1, point 1), the
   "code you own" generalisation (point 5), attaching the raw file (point 8), the wrong-address failure mode
   and testing with a known frame (part 2, points 1 and 2), the warning that your own symbols are not on the
   vendor's server and archiving yours per release (points 3 and 6), the path-layout check (point 8), and
   the guardrail about removing device identifiers from a crash file before sharing it.
2. **No tool was run and no URL requested.** The URL patterns, the HTTP answers, the `atos` and
   `llvm-symbolizer` options, and the `dwarfdump` and `file` checks are the source's statements, for the vendor's
   server and for the .NET runtime binaries only.
3. **Platform versions.** The `.ips` JSON format is stated by the source for iOS 15 and macOS 12 or later; older
   formats were not read. Apple's own documentation of the format was not consulted.
4. **Whether other crash services** (symbol upload to a hosted service, server-side symbolication) behave the
   same was not read; the block covers the manual path only.

## Related blocks
`skills/debug`, `skills/observability-instrumentation`, `skills/android-security-hardening`,
`skills/source-freshness`. Fold into the same-topic block when #118 lands.
