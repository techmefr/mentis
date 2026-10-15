# regex-validation-pitfalls §2 — ReDoS

> Section 2 of `skills/regex-validation-pitfalls`. Read it when a pattern runs on text an outsider chooses.
> Restated from the OpenSSF Best Practices Working Group guide and rationale page (commit `8259081`, CC-BY-4.0;
> credit and changes in `references/origin.md`), read 2026-10-16. Engine option names and availability are
> version-bound. Sentences marked "own guidance" are ours.

1. **Backtracking engines can be made very slow.** A regular-expression denial of service exploits the fact that
   most regex implementations can reach extreme cases where matching time grows exponentially with input size.
   Many implementations backtrack, trying all possible matches, so a poorly written pattern gives an attacker a
   cheap way to take a vast amount of time.
2. **Prefer an engine that never backtracks.** The guide's examples: Go's default regexp package (RE2) and, on
   .NET, the `RegexOptions.NonBacktracking` option (introduced in .NET 7). Such engines can be orders of
   magnitude faster and have no catastrophic case, but they omit features such as backreferences, and the .NET
   option cannot be combined with `RightToLeft` or `ECMAScript` options. If a pattern needs a feature the safe
   engine lacks, that is a reason to restructure the check, not to switch engines silently.
3. **Otherwise shape the pattern so it barely backtracks.** At each alternation the next character should choose
   the branch; at each optional repetition it should decide whether to repeat. Repetition inside repetition,
   such as `(a+)*`, is a common cause of needless backtracking. The guide says some tools can find these
   defects; own guidance: run one in CI over every gate regex, and read its report instead of trusting a green
   unit test.
4. **Bound the input and the repetitions.** A partial countermeasure is to limit the length of the untrusted
   input, the number of repetitions, or both: use `{0,4}` (zero to four times) where `*` would allow unlimited
   repetition. Own guidance: check the length before the regex runs, and treat the bound as part of the schema
   the way `security-hardening` §1.8 does for sizes and counts.
5. **On .NET, pass a timeout.** The guide's rationale quotes Microsoft's recommendation to pass a timeout to
   `System.Text.RegularExpressions` when processing untrusted input, noting that ASP.NET Core framework APIs that
   use regular expressions already do. The same timeout idea is covered for that platform in
   `dotnet-async-exception-pitfalls` §3.
6. **The pattern's origin matters as much as its shape.** Own guidance: a pattern that a user, a tenant or a
   configuration file supplies is attacker-controlled and must run only on a non-backtracking engine; a pattern
   inside a dependency counts too, and for Node the runtime-specific symptoms and fixes are in
   `node-async-performance` §3.
7. **A regex inside a sanitiser or validator configuration runs on hostile values.** DOMPurify's option for
   allowed URI patterns carries a note to keep the pattern linear-time for exactly this reason
   (`csp-and-sanitiser-pitfalls` §2.7).
8. **Test with the worst near-miss, not only with valid input.** Own guidance: for each gate regex keep one
   test that feeds a long string that almost matches (the repeated character the pattern loops on, then one
   character that breaks it) at two or three lengths and asserts that the time stays flat. A time that grows
   with length is the finding.
