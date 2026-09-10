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
24. **`RefreshDatabase` chooses its own strategy per driver, and knowing which one is running explains the
    speed and the failure modes.** Against SQLite in memory it wraps each test in a transaction and rolls
    it back; against a real MySQL or PostgreSQL connection it migrates fresh and still wraps in a
    transaction, which is why a test that commits inside a nested transaction of its own (a job that
    catches and swallows a `DB::commit()`, a raw `DB::unprepared('COMMIT')`) breaks the rollback the trait
    depends on — the failure looks like leaked state between tests and is actually the isolation mechanism
    itself being defeated.
25. **Parallel testing (`--parallel`) gives each worker process its own database, appended with the
    process token**, so a test that hardcodes a database name, reads a fixed file path shared across
    workers, or asserts on a global auto-increment id starting at 1 passes alone and fails only under
    `--parallel` — the `ParallelTesting` facade's `setUpProcess`/`setUpTestCase` hooks are where per-worker
    setup belongs, not a shared beforeEach that assumes a single database.
26. **A test double for an external boundary should model the contract, not the happy path alone.** Point
    13 says fake the boundary; the point here is what the fake returns — a payment gateway fake that never
    produces a decline, a timeout, or a malformed response teaches the suite that failure cannot happen,
    which is exactly the class of bug that reaches production first. `Http::fake()`'s response sequencing
    exists so the same test file can assert both paths.
27. **`assertDatabaseHas` and `assertDatabaseCount` verify the row exists; they do not verify which
    operation put it there.** A test asserting the count went up by one after an action that was supposed
    to update an existing row instead of inserting a duplicate needs the id checked, or the assertion
    passes for the wrong reason — this is point 5's "assert the outcome" pushed one level deeper, because
    the outcome itself has more than one shape that satisfies a loose assertion.
28. **A snapshot or golden-file assertion is a substitute for naming what changed, not an upgrade on it.**
    Approving a diff without reading it defeats point 14's red-first guarantee just as completely as never
    running the test — a snapshot test earns its keep on output too large or too structural to assert
    field-by-field (a rendered PDF, a large JSON export), not as a shortcut around writing real assertions
    on a small response.
29. **Testing a form request or a policy directly, outside an HTTP call, tests the rule in isolation but
    not the wiring that invokes it** — a `FormRequest` bound to the wrong route, a policy never registered
    for its model, a middleware ordering that lets the request past validation first. Point 6's controller
    anti-pattern generalises here: the unit-level check is a useful addition to the feature test that
    exercises the endpoint, never a replacement for it.
30. **`Bus::fake()->assertChained([...])` proves the jobs run in the declared order, which
    `Bus::assertDispatched()` on each job separately cannot.** Asserting each link individually passes even
    if the chain was built in the wrong order or one link was dispatched standalone instead of chained —
    point 5's "assert the observable outcome" here is the order itself, not merely that every job eventually
    ran once.
31. **`Notification::fake()` and actually rendering a channel are two different questions, and a suite that
    only ever does the first never proves the message reads correctly.** `assertSentTo` proves the
    notification was triggered for the right recipient and channels; a snapshot or a direct
    `toMail()`/`toArray()` assertion on one notification (point 28) is what proves the content is not broken,
    and a suite that fakes every notification everywhere never notices a broken `toMail()` until it ships.
32. **`Event::fake()` without `except()` silences every listener in the test, including ones the test never
    meant to touch** — a model's own lifecycle listener that maintains a computed column, faked away by a
    blanket `Event::fake()` further up the same test class, quietly stops updating it, and the assertion
    passes for a row the real listener would have changed. `Event::fake(except: [...])` keeps the listeners
    the test is not actually exercising switched on.
33. **`Http::fake()` accepts a sequence of responses for the same URL, and that is how a suite proves point
    11's five outcomes are handled rather than only the happy path.**
    `Http::fake(['api.example.com/*' => Http::sequence()->push($ok)->push($rateLimited)->pushStatus(500)])`
    exercises a retry path end to end in one test, which is what point 26 asks a fake to model — a fake
    returning the same success on every call cannot tell the suite whether a retry loop exists at all.
34. **`Queue::fake()->assertPushedWithChain()` checks the chain attached to one job, and
    `assertPushedWithoutChain()` checks the opposite** — a job that used to chain a follow-up step and lost
    the chain in a refactor still passes `assertPushed()` alone, because the job itself was still dispatched;
    only the chain-specific assertion notices the follow-up step silently stopped happening.
35. **`Mail::fake()` proves a mailable was queued or sent; it does not prove the recipient received the
    right locale or the right attachment** — `assertSent(Invoice::class, fn ($mail) => $mail->hasTo($user->email) && $mail->locale === $user->locale)`
    is the version that actually checks the content point 5 asks for, rather than merely that some mailable
    of the right class went out.
36. **`Storage::fake()` gives each test an isolated in-memory-backed disk, and the assertion still has to
    name the path, not just the byte count.** `assertExists()`/`assertMissing()` on the exact path the code
    is supposed to write — a generated report keyed by the record's id, an upload stored under its owner's
    folder — catches the class of bug where a file is written successfully but to the wrong key, which
    `UploadedFile::fake()->create()` alone proves nothing about because the fake upload always succeeds.
