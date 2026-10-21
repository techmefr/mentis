# rust-test-supply-chain-ci: origin and source stamps

> Provenance of `skills/rust-test-supply-chain-ci`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No tool named here was installed or
run. Overlaps with `skills/rust-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| nextest site documentation (commit cd1d6d5, 2026-10-07): running, design, leaky tests, retries | MIT OR Apache-2.0 (both licence files present) | Process-per-test, no doctests, leaky tests, retries and flaky handling |
| proptest book (commit 4b0594e, 2026-10-03): failure persistence | MIT OR Apache-2.0 (both licence files present) | Regression files, seed-based persistence |
| cargo-mutants book (commit b00aff0, 2026-10-08): mutants, skip, baseline, in-diff, nextest, cautions | MIT (LICENSE re-read) | What it mutates and excludes, skipping, baseline, side-effect caution |
| loom README and crate documentation (commit 948c8cc, 2026-02-20) | MIT (LICENSE re-read) | Model checking use, replacement types, unsupported features |
| Microsoft Rust guidelines (commit 19723b3): `M-TAUTOLOGICAL-TESTS` | MIT (LICENSE.md re-read) | Tests that restate the code, mutation skip |
| cargo-deny book (0.19.9 tree, commit 7354164, 2026-10-07): checks, advisories, bans, licenses, sources | MIT OR Apache-2.0 (both licence files present) | Defaults that warn versus deny |
| cargo-semver-checks README (0.51.0, commit d54ace5) | MIT OR Apache-2.0 (both licence files present) | Scope, limits, feature selection, rustdoc JSON dependence |
| cargo-hack README (0.6.45, commit d6033c2) | MIT OR Apache-2.0 (both licence files present) | `--each-feature`, `--feature-powerset`, `--depth`, `--rust-version` |
| Cargo book (cargo 0.102.0 tree, commit 33f504c, 2026-10-08): `config.md`, `manifest.md` | MIT OR Apache-2.0 (both licence files present) | RUSTFLAGS source precedence, `[lints]`, `build.warnings` |

## Removed in the verification pass (no page supporting them)
- "Cargo-mutants to find assertions that prove nothing": reworded to what the book says it checks (that tests
  can fail), with the tautological-test guideline kept separate.
- "A regression file committed" for proptest: kept; the book recommends it.
- Any recommendation of RustTraining mutex or lockfile advice (unreliable, not used) and any claim from
  cargo-careful (inconsistent documentation, not read).
- nextest's `AGENTS.md`: it contains an instruction aimed at an LLM; treated as data, not followed, not a source.
- Claims about `cargo-mutants` attribute names and crates: not read, so the block says "an attribute" only.

## Not verified
1. **Own guidance, flagged as such in the text:** not enabling retries to hide a fixable test (§1.1.4),
   writing the minimal failing input as an ordinary example test next to a proptest regression (§1.2.2),
   repeating every flag in a job that sets `RUSTFLAGS` (§2.5.4).
2. **Tool defaults were read from documentation of the stated versions** and not run; `cargo deny`'s default
   behaviour with no configuration file was taken from the documented defaults.
3. **`build.warnings`** is documented as respected from Rust 1.97 in a tree whose own `rust-version` is lower;
   whether the pinned toolchain has it was not checked.
4. **cargo-semver-checks baseline flags** other than `--baseline-version` were not read.
5. **The nextest "fail on flaky" option's name and version** were not read beyond the retries page.

## Related blocks
`rust-async-unsafe-pitfalls`, `testing-anti-patterns` §1, `ci-workflow-hardening` §3, `security-hardening` §4.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Each repository was cloned shallow and the documentation files below were re-read on 2026-10-20. The heads moved since the earlier pass, so the commits read are recorded here: nextest 3fe4ef3, proptest 70cf37d, cargo-mutants 6c720ae, loom 948c8cc, cargo-deny f3e9507, cargo-semver-checks 8d93ebb, cargo-hack d398b7c. The Cargo book was read from its published pages. Instruction files inside the cloned repositories were not opened.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| nextest site documentation: why process-per-test, running, test coverage, leaky tests, retries | MIT OR Apache-2.0 (both licence files present), read 2026-10-20 | process model, doctests not run, leaky detection limited to inherited stdout or stderr, retries and the flaky-result option |
| proptest book: failure persistence | MIT OR Apache-2.0 (both licence files present), read 2026-10-20 | regression tree, replay, commit the files, seed stored, one shared file, failure_persistence config |
| cargo-mutants book: mutants, skip attributes, baseline, in-diff, nextest, cautions | MIT (LICENSE file present), read 2026-10-20 | unsafe and test functions not mutated, mutants::skip, baseline skip needs a manual timeout, in-diff limits, nextest fail-fast, side-effect cautions |
| loom README | MIT (LICENSE file present), read 2026-10-20 | cfg loom and release mode, C11 model, SeqCst treated as AcqRel, load buffering not explored |
| cargo-deny docs: advisories, bans, licenses, sources configuration | MIT OR Apache-2.0 (both licence files present), read 2026-10-20 | defaults for unmaintained, unsound, yanked, multiple-versions, wildcards, unknown-registry, unknown-git, required-git-spec, licence allow list, dev and build dependencies |
| cargo-semver-checks README | MIT OR Apache-2.0 (both licence files present), read 2026-10-20 | baseline flags, no need to be published, rustdoc JSON instability, nightly best effort, default feature selection, areas not caught |
| cargo-hack README | MIT OR Apache-2.0 (both licence files present), read 2026-10-20 | each-feature, feature-powerset, depth, rust-version, version-range |
| Cargo book: configuration page (build.rustflags, build.warnings) | facts only, official documentation, read 2026-10-20 | four mutually exclusive rustflags sources and their order, build scripts and --target, build.warnings respected as of 1.97 |
| Microsoft Rust guidelines, M-TAUTOLOGICAL-TESTS (and the repository licence) | MIT (LICENSE.md read), read 2026-10-20 | tests that restate the code, mutation skip |

### Verified in this pass
1. 1.1 items 1 to 3; 1.2 items 1 to 3; 1.3 items 1, 2, 4, 5; 1.4 items 1 to 3 (the crate documentation was not read, only the README); 1.5 items 1 to 3.
2. 2.1 items 1, 3 to 6; 2.2 items 2 to 4; 2.3 all three; 2.4 item 3; 2.5 items 1 to 3.

### Corrected in this pass
1. 1.1 item 4: the option that fails a run on flaky tests is named and versioned (flaky-result, 0.9.131) and does not enable retries itself; the earlier open point is closed.
2. 1.3 item 3: the skip attribute is named; item 6: the marker left by an interrupted in-place run added.
3. 2.1 item 2: the unsound default (direct dependencies only) added.
4. 2.2 item 1: the other baseline flags exist (revision, root, rustdoc file); the earlier open point is closed.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.5 item 4 is a cross-reference.
2. 2.4 items 1 and 2 (the lints table, its package scope and the 1.74 version): the pages opened do not carry them, so the earlier statement stands unchecked.
3. 2.5 item 4 (repeat every flag in a job that sets the variable) is own guidance; item 5 (Cargo's caution about profile-managed flags) was not found again on the page read.
4. Own guidance kept: not hiding a fixable test behind retries, writing the minimal failing input as an example test, build.warnings depending on the pinned toolchain (the page says respected as of 1.97).
5. No tool was installed or run.

### Tally
Points 41. Sourced 31, corrected 5, still unverified 5.
