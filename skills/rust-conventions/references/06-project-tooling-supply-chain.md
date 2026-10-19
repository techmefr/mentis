# rust-conventions §6 — Project layout, tooling and supply chain

> Section 6 of `skills/rust-conventions`. Read it when `Cargo.toml`, a feature, a dependency, a lint level, a
> toolchain pin or a CI gate changes. The general supply-chain doctrine is `skills/security-hardening` §4.
> **Everything that names a tool version or a lint list is volatile**: read the project's pinned toolchain and
> the current lint documentation before applying a list from here (`skills/source-freshness`). The other
> sections and the guardrails stay in `SKILL.md`.

1. **Toolchain and edition.** Develop on a stable toolchain, never a nightly as the default (a nightly-only
   tool is run for one command, not by switching the project). A new crate or workspace targets the latest
   stable edition at the time. A library sets a minimum supported compiler version when it is created and keeps
   it a few releases behind the newest compiler; raising it is a minor-version change, since anyone with
   third-party dependencies already depends on a reasonably recent compiler. Check what the project currently
   pins before assuming any number.
2. **Static verification is the check-in gate.** Run, on a developer machine and in CI: the compiler's lints,
   `clippy` across all its main categories (complexity, correctness, perf, pedantic, style, suspicious, cargo)
   plus a small chosen set from the restriction group, `rustfmt`, a vulnerability audit of the dependency
   tree, a feature-combination check, an unused-dependency check and the undefined-behaviour interpreter on
   unsafe code. Configure lint levels in the manifest's `lints` tables, not scattered through the code, with
   category priority below the individual lints so single exceptions work. The compiler lints worth enabling
   beyond the defaults include missing `Debug` implementations, redundant imports and lifetimes, trivial
   numeric casts and unsafe operations in unsafe functions; the restriction lints worth it include the ones
   that demand a reason on every `allow`, forbid undocumented unsafe blocks and flag `clone` on reference-counted
   pointers. The exact list changes with the release, so copy it from the current documentation of the
   guideline set, not from here.
3. **A lint override is `expect`, with a reason.** Overriding a project-wide lint on one item uses `expect`,
   which warns when the lint stops firing, so stale overrides disappear. `allow` is kept for generated code and
   macros. Every override carries its `reason`. A diff that adds an override to make itself pass is a
   finding.
4. **Formatter and linter run regularly; their automatic fixes are read.** Format with the project's
   `rustfmt` configuration (default settings unless the repo says otherwise). An automatic fix from the
   linter or the compiler is a code change by a tool that does not know the intent: review it as a diff.
5. **Features are additive.** Enabling a feature never removes or changes a public item, and any combination
   of features compiles where the platform allows. Use `std` as a feature to opt in, never a `no-std` feature
   to opt out. A feature never depends on another being turned on by hand, nor on a parent crate enabling a
   feature in a child. New variants added to a public enum under a feature are acceptable only if the enum is
   `#[non_exhaustive]`. Crates are for things that can be used on their own; features unlock extras that
   cannot. If a module could be used independently, make it a crate: an extra crate costs little and the split
   speeds compilation and prevents dependency cycles.
6. **The lockfile is committed and the profiles keep the safety defaults.** `Cargo.lock` is tracked in
   version control, including for libraries in a secure-development context, so a build is reproducible.
   Overflow checks and debug assertions are not overridden in the development and test profiles (§2.8).
   Compiler flags that change safety behaviour are not set through the environment on a build machine.
7. **A workspace holds the shared settings.** Two or more related crates go in one workspace; metadata,
   lint tables and dependency versions are inherited from the root (`workspace.dependencies`,
   `workspace.lints`). A dependency used by only one crate is still declared at the root. Workspace entries
   disable default features and let members opt in. Intra-workspace dependencies resolve through the workspace
   entry rather than a relative path. Crates sit as siblings in a single folder (one level, then grouped
   sub-folders once there are a couple of dozen).
8. **Every direct dependency is vetted and the vetting is tracked.** Who owns it, how active it is, whether it
   contains `unsafe`, whether its licence fits, whether a smaller or standard-library alternative exists.
   Transitive dependencies should get the same look. Check for outdated dependencies and either update or
   justify keeping an older one. Check dependencies against the public advisory database at each build or on a
   schedule, not once.
9. **Git and path dependencies are pinned.** A dependency from a repository names a commit or a tag, and the
   lockfile records the resolved commit; a floating branch is a moving target. A path dependency does not
   appear in a published crate.
10. **A library works out of the box.** `cargo build` succeeds on every supported platform without the user
    installing a system tool. For a native wrapper crate: build the native code from the crate's build script
    with the compiler driver crate rather than a Makefile, embed the upstream sources with a verifiable
    reference (repository URL and hash), make external tools optional, and pre-generate the bindings.
11. **Applications may choose the allocator and the target CPU.** A binary can pick a faster general-purpose
    allocator and a more specific CPU target than a library may assume. A library does neither.
12. **Names and numbers are not guessed.** If a rule above says "a few releases" or "latest edition", read the
    project's file (`rust-toolchain`, `rust-version`, `edition`) and the current release before writing a
    value, and record that the check was made.
