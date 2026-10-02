# swift-conventions §6 — Linter configuration

> Section 6 of `skills/swift-conventions`. Read it when the linter configuration, an inline disable or a
> baseline changes. Only the linter's own README was read (`references/origin.md`); the rule catalogue and the
> formatter were not.

1. **One committed configuration file configures the linter**: rules enabled or disabled, opt-in rules,
   included and excluded paths, severities. Nested configurations merge, child over parent; a sub-project
   changes its own file and not the root.
2. **A baseline holds pre-existing violations so only new ones fail.** In a project with legacy findings
   write one, then shrink it deliberately. A diff never adds to a baseline to pass the gate.
3. **Strict mode (warnings as errors) is the CI setting** for a project that has reached zero warnings.
4. **An inline disable names one rule and has the narrowest scope** (this line or the next, never a file and
   never the all-rules keyword); it is a reviewed decision (`skills/testing-anti-patterns`).
