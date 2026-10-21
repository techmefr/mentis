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

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Read again on 2026-10-20: the OpenSSF compiler hardening guide (dated 2026-08-20) and annotations guide, the Clang sanitizer pages (undefined behaviour, address, thread, memory, leak), and the style guide for headers and macros. The standard secure-coding list used for sections 1 to 4 is not under an open licence and was not re-read; its rule identifiers stay as tracing marks only. Nothing was compiled or run.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| OpenSSF Compiler Options Hardening Guide for C and C++ (2026-08-20), main branch | CC BY 4.0 (licence line at the foot of the file; CC-BY-4.0 text present in the repository LICENSES folder), read 2026-10-20 | recommended flag table, staged rollout, warnings as errors in two forms, fortification level and prerequisites, strict flexible arrays, stack protector, control flow and zeroed registers, production semantics, relro, rpath, sanitizer limits, separate debug information |
| OpenSSF Compiler Annotations for C and C++ | CC BY 4.0 (licence line at the foot of the file), read 2026-10-20 | attribute list and versions (malloc with deallocator, alloc_size, access, fd_arg, noreturn, tainted_args, counted_by), double-bracket syntax and its placement rule |
| Clang undefined behaviour sanitizer documentation | Apache-2.0 with LLVM exceptions (llvm/LICENSE.TXT read 2026-10-20) | check list: signed overflow including INT_MIN divided by -1, shift ranges, divide by zero, null, alignment, vla-bound; the undefined group omits unsigned overflow and implicit conversions; minimal runtime and trap mode |
| Clang address, thread, memory and leak sanitizer documentation | Apache-2.0 with LLVM exceptions (same licence file) | optimisation and frame pointer advice, leak detection integrated in the address sanitizer, option variables read from the environment |
| Google C++ Style Guide (headers, include order, macros) | CC BY 3.0 (LICENSE of the style guide repository read 2026-10-20) | self-contained headers, guard naming from the full path, include what you use, related header first, macro rules |

### Verified in this pass
1. 5.1 staged adoption; 5.2 warning set and diagnostic pragma wrapping; 5.3 both forms of warnings as errors; 5.5 strict flexible arrays, stack clash, strong protector; 5.6 control flow, zeroed registers, exception tables; 5.7 production semantics; 5.8 position independence, relro and now, as-needed, no transitive entries, no-dlopen; 5.10 attributes and syntax; 5.12 separate debug file, no verification tool named by the guide.
2. 1.3 division by zero and the minimum signed value divided by -1, and 1.4 shift ranges, both appear as undefined-behaviour checks in the Clang sanitizer page.
3. 6.1, 6.2, 6.3 (including related header first) and 6.7 against the style guide.

### Corrected in this pass
1. 5.4: the guide says fortification is incompatible with the sanitizers in general (it names the address sanitizer and cites others), not only the memory sanitizer; text widened.
2. 5.9: the stand-alone leak sanitizer is ignored when the address or thread sanitizer is on, and the address sanitizer integrates leak detection; wording of the exclusions and of the production exception (minimal runtime in Clang, trap mode in GCC) rewritten; added that the Clang undefined group omits unsigned wrap and implicit conversions.
3. 5.8: added that read-only relocations are disabled for the application if any loaded library lacks them; added the rpath hazards.
4. 6.7: added the define-before-use and undefine-after rule and the avoid-## advice.

### Still unverified (no page found that says it, kept as own guidance)
1. Sections 1 to 4 (identifiers in brackets): the secure-coding list is not permissive and was not re-read; apart from the two cross-checks above they stay unsourced this pass.
2. 5.11 (fuzz the parsers): the pages read do not say it; own guidance. 5.5 aarch64 compiler version: the guide gives two passages that differ (one says GCC 7 or later, one says to check the toolchain), so the block keeps the general wording.
3. 6.4 (a header declares, does not define), 6.5 (no cycles), 6.6 (globals), 6.8, 6.9: no permissive page read.
4. Flag spellings and minimal versions in the table of the guide change; nothing was compiled.

### Tally
Points 64. Sourced 15 (two of them extended with an added sentence), corrected 2, still unverified 47.
