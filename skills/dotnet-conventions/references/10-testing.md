# § 10 — Testing

> Section 10 of `skills/dotnet-conventions`. Read it when a test project, a fixture, a double, an integration
> test against the HTTP surface or a database-backed test is written or modified. The doctrine of *what* to
> test and the default-fail contract live in `skills/tdd`; the ways a green suite lies are in
> `skills/testing-anti-patterns`; this section is the .NET mechanics of both.

1. **Unit and integration tests live in separate projects.** An integration project references the web
   host, the database provider and a container library; a unit project references none of them. Mixing the
   two means the fast suite cannot be run without the slow suite's packages, and the day someone adds a
   `using` for the host into a unit test nothing stops it. The test tree mirrors the source tree, one test
   class per class under test, so a moved source file orphans its test visibly.
2. **A test class is constructed once per test.** xUnit builds a new instance for every `[Fact]`, so
   instance fields are fresh state and the constructor is the arrange step shared by the class. Anything
   asynchronous goes through `IAsyncLifetime` (`InitializeAsync`/`DisposeAsync`), never a `.Result` in the
   constructor. A `static` field in a test class is the one way to leak state between tests, and it is
   forbidden for the same reason it is in production code (§4).
3. **A fixture is shared state with a name, so decide who may mutate it.** A class fixture is built once for
   the tests of one class; a collection fixture is built once for every class placed in that collection.
   Tests inside one collection run serially and different collections run in parallel, so a database or a
   process-wide setting shared through a fixture is either read-only for the tests or isolated per test
   (point 14). A fixture that "works" because the suite happens to run in one order is the flaky test that
   has not failed yet.
4. **Name the behaviour, not the method.** `Handle_ReturnsConflict_WhenSlotAlreadyTaken` says what broke
   when it goes red; `Handle_Test3` says nothing. Underscores in test names are the readable convention and
   the naming analysers are scoped away from the test project for exactly that reason (Guardrails). One
   logical assertion per test: several `Assert` calls on one result are fine, two acts are two tests.
5. **`[Theory]` is for one behaviour over many inputs, never for several behaviours behind a branch.** A
   theory whose body switches on a parameter to decide what to assert is a table of unrelated tests with the
   failure messages removed. Use `TheoryData<T1, T2>` rather than `object[]` so the compiler checks the row
   shape, and give a case a name (the display name, or a descriptive first argument) so a red row can be
   read without opening the file.
6. **The built-in `Assert` class is enough.** An assertion library is a dependency like any other, and a
   dependency has a licence that can change under you: a widely used assertion library moved to a paid
   licence for commercial use at its 8.0 release. Before adding one, read the licence of the version you
   would resolve, and pin the major. If the project already has one, keep using it consistently in the
   files that use it; mixing two assertion styles in one file is a half-migrated state, worse than either.
7. **Assert the typed result, not its text.** Asserting on `ToString()`, on an exception's message or on a
   serialised string couples the test to wording the next person will legitimately change. Assert the status
   code, the typed property, the exception type and its structured members. Where the message *is* the
   contract (a problem-details `type` URI, an error code), assert exactly that field.
8. **A double replaces a collaborator the code under test does not own.** For an outbound boundary (an HTTP
   client, a queue, a mail sender) a substitution library that records calls is fine, and the assertion is
   on the *consequence* observable by the caller before it is on the call. For a collaborator with
   behaviour (a repository, a cache), write a small in-memory fake that honours the contract, because a
   mock configured to return what the test wants proves nothing about what the real one returns. Verifying
   that a mock was called is the first anti-pattern in `skills/testing-anti-patterns`.
9. **Do not mock the logger; capture it.** `ILogger<T>` is a message sink, and a substitute of it cannot
   tell the difference between a message that carries structured state and one that does not. The
   framework's testing package provides a fake logger that records each entry with its level, event id and
   structured values, so the test asserts "a warning with this event id was written" rather than the
   rendered sentence. Test a log only when the log is the observable (an audit trail, an operator alarm).
10. **Time is injected, so the test advances it.** Production code takes a `TimeProvider` (§2); the test
    registers the framework's fake time provider, sets the start instant explicitly and advances it. A test
    that calls `Task.Delay` or `Thread.Sleep` to let a timer fire is a bet on machine speed. A fixed instant
    also pins the culture and time-zone assumptions the test would otherwise inherit from the build agent.
11. **Cancellation is a behaviour with its own test.** Pass `CancellationToken.None` only where
    cancellation is not the subject. To test it, pass an already-cancelled token and assert that the method
    ends in `OperationCanceledException` (`Assert.ThrowsAnyAsync`, since the exact derived type varies) and
    that no side effect happened. A method that takes a token and a test suite that never cancels it means
    the propagation rule of §1 is untested. xUnit v3 exposes the test's own token through its test context;
    on v2 create a source in the test.
