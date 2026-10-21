# zig-pitfalls: origin and source stamps

> Provenance of `skills/zig-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. Nothing was compiled and no Zig
toolchain was run while writing it. Overlaps with `skills/zig-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Zig 0.17.0 language reference (ziglang.org documentation page for 0.17.0) | MIT (the Zig repository licence, re-read) | try, catch, unreachable, defer, errdefer, error sets, memory and the allocator selection guide, testing and leak reporting, comptime, optimisation modes |
| Zig 0.17.0 release notes (released 2026-10-01 per the download index) | MIT (the website repository licence, re-read) | errdefer capture removed, SafeAllocator and DebugAllocator deprecation, BufferFirstAllocator, `@bitCast`, removed syntax, `@hasDecl`, known regressions |
| Zig build system page (ziglang.org, learn section) | MIT (same repository family) | steps graph, standard options, test run step, stdin and stdout channel, output paths, and the page's own failing `ArrayList.init` example on 0.17.0 |

## Removed in the verification pass (no page supporting them)
- "A catch that discards needs a named reason": no page says it; kept only as the `catch unreachable`
  assertion rule the reference does state.
- "Re-pin the style reference to a current release": the style reference belongs to the `skills/zig-conventions`
  block and cannot be edited here; the drift rule (§4.4) covers the idea.
- "Comptime for types and constants, not to hide runtime cost": the second half is not on any page; kept in §3.2
  as a labelled own-guidance line.
- "Test blocks use the testing allocator so leaks fail": kept, but only as the documented behaviour of
  `std.testing.allocator`; nothing about the build-step layout beyond the build page was added.
- The zig-book (CC BY 4.0) and the TigerStyle naming rules were not used here.
- The `minimum_zig_version` field and any claim about how to pin a toolchain in `build.zig.zon`: no page read
  states it, so only "pin the toolchain version in the project's tooling" remains, as own guidance.

## Not verified
1. **Own guidance, flagged as such in the text:** the order of an acquire and its `errdefer` (§1.2.3), inferred
   error sets being fine for ordinary internal functions (§1.3.3), not handing a test an arena (§2.3.2),
   arenas outliving rule (§2.4.3), not using comptime to hide run-time cost (§3.2.2), treating a large branch
   quota as a design signal (§3.3.2), running the test step in the shipped mode too (§4.3), pinning the
   toolchain (§4.4.2).
2. **The optimisation mode spellings disagree** between the language reference (`debug`, `fast`, `safe`,
   `small`) and the build system page (`Debug`, `ReleaseSafe`, ...) of the same release; the block tells the
   reader to check `zig build --help`.
3. **The language reference still names `DebugAllocator`** while the release notes deprecate it; which one is
   right for a given project depends on the pinned release.
4. **Release-note items were read as headings and summaries only** for `ArrayList` pointer stability, the
   build-system rework and the incremental compilation items; the block does not rely on them.
5. **Examples in the 0.17.0 documentation were not compiled.**

## Related blocks
`systems-assertion-discipline` (assertions and bounds, `unreachable` in release modes), `testing-anti-patterns`,
`source-freshness` §3.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The 0.17.0 language reference, release notes and build system page were re-opened and each claim was checked against the passage; the licence files of both repositories were read again (MIT). Nothing was compiled.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Zig 0.17.0 language reference (errors, defer, memory, testing, comptime, optimisation modes) | MIT (ziglang/zig LICENSE read 2026-10-20) | catch rules, unreachable panic text, errdefer, defer rule, anyerror, allocator selection guide, leak report, overcommit argument, 1000 branch budget and quota builtin, four modes, test filter, SkipZigTest, is_test |
| Zig 0.17.0 release notes | MIT (ziglang/www.ziglang.org LICENSE read 2026-10-20) | errdefer capture removed, SafeAllocator, BufferFirstAllocator, bitCast, removed syntax, hasDecl, allocPrint move, last rename, notable regressions, proposal counts |
| Zig build system page (learn section) | MIT (same repository) | installArtifact, standard options, createModule, addLibrary, options step, run artifact, stdin and stdout channel, zig-out prefix, zig-cache, ArrayList init failing |

### Verified in this pass
1. 1.1 items 1 to 5; 1.2 items 1, 2, 4, 5; 1.3 items 1, 2.
2. 2.1 items 1 to 4; 2.2 items 1 to 6; 2.3 items 1, 3; 2.4 items 1, 2; 2.5.
3. 3.1 items 1 to 3; 3.2 items 1, 3; 3.3 both items (the error text and the quota note are on the page); 3.4; 3.5.
4. 4.1 items 1 to 5; 4.2 items 1 to 5; 4.3 (the four modes, and the spelling mismatch: the reference writes -Doptimize=debug, safe, fast, small while the build page writes Debug, ReleaseSafe, ReleaseFast, ReleaseSmall); 4.4 items 1, 3, 4, 5 (about 25 accepted, about 125 rejected proposals; the regression list does name the response file issue for Step.Run).

### Corrected in this pass
1. 3.3 item 2: added that the builtin takes a u32 and that the compiler note on the error points to it; the earlier wording of the ignore rule is confirmed on the page.

### Still unverified (no page found that says it, kept as own guidance)
1. Own guidance kept: 1.2.3, 1.3.3, 2.3.2, 2.4.3, 3.2.2, 3.3.2 second half, 4.3 last sentence, 4.4.2.
2. 2.4 item 3 and 2.1 item 2 are inferences from the selection guide, not statements.
3. Nothing was compiled.

### Tally
Points 56. Sourced 49, corrected 1, still unverified 6.

Independent verification 2026-10-21: 26 checked, 26 matched, 0 corrected, 0 unverified (0.17.0 language reference, release notes and build system page re-read; the 0.17.0 release date 2026-10-01 confirmed in the download index).
