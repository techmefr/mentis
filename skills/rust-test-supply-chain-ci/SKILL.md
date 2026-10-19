---
name: rust-test-supply-chain-ci
description: "Use when setting up or reviewing Rust tests and CI: what nextest does and does not run, proptest regression files, cargo-mutants and tests that assert nothing, loom for concurrency, and cargo-deny, cargo-semver-checks, cargo-hack, the Cargo lints table and the RUSTFLAGS override trap in a pipeline."
---

# rust-test-supply-chain-ci

Step 6 of the pipeline (`WORKFLOW.md`), for the checks around Rust code rather than the code. The premise:
**each of these tools is easy to add and easy to configure into doing nothing**: nextest skips doctests,
cargo-deny warns by default on things you assumed it denied, and one environment variable in CI silently
replaces the flags in the config file. Generic test smells are `testing-anti-patterns`; workflow and
dependency hygiene across languages is `ci-workflow-hardening`; the unsafe and async rules these checks back
are `rust-async-unsafe-pitfalls`.

## When
- A Rust test runner, a property test, a mutation run or a concurrency model test is added.
- A dependency audit, a semver check or a feature-matrix check is added to CI.
- `RUSTFLAGS`, `.cargo/config.toml` or the `[lints]` table is touched.
- A green pipeline is cited as evidence that the tests cover something.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Tests: nextest, proptest, cargo-mutants, loom, tests that assert nothing | a test tool is added or a test suite is judged | [`01-tests.md`](./references/01-tests.md) |
| 2 | Supply chain and CI: cargo-deny, semver-checks, cargo-hack, lints table, RUSTFLAGS | a CI job, a dependency policy or a build flag is written | [`02-supply-chain-ci.md`](./references/02-supply-chain-ci.md) |

## Output / checkpoint
Each tool added states what it will fail on (not only that it runs), the doctest and feature-combination gaps
are covered by an explicit step, and a change to compiler flags names the single place they are set. A claim
that "CI checks dependencies" without saying which checks deny and which warn is not verified.

## Guardrails
- Never assume nextest ran doctests (§1.1).
- Never write a test whose expected value restates the code under test, and never write one to satisfy a
  mutant (§1.5).
- Never set `RUSTFLAGS` in CI without checking what it displaces (§2.5).
- No block and no agent installs a tool: the blocks name the tool and the user installs it (`CONVENTIONS.md`).
- Versions: each rule names the tool version of the documentation it came from. Nothing was run while writing
  this block.

## Origin
Rewritten from the nextest documentation, the proptest book, the cargo-mutants book, the loom README, the
cargo-deny book, the cargo-semver-checks README, the cargo-hack README, the Cargo book and the Microsoft Rust
guidelines (all MIT or MIT OR Apache-2.0 repositories), read 2026-10-08. Meant to be folded into the Rust
language block when the extended systems-language blocks (the unmerged PR 118) land; until then it stands
alone. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
