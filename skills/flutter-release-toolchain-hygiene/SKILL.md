---
name: flutter-release-toolchain-hygiene
description: "Use when measuring a Flutter app's performance or size, versioning and shipping a build, changing dependencies or the lockfile, running code generation, or defining CI checks for a Flutter or Dart project: profile mode and real-device measurement, which build gives a representative size, the version line and build-number rules of both stores, the merged Android manifest, pub constraints, lockfile and advisories, analyzer and format gates, and accessibility guideline tests."
---

# flutter-release-toolchain-hygiene

Step 6 of the pipeline (`WORKFLOW.md`), for the facts around a Flutter build that no widget code
shows: how to measure it, how to version it, how its dependencies are held, and what CI should insist on.
The premise: **a number taken from the wrong build, a version that was already used, or a dependency set that
nobody pinned makes the same app a different app between two machines**. Widget, state and test rules are in
`flutter-conventions`; workflow-file security and required checks are in `ci-workflow-hardening`; the generic
release flow is `ship`.

## When
- A performance or app-size claim is about to be made.
- A version or build number is bumped, an upload is prepared, or an uploaded build is rejected.
- `pubspec.yaml` or `pubspec.lock` changes, or a package conflict has to be resolved.
- A CI job for a Flutter or Dart project is written or reviewed, or code generation is wired in.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Build modes, devices, what a representative size is, the size report, image decode size | a speed or size number is quoted or a performance fix is claimed | [`01-measuring.md`](./references/01-measuring.md) |
| 2 | The version line, build numbers in both stores, the merged manifest | a version is bumped, an upload is prepared or rejected, or permissions are reviewed | [`02-versions-and-release-facts.md`](./references/02-versions-and-release-facts.md) |
| 3 | Pub constraints, the lockfile, conflicts, advisories, code generation scope | dependencies or generated code change | [`03-pub-and-codegen.md`](./references/03-pub-and-codegen.md) |
| 4 | Format and analyze gates, accessibility guideline tests and scanners, coverage | a CI job or a test for accessibility is written | [`04-gates-and-a11y-tests.md`](./references/04-gates-and-a11y-tests.md) |

## Output / checkpoint
The number or version quoted has its build and device attached: a profile-mode run on a named physical
device, or a size read from the store's own report, or a version line and build number that are new to both
stores, or a CI run in which the analyzer, formatter and guideline tests failed on a seeded violation (§4).
A claim without its build attached is not verified.

## Guardrails
- Never quote a speed result from a debug build, an emulator or a simulator (§1).
- Never quote a download size from a debug build or from the artifact built for upload (§1).
- Never reuse a build number that has been uploaded (§2).
- Never delete the whole lockfile to clear a conflict (§3).
- Never let a CI job fix what it is meant to check (§4).
- Versions: each rule names the documentation it was read from; Flutter and Dart version limits are those of
  the page on 2026-10-08. Nothing was built or run while writing this block.

## Origin
Rewritten from the Flutter website's build-modes, UI-performance, app-size, Android and iOS deployment and
accessibility-testing pages, the Dart site's pub and analysis pages, the agent-plugins package-conflict,
static-analysis and coverage skills, and the Android and Apple release pages, read 2026-10-08. The
store-and-version material (§2) and the pub and gate material (§3, §4) are meant to be folded into the
same-topic sections (the mobile release block and the Dart habits and testing sections of
`flutter-conventions`) when the extended versions of those blocks land; §1 and the accessibility part of §4
can be folded into the main-branch sections on performance and accessibility testing at any time. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
