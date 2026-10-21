# laravel-feature-test-pitfalls §3 — Isolation and determinism

> Part 3 of `skills/laravel-feature-test-pitfalls`. Read it when a test fakes something, or fails depending on
> time or order. Sourced from `.ai/laravel/skill/testing-best-practices/rules/isolation.blade.php` in
> `laravel/boost` (commit `f1411f9`), read 2026-10-16, the variant for PHPUnit. Sentences marked "own
> guidance" are ours.

1. **Control the four sources of flakiness.** The source says tests that depend on actual time, randomness,
   sleeping or network calls can fail for reasons unrelated to the code, and that all four must be
   controlled. For each dependency choose the first option that applies: a framework fake for facades such as
   events, queues, mail, notifications, storage, the HTTP client, time and sleep (the framework documents the
   event, queue, time and sleep fakes and the random-string hook; the exceptions fake and the lazy refresh trait
   exist in the 12.x source); then a fake implementation
   the application itself provides; then a mock of a container-resolved contract, only when the real
   implementation leaves the process or is nondeterministic; otherwise the real thing, including the database.
   A framework fake keeps the real code path while a mock replaces the dependency.
2. **Name the classes in event and queue fakes.** Pass class names when you know what the code dispatches,
   because a fake without names can hide an unexpected dispatch. Use the no-name form only when the test asserts
   the complete result, including that nothing else was pushed. Write one assertion per fake (dispatched, or not
   dispatched), and assert the job's or event's data when the data is part of the behaviour. Create each fake in
   the test that needs it, not in `setUp()`.
3. **Create prerequisite factory records before faking events.** Factories rely on model events, such as a
   creating hook that generates a UUID; a fake with no class names suppresses them and the factory can then
   produce an invalid model. Fake first only when a factory event is the thing under test, and pass that
   event's class name. The framework's event testing section gives the same advice: call the fake after the
   factories when they rely on events such as one that generates a UUID.
4. **No stray HTTP, no real clock, no real sleep.** The source's rules: call `Http::preventStrayRequests()` so
   an unfaked request fails without reaching the network; fake the exact endpoint each test calls and never
   call the HTTP fake without one, since that accepts unexpected requests; freeze or move time in every test
   that depends on a date or period with the framework helpers (`freezeTime`, `travelTo`, `travel`,
   `travelBack`) and not by setting the test-now value by hand; fix generated strings with
   `Str::createRandomStringsUsing()` when a test asserts an identifier or slug; use `Sleep::fake()` and assert
   the sleeps requested; and restore time and randomness after each test if the suite does not do it.
5. **Assert reported exceptions with the exceptions fake.** Use `Exceptions::fake()` to assert the application
   reports the right exception; the source says not to use `withoutExceptionHandling()` for this because it
   changes the response under test.
6. **Mocks: declare before, spy after, and use the container's mock helper.** `shouldReceive()` before the action
   declares an expectation; `shouldHaveReceived()` after is a spy; for an argument that equality cannot
   describe, such as one field of a value object, use `Mockery::on()` or `withArgs()`. Put a mock in the
   container with the test case's mock helper, and do not build a PHPUnit mock for a class Mockery can double,
   because the project uses Mockery (the source's statement about the project it targets; follow your
   project's choice).
7. **Use the real database.** Run real queries against real records; do not mock the query builder, because the
   test then asserts the mock. Assert the exact keys of `toArray()` when the serialised shape is a contract, so
   a newly exposed attribute fails the test. Test behaviour that the schema causes (dependent records deleted
   through a cascade) and not the database engine's cascade. Prefer the lazy database refresh trait over the
   plain one, so a test that does not use the database does not run the migrations.
