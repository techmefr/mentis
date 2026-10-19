# android-agp9-r8-gradle §1 — AGP 9 migration

The Android developer pages "Android Gradle plugin 9.0.1 release notes" (last updated 2026-10-07) and "Migrate to
built-in Kotlin" (last updated 2026-09-15), read in full as page text on 2026-10-08.

## 1.1 Minimum versions
1. **AGP 9.0 lists these minimum and default versions:** Gradle 9.1.0, SDK Build Tools 36.0.0, JDK 17 and Kotlin
   Gradle plugin 2.2.10. The maximum API level it supports is 36.1.
2. **AGP 9.0 has a runtime dependency on KGP 2.2.10,** so you no longer declare a KGP version. A lower KGP is
   upgraded to 2.2.10, and a KSP lower than 2.2.10-2.0.2 is upgraded to 2.2.10-2.0.2.
3. **To use a higher KGP or KSP, put it on the top-level build script classpath** (`buildscript` dependencies). A lower
   version can be used only after opting out of built-in Kotlin.

## 1.2 Built-in Kotlin
1. **Built-in Kotlin is on by default in AGP 9.0:** the `org.jetbrains.kotlin.android` (`kotlin-android`) plugin is no
   longer needed to compile Kotlin. On upgrade you migrate or opt out. Remove the plugin from every module, from the root
   `apply false` line and from the version catalog.
2. **`kotlin-kapt` is incompatible with built-in Kotlin.** The page recommends moving to KSP. If that is not yet
   possible, replace it with `com.android.legacy-kapt` at the same version as AGP.
3. **Move `android.kotlinOptions {}` to `kotlin.compilerOptions {}`.** With built-in Kotlin the JVM target defaults to
   `android.compileOptions.targetCompatibility`.
4. **Add Kotlin source directories through `android.sourceSets { named("main") { kotlin.directories += ... } }`.** The page says
   that is the only supported option; `kotlin.sourceSets` and adding to the Java set are not supported. The variant API
   (`addStaticSourceDirectory`, `addGeneratedSourceDirectory`) is the page's route for variant-specific and generated sources.
5. **A module with no Kotlin sources can set `android { enableKotlin = false }`,** which removes the Kotlin compile task
   and the automatic Kotlin standard library dependency; the page recommends it in large projects.
6. **Kotlin Multiplatform:** built-in Kotlin replaces only `kotlin-android`. A KMP library module still applies the
   multiplatform plugin and `com.android.kotlin.multiplatform.library`, and the multiplatform plugin together with
   `com.android.library` or `com.android.application` is no longer allowed while built-in Kotlin is on.
7. **The opt-out is temporary:** `android.builtInKotlin=false`, which also needs `android.newDsl=false` because
   `kotlin-android` is not compatible with the new DSL. The build warns, and the page says built-in Kotlin cannot be
   disabled in AGP 10.0.
8. **Module by module:** set `android.builtInKotlin=false`, apply `com.android.built-in-kotlin` (same version as AGP)
   to each module you migrate, then remove both when all are done.

## 1.3 New DSL and removed features
1. **`android.newDsl` flips to true in AGP 9.0:** the legacy implementations of the `android` block and the legacy
   variant API (for example `android.applicationVariants`) are no longer accessible; use `androidComponents.onVariants`.
2. **Opt-out `android.newDsl=false`** gives the old DSL back; the page says the ability to opt out will be removed in AGP
   10.0 (page text: "mid-2026") and that AGP 9.4 adds a per-module variant-API opt-out.
3. **Removed in 9.0:** embedded Wear OS apps (`wearApp`), density split APKs (use app bundles), the
   `androidDependencies` and `sourceSets` report tasks, and several deprecated DSL elements such as `dexOptions`.

## 1.4 Defaults that flipped
1. **Changed from AGP 8.13 to 9.0, each with an opt-out of the same name:** `android.newDsl` and
   `android.builtInKotlin` (false to true); `android.uniquePackageNames` (distinct package name per library);
   `android.useAndroidx`; `android.default.androidx.test.runner` (AndroidJUnitRunner is the default
   instrumentation runner); `android.enableAppCompileTimeRClass` (non-final R class in apps, so R fields cannot sit in
   `switch` cases); `android.sdk.defaultTargetSdkToCompileSdkIfUnset` (target SDK defaults to compile SDK, it used to
   default to min SDK: set it explicitly); `android.onlyEnableUnitTestForTheTestedBuildType` (one unit test variant,
   debug); `android.proguard.failOnMissingFiles` (a missing keep file fails the build); `android.r8.optimizedResourceShrinking`;
   `android.r8.strictFullModeForKeepRules` (`-keep class A` no longer implies keeping its default constructor).
2. **`android.dependency.useConstraints` went the other way, true to false,** so constraints are used only in
   application device tests.
3. **Read this table when an upgrade changes tests, the R class, shrinking or keep behaviour** without any source
   edit. The AGP Upgrade Assistant in Android Studio helps preserve old behaviour during migration.
