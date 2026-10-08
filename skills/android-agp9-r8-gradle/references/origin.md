# android-agp9-r8-gradle: origin and source stamps

> Provenance of `skills/android-agp9-r8-gradle`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No project was built and no AGP was installed.

**Fold-in note.** Meant to be folded into `kotlin-android-conventions` (and the release part into `mobile-release`)
when PR 118 lands.

## Sources (read 2026-10-08, rewritten, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| developer.android.com: AGP 9.0.1 release notes, migrate to built-in Kotlin, enable app optimization | Android docs: CC BY 4.0 for text, code Apache 2.0 (facts only, rewritten) | §1, §2 |
| docs.gradle.org: General Gradle Best Practices (headed version 9.8.1) | Gradle docs: Apache-2.0 (facts only, rewritten) | §3 |

No third-party repository was used. The pages were downloaded and read as page text, and every flag, version and
default in the block was compared with that text in a second pass.

## Re-verified against page text in the second pass
Minimum versions and KGP and KSP auto-upgrade; the built-in Kotlin default, kapt and legacy-kapt, kotlinOptions,
source directories, `enableKotlin`, KMP restriction, opt-out with `newDsl=false`, the AGP 10.0 removal wording; the
table of flipped defaults; removed features; R8 DSLs, `proguard-android.txt` dropped in 9.0, full mode since 8.0,
`keepRules` directory, companion-method change, the analyzer availability; every Gradle practice in §3.

## Corrected in the second pass
- Added the `android.r8.strictFullModeForKeepRules` default flip (missing before).
- Replaced "built-in Kotlin has a temporary opt-out" with the pages' exact condition: both properties are needed and
  built-in Kotlin cannot be disabled in AGP 10.0.
- Replaced the KMP sentence with the page's: the multiplatform plugin cannot be combined with the Android application
  or library plugin while built-in Kotlin is on.
- Replaced "the page recommends narrow keep rules" with what the page says: refine keep rules, use the analyzer.
- Corrected the logger and `afterEvaluate` wording to the page's.

## Removed
- The review's claim that AGP 9 forces built-in Kotlin with no opt-out: the pages show a temporary opt-out.
- Version catalog recipes, convention-plugin recipes and configuration-cache adoption steps: no page read for them.
- The known-issue line that `legacy-kapt` skips annotation processing: the page lists it without a status; not stated.

## Not verified
1. **AGP 9.1, 9.2 and 9.4 release notes** were not read; the 9.1 repackaging and the 9.4 per-module opt-out are
   statements of the pages listed above only.
2. **AGP 9.3** is covered only by the optimisation page's table; the 9.3 release notes were not read.
3. **The R8 analyzer** was not run, and its Android skill page was not opened.
4. **Flutter or React Native Android builds** are not covered; see `flutter-release-toolchain-hygiene`.

## Related blocks
`flutter-release-toolchain-hygiene`, `jvm-pitfalls`.
