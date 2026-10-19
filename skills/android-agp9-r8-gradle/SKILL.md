---
name: android-agp9-r8-gradle
description: "Use when moving an Android build to Android Gradle Plugin 9 or fixing it after the move: removing the org.jetbrains.kotlin.android plugin for built-in Kotlin, replacing kapt with KSP or the legacy-kapt plugin, kotlinOptions to kotlin compilerOptions, kotlin source set directories, the new DSL and the removed variant API, the changed default gradle.properties flags, minimum Gradle JDK and Kotlin versions, enabling R8 and resource shrinking, proguard-android-optimize versus proguard-android, narrow keep rules, R8 full mode surprises, and Gradle build hygiene such as the plugins block, afterEvaluate and flags in gradle.properties."
---

# android-agp9-r8-gradle

Step 6 of the pipeline (`WORKFLOW.md`), for the Android build that stopped working after a plugin upgrade or that
ships a release build behaving differently from debug. The three sections share one premise: **AGP 9 changed several
defaults at once, so a build that "just fails after the upgrade" has a list of named flags and plugins behind it, and
each one is either migrated or opted out on purpose, with the opt-out dated**. Flutter and Dart build hygiene is in
`flutter-release-toolchain-hygiene`; the JVM and Kotlin language pitfalls are in `jvm-pitfalls`.

## When
- Upgrading AGP to 9.x, or a build breaks on `kotlin-android`, `kapt`, `kotlinOptions` or a variant API.
- Turning on R8 or resource shrinking, or a release build crashes where debug does not.
- Cleaning up a Gradle build (plugins, flags, `afterEvaluate`).

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | AGP 9: minimum versions, built-in Kotlin, kapt and KSP, DSL, changed flags, removed features | the AGP version changes | [`01-agp9-migration.md`](./references/01-agp9-migration.md) |
| 2 | R8: enabling it, the default rules file, full mode, keep rules, the analyzer | a release build is shrunk or crashes | [`02-r8.md`](./references/02-r8.md) |
| 3 | Gradle hygiene: plugins block, flags, `afterEvaluate`, subproject properties | a build script is written or cleaned | [`03-gradle-hygiene.md`](./references/03-gradle-hygiene.md) |

## Output / checkpoint
The build ran from clean on the new AGP with the Gradle and JDK it requires (§1); every opt-out left in
`gradle.properties` has a reason and an expiry (§1); a release build was installed and its main screens were opened
(§2); the build ran with the configuration cache on (§3). A build that only synced in the IDE is not verified.

## Guardrails
- Never leave `android.builtInKotlin=false` or `android.newDsl=false` without a dated reason; the pages say both opt-outs
  go away in AGP 10.0 (§1).
- Never solve an R8 crash with a global `-dontoptimize` or a broad keep; write the narrowest rule (§2).
- Never use `afterEvaluate` in a new build script (§3).
- Version numbers and flags here are those of the developer.android.com and docs.gradle.org pages on the date in
  [`references/origin.md`](./references/origin.md); nothing was built while writing this.
- Raising AGP, Gradle, JDK or Kotlin versions is the user's step; this block names it and stops.

## Origin
Rewritten from the Android developer pages on AGP 9.0 release notes, built-in Kotlin migration and app optimisation
with R8, and from the Gradle best-practices page (read 2026-10-08). 🟡: never run by us; meant to be folded into
`kotlin-android-conventions` (and `mobile-release` for the release part) when PR 118 lands; open points are in
[`references/origin.md`](./references/origin.md).
