# jvm-pitfalls §3 — Null checking in the build

`java-conventions` §1 says where `Optional` belongs and to avoid returning `null`. That is a convention; this
section is the tool that enforces the rest. The tool is NullAway, a plugin for Error Prone, as described in
its README (read 2026-10-08).

## 3.1 How the checker thinks
1. **Everything is non-null unless annotated.** NullAway assumes every parameter, return value and field can
   never be `null`, and reports passing `null` to one and dereferencing one marked `@Nullable`. So the work
   is to annotate the exceptions, not the rule.
2. **Any `@Nullable` annotation works.** The README recommends JSpecify's, and says the AndroidX and
   JetBrains ones are also fine.
3. **It is type-based and local, so it is fast and incomplete.** The README's own claim is that it does not
   prevent every possible `NullPointerException` and catches most of those seen in production at low build
   cost. A green run is not a proof.

## 3.2 Turning it on
1. **Set the severity to error.** NullAway emits warnings by default; a warning nobody has to fix is
   background noise. The README's Gradle example sets `check("NullAway", CheckSeverity.ERROR)`.
2. **Tell it which code is checked.** Exactly one of the `AnnotatedPackages` option or the `OnlyNullMarked`
   option is required, to distinguish code that follows the convention from code that does not. New packages
   go into the annotated set from their first commit, so the set only grows.
3. **Requirements at the time of reading:** JDK 17 or higher and Error Prone 2.36.0 or higher. A newer
   README may say otherwise; check the version in use.
4. **Exclude generated code from the check.** Annotation processors that generate code into your package
   namespace can fail a build set to error; the README's answer is to exclude the generated directory
   with Error Prone's excluded-paths option rather than lower the severity for everything.
5. **Test code is a separate decision.** The README shows how to disable the check on test code; if you do,
   say so in the build file, not by omission.
6. **Android:** recent versions of the Gradle Error Prone plugin no longer support Android, so the setup
   needs extra configuration there; check the README's Android notes.

## 3.3 Checks
- Introduce a deliberate `null` argument to a non-annotated parameter and see the build fail.
- Count the packages in the annotated set before and after a change: the number did not drop.
- A `@Nullable` that is only there to silence the checker has a call site that really passes `null`.
