# over-engineering-review: origin and source stamps (§2)

> Provenance of section 2 of `skills/over-engineering-review`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule. The provenance of the
> rest of the block stays in the `Origin` section of its `SKILL.md`.

**Status: 🟡.** Written from reading one skill, never run by us: no `debt.md` was written or scanned on a real
feature while writing it.

## Sources (re-read 2026-10-19, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| DietrichGebert/ponytail, `skills/ponytail-debt/SKILL.md` (commit 09c434a), read in full | MIT (repository LICENSE file, "Copyright (c) 2026 DietrichGebert", standard MIT text, read in this session) | The idea of a deferral carrying its ceiling and an upgrade trigger, one ledger row per deferral (where, what was simplified, ceiling, trigger), the `no-trigger` tag on rows that name no upgrade path and its count, the closing count of entries and entries without a trigger, and the report-only boundary |

## Rewrite notes
**Changed on purpose.** The source records a deferral as a marker comment in the code and finds it by searching
comments. Ours moves the record to `specs/<NNN>-<name>/debt.md`, the feature's spec-kit folder, because this
repository writes no comments in code and because the spec folder is where a team already looks. As a result
the scan reads those files and never searches code. Line numbers became names (lines move). Added by us: the
project template wins, the row is written and removed in the change that takes and pays the shortcut, an
invented ceiling or trigger is refused, a crossed ceiling is reported as a finding, and an empty ledger is not
proof of no debt.

**Removed.** The marker word and its alternatives, the version-control search command and its flags, the
owner-per-row blame option, the offer to write the ledger to a file (the file is the record here), and the
tool's name and persona.

## Not verified
The rest of the source repository (other skills, benchmarks, adapters) was not read for this section. Nothing
about how the source behaves at run time was observed.
