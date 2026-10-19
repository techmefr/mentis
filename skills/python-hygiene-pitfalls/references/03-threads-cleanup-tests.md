# python-hygiene-pitfalls §3 — Threads, cleanup and tests

Three places where the first success proves little: a shared value under a second thread, a resource whose
release is left to the garbage collector, and a test that passes for the wrong line.

## 3.1 Do not rely on the atomicity of built-in operations
1. **A dictionary or list operation that appears atomic is not guaranteed to be.** The Google guide says
   there are corner cases (for example when `__hash__` or `__eq__` are Python methods), and that you should
   not rely on atomic variable assignment either, since that depends on dictionaries.
2. **Pass data between threads with `queue.Queue`.** It is the preferred mechanism in the guide.
3. **For shared mutable state use the `threading` locks,** and prefer a `threading.Condition` to lower-level
   locking primitives when a thread has to wait for a state change.

## 3.2 Release resources with `with`, not `__del__`
1. **Close files, sockets, database connections and similar stateful resources explicitly,** by a `with`
   block where there is one. The Google guide lists the cost of leaving them open: exhausted descriptors,
   files that cannot be moved or deleted, and reads or writes after the resource was logically finished.
2. **A finalizer is not a guarantee.** There is no promise of when `__del__` runs, and different Python
   implementations behave differently; a reference kept in a global or a traceback keeps the object alive
   longer than intended. The guide says relying on finalizers for cleanup with observable effects has led
   to major problems across languages.
3. **A class that owns a resource implements the context manager protocol** (`__enter__` and `__exit__`, or
   an `@contextmanager` function) so its callers can use `with`, and its owner closes it.
4. **If the resource needs async cleanup, use an async context manager.** Cleanup that awaits cannot run
   in a finalizer at all.

## 3.3 One statement in `pytest.raises`
1. **The body of `with pytest.raises(...)` is the single statement that raises.** With several statements,
   the test passes when an earlier one raises the expected exception, and the later ones, including your
   assertions, never run. The Ruff documentation (PT012) describes this.
2. **Do the setup before the block** and the assertions after it. The block contains only the call under
   test.
3. **Match the message when the type alone is too broad** (the `match` argument), so a different error of
   the same type does not satisfy the test.
4. **A test that passes for the wrong reason is the case in `python-conventions` §8.14:** make it fail once
   by changing the code under test.

## Verification
- A scratch version of the raises-test that raises in the setup line fails.
- A shared structure used by two threads was exercised under a loop of both and stayed consistent, or was
  replaced by a queue.
- A resource owner was used in a `with` block and its resource was closed when the block ended, observed
  by an error on use afterwards.