12. **Async tests return `Task`, and nothing in a test blocks on one.** `async void` swallows the failure
    and the runner reports green; `.Result` and `.Wait()` can deadlock under a synchronisation context and
    always wrap the failure in an aggregate. The xUnit analysers flag both, and the build should treat them
    as errors in the test project.
13. **Go through the HTTP surface for anything the framework wires.** `WebApplicationFactory<TEntryPoint>`
    boots the real host in memory, so routing, model binding, validation, the middleware order (§6),
    authorisation and serialisation all run. Calling a controller method directly bypasses every one of them
    and tests a class the framework never invokes that way. An application using top-level statements has an
    internal `Program` class; expose it with a `public partial class Program` declaration or an
    `InternalsVisibleTo`, not by changing the application's structure for the tests.
14. **Replace what leaves the process, keep what is yours.** The factory's `ConfigureTestServices` runs
    after the application's own registration, so the test swaps outbound HTTP handlers, the clock, the
    message bus and the email sender, and leaves the validators, the policies and the handlers alone. A
    service replaced because "it was easier" is a path the suite no longer covers; list the replacements in
    one place so the reader knows exactly what the test did not exercise. A host that validates its service
    graph at startup (§2) gets that validation for free in the first integration test.
15. **Authenticate through the real pipeline, and refuse through it too.** Register a test authentication
    scheme whose handler builds the principal from request headers, so the policy, the role/permission
    requirement and the fallback policy of §3 all execute against a principal the test chose. Never disable
    authorisation, never replace the fallback policy with `AllowAnonymous`, never bypass the middleware by
    calling the handler directly. Every protected endpoint needs the negative pair: anonymous gets 401, an
    authenticated caller without the permission gets 403, and the test names which of the two it asserts.
16. **The in-memory EF provider is not a database.** It has no foreign keys, no unique constraints, no
    transactions, a different case-sensitivity model and no SQL translation, so a query that is wrong
    against the real engine passes against it, and a constraint violation never fires. The EF Core
    documentation says as much and recommends testing against the production engine. A lighter embedded
    engine is a different engine with its own dialect; use it only where the queries are portable by
    design (§6) and say so.
17. **Test the real engine in a throwaway container.** Start the production engine (same major version,
    pinned image tag) from a container library, apply the real migrations, and run the repository and query
    tests against it. Start the container **once per fixture**, not per test; the library waits for
    readiness, and the test must not add a sleep on top. When no container runtime is available the test
    must fail with a message or be skipped with an explicit reason; a test that quietly passes because there
    was nothing to connect to is the default-is-failure violation (`WORKFLOW.md` §3).
18. **Isolate data per test, not per run.** A shared container with shared rows makes the second test depend
    on the first. Choose one: a transaction rolled back at the end of the test, a reset utility that
    truncates between tests, or a database per class built from a template. Rows created in a test are
    created by that test's builder, with explicit values for everything the assertion reads. Parallel
    collections never share a database.
19. **Migrations are tested as an artefact.** One test applies every migration to an empty database and
    asserts it reaches the model's expected schema; another fails when the model has changes that no
    migration captures. These two catch the failure that only shows on the deploy: a migration that works
    incrementally and cannot create the database from nothing, or a model edited without its migration.
20. **Test data comes from builders that produce a valid minimal object.** A builder with sensible defaults
    and `With…` overrides keeps each test stating only what it cares about. If a data generator supplies
    random values, seed it, so a failing run reproduces; and keep dates, ids and amounts that the assertion
    reads explicit rather than generated.
21. **Test the configuration that fails at boot.** A host built with an invalid options section must refuse
    to start (`ValidateOnStart`, §2). Build the host with the bad value in the test and assert the startup
    exception; this is the only place the rule is proven, because the application's own run never uses the
    bad value.
22. **Background work is tested through the unit it executes, not through the host's timing.** A hosted
    service's loop body is a method; call it with a fake clock and an in-memory dependency and assert the
    outcome. Starting the host and waiting for a side effect is the condition-based wait of
    `skills/testing-anti-patterns` with a timeout at best, and a sleep at worst.
23. **Null-forgiving in a test is an assertion in disguise.** `result!.Name` states "this cannot be null"
    without checking it, and a null shows up as a `NullReferenceException` in the wrong place. Assert
    not-null first, then use the value, so the failure names the missing object.
24. **Coverage reports lines executed, not behaviour verified.** The coverage collector is a tool for
    finding the failure path nobody exercised (the `catch`, the refused request, the cancelled token), not a
    target. Where the project's testing doctrine sets a floor it applies and this block adds none of its own;
    whoever owns the number states beside it which code is excluded (generated code carries the standard exclusion attribute) so the number
    cannot be met by moving code around. A test written only to touch a line is the worst kind: it passes
    whatever the line does.
25. **Read the test run, not only its exit code.** The output lists skipped tests and the reason; a suite
    that is green with forty skipped tests has not run forty tests. Build warnings from the test project
    belong to the diff that introduced them; reading the artefact and not the exit code is `skills/gate`, step 5.
