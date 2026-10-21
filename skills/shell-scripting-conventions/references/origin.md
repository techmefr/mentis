# shell-scripting-conventions: origin and source stamps

> Provenance of `skills/shell-scripting-conventions`. Read it when a rule has to be traced to its source,
> never to apply a rule.

**Status: 🟡.** Nothing here was run in this pass.

## Sources (read 2026-10-20, own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| GNU Bash Reference Manual: The Set Builtin, Pipelines, Bash Builtins (`command`, `local`) | GNU documentation licence, not re-read; facts only | `-e` ignored contexts (§1.2), `-u` exclusions, `pipefail`, `command -v` status, `local` return status (§1.3) |
| git `Documentation/git-update-index` (raw source) and `COPYING` | GPL-2.0 (`COPYING` read); facts only | `--chmod=(+|-)x` (§3.3) |

The Bash manual host was unreachable for the Shopt and Shell Scripts pages (connection refused on 2026-10-21).

## Second pass
Sourced: `-e` contexts, `pipefail`, `-u` exclusions, `local` masking, `command -v`, `--chmod`. Corrected: the
vague "command substitution in some positions" was replaced by the listed contexts and `local`; command
substitution itself was not confirmed. Unsourced: CRLF in shebangs (§3.2), `sh` versus bash portability
(§3.1), shellcheck coverage (§4.1), the 50-line threshold, the fail-closed posture (our own experience).
Not verified: `inherit_errexit`, how the shell executes a script without a shebang.
