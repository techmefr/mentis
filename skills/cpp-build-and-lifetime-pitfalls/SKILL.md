---
name: cpp-build-and-lifetime-pitfalls
description: "Use when writing or reviewing C++ with global or thread_local state, or its CMake build: static initialisation and destruction order, constinit, target-scoped CMake commands and visibility keywords, compile_commands, presets, dependency pinning, and which sanitizers can share a build."
---

# cpp-build-and-lifetime-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for C++ changes at program scope: objects that outlive `main`'s
locals, and the build that compiles them. The premise: **two global objects in different translation units
have no defined initialisation order, and a CMake file that sets flags globally makes every target pay for
every other target's choices**; both bugs pass review because each line looks harmless. Assertions that
survive `NDEBUG` are `systems-assertion-discipline`; supply-chain rules for fetched dependencies are
`ci-workflow-hardening` §3; generic test smells are `testing-anti-patterns`.

## When
- A namespace-scope variable, a `static` member, a function-local `static` or a `thread_local` is added.
- A `CMakeLists.txt`, a preset file or a dependency declaration is written or reviewed.
- A sanitizer is added to a build, or a sanitizer job is red for a reason nobody understands.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Static storage duration and thread_local: init order, destruction, constinit | a global, static or thread-local object is added or its constructor changes | [`01-static-storage.md`](./references/01-static-storage.md) |
| 2 | CMake targets: scoped commands, visibility keywords, language standard, options as a target | a CMakeLists is written or flags are set | [`02-cmake-targets.md`](./references/02-cmake-targets.md) |
| 3 | Presets, sanitizers and dependencies: build matrix, sanitizer combinations, pinned fetches | a preset, a CI build type, a sanitizer flag or a fetched dependency is added | [`03-presets-sanitizers-deps.md`](./references/03-presets-sanitizers-deps.md) |

## Output / checkpoint
Every global or thread-local object in the change is either constant-initialised and trivially destructible,
or a function-local static with a stated reason; every CMake setting is attached to a target with an explicit
scope; sanitizer builds are listed per build type. A claim that "sanitizers pass" without saying which sanitizer
set, compiler and build type is not verified.

## Guardrails
- Never add a namespace-scope object with a non-trivial destructor (§1.2).
- Never use `include_directories`, `add_compile_options` or the keyword-less `target_link_libraries` form in a
  new CMakeLists (§2.1).
- Never combine AddressSanitizer or LeakSanitizer with ThreadSanitizer in one build (§3.2).
- No block and no agent installs a tool or a dependency: the blocks name it and the user installs it
  (`CONVENTIONS.md`).
- Versions: each rule names the standard draft, CMake or compiler documentation it came from (C++ working draft
  as of 2026-10-08, CMake 4.4.4, the current GCC and Clang manuals). Nothing was built or run while writing
  this block.

## Origin
Rewritten from the Google C++ style guide (CC BY 3.0, attribution: Google), the C++ working draft, the CMake
4.4.4 reference manual, the GCC and Clang sanitizer documentation and the cmake_template repository
(Unlicense), read 2026-10-08. Meant to be folded into the C++ language block when the extended systems-language
blocks (the unmerged PR 118) land; until then it stands alone. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
