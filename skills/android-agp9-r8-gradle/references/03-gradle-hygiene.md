# android-agp9-r8-gradle §3 — Gradle hygiene

The Gradle "General Gradle Best Practices" page (the page is headed version 9.8.1), read as page text on 2026-10-08.

## 3.1 Build scripts
1. **Prefer the Kotlin DSL for new builds and subprojects:** strict typing gives better IDE completion, the code is
   easier to follow, and a Kotlin project needs no Groovy. It is the default of `gradle init` since Gradle 8.0, and Android
   Studio defaults to it.
2. **Apply plugins with the `plugins` block.**
3. **Do not write build logic that assumes plugin order.** The page's example replaces `afterEvaluate` and
   `subprojects {}` ordering tricks with `pluginManager.withPlugin("...") {}`.
4. **Avoid `afterEvaluate`.** The page says it defeats task configuration avoidance, is incompatible with the
   configuration cache and makes configuration depend on callback order; lazy `Property` and `Provider` wiring is its
   replacement.
5. **Do not use Gradle internal APIs.** Gradle and plugins such as AGP and KGP treat them as subject to unannounced
   breaking changes, even in minor releases.
6. **Use `@Incubating` APIs deliberately.** They can change in non-major releases; the closer to stable, the less
   likely.

## 3.2 Configuration
1. **Set Gradle build flags in the root `gradle.properties`,** under source control, not on the command line (the page
   calls the command line short-term testing). Do not set a property to its default value.
2. **Do not use `gradle.properties` in subprojects:** support is inconsistent, and Gradle, AGP and KGP do not
   reliably handle it. Set a single subproject's value in its build script, or share it through a convention plugin.
3. **Name the root project in `settings.gradle(.kts)`,** otherwise the name comes from the build directory and can
   differ between machines and CI.
4. **Stay on the latest minor version of your major Gradle release,** and update plugins. Only the latest minor of the
   current and previous major release is actively supported.
5. **In a plugin, build service or helper class, get the logger with `Logging.getLogger(Class)`** so output is named
   after the class, not `project.logger`, which is shared and not compatible with the configuration cache at task
   execution. Inside a task use the inherited `getLogger()`.
