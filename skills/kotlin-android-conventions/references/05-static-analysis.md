# kotlin-android-conventions §5 — Static analysis

> Section 5 of `skills/kotlin-android-conventions`. Read it when the analyser configuration, a suppression or
> a baseline is touched, or a pull request is gated.

1. **The analyser is the code-smell tool for Kotlin that the build runs**, in addition to the compiler's
   warnings and the formatter. Its configuration is a committed file generated from the tool's default and
   edited to differ from it: set the option that builds upon the default configuration and list only the
   changes, so a tool upgrade brings new default rules without a hand merge.
2. **A baseline freezes legacy findings, not new ones.** In a project with existing findings, generate a
   baseline so the gate fails only on issues the diff introduces, then reduce it deliberately. A diff never
   adds entries to a baseline to get green.
3. **A suppression annotation names the rule and sits on the smallest scope**, a declaration, never a file;
   it is a reviewed decision, not a way to pass the gate (`skills/testing-anti-patterns`).
4. **The gate runs the analyser in CI and reports in a format the platform can show** (the tool emits several,
   including SARIF).
