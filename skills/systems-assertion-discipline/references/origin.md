# systems-assertion-discipline: origin and source stamps

> Provenance of `skills/systems-assertion-discipline`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. This block is meant to be folded into
the Zig, Rust, C and C++ language blocks when the extended systems-language blocks (the unmerged PR 118 branch)
land; until then it stands alone and cites only sections that exist on the main branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TigerBeetle style document (`docs/TIGER_STYLE.md`, tree dated 2026-10-06, commit c95d7a5) | Apache-2.0 (LICENSE re-read) | Assertions versus operating errors, boundary assertions, pairing, positive and negative space, splitting, limits on loops and queues, no recursion, static allocation, compile-time assertions |
| Zig 0.17.0 language reference | MIT (repository licence re-read) | `unreachable` and `std.debug.assert` per optimisation mode, `@panic` versus `std.debug.panic`, comptime evaluation, recursion and stack overflow |
| Rust standard library documentation for `assert!` and `debug_assert!` (rust-lang/rust master, library macros) | MIT OR Apache-2.0 | Always-on versus debug-only behaviour, unsafe code relying on `assert!` |
| cppreference pages for `assert` (C and C++), `static_assert` (C++) and `_Static_assert` (C) | CC BY-SA 3.0 (not re-read; only facts were taken, no wording reused) | `NDEBUG` disables `assert`, macro comma limit, `static_assert` forms and standards versions |

## Removed in the verification pass (no page supporting them)
- "Static allocation after start-up where feasible" as a general rule: kept only as that project's design
  choice, labelled so (§1.3.3).
- "One condition per assertion" as an absolute: kept as the document's "split compound assertions" with the
  implication form.
- "No recursion in bounded paths" as a Zig or Rust rule: kept as the document's rule with the Zig reference's
  stack overflow note; no Rust or C page on recursion was read.
- A Rust compile-time assertion form (`const` blocks or equivalents): no page read, so §1.4 says so.
- The TigerStyle naming, line length and 70-line taste rules beyond one labelled mention.

## Not verified
1. **Own guidance, flagged as such in the text:** choosing `assert!` versus `debug_assert!` by consequence
   (§2.1.3), no side effects in an assertion condition (§2.3.2), reading the build flags for `NDEBUG` (§2.3.1),
   stating which build runs the tests (§2.4), when to adopt static allocation (§1.3.3).
2. **TigerStyle's "two assertions per function" and 70-line figures** are that project's numbers; they were
   read, not validated.
3. **The study of production failures** that TigerStyle cites was not read; §1.1.3 only relays that it is
   cited.
4. **C and C++ `assert` behaviour was taken from cppreference,** not from the standard text.
5. **Rust `debug_assert!` behaviour is quoted from the master documentation** of 2026-10-08; the flag name
   `-C debug-assertions` was not checked against the compiler book.

## Related blocks
`zig-pitfalls`, `security-hardening` §1, `testing-anti-patterns`.
