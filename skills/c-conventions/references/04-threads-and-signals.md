# c-conventions §4 — Threads and signals

> Section 4 of `skills/c-conventions`. Read it when a thread, a mutex, a condition variable, an atomic object
> or a signal handler appears. Bracketed identifiers trace to the published standard in
> `references/origin.md`. The other sections and the guardrails stay in `SKILL.md`.

1. **A data race is undefined behaviour, not a flaky result.** Two threads touching the same object, one of
   them writing, without synchronisation [CON43]. Every object shared between threads has a synchronisation
   story written next to it: which mutex protects it, or that it is atomic, or that it is immutable after
   publication. A mutex protects the data it is declared with and nothing adjacent, so keep unrelated data
   from sharing a protected structure or a bit-field word [CON32, POS49].
2. **Shared objects live long enough.** An object handed to a thread has static or allocated storage, not
   automatic storage of the creating function, which may return first [CON34, POS50]. Clean up
   thread-specific storage [CON30]. Do not destroy a mutex while it is locked [CON31] or unlock or destroy one
   that another thread holds [POS48].
3. **Lock in a fixed order.** Two locks taken in opposite orders on two paths deadlock [CON35, POS51]. Document
   one global order and take multiple mutexes in that order. Do not perform an operation that can block while
   holding a lock [POS52]; copy the data out under the lock and block outside it.
4. **Condition variables are waited on in a loop and with one mutex.** A wait can wake spuriously, so it sits in
   a loop that re-tests the predicate [CON36]; a condition variable pairs with exactly one mutex [POS53]; take
   care to keep liveness when signalling [CON38]. Any function documented to fail spuriously (a weak
   compare-and-exchange) is retried in a loop [CON41].
5. **Atomics.** Do not refer to an atomic object twice in one expression, since the second reading may differ
   from the first [CON40].
6. **Join or detach a thread exactly once** [CON39]. A thread you cannot account for at shutdown is a leak and a
   race. Do not use signals to end threads [POS44], and do not use threads that can be cancelled
   asynchronously [POS47].
7. **Library functions are not automatically thread-safe** [CON33]. Use the re-entrant variant of a function
   that keeps hidden static state, or serialise calls to it. With POSIX threads on a GNU library build the
   multithreaded C code with the exception-propagation flag of §5.6.
8. **Signal handlers do almost nothing.** A handler calls only functions documented as safe in that context
   [SIG30], does not touch shared objects other than a flag of the dedicated atomic signal type [SIG31], does not
   re-install itself while interruptible [SIG34], and never returns from a computational-exception handler
   (a divide-by-zero or similar) [SIG35]. The usual shape is: the handler sets a flag or writes to a
   self-pipe, and the main loop does the work. Do not call `signal()` in a multithreaded program [CON37].
