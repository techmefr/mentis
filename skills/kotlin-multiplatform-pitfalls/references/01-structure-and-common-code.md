# kotlin-multiplatform-pitfalls §1 — Structure and common code

Source: own craft knowledge; plugin and library behaviour is to be re-read in the documentation of the versions in use.

## 1.1 What belongs in common code
1. **Share logic that has no platform opinion:** models, validation, business rules, repositories over an interface, state holders, parsing and formatting. Keep the UI native or shared deliberately (§2.3), not by default.
2. **The common source set sees only the standard library and multiplatform libraries.** A Java class, an Android type or a platform API in it is a compile failure on the other target; the fix is an interface in common and an implementation per platform, not a conditional.
3. **Symptom: the Android build is green and the iOS build fails at link or compile time.** Cause: a dependency declared in common that has no variant for that target, or a call to a JVM-only function. Fix: build every target locally before merging a dependency change.
4. **Do not share for the sake of the percentage.** Code that needs a platform feature through five `expect` declarations is cheaper written twice behind one interface. Share where the contract is small.

## 1.2 Source sets and targets
1. **Use the default hierarchy template and add intermediate source sets only for a real shared subset** (for example all Apple targets). A hand-built hierarchy with overlapping sets produces ambiguous-dependency errors that are hard to read.
2. **Put each dependency in the narrowest source set that needs it.** A dependency in common is demanded by every target; a platform-only library belongs in that platform's set.
3. **Declare targets you will ship and test.** A declared-but-untested target rots; remove it or add its tests and its place in the pipeline.
4. **Keep the shared module's public surface small.** Mark helpers internal; every public declaration becomes part of what the apps depend on and what Swift sees.

## 1.3 Libraries for common code
1. **Check that a library lists every target you ship before adopting it.** Many Java-only libraries have no common equivalent; use the multiplatform alternative or put the dependency behind an interface.
2. **Time:** use a multiplatform date-time library rather than the JVM time classes, and inject a clock. Time zone data and formatting differ per platform; test with fixed zones.
3. **Networking:** use a multiplatform HTTP client with a platform engine per target, configure timeouts and certificate handling in each, and keep the client behind an interface so tests do not call the network.
4. **Storage:** use a multiplatform database or key-value library, keep the schema and migrations in common code, and open the connection through a platform-specific factory that supplies the file path. Do not store tokens in plain preferences; use each platform's secure store behind an interface.
5. **Serialisation:** use the compiler-plugin based serialisation library and keep field names stable; renaming a property in a shared model silently breaks stored data and API payloads on every platform at once.
6. **Dependency injection:** prefer constructor injection with a small hand-written or multiplatform container; reflection-based containers do not work on iOS.
7. **Logging and errors:** log through one interface; map platform exceptions to your own error types at the seam so common code never catches a platform exception class.

## 1.4 Version management
1. **Keep one version catalogue for the whole build** and update the Kotlin version, the Compose plugin and the main libraries together; a mismatch shows up as a cryptic compiler or metadata error.
2. **Upgrade the compiler in its own change** with a full build of every target, since language and interop behaviour change between versions.
3. **Read the library's target list again on each major upgrade;** a library can drop a target.

## Checks
- Common imports nothing platform-specific; each dependency sits in the narrowest set (§1.1, §1.2).
- Every shipped target builds and has tests (§1.2).
- Libraries cover all targets; secrets are in secure stores (§1.3).
- One version catalogue; compiler upgrades are isolated (§1.4).
