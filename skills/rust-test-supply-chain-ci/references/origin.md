# rust-test-supply-chain-ci: origin and source stamps

> Provenance of `skills/rust-test-supply-chain-ci`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No tool named here was installed or
run. This block is meant to be folded into the Rust language block when the extended systems-language blocks
(the unmerged PR 118 branch) land; until then it stands alone and cites only sections that exist on the main
branch or in this block.

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
