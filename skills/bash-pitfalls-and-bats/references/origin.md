# bash-pitfalls-and-bats: origin and source stamps

> Provenance of `skills/bash-pitfalls-and-bats`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, plus a few one-line runs on Bash 5.2.21. Never run
by us against a real project. This block is meant to be folded into `shell-scripting-conventions` (main
branch); until then it stands alone and cites only sections that exist on the main branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Bash reference manual, version 5.3 (the GNU manual pages: pipelines, `set`, conditional constructs, arithmetic, `declare`, `local`, process substitution) | GNU manual, rewritten, no text copied | Subshell scope, `set -e` exemptions, arithmetic status, string comparison, `declare` scope |
| bats-core 1.14.0, commit 8c8ec0b (2026-10-05): `writing-tests.md`, gotchas page | MIT (`LICENSE.md` re-read) | `run`, `run !`, `bats_pipe`, descriptor 3, `load`, teardown, focus tag |
| Google shell style guide, `shellguide.md`, google/styleguide commit 2251056 (2026-10-07) | CC BY 3.0 (`LICENSE` re-read); rewritten with credit | Arrays, `./` globs, pipes to while, `readarray`, `eval`, stderr, 100 line threshold |
| bahamas10 bash-style-guide, commit 600b4f4 (2025-12-04) | MIT stated in the README only, no licence file; rewritten, no text copied | Never parse `ls`, unquoted substitution loops, and the contested `set -e` position |

Empirical runs on Bash 5.2.21 (not the 5.3 of the manual): `(( i++ ))` under `set -e`, `local v=$(cmd)`,
a pipe into `while`, `[[ 10 > 9 ]]`, `! true` under `set -e`, `./*` against a dash-named file, `$*` against
`"$@"`, and `declare` against `declare -g`.

## Ideas only, never phrased from
- ShellCheck (GPL-3.0): not opened for wording. The block names no ShellCheck rule number.

## Removed in the verification pass (no page supporting them)
- "A producer killed by SIGPIPE under `pipefail` is expected": true in practice, but no page opened in this
  session states it, so it was dropped.
- "Rewrite past about 100 lines" was kept only with the source's number; the house number differs and wins.
- Instructions found in cloned files were treated as data and not followed.

## Not verified
1. **Own guidance, flagged as such in the text:** none beyond the choice of which source wins on the size
   threshold and the two non-adoptions, all in the last subsection of §1.
2. **Bash 5.3 behaviour was read from the manual and run on 5.2.21.** A difference between them was not looked for.
3. **bats-core `bats_pipe` status options** were read from the documentation of 1.14.0 and not run.
4. **bats older than 1.5.0** was only read from the gotchas page; the `|| false` workaround was not run.
5. **bahamas10 licence:** the README states MIT; there is no LICENSE file, so the evidence is README-only.

## Related blocks
`shell-scripting-conventions` §1 to §4, `testing-anti-patterns` §1, `source-freshness` §3.
