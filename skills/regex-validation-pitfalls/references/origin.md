# regex-validation-pitfalls: origin and source stamps

> Provenance of `skills/regex-validation-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no regex was executed against any engine except as
the one-line Python illustration in §1.4, whose behaviour is the guide's. Each file below was re-read in full on
2026-10-16 before a rule was taken from it, each rule was checked against it in a final pass, and the
repository's licence files were read again.

## Attribution (CC-BY-4.0 material)
This block restates, in our own words and with changes, "Correctly Using Regular Expressions for Secure Input
Validation" and its rationale page, by the **OpenSSF Best Practices Working Group** (the rationale credits David
A. Wheeler as original author and lead, with Nikita Koselev and Seth Larson as contributors), published at
https://github.com/ossf/wg-best-practices-os-developers under the Creative Commons Attribution 4.0 International
License (https://creativecommons.org/licenses/by/4.0/). Changes: the guide was condensed, reordered and combined
with other material, its table was restated, and examples were replaced by our own. The authors have not endorsed
this block.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| OpenSSF Best Practices WG (`ossf/wg-best-practices-os-developers`, commit `8259081`), `docs/Correctly-Using-Regular-Expressions.md` and `docs/Correctly-Using-Regular-Expressions-Rationale.md` | CC-BY-4.0, stated in the file itself ("This document is released under the Creative Commons CC-BY-4.0 license"), by the README ("documentation is released under the CC-BY-4.0 license") and by `LICENSES/CC-BY-4.0.txt`. The repository has no top-level LICENSE file; software in it is Apache-2.0 and `LICENSES/` also holds an MIT text | Full-match rule, anchors and the per-platform table, permissive `$`, alternation grouping, translation between platforms, the Java conflict, `\A` and `\z` status, tests, ReDoS options (non-backtracking engines, pattern shape, bounds), the .NET timeout recommendation |

Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **"`$` is strict on JavaScript and Go" as a flat statement.** Kept per the guide's table, but Java is stated
   as disputed (§1.3, §1.8) because the guide's two tables and the vendor documentation disagree.
2. **A flat "Python supports `\z`".** The rationale says Python agreed to add it and shows a pull request, but
   also says current Python 3 raises an exception on `\z`; the release that carries it was not found in the file,
   so §1.9 says to verify.
3. **The platform notes for Gnulib, Perl internals, PCRE history and the history section** of the rationale. Read,
   but no rule depends on them.
4. **Statistics beyond the one in §1.6.** The rationale's second study (regex bugs, 46.3%) is not used.
5. **The review's "ReDoS: no nested repetition" as an absolute.** The guide calls repetition in repetition a
   common cause of needless backtracking, not a rule; §2.3 says so.

## Not verified
1. **Own guidance, flagged in the text:** a regex tool in CI (§2.3), checking length before the regex and tying
   it to the schema (§2.4), attacker-controlled patterns only on safe engines (§2.6), the worst-near-miss timing
   test (§2.8), what to use on Python and in JavaScript or POSIX tools (§1.9), the replay in `SKILL.md`, and the
   decision on Java (§1.8), which follows the guide's own conclusion.
2. **Engine behaviour was not tested.** Every anchor and `$` statement is the guide's, with platform versions as
   cited by it (for example Java 8 and 21, Perl 5.38.2, Ruby 3.3.0, .NET 7 for the non-backtracking option).
3. **Date of the POSIX change.** The rationale gives April 2024 in one place and 2025 in another; §1.9 reports
   both and relies on neither.
4. **The linked external pages** (language documentation, CWE-625, the cited studies and blog post) were not
   opened.

## Decisions where sources disagree
Java `$`: the guide's own tests and the Java 8 documentation say it is not permissive; one vendor documentation
page and the guide's survey table say it is. Decision: use `\z` (§1.8).

## Related blocks
`skills/security-hardening`, `skills/csp-and-sanitiser-pitfalls`, `skills/node-async-performance`,
`skills/dotnet-async-exception-pitfalls`.
