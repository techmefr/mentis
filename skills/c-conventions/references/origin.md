# c-conventions — origin and source stamps

> Provenance of `skills/c-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡, base to be confronted with a real C project.** No production C experience in house stands behind
this block. Sources were read on **2026-10-02**; rules are rewritten from the mechanism, no text is copied.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| SEI CERT C Coding Standard, rules list (public site of a university software-engineering institute) | list of 122 rules read on 2026-10-02; the standard's own edition is not pinned in the list page | copyright of the institute; no open licence found | the *rule statements* (one line each) for expressions, integers, floating point, arrays, strings, memory, I/O, environment, errors, concurrency, signals, preprocessor, POSIX. Bracketed identifiers in the references are for tracing. | **idea only**: the mechanisms were rewritten; rule bodies and code examples were not read, so a "why" that goes beyond the one-line statement is the author's reasoning from the language rules and is marked as such in the text where it matters |
| Compiler Options Hardening Guide for C and C++, and Compiler Annotations for C and C++ (a security foundation's best-practices group) | guide dated 2026-08-20, annotations dated 2026-06-30, repository commit `4e2b1e0` of 2026-10-01 | CC BY 4.0 (stated in each file) | the recommended flag set and its reasons, the staged adoption approach, sanitizer coverage and limits, debug-information handling, and the attribute catalogue | rewritten with this credit; **volatile**, re-check the guide before applying a flag |
| A style guide for a large C++ code base (header, macro and include rules) | commit `fc98150` of 2026-10-01 | CC BY 3.0 | self-contained headers, guard naming, include-what-you-use, macro restrictions | rewritten with this credit (headers and macros only; the C++-specific rules live in `cpp-conventions`) |
| A kernel coding-style document, section on centralised function exit | fetched 2026-10-02 | GPL-2.0 documentation | the idea of one labelled cleanup path named after what it frees, labels in reverse order of acquisition, and the one-error-bug when a label frees something not yet acquired | **idea only**: wording is the author's |
| The C++ core guidelines (header and global-variable rules) | commit `33bcd01` of 2026-08-06 | a licence that allows copying and derivatives for **personal or internal business use only**, not an open licence; the veille had recorded it as MIT, which is wrong | the rule titles on headers, source-file cycles and globals | **idea only**: no phrasing reused, which is also why those points carry no quotation |

**What was left out, and why.**
- MISRA C (paid, proprietary), the compiler vendors' own manuals, `clang-tidy` and `cppcheck` rule sets, and
  the static analysers' checkers: not read in this pass, so no rule is attributed to them. Naming them as
  tools in §5 is the extent of it.
- Test frameworks for C (mocking and unit libraries): no primary source read, so the block says what a test
  run must include (sanitizers, fuzzing, failure injection) and not which library to use.
- The C standard itself: the block cites the standard's *behaviours* (undefined, unspecified) the way the
  secure-coding list states them; it does not quote the standard.
- Windows-specific rules (WIN30 is cited once for allocation pairing) and the embedded safety standards:
  outside the first scope; a later pass may add a section.

**Volatile content to re-check at the next pass:** every flag name and the minimal compiler version in §5,
which follows the guide's table; the sanitizer compatibility matrix in §5.9; the attribute availability in
§5.10 (several are very recent in one compiler).

**Crossings with other blocks.** `cpp-conventions` cites §5 as its hardening section and §6 for the shared
header rules. `security-hardening` is the general injection and secret doctrine; this block points at it from
its own §3.8 and its own §1.12. `rust-conventions` §3 covers the same ground from the memory-safe side.
