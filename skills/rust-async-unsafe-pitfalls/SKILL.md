---
name: rust-async-unsafe-pitfalls
description: "Use when writing or reviewing async Rust or unsafe Rust: cancellation safety and select loops, locks and blocking work in async code, large futures, panics that unwind through unsafe code, uninitialised memory, FFI unwinding, and what Miri can and cannot prove."
---

# rust-async-unsafe-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for Rust changes where the compiler's guarantees stop: a future that can
be dropped at any await, and a block that opts out of memory safety. The premise: **neither failure is caught by
a type error, and both show up only under load or on a panic**, so the rules below are about what to check by
hand and what tool backs the check. Assertion rules are `systems-assertion-discipline`; tests and CI for Rust
are `rust-test-supply-chain-ci`; generic test smells are `testing-anti-patterns`.

## When
- An `async fn`, a `select!` or `join!`, a spawned task or a channel loop is written or reviewed.
- A lock, a blocking call or a long computation appears inside async code.
- An `unsafe` block, an `unsafe fn`, uninitialised memory or an `extern` boundary is written or reviewed.
- Miri is added to CI or a Miri result is cited as evidence.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Cancellation and select: what an await point can lose, select in a loop, join | a future can be dropped, or `select!` is used in a loop | [`01-cancellation.md`](./references/01-cancellation.md) |
| 2 | Locks, blocking and future size in async code | a guard, a blocking call, a CPU-heavy loop or a large local appears in async code | [`02-locks-blocking-size.md`](./references/02-locks-blocking-size.md) |
| 3 | Unsafe: unwinding, uninitialised memory, FFI, Miri, safety docs | an `unsafe` block or an FFI boundary is written, or Miri is run | [`03-unsafe.md`](./references/03-unsafe.md) |

## Output / checkpoint
For async changes: each `await` that can be cancelled was considered, and every `select!` branch is named as
cancellation safe or not. For unsafe changes: each block states which invariant it relies on and what a panic
inside it leaves behind, and Miri was run on the tests that reach it (or the change says why not). A claim of
"cancel safe" or "sound" with no such check is not verified.

## Guardrails
- Never hold a standard-library or `parking_lot` guard across an `.await` (§2.1).
- Never call blocking I/O or run long CPU work on an async worker thread (§2.2).
- Never use `mem::uninitialized`, and never use `mem::zeroed` for a type where all zero bytes are invalid (§3.2).
- Never claim unsafe code is sound because Miri passed (§3.4).
- Versions: each rule names the version of the documentation it came from (Tokio 1.53.2 sources, the async
  book at its 2026-05 commit, the Rust documentation tree of 2026-10). Nothing was compiled or run while
  writing this block.

## Origin
Rewritten from the Rust async book (MIT), the Tokio crate documentation (MIT), the Rustonomicon (MIT OR
Apache-2.0), the standard library documentation, the Miri README (MIT OR Apache-2.0), the Clippy lint
documentation (MIT OR Apache-2.0) and the Microsoft Rust guidelines (MIT), read 2026-10-08. Meant to be folded
into the Rust language block when the extended systems-language blocks (the unmerged PR 118) land; until then it
stands alone. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
