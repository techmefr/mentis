# java-upgrade-and-maven-audit-pitfalls §1 — JDK and framework upgrades

Source: the Java migration skill of the claude-code-java repository (MIT, commit 0d98fe9, read 2026-10-16),
rewritten. Its release facts are the skill's statements, not re-checked against the JDK release notes.

## 1.1 Path and order
1. **Move from one long-term-support release to the next one** (8, 11, 17, 21, 25 in the skill's path), not from
   an old one straight to the newest.
2. **Assess first with searches, not with guesses**: the current JDK, the compiler target in the build file,
   imports of internal packages (`sun.*`, `com.sun.*`), imports of removed Java EE packages, and security-manager
   use before a release that removes it.
3. **Check the frameworks before the JDK**: the skill's compatibility table shows, for example, a Spring Boot 2
   line and a Hibernate 5 line that stop being supported on the newest releases, and a Mockito and Lombok that
   need newer versions. Update those tools when tests or annotation processing fail after the bump.

## 1.2 What breaks, by step (the skill's quick reference)
1. **8 to 11**: the Java EE modules are gone (XML binding, activation, common annotations, transactions, CORBA),
   so add the Jakarta artifacts as dependencies (JEP 320; the XA subpackage of the transaction API stays with the SQL
   module, the rest of it goes); some `sun.misc` classes go (Base64 has a standard
   replacement); the module system starts to matter for reflection on JDK internals.
2. **11 to 17**: strong encapsulation is on, so the old illegal-access switch no longer works (JEP 403: in 17 any use of it only prints a warning)
   and only explicit opening flags do; preview features that became final may change syntax.
3. **17 to 21**: `finalize` is deprecated for removal (JEP 421, release 18; use a cleaner or try-with-resources);
   the default charset of the standard APIs becomes UTF-8 (JEP 400, release 18), which matters when code assumed the platform encoding.
4. **21 to 25**, as the skill lists them and as the JEPs state them: the security manager can no longer be
   enabled at start-up and its API behaves as if none were ever enabled (JEP 486, release 24; the API is
   retained, not removed); the memory-access methods of `sun.misc.Unsafe` are deprecated for removal (JEP 471,
   release 23; use the variable handle or foreign-memory APIs) and the skill's word "removed" overstates it;
   only the 32-bit x86 port is removed (JEP 503, release 25); loading agents into a running JVM prints a
   warning from 21 (JEP 451), which announces disallowing it by default in a later release, and the flag that
   silences the warning is `-XX:+EnableDynamicAgentLoading`.

## 1.3 Build settings
1. **Set the release in one place**: a property used by the compiler source and target settings, or the
   compiler plugin's `release` setting for Maven, or a toolchain language version for Gradle.
2. **Fix compile errors iteratively**, then run the tests, then run the application and read the runtime warnings
   about reflective access.

## 1.4 Runtime flags
1. **An `--add-opens` flag is a debt entry**: it is the workaround for reflection on JDK internals. Pass it to
   the test runner's argument line as well as to the application, name the library that needs it, and remove it
   after the library is upgraded.
2. **A `ClassNotFoundException` for the XML binding context after the 8 to 11 step means the Jakarta artifacts
   are missing**, not that the JDK is broken.
3. **A reflective access exception at run time is the 17 symptom** of the same encapsulation.

## 1.5 Spring Boot 2 to 3
1. **Spring Boot 3 requires Java 17 or later and Jakarta EE 9 or later.** The `javax.persistence`,
   `javax.validation` and `javax.servlet` imports become `jakarta` ones.
2. **Search for the old imports with an exclusion for the packages that stay** (`javax.crypto`, `javax.net` in
   the skill's own command), so a blind replacement does not rename JDK packages.
3. **Automated recipes exist**: the skill runs an OpenRewrite plug-in with a Spring Boot 3 upgrade recipe. It is a
   tool the user installs; this block does not copy the recipe.
4. **Hibernate 5 to 6**: queries take an explicit result type; the identifier strategy deserves a deliberate
   choice (the skill prefers the identity strategy).

## 1.6 Checklist the skill ends with
Before: record the version, list dependencies, find internal-API use, check framework compatibility, make a
branch. During: update the build, add the Jakarta artifacts, rename imports if moving to Spring Boot 3, add
opening flags if needed, update test and annotation tools, fix compile errors, run the tests. After: remove flags
no longer needed, adopt new language features separately, update the CI pipeline, document the change. Keeping
the adoption of new language features out of the upgrade commit is the skill's ordering; running the suite on the
target JDK in CI before production is own guidance, not stated in the skill.
