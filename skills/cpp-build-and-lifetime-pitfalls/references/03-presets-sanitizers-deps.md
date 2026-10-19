# cpp-build-and-lifetime-pitfalls §3 — Presets, sanitizers and dependencies

Sources: the CMake 4.4.4 manual (`cmake-presets(7)`, the `FetchContent` module), the GCC instrumentation
options manual and the Clang AddressSanitizer and ThreadSanitizer pages (read 2026-10-08), and the
cmake_template repository (Unlicense) for how one project wires them.

## 3.1 Presets: one checked-in file, one local file
1. **`CMakePresets.json` is for project-wide settings and may be committed; `CMakeUserPresets.json` is for a
   developer's local choices and should not be.** Both live in the project root and have the same format;
   add the user file to the ignore list. Presets exist since CMake 3.19.
2. **A configure preset names the generator, the build directory and the cache variables**, and can inherit
   from another; hidden presets act as a shared base. The template uses a hidden common preset with a build
   directory under the source tree keyed by the preset name, then one preset per compiler and build type.
3. **Use one preset per build type you intend to test**, including the sanitizer builds of §3.2, so a CI job is
   `cmake --preset <name>` and a local run is the same command (own guidance on the CI shape).
4. **The schema has a version number, and the CMake release must support it**; the manual's Versions section
   lists what each version adds. Set the `version` field to the lowest that has what you use (own guidance).

## 3.2 Sanitizers: which can share a build
1. **AddressSanitizer cannot be combined with ThreadSanitizer, and LeakSanitizer cannot be combined with
   ThreadSanitizer** (GCC manual). The template's own function refuses to enable thread with address or leak,
   and warns that memory sanitizer cannot be combined with address, thread or leak. So one build can hold
   address plus undefined behaviour; thread is its own build; memory (Clang only) is its own build.
2. **No restriction on combining UndefinedBehaviorSanitizer was found in the passages read** (not a statement
   that none exists), and the template enables address and undefined behaviour together by default where the
   compiler supports them; the compiler manual for the pinned version is the authority.
3. **Pass the flag to compile and link.** The template adds `-fsanitize=...` to both the compile and the link
   options of its options target; leak sanitizer only matters at link time (GCC manual).
4. **ThreadSanitizer needs the whole program compiled with it.** Clang's page says precompiled libraries without
   the flag can hide races or give false positives, static linking of libc or libstdc++ is not supported, and
   it implies position-independent code. Its overhead is stated as roughly 5 to 15 times in time and 5 to 10
   times in memory.
5. **MemorySanitizer needs every dependency, including the C++ standard library, instrumented** or it reports
   false positives (the template's warning). MSVC supports only the address sanitizer (also the template's
   statement).
6. **AddressSanitizer wants optimisation of at least `-O1` for tolerable speed and `-fno-omit-frame-pointer`
   for readable stack traces** (Clang page), so a sanitizer preset is a distinct build type, not Debug plus a
   flag by accident.
7. **Run each sanitizer build in CI, separately from the plain build**, and name them in the pipeline so a green
   job says which sanitizer it covered (own guidance).

## 3.3 Dependencies: pin by content, fetch one way
1. **When you do not control the server, pin `GIT_TAG` to a commit hash, not a branch or tag name.** The
   `FetchContent` manual says a hash is more secure and confirms that what was downloaded is what you
   expected. The manual's examples keep the readable tag as a trailing comment; under the house rule against
   comments, record the tag in the commit message instead.
2. **Fetch every dependency through one mechanism** (own guidance). The template wraps `FetchContent` in
   CPM.cmake for all its dependencies; mixing a package manager, `FetchContent` and vendored copies makes it
   impossible to answer which version of a library is in a build.
3. **Do not use `FETCHCONTENT_FULLY_DISCONNECTED` to forbid network access on a first configure.** The manual
   says that can break projects, give misleading errors and hide population failures; the variable is meant to
   be turned on only after the first run, and a dependency provider populating from local content is the
   documented way to prevent network access from the start.
4. **Dependency age, bot pull requests and lockfile audits are `ci-workflow-hardening` §3**, and the
   decision to add a dependency at all is `security-hardening` §4.
