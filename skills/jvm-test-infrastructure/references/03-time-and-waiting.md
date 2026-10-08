# jvm-test-infrastructure §3 — Time and waiting

`testing-anti-patterns` §3 states the general rule: wait for the condition, not for a duration. This section
is the JVM tooling for it: Awaitility for polling, and an injected `java.time.Clock` for the instant the code
under test sees.

## 3.1 Poll, with a timeout
1. **Use Awaitility instead of `Thread.sleep`.** Its `await()` polls a condition until it holds or a
   timeout expires; the timeout is explicit with `atMost(...)`. By default it waits up to 10 seconds and then
   throws a `ConditionTimeoutException`, which fails the test rather than hanging.
2. **Assert inside the poll when the condition is an assertion.** `untilAsserted` retries an assertion
   (for example an AssertJ one) until it passes, and reads the value fresh on every attempt, so the failure
   message is the real mismatch and not a timeout.
3. **Tune the polling when you must,** with a poll delay and interval, and name the wait (`await("alias")`)
   so a failure says which of several waits in a test it was.
4. **Exceptions during the condition can be ignored on purpose.** Awaitility can treat exceptions thrown while
   evaluating the condition as "not yet" and keep polling; use it for the call that fails until the system is
   ready, and not to hide a real error.
5. **Polling in the test's own thread is an advanced option** (`pollInSameThread`), and the library warns
   that it cannot interrupt a condition that waits forever or for a long time there.
6. **A deliberate duration is for the one case where the duration is the thing under test.** There,
   `atLeast` and `during` express a minimum or a stable period without a sleep.

## 3.2 Inject a Clock
1. **Take a `java.time.Clock` as a dependency and ask it for the time,** instead of calling `Instant.now()`
   or `LocalDate.now()` with no argument. The `Clock` documentation states its purpose: to allow alternate
   clocks to be plugged in as and when required, and to simplify testing, with dependency injection as the
   intended way to supply it.
2. **In a test, supply a fixed clock** (`Clock.fixed(instant, zone)`), or an offset clock to move time forward
   from a base. The production configuration provides the system clock (`Clock.systemUTC()` or a clock with
   the zone you mean).
3. **Pick the awkward instants on purpose:** midnight in the business time zone, the last day of a month, a
   daylight-saving transition, a leap day. A test that "passes except around midnight" is a test that used the
   real clock.
4. **A clock that must move during the test is a small test-only class** wrapping a mutable instant, rather
   than a sleep or a repeated mock.

## 3.3 Checks
- No `Thread.sleep` in the test sources, and no `now()` call without a clock in the classes under test.
- A wait that times out fails with a message naming the wait.
- The same test run with the clock set a day, a month and a year later behaves as the business rule says.
