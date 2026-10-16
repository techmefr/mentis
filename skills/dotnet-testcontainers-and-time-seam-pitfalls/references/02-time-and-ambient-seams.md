# dotnet-testcontainers-and-time-seam-pitfalls §2 — Time and ambient seams

Source: the dotnet/skills testability-obstacle skill (MIT, commit 6364668, read 2026-10-16), rewritten. Where a
point is not in the skill it says "own guidance".

## 2.1 Prove the obstacle, then take the smallest seam
1. **Add a seam only when a test is impossible without one.** If the dependency is already injected or passed in,
   write the test with a fake through the existing seam and change no production code.
2. **Wrap only the members the target behaviour uses**, with a default that delegates straight to the original
   API; do not move business logic into the wrapper or fix unrelated defects while there.
3. **Pick the seam by dependency**: time and timers take `TimeProvider`; a file read or write takes the
   repository's existing abstraction, otherwise one injected delegate or a one-member interface; HTTP takes the
   existing typed client or handler; randomness takes an injected function when one final value is enough and a
   `Random` or small generator when there is state; environment, console and process take a minimal interface.
4. **Keep the production default wired.** Update every composition root so production still uses the real
   dependency, pass it explicitly from a hand-written factory and do not add a DI container to a library for
   the purpose. Build the production project before writing the tests, because a compile failure there is a
   seam problem.
5. **Keep the public API as it was.** A test-only constructor is internal, with a friend-assembly entry only when
   the exact test assembly is known and no public seam already accepts the fake.

## 2.2 Time
1. **Inject `TimeProvider` and use `FakeTimeProvider` in tests.**
2. **Use the overloads that take the provider instead of inventing a delay wrapper**: `Task.Delay` with the
   provider, `CancellationTokenSource` with a delay and the provider, and `PeriodicTimer` with the provider
   where the target framework offers it.
3. **Convert the current-time calls exactly**: UTC time becomes the provider's UTC now, local time its local now,
   and converting a UTC value through `.UtcDateTime` keeps the UTC kind, where `.DateTime` loses it.
4. **Test a delay by starting the operation, asserting it is incomplete, advancing the fake clock, then
   awaiting.** For a deadline, advance to just before it and assert the task is still incomplete, then cross it;
   an assertion straight after the start proves nothing about the boundary. Never wait for wall-clock time.

## 2.3 A static API that must keep its shape
1. **Use a scoped ambient override only when injection is impossible**, for example a public static API that
   cannot change.
2. **Store the value in `AsyncLocal<T>`, not a thread-static field**, so it flows across `await`.
3. **The scope returns a disposable that restores the previous value**, never an assignment to null, and nested
   scopes are disposed in reverse order. Store the provider itself in the slot, not a stack or list, because
   child contexts can inherit the same mutable object and corrupt each other.
4. **A mutable fake provider is created fresh inside each parallel flow**, not mutated from an inherited parent.
5. **Tests for such a seam cover substitution, nested restoration, restoration after an exception and two
   overlapping async flows seeing only their own override**, using distinct values so a cleared slot cannot pass
   by accident. Do not change process environment variables to test an environment seam.

## 2.4 Assertions and completion
1. **Do not compute the expected value with the production code under test**; write the literal expectation
   (own guidance, from the review's testability item; the skill's own rule is the next point).
2. **Assert the business result and one observable that proves the fake drove the path**, with no real file,
   network, environment change or sleep.
3. **Read the test summary, not only the exit code.** Zero discovered tests, a build with no test run or any
   failing test means the task is not done. For deterministic serialised text across platforms, use the
   format's explicit separator rather than the platform's newline, and assert the literal.
4. **Use the test project's existing framework and assertion style**; never add a hand-written attribute or
   stand-in type to make a test compile.
