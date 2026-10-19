# cpp-build-and-lifetime-pitfalls: origin and source stamps

> Provenance of `skills/cpp-build-and-lifetime-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. Nothing was configured, built or run
under a sanitizer while writing it. This block is meant to be folded into the C++ language block when the
extended systems-language blocks (the unmerged PR 118 branch) land; until then it stands alone and cites only
sections that exist on the main branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Google C++ style guide (`cppguide.html`, commit 2251056, 2026-10-07): static and global variables, `thread_local` | CC BY 3.0 (LICENSE re-read); credit: Google | Trivially destructible statics, constant initialisation, patterns, `thread_local` rules |
| C++ working draft (eel.is/c++draft): `[basic.start.dynamic]`, `[dcl.constinit]` | ISO working draft; facts only, no text reused | Ordering of dynamic initialisation, deferral, exceptions, `constinit` |
| CMake 4.4.4 reference manual: `target_link_libraries`, `target_include_directories`, `include_directories`, `add_compile_options`, `target_compile_features`, `CMAKE_CXX_STANDARD`, `CMAKE_EXPORT_COMPILE_COMMANDS`, `cmake-presets(7)`, `FetchContent` | Kitware documentation; licence not re-read, facts only | Scopes, keywords, standard, compile commands, presets, pinning |
| GCC manual, instrumentation options | GNU documentation; licence not re-read, facts only | Sanitizer combination restrictions |
| Clang AddressSanitizer and ThreadSanitizer pages | LLVM documentation; licence not re-read, facts only | Optimisation and frame-pointer advice, ThreadSanitizer limitations and overhead |
| cmake_template (commit b86318a, 2026-07-25): `CMakeLists.txt`, `ProjectOptions.cmake`, `cmake/Sanitizers.cmake`, `cmake/StandardProjectSettings.cmake`, `CMakePresets.json` | Unlicense (LICENSE re-read) | A worked structure: options target, sanitizer wiring, presets, CPM |

## Removed in the verification pass (no page supporting them)
- "Hardened standard library mode in release builds", "span and checked access" and compiler hardening flags
  (items 10 and 11 of the earlier review): not part of this block; none of their sources was re-read.
- "Warnings and sanitizers as presets per build type" as a rule: kept as an example of the template and as
  own guidance (§3.1.3), since the manual only documents the mechanism.
- "Compile_commands exported for tooling" as a mandate: kept as the manual's feature plus the template's use.
- project_options (MIT or Unlicense): its LICENSE was checked, but its files were not read for rules.
- cppbestpractices (CC BY-NC) and the C++ Core Guidelines (personal and internal use only): idea-only, not
  opened or phrased from; the static storage rules come from the Google guide and the standard draft.
- The review's statement that address, undefined and thread sanitizers must be built "separately": narrowed to
  what the GCC manual and the template state (address and thread cannot combine, leak and thread cannot
  combine); no page read says undefined cannot combine with thread.

## Not verified
1. **Own guidance, flagged as such in the text:** adopting the Google rule as a house default (§1.2), the
   review checklist for a global (§1.5), one preset per build type and the CI shape (§3.1.3, §3.2.7), lowest
   preset schema version (§3.1.4), one fetch mechanism (§3.3.2).
2. **The Google guide is one company's project policy**, not a language rule; the language facts come from the
   draft, which was read in the working-draft form and not in a published standard.
3. **The `CMAKE_CXX_EXTENSIONS` rationale** is the template's own comment; the manual page for the variable was
   not read.
4. **Sanitizer overheads (5 to 15 times, 5 to 10 times)** are the Clang page's figures for the current page
   version.
5. **The GCC manual passages** were the address, thread, leak and hwaddress entries; the undefined behaviour
   entry was not read in full.
6. **Presets schema versions** and which CMake release supports which were not checked.
7. **cppreference was not used here**; the assertion block uses it for `NDEBUG` facts.

## Related blocks
`systems-assertion-discipline`, `ci-workflow-hardening` §3, `security-hardening` §4, `testing-anti-patterns`.
