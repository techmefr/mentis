# § 6 — Ruby judgment calls, tests and tooling

> Section 6 of `skills/rails-conventions`. Read it when Ruby code that is not obviously Rails is written (error
> handling, defaults, metaprogramming), when a test is added, or when the lint and CI set-up is touched. The
> formatting rules of the Ruby style guide (spacing, quoting, line length, trailing commas) are left to the
> linter on purpose: a rule a tool auto-fixes costs no reviewer attention, the same reasoning as in
> `skills/python-conventions`. What is here is what a tool cannot decide. Read 2026-10-02.

## Ruby

1. **Never rescue `Exception`.** It traps signals and `exit`, so the process can only be stopped with `kill -9`.
   Rescue the specific class, put the more specific classes first in the chain (a later specific clause is
   unreachable behind a general one), and release external resources in `ensure` or with the block form of
   `open`.
2. **Do not suppress an exception, do not use one for control flow.** An empty `rescue` hides the failure that the
   next line then trips over; an exception raised to leave a loop or to signal an ordinary outcome is a slow,
   confusing `return`. A failure that is routine gets a method designed for it (the style guide calls them
   contingency methods) instead of every caller wrapping its own `begin` block.
3. **Prefer the standard library's exception classes** over a new class per message; define a class when a caller
   will rescue it specifically.
4. **No mutable default shared between keys.** `Hash.new([])` and `Hash.new({})` hand every missing key the same
   object, so an append through one key shows up under all of them; use the block form. Do not use a mutable
   object as a hash key.
5. **Do not compare floats for equality.** Floating-point values carry representation error after any
   arithmetic; compare against a tolerance.
6. **Do not mutate arguments** unless that is the method's purpose; copy first. Keep parameter lists to three or
   four; past that, take a keyword argument or an object. Pass booleans as keyword arguments (`save(validate:
   false)`), so the call site reads without the signature.
7. **No class variables** (`@@x`): every class in the hierarchy shares one, which makes a subclass change its
   siblings. A class-level instance variable is per class.
8. **No monkey-patching of core classes in a library, no `method_missing`, no needless metaprogramming.** A
   patched core class changes behaviour for every other gem in the process; a dynamic method cannot be found by
   searching, and a typo becomes a `NoMethodError` somewhere else. Use `public_send` when the method name is
   data, so a private method is not reachable by accident.
9. **File operations are atomic where they can be:** `FileUtils.mkdir_p` and `rm_f` rather than "check, then
   act", which races under parallel processes in ways that are hard to reproduce.
10. **No comments in the code produced** (the repo-wide rule): the rationale goes in the commit or the
    documentation, and an unclear name is renamed, not annotated.

## Tests

11. **Integration-style request tests over controller-unit tests.** Drive the application through
   `ActionDispatch::IntegrationTest` (`get articles_url`, assert the response, the redirect and the content): it
   exercises routing, filters and rendering together, which is where the real failures are.
12. **Assert the refusals next to the success.** For each endpoint: the unauthenticated request, another user's
   record (a not-found or forbidden, §5.4), an invalid body, a missing parameter (400 from
   `params.expect`).
13. **Fixtures hold the common case, not every object.** Fixtures are a shared, predefined baseline for default
   data; build the unusual object in the test that needs it. A suite that needs fifty fixture rows to set up one
   scenario has made the baseline the scenario.
14. **Freeze time, don't read it.** `freeze_time` in place of `travel_to(Time.now)` and its variants; any test of
   expiry or scheduling sets the clock inside a block that restores it.
15. **Reserve system (browser) tests for critical user paths.** They are slower, more brittle, and cost more
   maintenance than request tests; use them for the core workflows and the JavaScript interactions that cannot
   be tested lower.
16. **Test jobs in isolation and in context:** the job's own effect with `ActiveJob::TestCase`, and that the
   enqueue happens from the code that should enqueue it.
17. **Run the suite in parallel, and keep failures reproducible.** Tests are distributed by a fixed rule, so the
   same seed and worker count give the same distribution; a flaky test that depends on its neighbour is
   reproduced by re-running with both. Run with `strict_loading` on (§2.26) and with eager loading in CI
   (new applications are configured that way), so a load-order problem fails in CI and not on the first request
   in production.
18. **A schema or migration change runs against a real database in CI**, and the schema file is regenerated and
   committed (§3.1).

## Tooling

19. **RuboCop with the Rails extension is the lint gate.** Its cops are the mechanical form of the rules here
   (`Rails/FindEach`, `Rails/SaveBang`, `Rails/HasManyOrHasOneDependent`, `Rails/UniqueValidationWithoutIndex`,
   `Rails/TimeZone`, `Rails/SkipsModelValidations`, `Rails/OutputSafety`, `Rails/EnvironmentVariableAccess`,
   `Rails/ThreeStateBooleanColumn`, `Rails/NotNullColumn`, `Rails/ReversibleMigration`, `Rails/DefaultScope`,
   `Rails/StrongParametersExpect`, `Rails/WhereMissing`, `Rails/WhereNotWithMultipleConditions`). Cops marked
   pending or disabled by default are opt-in: turn on the ones this document cites, and record each one left off
   with a reason in the configuration, not in somebody's head.
20. **Never loosen a cop to get a diff through.** Changing the lint configuration is a project decision, made in
   its own change.
21. **Lockfile and advisories.** `Gemfile.lock` is committed; the dependency set is scanned for known advisories
   in CI, and a vulnerable gem is bumped on its own (§5.14). The tool is the project's choice; this document
   names none because none was read for it.
