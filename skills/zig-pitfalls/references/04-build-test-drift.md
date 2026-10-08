# zig-pitfalls §4 — Build, tests and release drift

Rules from the Zig 0.17.0 language reference, the build system page and the 0.17.0 release notes (0.17.0 was
released 2026-10-01 per the download index; pages read 2026-10-08).

## 4.1 build.zig
1. **The build is a graph of steps run independently and concurrently**, and nothing happens for an artifact
   until something depends on it: `installArtifact` for the install step, a named `b.step(...)` for anything
   else. An executable declared but never installed or depended on is never built.
2. **Take the target and the optimisation mode from the user**, with `b.standardTargetOptions(.{})` and
   `b.standardOptimizeOption(.{})`. By default no release mode is preferred, so the person running the build
   chooses. Do not hard-code them in a library or tool that others build.
3. **Never hard-code output paths.** The page says it breaks caching, concurrency and composability and
   annoys the user; the install prefix (`zig-out` by default) belongs to whoever runs `zig build`, and
   `.zig-cache` is disposable and not meant for version control.
4. **Pass configuration into the code with an options step** (`b.addOptions()`, `addOption`, then
   `addOptions("config", ...)` on the module) and read it with `@import("config")`; the value is known at
   compile time (§3). Expose user settings with `b.option(...)`, which also appears in `zig build --help`.
5. **Zig 0.17.0 shape of the API:** an executable takes a module made with `b.createModule(.{ ... })` through
   `.root_module`, and a library is `b.addLibrary(.{ .linkage = .static, ... })`. Examples using the older
   field layout do not apply (§4.4).

## 4.2 Tests
1. **Test declarations are compiled only in a test build.** Outside `zig test` they are omitted, so a test
   file nobody wires into the build is never run.
2. **From a build script, a test needs two steps:** a compile step from `b.addTest(...)` and a run step from
   `b.addRunArtifact(...)`. The page states that without the run step the tests are not executed. Hang the run
   step off a named `test` step, one per target you care about.
3. **Do not write to standard output from a unit test.** Under the build system the build runner and test
   runner talk over stdin and stdout, so output there interferes with the channel; use the testing and
   logging facilities, which write to standard error.
4. **Skip with `error.SkipZigTest`**, which the default runner reports as skipped. Unnamed test blocks always
   run and are exempt from `--test-filter`.
5. **Detect a test build with `@import("builtin").is_test`**, and use `std.testing.allocator` so leaks fail
   the run (§2.3).

## 4.3 Safety follows the optimisation mode
The reference lists four modes: debug (default), safe, fast and small. **Safety checks are on in debug and
safe and off in fast and small**, and debug compiles fast with slow code while the other three are reproducible
builds. A test or assertion that passed in debug says nothing about the mode you ship, because `unreachable`
becomes an optimiser assumption in fast and small (`systems-assertion-discipline` §2.2). Run the test step in
the mode you ship as well as in debug (own guidance). The reference spells the modes `debug`, `fast`, `safe`,
`small` where the build system page spells them `Debug`, `ReleaseSafe`, `ReleaseFast`, `ReleaseSmall`: the two
pages of the same release disagree, so run `zig build --help` on the pinned toolchain for the accepted spelling.

## 4.4 Drift between releases
1. **Zig is not 1.0 and breaks between releases.** The 0.17.0 notes report about 25 accepted and 125 rejected
   language proposals since 0.16.0 with undecided ones still open, and say that working on a non-trivial
   project may require taking part in the development process.
2. **Pin the toolchain version in the project's tooling and say it in the change** (own guidance), and read the
   release notes for that version before writing against its standard library.
3. **Compile examples before trusting them.** The build system page's own unit-test example, written with
   `std.ArrayList(i32).init(...)`, fails to compile on 0.17.0 in the page's own output. An example from
   another release, a tutorial or a model answer is a hypothesis.
4. **Breaking changes listed in the 0.17.0 notes that bite silently or loudly:**
   - `errdefer |err|` capture removed (§1.2).
   - `@bitCast` redefined as a reinterpretation of the logical bit representation; results for array and
     vector types changed, and the notes warn it can break existing code without a compile error, so audit
     every `@bitCast` touching arrays or vectors on upgrade.
   - `a ** b` array multiplication removed (use `@splat`); `void{}` removed (use `{}`); `i0` removed (use
     `u0`); `internal` and `link_once` global linkage removed.
   - `@hasDecl` true only for public declarations, in every file.
   - `std.heap.StackFallbackAllocator` reworked and renamed `BufferFirstAllocator`, `std.heap.stackFallback`
     removed; `DebugAllocator` deprecated for `SafeAllocator` (§2.2).
   - `std.fmt.allocPrint` moved to the allocator (`arena.print(...)`); `ArrayList.getLastOrNull` renamed
     `last`.
5. **The notes also list known regressions**, among them a separation of the maker and configurer build
   processes that breaks response files for `std.Build.Step.Run`; read that list before bumping a build that
   uses run steps.
