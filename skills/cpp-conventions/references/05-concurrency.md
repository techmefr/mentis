# cpp-conventions §5 — Concurrency

> Section 5 of `skills/cpp-conventions`. Read it when a thread, a task, a mutex, a condition variable, an
> atomic, a coroutine or a callback run under a lock appears. The C-level mutex and signal rules
> (`skills/c-conventions` §4) apply to the underlying primitives. The other sections and the guardrails stay
> in `SKILL.md`.

1. **Assume your code runs in a multi-threaded program.** A function in a library may be called from any
   thread, and code that is single-threaded today is called concurrently tomorrow. Avoid data races (two
   unsynchronised accesses, one a write, are undefined), and minimise the explicit sharing of writable data:
   pass data by value, share immutable data, give each task its own slice.
2. **Locks are RAII objects, always.** Never call `lock()` and `unlock()` by hand: an exception or an early
   return leaves the mutex held. Name your lock objects (an unnamed temporary releases at once and protects
   nothing). To take several mutexes at once use the facility that locks them together in a deadlock-free way.
   Declare the mutex in the same class as the data it protects, so the pairing is visible.
3. **Run no foreign code under a lock.** A callback, a virtual call or a caller-supplied
   functor may take other locks or re-enter this code, and that is how deadlocks start. Copy what you need out under
   the lock, release it, then call. Keep critical sections short.
4. **Wait on a condition, never without one.** A bare wait can miss a wake-up or wake just to find nothing to
   do; give it a predicate that is re-tested under the mutex.
5. **Threads are scoped containers.** Prefer a joining thread whose lifetime is bounded by the scope that
   created it, so the pointers it uses stay valid; a thread that may outlive its scope is a global container
   and its data must be as long-lived. **Never `detach()` a thread:** it becomes impossible to monitor, to
   communicate with or to know whether it completed or is still using data that is going away. Give a thread
   small inputs by value, not by reference or pointer; data that unrelated threads must keep alive
   belongs behind a shared pointer.
6. **Think in tasks, not threads.** Return a value from a concurrent task with a future, spawn tasks with the
   library's task facility, minimise thread creation and destruction and context switching.
7. **`volatile` is not synchronisation.** In C++ it is for talking to memory outside the language's model
   (hardware registers); an atomic is the tool for shared flags and counters.
8. **Lock-free programming is a last resort.** Do not use it unless you absolutely have to; distrust your
   hardware and compiler combination, study the literature first, and never write your own double-checked
   locking: use the library's one-time initialisation facility.
9. **Coroutines.** Do not hold a lock or other synchronisation primitive across a suspension point: the
   coroutine may resume on another thread (undefined for a lock acquired on the first) or the same thread
   may be re-entered and deadlock on the lock it already holds. Do not write coroutines as capturing lambdas, and
   do not pass coroutine parameters by reference: the referenced object can be gone when the coroutine
   resumes.
10. **Validate with tools.** Run the thread sanitizer on the test suite of any threaded code (`c-conventions`
    §5.9); a race that has never failed in a test is not proof of absence.
