# nestjs-node-conventions §7 — Tests, mechanical checks and the read-only audit

> Section 7 of `skills/nestjs-node-conventions`. Read it when a Nest test is written (unit or end-to-end), or when
> an existing backend is reviewed without being changed. The other sections and the guardrails stay in
> `SKILL.md`. Pinned to NestJS 12 (documentation read 2026-10-02).

## Tests
1. **Build the module under test with the testing module**, compile it (the call is asynchronous), and take
   instances from it. Mock the injected providers, never the unit under test. A class with many dependencies
   can take a mock factory for its missing providers; the request and inquirer providers cannot be
   auto-mocked and are overridden explicitly.
2. **End-to-end tests start the application from the real module graph** with the production providers
   replaced only where they cross a boundary: override the provider (or module, guard, interceptor, pipe,
   filter) with a test double through the override calls, create the application, initialise it, and send
   requests to its HTTP listener with a request-simulation library. Apply the same global pipes, filters and
   prefixes as the entry point, otherwise the test passes against a different application. A guard overridden
   to "always allow" is stated in the test name.
3. **Close the application after the suite.** An open application keeps handles alive and the runner does not
   exit. Keep end-to-end files in a separate `test` directory with their own suffix and their own runner
   configuration, so unit runs stay fast.
4. **Database tests use a real database of the production kind** (container or a dedicated schema) rather than
   a mock of the data client; migrations are applied to it before the run, and each test leaves it as it
   found it. A mocked client proves the call shape, not the query (`skills/testing-anti-patterns`).
5. **Test the cross-cutting components in isolation and through the pipeline**: a guard with a fake execution
   context, then once more end to end to see its order relative to pipes and filters (`references/05`).
6. **Do not enable shutdown hooks in tests** (listener warnings with many instances), and close each created
   application.

## Mechanical checks (lint-level)

```
grep -rnE "new [A-Z][A-Za-z]*(Service|Repository|Controller)\(" src test
grep -rnE "useGlobal[A-Za-z]+\(" src test
grep -rnE "app\.close\(|afterAll" test
grep -rnE "forwardRef" src
grep -rnE "process\.env" src
grep -rnE "console\.(log|error|warn)" src
grep -rnE "@Res\(\)" src
```

- A manual `new Service()` is a DI bypass (`references/01`).
- An end-to-end file without `app.close()` leaks the application.
- `console.*` in services bypasses the framework logger; use the logger (JSON output in production, levels
  from configuration).

## Read-only audit of an existing backend
Used when asked to review or assess a Nest codebase without changing it. It writes no code and runs no
migration; the output is a finding list, each with file and line, the rule it breaks, and its severity.

1. **Map first.** List modules and their imports/exports, controllers and their routes, global bindings
   (`main.ts` and the `APP_*` tokens), the configuration files, the data layer and the test layout. Say what
   you did not read.
2. **Boundary pass.** Every input has a validated shape (§2); validation is global; no raw `any` reaches a
   handler; the global pipe options are the strict ones; errors are mapped by a filter (§5).
3. **Access pass.** Which routes are public, by default or by exception; where authentication and
   authorisation sit; whether a route is protected only by being unlisted; rate limiting present on sign-in and
   expensive routes (`skills/security-hardening`).
4. **Data pass.** Repositories own queries; no query in a controller; atomic use cases are transactions that
   use the transaction client; no query in a loop (`skills/code-baseline`); migrations committed (§4).
5. **Lifecycle pass.** Configuration validated at boot, no scattered `process.env`; shutdown hooks enabled in
   the entry point; every opened resource has a destroy hook; no unexplained request-scoped provider (§6).
6. **Test pass.** Unit tests build the testing module; an end-to-end suite exists for the sign-in and the main
   write path; it uses the same global set-up as production; the database is real (rule 4).
7. **Report** by severity, with the evidence (the line, the command output) and never a fix applied. A finding
   that depends on a runtime fact is marked unverified. Unread areas are listed as such.
