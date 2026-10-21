# quality-bar-and-ratchets-pitfalls: origin and source stamps

> Provenance of `skills/quality-bar-and-ratchets-pitfalls`. Read it to trace a rule to its source, never to apply one.

**Status: 🟡 never dogfooded.** Written from a reading of a skill and a reference; no guard was run, no bar file
was written on a real project, no command named in the text was executed.

## Sources (read 2026-10-20 and 2026-10-21, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| addyosmani/agent-skills at commit aeac41d (2026-10-13): `skills/constraint-driven-development/SKILL.md` and `references/floor-guard.md` | MIT, Copyright (c) 2025 Addy Osmani (root `LICENSE` read 2026-10-21; no per-folder licence) | The written bar with a reason and a command per number, the floor, external versus project versus suite checks, placement by cost, ratchets, exceptions with owner and expiry, the five diff moves, directional threshold comparison, exit states |

## Removed (in the source, not carried)
- Every default number: coverage on changed lines, mutation score, vulnerability level, web performance figures, exception lifetime, ratchet tolerance, the task-end time budget. Unsourced there; ours state a reason or a ratchet.
- The Node reference script and its tool install table: a runtime dependency on named tools; the contract is kept, the code is not.
- Slash-command wiring and host-specific hook examples.

## Not verified
1. The source's claims about how often agents loosen checks and about training incentives are its author's reading.
2. The guard contract was written from reading a script, not from running one; edge cases (renamed files, mode changes) are untested.
3. Overlap with `guard-test-changes` and `config-protection` was judged from their descriptions and the hooks list, not by running them.
4. Re-read before relying: any tool, flag or licence named in a section.

## Related blocks
`gate`, `architecture-fitness-functions-pitfalls`, `python-testing-strictness`, `agent-hook-guard-pitfalls`, `source-freshness`.
