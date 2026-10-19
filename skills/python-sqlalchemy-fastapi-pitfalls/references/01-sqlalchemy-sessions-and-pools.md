# python-sqlalchemy-fastapi-pitfalls §1 — SQLAlchemy sessions and pools

A session is one transaction in progress and a pool is a fixed set of sockets. Both are cheap to misuse in a
single request and expensive at concurrency, so each rule names what breaks and when.

## 1.1 One session per concurrent task
1. **An `AsyncSession` is a mutable, stateful object that represents one transaction in progress.** The
   SQLAlchemy documentation says it is not safe to use in several concurrent tasks, and that APIs such as
   `asyncio.gather` should be given a separate session per task.
2. **Interleaved awaits on one session interleave statements on one connection:** the failures are
   confusing (a transaction state error, results attached to the wrong statement) and appear only when two
   tasks actually overlap, so a test that runs them in sequence passes.
3. **Create the sessions inside the tasks, from a session factory held at application scope.** A request
   gets one through a dependency; a fan-out inside a request opens one per branch.
4. **A background task gets its own session** and does not reuse the request's, which is closed when the
   response completes (`python-conventions` §7.5 gives the closed-session half).

## 1.2 `expire_on_commit` under asyncio
1. **Commit normally expires every loaded attribute, and the next access reloads it with a query.** In async
   code that implicit reload cannot be awaited, and it surfaces as the `MissingGreenlet` error the
   documentation describes: a database call made outside the greenlet context the async proxies set up,
   nearly always a lazy load.
2. **Create the session with `expire_on_commit=False`** (on the session or the session factory). The
   documentation says this is what allows attribute access after `commit`, and that expiration should
   normally not be needed under asyncio.
3. **If you need fresh data, say so:** `await session.refresh(obj)`, optionally with the attribute names to
   load, rather than expiring and hoping.
4. **It does not replace non-loading relationships.** Keep relationships declared to raise on lazy load
   and load what the caller needs with an eager strategy (`python-conventions` §7.3, §7.5); the two rules
   address different attributes.

## 1.3 Dispose of the engine
1. **Dispose of an async engine explicitly at shutdown** (`await engine.dispose()`), usually in the
   application's lifespan after the `yield`. The documentation says the connections held by the pool
   cannot be properly disposed of from `__del__`, so letting the engine fall out of scope leaves them open.
2. **An engine used from a different event loop has to be disposed first.** Passing an `AsyncEngine` from
   one loop to another with the default pool can raise a different-loop `RuntimeError`; dispose before
   reuse, or configure no pooling for that engine.
3. **In tests, create the engine inside the loop that uses it** (`python-testing-strictness` §3.3).

## 1.4 Forks and child processes
1. **Pooled connections must not be shared with a forked process.** TCP connections are file descriptors,
   and a child that inherits them uses the same socket as the parent concurrently: the documentation says
   the result ranges from non-working connections to interleaved messages, the latter being the common one.
2. **In a process pool initialiser, call `engine.dispose(close=False)`.** The documentation recommends this
   approach: the child starts with a new pool and does not close the parent's connections (parameter added
   in SQLAlchemy 1.4.33). Calling `dispose()` in the parent immediately before creating the child is the
   alternative; disabling pooling with `NullPool` is the blunt one.
3. **A server that forks workers after importing your application** has the same problem if the engine
   was created or used at import time: create it lazily, in the worker, or dispose in a post-fork hook.

## 1.5 The pool is a budget
1. **A queue pool allows `pool_size` plus `max_overflow` connections per engine;** the documented defaults
   are 5 and 10, so 15 per process. Each process has its own pool.
2. **The total is that figure times worker processes times replicas,** and it has to stay under the
   database's maximum connections with room for migrations, admin sessions and other services. This is
   arithmetic of ours, not a documented limit: the limit itself is a database setting.
3. **Scale-out multiplies it silently.** Raising workers per container or replicas per service without
   recomputing is how a healthy service starts getting "too many connections" at peak.
4. **Size the pool for concurrency inside one process,** not for total load: in an async app that is the
   number of tasks that hold a connection at once, which a limit on concurrent database work can cap.
5. **Check liveness separately** (`python-conventions` §7.20); a larger pool does not fix dead connections.

## Verification
- Two concurrent tasks run with separate sessions; a deliberate shared session fails the test.
- After a commit, an attribute is read without a database call and without `MissingGreenlet`.
- With the worker count and replica count written down, the product is below the database limit.
- A child process was started and its first query used a connection the parent did not hold.
