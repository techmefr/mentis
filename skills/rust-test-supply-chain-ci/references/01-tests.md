# rust-test-supply-chain-ci §1 — Tests

Sources: the nextest site documentation (tree of 2026-10-07), the proptest book (tree of 2026-10-03), the
cargo-mutants book (tree of 2026-10-08), the loom README, and the Microsoft Rust guidelines
(M-TAUTOLOGICAL-TESTS, tree of 2026-09-25).

## 1.1 nextest
1. **nextest runs each test in its own process.** Its documentation gives this as the model that will always be
   the default: processes are natural fault boundaries, so a hung or crashing test can be killed on its own
   and one test timing out does not take the others down. The cost it names: tests that share in-memory state
   (a semaphore, a primed cache, an in-process server) must move that state out of process or into the
   runner's test groups.
2. **nextest does not run doctests.** The documentation says they are not supported because of limits in
   stable Rust, and to run them with `cargo test --doc` as a separate step; coverage from nextest must be
   merged with doctest coverage. A pipeline that replaced `cargo test` with nextest and nothing else has
   stopped running every documentation example.
3. **Leaky tests are detected, not fixed.** A test that leaves a subprocess running while holding standard
   output or error open is marked leaky; `std::process::Child` does not kill the child on drop, so use a guard
   that does, or `tokio::process::Command` with `kill_on_drop`.
4. **Retries mark a test flaky and treat it as passing by default**, with the run's exit code 0 when nothing
   else failed; a newer option makes flaky tests fail the run. Do not enable retries to hide a test you could
   fix (own guidance); use the stress feature to reproduce a nondeterministic failure instead of retrying on
   success.

## 1.2 proptest
1. **A failing case is saved and replayed.** By default proptest writes the failing case to a file under a
   `proptest-regressions` tree next to the source and replays it before generating new cases; the book
   recommends committing these files so collaborators and CI replay the same cases.
2. **What is stored is the random seed, not the value.** If the strategy later changes, the same seed may no
   longer produce the problematic value. For a bug that matters, also write the minimal failing input as an
   ordinary example test (own guidance following from that fact).
3. **All tests in a crate share one persistence file by default**; the `failure_persistence` setting on the
   test configuration splits them if the replay set grows.

## 1.3 cargo-mutants
1. **It checks that the tests can fail.** It rewrites function bodies (a value of the right type, or unit for
   `()`) and reports mutants that no test catches. It first builds and runs the unmutated tree as a baseline to
   confirm the tests pass and to set the timeout; `--baseline=skip` is for pipelines that already ran the
   tests, and then `--timeout` must be set by hand and the tests must really be green or the result is
   meaningless.
2. **Unsafe functions and test code are excluded from mutation**; it does not tell you anything about unsafe
   blocks (`rust-async-unsafe-pitfalls` §3.4 covers what does).
3. **Skip what cannot be tested, visibly.** The book gives three ways, an attribute, a path filter and a name
   filter, and advises the attribute where a particular function is hard to test so that the skip is
   visible in the code, and a config path or regex filter for whole modules or classes such as `Debug`
   implementations. Preview the effect with `--list`.
4. **`--in-diff` is a speed-up, not a substitute for a full run**: it only mutates code in the changed
   regions, ignores a diff that only changes tests, and cannot see a regression in an untouched region.
5. **With nextest** (`--test-tool=nextest`) a run stops at the first failing test, which suits mutation
   testing; the book warns nextest lets straggling tests finish, which can make it slower than `cargo test`
   on trees with slow integration tests, and that a configuration with fail-fast off should be turned back on.
6. **Mutated code runs your side effects.** The book's caution: a mutant can change an existing deletion path,
   so run it in a container, a CI job or a VM, with no production credentials, and with `--in-place` only on a
   disposable checkout.

## 1.4 loom
1. **loom permutes the possible interleavings of a concurrent test** under a model of the C11 memory model,
   with state reduction to keep the number of executions manageable. The code under test must use loom's
   types (`loom::sync`, `loom::thread`) behind `cfg(loom)`, and the test body runs inside `loom::model`. The
   crate documentation says any code that does not use loom's replacement types is invisible to loom, so a
   `std::sync` type left in the code under test is simply not checked.
2. **Run it as the README shows**: with `RUSTFLAGS="--cfg loom"` and in release mode. Note this overrides any
   other `RUSTFLAGS` and config-file flags (§2.5).
3. **It is not a complete model.** `SeqCst` accesses are treated as `AcqRel`, which can produce false alarms,
   and load-buffering behaviour is not explored, so a pass does not prove the absence of bugs. It does
   supply what Miri's partial weak-memory emulation does not (`rust-async-unsafe-pitfalls` §3.4).

## 1.5 Tests that assert nothing
1. **Do not restate the code in the test.** The Microsoft guideline, written about agent-produced tests, says a
   test that repeats the expected value from the same logic the code uses, or mirrors its branches, passes by
   construction and only adds noise to later changes. Its example asserts that a constant array equals the
   same literal.
2. **Test a property of the value instead**: that constants are evenly spaced, increasing, or related in the
   way the logic needs.
3. **Do not write such a test to kill a mutant.** The guideline says that where tests are written to satisfy
   mutation testing, the mutation should be skipped instead (§1.3).
4. **The general rule is `testing-anti-patterns` §1**: assert what the code does (value, state, observable
   effect), not what you configured.
