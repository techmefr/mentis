# rust-test-supply-chain-ci §2 — Supply chain and CI

Sources: the cargo-deny book (version 0.19.9 tree, 2026-10-07), the cargo-semver-checks README (0.51.0), the
cargo-hack README (0.6.45), and the Cargo book (cargo 0.102.0 tree, 2026-10-08). Dependency policy across
languages is `ci-workflow-hardening` §3; the broader dependency rules are `security-hardening` §4.

## 2.1 cargo-deny: know which checks fail and which warn
1. **Four checks:** advisories, licenses, bans and sources. `cargo deny check` runs all of them with each
   check's defaults when it has no configuration.
2. **advisories** read the RustSec database by default. A match on an `unmaintained` advisory fails the check
   (default `all`; `workspace` limits it to direct dependencies, `none` ignores them). A **yanked** version
   only **warns** by default; set `yanked = "deny"` to fail on it.
3. **licenses** are denied unless explicitly allowed, so the `allow` list is the policy; dev-dependencies are
   not checked by default and build-dependencies are.
4. **bans** warn, and do not fail, on **multiple versions of the same crate** by default, and likewise warn on
   a wildcard version requirement. Set `multiple-versions` and `wildcards` to `deny` to make them gate; a
   duplicate that cannot yet be removed goes in the skip list.
5. **sources** warn by default for a crate from an unlisted registry or git repository. Set `unknown-registry`
   and `unknown-git` to `deny` and allow-list what you accept; git sources also take a `required-git-spec`
   because an unpinned git dependency is effectively a wildcard on that repository.
6. **Net effect:** with no configuration the check fails on a few things and warns on the rest, so a green job
   does not mean the duplicate, yanked and source policies were enforced. Write the policy into `deny.toml` and
   say in the change which fields deny.

## 2.2 cargo-semver-checks before publishing a library
1. **Run `cargo semver-checks` before releasing a library** to compare the new API against the last published
   version, looked up on crates.io by default or selected by a baseline flag such as `--baseline-version`; the
   crate does not have to be published.
2. **It does not catch every violation.** The README lists areas it misses: breaking changes in the type of a
   field or parameter, and in generics or lifetimes, among others, and says more lints are added over time.
   A pass is evidence, not proof.
3. **It reads rustdoc JSON, which is unstable**, so a version supports the current stable and beta Rust at
   release, and nightly only best effort; pin a nightly if you must use one, and update the tool when you
   update Rust.
4. **Feature selection matters.** By default it checks all features except those named `unstable`, `nightly`,
   `bench`, `no_std` or with a leading `_`, `unstable-` or `unstable_`; use `--all-features`,
   `--default-features` or `--only-explicit-features` to change that.

## 2.3 cargo-hack for feature combinations and the minimum Rust version
1. **A crate with features should be checked per feature, not only with defaults.** `cargo hack check
   --each-feature --no-dev-deps` checks each feature (plus the defaults and no-default-features), and
   `--feature-powerset` checks every combination, de-duplicating equivalent ones; the README recommends
   `--no-dev-deps` with both to avoid a Cargo issue.
2. **The powerset grows fast.** Use `--depth` to cap how many features are combined; `--depth 1` equals
   `--each-feature`.
3. **`--rust-version` runs a command on the version in `package.rust-version`, and `--version-range` runs it
   across a range of Rust versions**, so the declared minimum supported version is tested, not asserted.

## 2.4 Put lint levels in the manifest
1. **The `[lints]` table** (`[lints.rust]`, `[lints.clippy]`, `[lints.cargo]`) sets levels per package in one
   reviewable place; a lint is named under the tool before the `::` (rustc if none). Levels are `forbid`,
   `deny`, `warn` and `allow`, and a `priority` orders lint groups against single lints.
2. **It applies to the current package only, not to its dependencies**, and Cargo caps lints from non-path
   dependencies. It is respected from Rust 1.74.
3. **Newer Cargo adds `build.warnings`** (`warn`, `allow` or `deny`) to adjust the effective level of lint
   warnings for local packages, documented as respected from Rust 1.97 and affecting only lints, not other
   warnings. Check the pinned toolchain before relying on it.

## 2.5 The RUSTFLAGS override trap
1. **Cargo takes extra compiler flags from the first of four mutually exclusive sources**, in this order:
   `CARGO_ENCODED_RUSTFLAGS`, the `RUSTFLAGS` environment variable, the matching `target.<tuple>.rustflags`
   config entries, then `build.rustflags`. Setting `RUSTFLAGS` in a CI job therefore **replaces**, and does not
   add to, flags configured in `.cargo/config.toml`.
2. **So a one-off `RUSTFLAGS="--cfg loom"` or `RUSTFLAGS="-D warnings"` drops every flag the project
   configured**: a hardening or lint flag silently disappears in exactly that job.
3. **Without `--target`, the flags go to build scripts and proc macros too**, since dependencies are shared;
   passing `--target` with the host tuple restricts them to the target build.
4. **Prefer the manifest and the lints table for lint levels** (§2.4), so CI does not need `RUSTFLAGS` for them,
   and where a job must set it (loom, §1.4), repeat every flag it needs in that one job (own guidance).
5. **Cargo's own caution:** passing flags that Cargo manages through profiles is discouraged and may conflict
   with future Cargo versions; use the profile setting instead.
