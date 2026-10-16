# mobile-crash-symbolication-pitfalls §2 — Matching symbols and stopping

> Part 2 of `skills/mobile-crash-symbolication-pitfalls`. Read it when symbols are being fetched or applied, or
> a result looks wrong. Sourced from the same two `dotnet/skills` skill files and the `.ips` format reference
> as part 1 (commit `6364668`), read 2026-10-16. Tool names are the source's. Sentences marked "own guidance"
> are ours.

1. **Match the symbol file by its identifier.** For Apple, the UUID in the crash log must equal the one in the
   symbol bundle, checked with `dwarfdump --uuid`; the source says always verify and requires an exact match.
   For Android, the symbol file is chosen by the build id on the frame line. Own guidance: a symbol file that
   is "the right version" by name or date but has another identifier produces confident, wrong function names;
   write the identifiers next to the result.
2. **Apple: find the bundle, then point the tool inside it.** The source's search order: the symbol server
   (the vendor's, by UUID), the build output's bundle, the SDK packs, the package cache, and a symbol
   download tool. `atos` is run with the architecture from the image list, `-o` pointing at the DWARF file
   inside the bundle's `Contents/Resources/DWARF` and not at the bundle, `-l` with the image's load address,
   and the frame addresses; several addresses can be passed in one call. Own guidance: a wrong `-o` or `-l`
   gives unresolved or plausible-looking wrong frames, so test with a frame whose answer you know.
3. **Apple symbol server download.** For the .NET runtime the source builds the URL from the UUID in lower case
   without dashes and converts the downloaded `.dwarf` into a bundle by placing it under
   `Contents/Resources/DWARF` with the image's name. The server answers 302 on a hit and 404 on a miss, and
   macOS runtime packages ship without symbols, so a separate symbols package may be needed. This is the
   vendor's server for the vendor's binaries; your own app's symbols are not there (point 6).
4. **Android: download by build id, then check the file.** The symbol URL is built from the build id on the
   frame line. After downloading, `file` should report an ELF with debug info that is not stripped; a 404 or an
   HTML answer means symbols were not published for that build. The tool is `llvm-symbolizer` from a modern
   LLVM (the source says 14 or newer for best compatibility), usually found in the Android NDK, run with the
   debug file and the offset and options for function names and demangling.
5. **One attempt per identifier, then stop.** The Android skill's stop rule: on a 404, make one attempt per
   build id and report the unsymbolicated frames with their build ids and offsets. Pre-release or internal
   builds may not publish symbols; look for an unstripped library in the build artifacts or the runtime
   package instead.
6. **Your own binary needs your own symbols.** The source notes that with ahead-of-time compiled apps the
   runtime is linked into the app binary, so the app's debug symbols have to come from your build output,
   while the separate native libraries can still use the public server. Own guidance: archive the symbol
   files (debug symbol bundles, unstripped libraries) of every release build with its UUIDs or build ids,
   because they cannot be rebuilt identically later.
7. **Do not install a toolchain to symbolicate.** If the tool is missing, both skills say to present the
   commands for the user to run (`atos` comes with Xcode's command line tools; the Android skill says not to
   spend time installing LLVM), and the Android script has a parse-only mode that lists the libraries, build
   ids and URLs without downloading.
8. **Clean the paths before reading them.** Resolved paths start with a continuous-integration workspace
   prefix; the source says to strip it, and that the meaningful path starts at `src/runtime/` in the runtime's
   monorepo (older builds may show `src/mono/`). Own guidance: a resolved path that points into a layout that
   does not match your project is a sign that the symbol file belongs to a different binary.
9. **Validate the result with three checks.** The source's list: the identifier matches, at least one frame
   resolves to a function name rather than a raw address, and the resolved paths look like the expected
   code base. When everything resolves, present the symbolicated backtrace with a brief reading (faulting
   thread, exception type, likely area) and go deeper only if asked; when it does not, report the
   unresolved frames with their identifiers and addresses and suggest finding the original build artifacts.
10. **Keep unresolved lines as they were.** The Android format keeps the original frame line, with build id and
    offset, for any frame that stays unresolved, so that a later attempt does not start from a lossy report.
