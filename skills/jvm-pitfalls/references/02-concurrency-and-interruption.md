# jvm-pitfalls §2 — Concurrency and interruption

These are the concurrency mistakes that pass every single-threaded test. The general rules (a collection
shared between threads, the shortest synchronised block, a bounded executor that is shut down) are in
`java-conventions` §3; this section adds the specific traps. Each names the Error Prone check that finds it.

## 2.1 Locks and visibility
1. **Never lock on a boxed primitive.** `valueOf` can return a cached instance, so the "private" lock is
   shared with any other code that locked on the same value. Use a dedicated `private final Object lock`.
   Check: `LockOnBoxedPrimitive`.
2. **Never synchronise on a field that is not `final`.** If it is never reassigned, make it `final`; if it
   must change, add a separate private final lock object and guard every access with it. Check:
   `SynchronizeOnNonFinalField`.
3. **A `volatile` field makes each read and write visible, not a sequence of them atomic.** `count++` and
   `total += x` on a volatile are a read, a change and a write, and two threads interleave them. Use an
   atomic type (`AtomicInteger`) or guard every update with the same lock. Check: `NonAtomicVolatileUpdate`.
4. **Double-checked locking needs a `volatile` field.** Without it the compiler may reorder the accessor and
   another thread can see a partly built object. The correct form reads the field into a local, checks it,
   locks, checks again, then assigns. For code that is not performance-critical, prefer a synchronised
   accessor, which is simpler and correct. Check: `DoubleCheckedLocking`.
5. **`wait()` and `Condition.await()` sit in a `while` loop that re-tests the condition.** A thread can wake
   without being notified (a spurious wakeup), so an `if` lets it proceed while the condition is still false.
   The condition check also belongs inside the synchronised block, or it races with the code that sets it.
   Check: `WaitNotInLoop`.
6. **Call `lock()` immediately before the `try` whose `finally` unlocks.** `lock()` may throw an unchecked
   exception, in which case an unlock in the `finally` would run for a lock never taken; and any statement
   between `lock()` and `try` that throws leaves the lock held forever. Move such statements before the
   `lock()` or inside the `try`. Check: `LockNotBeforeTry`.
7. **Store a `ThreadLocal` in a `static` field.** As an instance field, each thread keeps one value per
   instance of the containing class, so the number of live values is threads times instances, each alive as long
   as its thread. Check: `ThreadLocalUsage`.

## 2.2 Interrupts
1. **Do not hide `InterruptedException` inside a catch of `Exception` or `Throwable`.** Interruption must be
   handled on purpose; a broad catch makes it impossible to see that it can happen. Catch the specific
   exception types, or a multi-catch that does not include `InterruptedException`, and handle that one
   separately. Check: `InterruptedExceptionSwallowed`.
2. **When you stop because of an interrupt, restore the flag.** Call `Thread.currentThread().interrupt()` before
   rethrowing as another exception type or returning, so callers up the stack can still see it. Calling
   `Thread.interrupted()` instead clears the flag. Check: `InterruptedInCatchBlock`.
3. **`Thread.join()` can be interrupted.** Code that must wait for the thread to end loops until the join
   succeeds (or uses a helper that does) rather than giving up on the first interrupt. Check:
   `ThreadJoinLoop`.

## 2.3 Futures and finally
1. **Never ignore the return value of a method that returns a `Future`.** Such methods report failure by
   returning a future that eventually fails, so dropping it means you never find out; nested futures can
   also lose cancellation or hide exceptions. Check: `FutureReturnValueIgnored`. For a
   `CompletableFuture` started with `supplyAsync`, attach a handler (`exceptionally` or `handle`) that logs
   or recovers, or keep the future and wait on it.
2. **A `finally` block always completes normally.** A `return`, `throw` or `break` in it cancels the outcome of
   the `try` and `catch`, and a `close()` that throws in it replaces the first exception, which is lost. Prefer
   `try-with-resources`: if the body and the close both fail, the close failure is attached to the first as a
   suppressed exception (Java 7 and later). Check: `Finally`.

## 2.4 Checks
- Error Prone on, the checks above at error level, build clean.
- A test that interrupts the thread under test and asserts the flag is still set afterwards and the work
  stopped (§2.2).
- A test whose async task throws: the failure reaches a log line or the caller, not nothing (§2.3).
- Search for `synchronized (` on a field and for `ThreadLocal<` that is not `static`.
