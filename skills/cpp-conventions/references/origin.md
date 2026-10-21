# cpp-conventions — origin and source stamps

> Provenance of `skills/cpp-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡, base to be confronted with a real C++ project.** No production C++ experience in house stands
behind this block. Sources were read on **2026-10-02**; only mechanisms are taken, no wording is copied.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| The C++ core guidelines (a standards-foundation guideline document) | commit `33bcd01` of 2026-08-06 | a licence that allows copying and derivative works for **personal or internal business use only** and requires the notice to be kept; **not an open licence** (the veille had recorded it as MIT, which the licence file contradicts) | the section structure (philosophy, interfaces, functions, classes, resources, expressions, errors, concurrency, templates, source files, enumerations, standard library, performance), the rule statements and, for about forty rules, the *reason* paragraphs. About 515 rule headings were read in full; reasons and examples were read for the rules named in §1 to §7 that needed a check. | **idea only**: every point is rewritten from the mechanism; none of the document's phrasing, examples or numbering is reused. The block must not be distributed as a derivative of the document. |
| A style guide for large C++ code bases (a search company's public guide) | commit `fc98150` of 2026-10-01 | CC BY 3.0 | header rules (self-contained, guards, include-what-you-use, forward declarations, definitions in headers), the exception stance, the integer-type stance, inheritance (composition first, public only), ownership, casting, macros, doing work in constructors | rewritten with this credit |
| Compiler Options Hardening Guide and Annotations Guide for C and C++ (an open-source security foundation) | see `skills/c-conventions/references/origin.md` | CC BY 4.0 | the whole hardening section, kept in one place: `c-conventions` §5 | cited, not duplicated |

**Arbitration made once, here.**
- *Exceptions*: the two sources disagree. The core guidelines make exceptions plus RAII the basis of error
  handling and describe what to do without them (fail fast, systematic codes, simulated RAII). The style guide
  forbids exceptions for its own code base for reasons rooted in its legacy (cost of retrofitting, mixed
  libraries). The block states the project's existing choice as the rule and gives both disciplines in §3;
  it takes no side for a project that has not chosen.
- *Integer types*: both sources agree that signed types are for arithmetic and that unsigned types are not a
  way to say "never negative"; the wording differs (plain `int` and exact-width types versus signed for
  arithmetic and unsigned for bits), and §1.6 states both.
- *Forward declarations*: the style guide avoids them; the core guidelines are silent. The block follows the
  style guide.

**What was left out, and why.**
- Pre-C++11 idioms, `std::auto_ptr` and similar: outside scope.
- The guidelines' support library (non-null wrappers, spans, owners) and the profiles mechanism: tooling that
  moves; the block names the *idea* (a span, a non-null wrapper) and not the library.
- `clang-tidy` check names and `cppcheck`: the primary documentation of those tools was not read in this
  pass, so no check is attributed to them; naming them as tools is the extent of it.
- Test frameworks (`GoogleTest`, `Catch2`) and build systems (CMake): no primary source read; the block says
  what a test run must contain (sanitizers, fuzzing, failure injection), not which library.
- Modules and the newest library additions (`std::expected` and others): the standard's support varies per
  toolchain; §6.10 and §3.10 name the question and leave it to the project.
- The style guide's naming, comment and formatting sections: the formatter and the project's own style decide.

**Volatile content to re-check at the next pass:** everything in the hardening section (see the C origin), and
the language-standard dependent advice (concepts, spans, coroutines) against the project's chosen standard.

**Crossings with other blocks.** `c-conventions` for hardening (§5), headers (§6.1 to §6.5), arithmetic (§1),
threads and signals (§4); `rust-conventions` §3 and §4 for the same ownership problems from the other side.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The style guide for large C++ code bases was re-read in full on 2026-10-20 (raw page from its repository main branch, licence file read). The C++ core guidelines, which carry most of sections 1 to 7, are not under an open licence and were not re-read; the hardening section is `c-conventions` section 5 and was verified there. Nothing was compiled.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Google C++ Style Guide (exceptions, noexcept, integer types, casts, nullptr, implicit conversions, copyable types, structs and classes, inheritance, operators, RTTI, ownership and smart pointers, namespaces, headers, macros, output parameters) | CC BY 3.0 (LICENSE of the style guide repository read 2026-10-20) | each rule listed under Verified, below |
| OpenSSF hardening guide, Clang sanitizer pages (see `skills/c-conventions/references/origin.md`) | CC BY 4.0 and Apache-2.0 with LLVM exceptions | section 7 intro: library checks, debug mode ABI difference, thread sanitizer |

### Verified in this pass
1. 1.6 (plain int, exact-width types, 64-bit for values reaching 2^31, unsigned only for bit patterns or modular arithmetic); 1.7 (C++ casts, brace conversion for arithmetic types); 1.8 (nullptr).
2. 2.4 (single owner preferred, unique_ptr for transfer, shared ownership only for a very good reason).
3. 3 intro and points 8 and 9 (ban on exceptions for practical, legacy reasons; error codes and assertions as the alternative; factory function instead of a failing constructor).
4. 4.5 (struct only for passive data without invariants); 4.6 (explicit conversions, no virtual calls in constructors); 4.7 (composition first, public inheritance, one of override or final); 4.8 (avoid RTTI); 4.9 (judicious overloading, no implicit conversions).
5. 6.2 (related header first), 6.3 (definitions of templates and inline functions in the header), 6.4 (avoid forward declarations), 6.6, 6.7 (macros), 6.8 (nothing added to the standard namespace).
6. 7.1 lambda captures (explicit captures for lambdas that may escape; by-value default capture of this is misleading); 7.2 (prefer return values to output parameters; values or const references for inputs).

### Corrected in this pass
1. 6.5: the style guide forbids using-directives in every file, where the block allowed them in source files; the disagreement is now stated.
2. 3 intro, 4.6 and 6.6: added the guide's own details (exception-related library types, Windows carve-out, copy and move constructors not explicit, ten-line rule for in-class definitions).

### Still unverified (no page found that says it, kept as own guidance)
1. Points drawn only from the core guidelines (most of 1 to 5 and 7) stay unsourced this pass: no open licence, not re-read.
2. 1.7 never cast away const, 4.10 unions, 5 all points, 7.5 concepts: no permissive page read.
3. Nothing was compiled; language-standard dependent advice depends on the project standard.

### Tally
Points 75. Sourced 18, corrected 1, still unverified 56.
