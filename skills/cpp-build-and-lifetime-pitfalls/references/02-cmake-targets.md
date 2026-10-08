# cpp-build-and-lifetime-pitfalls §2 — CMake targets

Sources: the CMake 4.4.4 reference manual (command pages read 2026-10-08) and the cmake_template repository
(Unlicense, tree of 2026-07-25), used as a worked example of structure and not as a rule source.

## 2.1 Attach everything to a target, with a scope
1. **`include_directories` and `add_compile_options` are directory-scoped.** The first adds the directories to
   the directory property and to every target in that directory; the second sets the directory's compile
   options for all targets in it and below. The manual's own note on `include_directories` says to prefer
   `target_include_directories`, which can also propagate the directories to dependents.
2. **Use `target_*` commands with an explicit `PRIVATE`, `PUBLIC` or `INTERFACE` keyword.** For include
   directories, `PRIVATE` and `PUBLIC` items populate the target's own include directories, `PUBLIC` and
   `INTERFACE` ones populate what dependents see. A header directory used only to compile the library is
   `PRIVATE`; the directory holding its public headers is `PUBLIC`.
3. **For `target_link_libraries`, the plain form (no keyword) is transitive**: the linked libraries appear on the
   link line of everything that links the target. Prefer the keyword form: `PUBLIC` libraries are linked and
   part of the link interface, `PRIVATE` ones are linked but not exposed, `INTERFACE` ones are exposed but not
   used by the target itself. The `LINK_PUBLIC` and `LINK_PRIVATE` spellings are legacy.
4. **Usage requirements of linked targets propagate and affect compilation of the target's own sources**, so a
   `PUBLIC` dependency leaks into every consumer's flags; keep dependencies `PRIVATE` unless the headers expose
   them.
5. **Link flags go through `target_link_options`**, and compile options set by `add_compile_options` are not
   used when linking (the manual says to use `add_link_options` for that); a flag string passed as a library
   item lands in the link line wherever the libraries are, which may not be where the linker wants it.

## 2.2 Language standard
1. **State the required standard on the target**, with `target_compile_features(<target> PUBLIC cxx_std_NN)`:
   CMake adds the compiler flag if one is needed, and a feature the compiler does not list is reported as a
   CMake error.
2. **`CMAKE_CXX_STANDARD` is only the default for the `CXX_STANDARD` property of targets created afterwards.**
   Setting it globally is the default for a top-level project, not a substitute for the feature requirement on a
   library that others consume.
3. **The template sets `CMAKE_CXX_EXTENSIONS OFF`** with a comment that this avoids a conflict between
   `-Wpedantic` and `-std=gnu++NN`, notably with precompiled headers; the manual page for the variable was not
   read, so treat this as the template's claim (§2.5).

## 2.3 Warnings and options as one target
1. **Put project-wide warning and option flags on a single `INTERFACE` library target and link it `PRIVATE`
   from each target**, instead of calling `add_compile_options` in a top-level file. The template does exactly
   this (an `options` target and a `warnings` target, each aliased into a project namespace), and its sanitizer
   function adds the sanitizer flags to the options target for both compiling and linking.
2. **Conditional flags per compiler**: the manual's own example uses `/W4` for MSVC and `-Wall -Wextra
   -Wpedantic` otherwise; use the `$<COMPILE_LANGUAGE:...>` generator expression for per-language options.
3. **Flags de-duplicate**, and de-duplication can split an option group; the manual's fix is the `SHELL:`
   prefix on a quoted group such as `"SHELL:-option A"`.

## 2.4 Make the compile commands available
1. **Export `compile_commands.json`** with `CMAKE_EXPORT_COMPILE_COMMANDS`: it lists the exact compiler call for
   every translation unit, which is what clang-based tooling reads. The template sets it on in its standard
   settings.
2. **Only the Makefile and Ninja generators implement it**; it is ignored elsewhere, and it does not work well
   with unity builds (`UNITY_BUILD` or `CMAKE_UNITY_BUILD`). Say so before enabling both.

## 2.5 What this section does not establish
The template's choices (an options target, out-of-source-build guard, compile commands on by default) are
examples of one working structure, not requirements from the CMake manual. Only the manual statements above are
rules; the rest is own guidance, flagged as the template's.
