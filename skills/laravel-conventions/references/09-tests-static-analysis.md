# laravel-conventions §9 — Tests and static analysis

> Section 9 of `skills/laravel-conventions`. Read it when tests are written, or Larastan/Pint is in play. The other sections and the guardrails stay in `SKILL.md`.

1. **Two tiers, and no third.** A **feature test** boots the framework and asserts an observable outcome —
   a row written, a job dispatched, a notification sent, a response returned. A **unit test** covers code you
   wrote yourself with non-trivial logic and no framework coupling: a money converter, a period value object,
   a working-hours calculator. There is no "integration", "controller" or "service" folder; if something
   doesn't fit the two, the test is aimed at the wrong thing.
2. **The default is the feature test**, and the reason is economic: one factory call plus one assertion on the
   dispatched job covers the model hook, the listener registration and the payload at once — and it's written
   against the contract, so it survives the refactor. The framework's own Eloquent, router and queue are
   already tested; a test that mocks the database to prove a listener was wired proves only that you wrote a
   mock.
3. **The routing is mechanical**, which is the point — nobody should debate it: a model lifecycle side effect,
   an HTTP endpoint, a console command, a listener or job `handle()`, a notification or mail, a policy, a
   scope/accessor/mutator → **feature**. A pure custom domain piece → **unit**.
4. **Arrange / Act / Assert, with exactly one Act.** One action means one reason to fail; two Act blocks are
   two tests sharing a name. Name the method after the **behaviour**, not the method called —
   `it_marks_invoice_paid_when_payment_succeeds`, never `it_marks_paid`.
5. **Assert observable outcomes, never internal calls.** `shouldReceive('save')->once()` asserts your own
   plumbing; the row, the response, the dispatched job and the sent mail are what the user experiences.
6. **Four anti-patterns with the same root**: instantiating a controller and calling its action (it bypasses
   middleware, the form request, route binding and the response contract); unit-testing a job or listener
   against a mocked database; booting the framework to test a calculator; and reaching for a mocking library
   in a unit test — if you need to mock a collaborator, the collaborator is framework-touching and the test
   belongs one tier up.
7. **One test style across the project**, applied uniformly — but **inside an existing file, match that
   file's local style**. Half-migrating a file between styles is worse than either style.
8. **Seeders and factories: no orphans.** Every foreign key resolved through a factory relationship or an
   explicit lookup, never a hardcoded id that happens to exist locally.
9. A factory produces a valid minimal object; the test states what it needs on top. A factory that fabricates
   a fully-populated aggregate makes every test depend on data it never asked for.
10. Reference data inserted by a migration or a seeder is idempotent — it runs again on the next environment.
11. **A change that introduces or changes persisted data ships its seed data in the same change.** The bar
    is a fresh migrate-and-seed showing the new feature populated with realistic, varied data, without
    anyone touching their database by hand: a new model gets its seeder registered, an extended enum gets
    rows for the new cases, a new column gets values that are not all the default. A feature whose data
    only exists on the author's machine is a feature the next person cannot see, and the seeder written
    three weeks later is written against a schema that has moved.
12. Where a static analyser is installed, detect its configured level on the first edit and **write to
    that level**, rather than introducing findings someone else has to clear. Its baseline is not a licence
    to add to the baseline.
13. **Fake every external boundary explicitly** — HTTP, mail, queue, storage, and any clock the code reads.
    The trap worth naming: a factory whose model has a lifecycle listener performing an outbound call. The
    test needs that call faked, or the suite makes real network requests and fails for reasons that look
    exactly like flakiness, which is how a real failure gets re-run until it passes.
14. **A test that has never failed proves nothing.** Write it red, or break the behaviour once and watch it
    go red before trusting it. This is the repo's default-is-failure guarantee applied to its own output
    (`WORKFLOW.md`): a test asserting something already true, or asserting nothing, is indistinguishable
    from a passing suite — and it is worse than no test, because it occupies the space where the real one
    would have been written.
15. **Freeze time and randomness.** A suite that reads the real clock fails on the first of the month, at
    23:59, on a leap day, or in the CI timezone that is not yours; the framework ships travel and freeze
    helpers precisely so the assertion can name the instant. The same holds for anything seeded by chance:
    a test that passes four times in five is a failing test with a slow reveal.
16. **Each test stands alone.** One that depends on another's leftovers passes in the order it was written
    and fails in the order CI happens to choose, which then reads as infrastructure trouble rather than as
    the coupling it is. Refresh or roll back the database per test, and keep mutable static state out of
    the suite entirely.
17. **Assert the refusal, not only the success.** Authorisation is tested per persona, and the personas
    that matter most are the ones who must *not* see the thing: the other tenant, the read-only role, the
    unauthenticated visitor (§2). A suite that only ever acts as the administrator proves the feature
    works and says nothing about who can reach it — and that is the failure that becomes an incident
    rather than a bug.
18. **Coverage is a smoke detector, not a target.** A line executed is not a line asserted, so a high
    number produced by tests that call code without checking its outcome is more dangerous than a lower
    honest one: it retires the question. Read what the uncovered branches are before reading the
    percentage.
19. **A slow suite gets skipped, so its speed is part of its design.** Seed only what the assertion needs
    — a feature test that builds the world to check one response spends its cost on every run forever, and
    the first thing a team under pressure does with a twenty-minute suite is stop running it locally.
20. **Pest's closures are a syntax choice, not a second tier.** `it('...', fn () => ...)` still produces
    exactly one feature or one unit test per point 1 — the expectation API changes how the assertion reads,
    not what it's allowed to assert. A file mixing `it()` with a PHPUnit test class is point 7's
    half-migration problem wearing a different name.
21. **A dataset replaces N near-identical tests, not N different behaviours.** `->with([...])` is for one
    assertion repeated over many inputs — every invalid shape for the same validation rule, every locale for
    the same formatter — never for cases that actually diverge in what they assert, which belongs in
    separate tests where the name still states the behaviour (point 4).
22. **An architecture test enforces a structural rule this block already states, so it doesn't restate the
    rule — it makes violating it fail the suite instead of the review.** `arch()->expects(...)` checking
    that models don't reach into HTTP, or that a `*Service`/`*Repository` name never lands (§1, §5), turns a
    convention a reviewer has to remember into one CI catches; it still needs the convention decided first,
    the same way a linter needs a style decided first.
23. **Mutation testing answers what coverage cannot: whether the assertions would catch a real regression.**
    A surviving mutant — the source changed and no test went red — is point 18's "line executed, not line
    asserted" made concrete and automatic. Run it on the code that changed, not the whole suite on every
    push; it is too slow for that and the signal is about the diff.
