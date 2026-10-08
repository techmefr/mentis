# rust-async-unsafe-pitfalls: origin and source stamps

> Provenance of `skills/rust-async-unsafe-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. Nothing was compiled, no Miri run was
made. This block is meant to be folded into the Rust language block when the extended systems-language blocks
(the unmerged PR 118 branch) land; until then it stands alone and cites only sections that exist on the main
branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Rust async book (commit 43891ce, 2026-05-25): part guide chapters `more-async-await` and `concurrency-primitives` | MIT (the repository ships one LICENSE, re-read) | Cancellation, cancellation safety, `select!` in loops, join and try_join, async block quirks, blocking |
| Tokio 1.53.2 sources: `sync/mutex.rs`, `macros/select.rs`, `task/blocking.rs`, crate documentation | MIT (LICENSE re-read) | Which mutex to use, cancel safe and unsafe method lists, `spawn_blocking` and `block_in_place` |
| Clippy lint documentation (`await_holding_lock`, `missing_safety_doc`, `undocumented_unsafe_blocks`; master) | MIT OR Apache-2.0 (LICENSE-MIT and LICENSE-APACHE re-read) | Lint groups, versions and fixes |
| Microsoft Rust guidelines (commit 19723b3, 2026-09-25): `M-YIELD-POINTS`, `M-ASYNC-STACK-SIZE` | MIT (LICENSE.md re-read) | Yield points, future size tracking |
| Rustonomicon (tree of 2026-10-04): exception safety, unchecked uninitialised memory, unwinding, FFI | MIT OR Apache-2.0 (both licence files present) | Minimal exception safety, `MaybeUninit`, `-unwind` ABIs |
| `core::mem` documentation for `zeroed` and `uninitialized` (rust-lang/rust master) | MIT OR Apache-2.0 | Validity of all-zero values, deprecation since 1.39.0 |
| Miri README (commit b5e9787, 2026-10-07) | MIT OR Apache-2.0 (both licence files present) | What Miri detects and its limits |

## Removed in the verification pass (no page supporting them)
- The review's "hot futures that hold large locals across awaits grow, so box or reduce": kept only as the
  guideline's tracking and `impl Future` advice; "box" was dropped, since no page read recommends boxing.
- "Select branches must not lose data when not chosen": replaced by Tokio's definition of cancellation safety
  and its method lists.
- "`extern "C-unwind"` only where unwinding crosses the boundary, otherwise abort": reworded to the
  Rustonomicon FFI chapter's statement; the "otherwise abort" half became the labelled reconciliation in §3.3.4.
- "Every unsafe block carries a safety justification in the docblock": no page supports a docblock on a block;
  Clippy's lint wants a line comment, which the house rule forbids, so §3.5 says to avoid the lint and wrap the
  block in a documented function (own guidance).
- Rust async book chapters on cancellation (an outline only), `sync` and `dtors` (outlines), and
  `part-reference` were read and not used.
- cargo-careful: not read here.

## Not verified
1. **Own guidance, flagged as such in the text:** `MaybeUninit::zeroed` with an explicit `assume_init`
   (§3.2.3), reconciling the two Rustonomicon chapters on FFI and unwinding (§3.3.4), stating Miri flags and
   toolchain (§3.4.5), the unsafe-block wrapper pattern (§3.5.2).
2. **The Rustonomicon's unwinding chapter and FFI chapter disagree** (the first says unwinding across FFI is
   undefined, the second describes `-unwind` ABIs); the FFI chapter was followed.
3. **Tokio's cancel safe lists** are for 1.53.2 and say they are not exhaustive; other versions may differ.
4. **The Microsoft figure of 10 to 100 microseconds between yields** is a starting point under their stated
   assumptions, not validated here.
5. **Clippy lint groups and "since" versions** were read from the master tree and may move.
6. **Miri's experimental aliasing models and flags** change with nightly; no Miri run was made.

## Related blocks
`rust-test-supply-chain-ci`, `systems-assertion-discipline`, `testing-anti-patterns`.
