---
name: systems-assertion-discipline
description: "Use when writing or reviewing systems code in Zig, Rust, C or C++ that checks its own invariants: what to assert at function boundaries, which loops and queues need an explicit bound, compile-time assertions, and what each language's assertion does, or silently stops doing, in a release build."
---

# systems-assertion-discipline

Step 5 of the pipeline (`WORKFLOW.md`), for code where a violated invariant means corruption rather than an
error to report. The premise: **an assertion is a claim about the program, not about its input, and in three of
the four languages it can quietly vanish or turn into an optimiser assumption in the build you ship**. Input
validation at the edge is `security-hardening` §1; the Zig specifics are `zig-pitfalls`; generic test smells
are `testing-anti-patterns`.

## When
- A function is written that has preconditions, postconditions or an invariant worth stating.
- A loop, queue, buffer or recursion is written whose size depends on something other than the code.
- An `assert`, `debug_assert!`, `std.debug.assert`, `unreachable` or `static_assert` is added or reviewed.
- A release or optimised build changes behaviour compared with a debug build.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What to assert and bound: boundaries, pairs, limits, compile-time checks | a function with invariants or an unbounded loop or queue is written | [`01-assert-and-bound.md`](./references/01-assert-and-bound.md) |
| 2 | What an assertion does in release: Rust, Zig, C and C++ | an assertion guards something that must hold in the shipped build, or a release build behaves differently | [`02-release-behaviour.md`](./references/02-release-behaviour.md) |

## Output / checkpoint
Each non-trivial function states what it requires and guarantees as assertions, each loop and queue has a named
bound, and every condition that must hold in production is enforced by a check that the shipped build keeps
(§2). A statement that "the invariant is asserted" without saying which build keeps the assertion is not
verified.

## Guardrails
- Never assert on input you do not control; validate it and return an error (§1.1, `security-hardening` §1).
- Never put a side effect in an assertion condition (§2.3).
- Never rely on a debug-only assertion for memory safety or for a security decision (§2).
- Versions: each rule names the language version of the page it came from. Nothing was compiled or run while
  writing this block.

## Origin
Rewritten from the TigerBeetle style document (Apache-2.0; read at commit c95d7a5, 2026-10-06 tree), the Zig
0.17.0 language reference (MIT), the Rust standard library macro documentation (MIT OR Apache-2.0) and
cppreference pages for `assert` and `static_assert` (facts only, no text reused), read 2026-10-08. Meant to be
folded into the Zig, Rust, C and C++ language blocks when the extended systems-language blocks (the unmerged
PR 118) land; until then it stands alone. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
