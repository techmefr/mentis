# cpp-build-and-lifetime-pitfalls: origin and source stamps

> Provenance of `skills/cpp-build-and-lifetime-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. Nothing was configured, built or run
under a sanitizer while writing it. Overlaps with `skills/cpp-conventions` (2026-10-19); cross-referenced, not merged.

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

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The CMake command, variable and module pages were read from the upstream source tree (a 4.5 development version per its version file; the block earlier cited the 4.4.4 manual), the Clang thread, address, memory and leak sanitizer pages, the OpenSSF hardening guide and the Google style guide were re-opened. The working draft of the standard is under a share-alike licence and was not re-read; the points that rest only on it stay unsourced. The GCC manual is under a copyleft documentation licence and was not re-read. Nothing was configured or built.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| CMake command pages (target_link_libraries, target_include_directories, include_directories, add_compile_options, add_link_options, target_compile_features), variable pages (CMAKE_CXX_STANDARD, CMAKE_CXX_EXTENSIONS, CMAKE_EXPORT_COMPILE_COMMANDS), cmake-presets(7), FetchContent | BSD-3-Clause (LICENSE.rst in the CMake repository read 2026-10-20) | scopes and keywords, transitive plain form, legacy keywords, link flag position, option de-duplication and the SHELL prefix, standard and features, compile commands generators, presets files, hash pinning, disconnected mode |
| Google C++ Style Guide: static and global variables, thread_local | CC BY 3.0 (LICENSE of the style guide repository read 2026-10-20) | trivially destructible statics, constant initialisation, patterns, function-local never-deleted object, thread_local rules |
| Clang ThreadSanitizer, AddressSanitizer, MemorySanitizer, LeakSanitizer pages | Apache-2.0 with LLVM exceptions (llvm/LICENSE.TXT read 2026-10-20) | overheads, static libc not supported, PIE implied, optimisation and frame pointer advice, instrumented dependencies, leak detection in the address sanitizer |
| OpenSSF Compiler Options Hardening Guide | CC BY 4.0 (licence line in the guide) | which sanitizers exclude each other, GCC and Clang runtimes not mixable |

### Verified in this pass
1. 1.1 items 1, 4, 5 (ordering across translation units, destruction before unjoined threads, per-thread initialisation) against the style guide; 1.2 items 1, 2, 4; 1.3 items 1 to 5; 1.4 items 1 to 5.
2. 2.1 items 1, 2, 3, 5; 2.2 items 1, 2; 2.3 items 2, 3; 2.4 items 1, 2.
3. 3.1 items 1 (presets since 3.19, user file not checked in and ignored) and 4 (versions section); 3.2 items 1, 4, 6; 3.3 items 1 and 3 (hash pin advice and the disconnected-mode caution quoted from the module page).

### Corrected in this pass
1. 2.1 item 1: the manual calls new use of the directory-scoped commands discouraged and gives the reason; text widened.
2. 3.1 item 2: the generator and build directory fields of a configure preset are optional from schema version 3; the block said a preset names them.
3. 3.2 item 5: the Clang page says all code including libc must be instrumented but that interceptors allow an uninstrumented libc; text now says both. Item 1: cross-checked with the guide and the leak integration note added.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.1 items 2 and 3, 1.2 item 3: facts that come only from the working draft (share-alike), not re-read.
2. 2.1 item 4 (usage requirements affect the target's own compilation): not located on the pages read. 2.2 item 3: the rationale is still only the template's comment. 2.3 item 1, 2.5: the template is an example, own guidance. 3.2 items 2, 3, 7, 3.1 item 3, 3.3 item 2: own guidance or template statements.
3. The CMake pages read are from a newer tree than 4.4.4; behaviour on the pinned CMake release is not checked.
4. Nothing was configured or built.

### Tally
Points 49. Sourced 33, corrected 2, still unverified 14.
