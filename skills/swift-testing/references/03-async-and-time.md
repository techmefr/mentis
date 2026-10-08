# swift-testing §3 — Asynchronous code and time

The Apple documentation pages "Testing asynchronous code", the confirmation function, the XCTest `fulfillment(of:)`
and `wait(for:)` pages and "Migrating a test from XCTest", read 2026-10-08, with one MIT-licensed iOS testing skill
for the hang and clock rules. Confirmation ranges need a Swift Testing release that accepts a range; the pages do not
number it.

## 3.1 Wait with `await`, and use a confirmation for events
1. **Mark the test `async` and `await` what you test.** Swift Testing integrates with Swift concurrency, so most
   asynchronous code needs nothing more. The page migrating from XCTest says to prefer Swift concurrency to an
   expectation wherever possible.
2. **A completion-handler API without `await` is bridged with a checked continuation,** `withCheckedContinuation`,
   which turns the call into an awaitable one (the page names it for this).
3. **Use a confirmation for an event you cannot await:** a delegate callback, an event handler, an event that
   happens more than once or never. Call `confirmation()` with the code under test in its closure and call the
   confirmation object each time the event occurs.
4. **A confirmation is checked when its closure returns; it does not suspend.** The page says that, unlike an
   `XCTestExpectation`, it does not block or suspend the caller waiting for a condition: the event must happen
   before the closure returns, or an issue is recorded. For a callback that fires later, bridge it with a
   continuation (the MIT skill's fix for a confirmation that fails against a completion-handler API).
5. **The expected count is part of the assertion.** The default is exactly one occurrence. Pass a number for more,
   `0` to assert the event never happens, or a range that has an explicit lower bound (`1...`, `5...`, `1 ... 5`,
   `0 ..< 100`). The page requires a lower bound: without one the library cannot tell whether an issue should be
   recorded when there were zero occurrences.
6. **An expectation can be fulfilled more than once only if you say so.** `XCTestExpectation` records an issue when
   fulfilled too many times unless configured; a confirmation with a range expresses the same intent.

## 3.2 Waiting in async XCTest code
1. **Use `await fulfillment(of:timeout:)` in an `async` XCTest method.** The Apple page names it the
   concurrency-safe alternative to `wait(for:)`, and the `wait` page says to use `fulfillment` in Swift code that
   requires concurrency.
2. **Never call the blocking `wait(for:)` there.** It blocks the current thread; if the fulfilment needs that thread
   (a `@MainActor` task), the test deadlocks. This mechanism is the MIT skill's; the Apple pages only direct you
   away from `wait`. The blocking form stays acceptable in a synchronous XCTest method.
3. **Give every wait a timeout.** With no timeout the wait runs until the test's execution allowance. The
   `fulfillment` page says to enable test timeouts so an unfulfilled expectation cannot hang the run.
4. **Swift Testing has the same safety net: the time-limit trait.** Set it on any test that waits on asynchronous
   work, so a continuation that is never resumed, or an `AsyncStream` that never finishes, fails the test instead of
   hanging the suite. When it is applied at suite and test level, the MIT skill reports the shorter duration wins.

## 3.3 Time is an input
1. **Do not wait on the wall clock.** A sleep in a test is a timing guess: fast machines pass it and slow CI fails
   it. Wait on the event (a confirmation, a continuation, an `await`) or advance a controlled clock.
2. **Inject a `Clock` into code that sleeps or measures time,** instead of calling `Task.sleep`, `ContinuousClock`
   or `Date()` directly. Tests then use an immediate clock when timing does not matter and a clock they advance by
   hand when it does. The MIT skill names two such clocks from a third-party package, which was not vetted here, and
   warns that an immediate clock collapses all time to zero and cannot test debounce, throttle or delay logic.
3. **Do not feed a confirmation from a publisher that debounces, throttles or delays,** or that receives on another
   scheduler: the count is checked when the closure returns, before the event arrives (the MIT skill; the pages read
   do not state it).
4. **Fix the data too.** `Date()`, `UUID()` and random values in test data make a run unrepeatable.
