# flutter-release-toolchain-hygiene §4 — Gates and accessibility tests

Sources: the Dart site pages for `dart analyze` and `dart format`, the agent-plugins static-analysis and
coverage skills (BSD-3-Clause), and the Flutter website's accessibility-testing page (repository text,
CC-BY-3.0 with BSD code), read 2026-10-08. Workflow-file security, pinning actions and required checks are in
`ci-workflow-hardening`, not here.

## 4.1 Format and analyze are hard gates
1. **Fail the build on formatting drift.** `dart format` has a flag to leave files untouched and a flag that
   exits non-zero if any file would change; run it as a check (Dart format page).
2. **Fail the build on info-level findings too.** The analyzer normally fails on errors and warnings but not
   on info-level issues; the fatal-infos flag changes that (Dart analyze page).
3. **Turn on the strict language checks** (casts, inference, raw types) in the analysis options and exclude
   generated files with glob patterns (static-analysis skill).
4. **CI never fixes what it checks.** A job that rewrites formatting, regenerates code or updates reference
   images and pushes the result turns a gate into a silent repair (our guidance).
5. **Every gate maps to a rule someone can name,** and none is allowed to fail (our guidance).

## 4.2 Accessibility guideline tests
1. **Run Flutter's accessibility guideline matchers in widget tests.** The page's example enables semantics in
   the test, pumps the widget, and checks: tappable nodes at least 48 by 48 logical pixels for Android and 44
   by 44 for iOS, labelled tap targets, and text contrast (3:1 for larger text, 18 point and above regular,
   per the page's comment). The page's example disposes the semantics handle at the end.
2. **Await each matcher.** The page's example awaits every `expectLater`; an unawaited one cannot fail the
   test (our guidance, reading the example).
3. **Pin the surface size and pixel ratio in layout tests** so a result does not depend on the machine
   (our guidance); never silence an overflow in a test to make it pass.
4. **Matchers do not replace scanners.** The page recommends the Android Accessibility Scanner, Xcode's
   Accessibility Inspector with its audit, and for web the browser's accessibility tree under the semantics
   host. Run each on the platform it covers.
5. **Rules about what must be announced or labelled** are `flutter-conventions` §9 and the `accessibility`
   block; this section is about proving them.

## 4.3 Coverage
1. **The coverage package's test-with-coverage script runs the tests and writes an LCOV report** under
   `coverage/` (coverage skill).
2. **A file no test imports is missing from the report,** which overstates coverage; the skill's validation
   step says to ensure missing files are imported and executed by tests (our reading of it). Exclusions are
   written as ignore directives in the files, which the skill lists.
3. **Generated-file globs belong in both the analyzer and the coverage exclusions** (our guidance, matching
   §3 of this block).
