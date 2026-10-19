# zig-pitfalls: origin and source stamps

> Provenance of `skills/zig-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. Nothing was compiled and no Zig
toolchain was run while writing it. This block is meant to be folded into the Zig language block when the
extended systems-language blocks (the unmerged PR 118 branch) land; until then it stands alone and does not
cite any section that exists only on that branch.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Zig 0.17.0 language reference (ziglang.org documentation page for 0.17.0) | MIT (the Zig repository licence, re-read) | try, catch, unreachable, defer, errdefer, error sets, memory and the allocator selection guide, testing and leak reporting, comptime, optimisation modes |
| Zig 0.17.0 release notes (released 2026-10-01 per the download index) | MIT (the website repository licence, re-read) | errdefer capture removed, SafeAllocator and DebugAllocator deprecation, BufferFirstAllocator, `@bitCast`, removed syntax, `@hasDecl`, known regressions |
| Zig build system page (ziglang.org, learn section) | MIT (same repository family) | steps graph, standard options, test run step, stdin and stdout channel, output paths, and the page's own failing `ArrayList.init` example on 0.17.0 |

## Removed in the verification pass (no page supporting them)
- "A catch that discards needs a named reason": no page says it; kept only as the `catch unreachable`
  assertion rule the reference does state.
- "Re-pin the style reference to a current release": the style reference belongs to the unmerged language block
  and cannot be edited here; the drift rule (§4.4) covers the idea.
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
