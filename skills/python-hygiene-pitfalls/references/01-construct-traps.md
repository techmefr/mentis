# python-hygiene-pitfalls §1 — Construct traps

Each point is one construct, the case where it works, and the case where it does not. The Ruff rule codes
are only pointers to where a linter detects the same trap; the rules are ours.

## 1.1 `assert` is not validation
1. **Assertions are removed when Python runs with optimisation (`-O`),** which is a common production
   setting, so a check written as `assert` disappears exactly where it matters. The Ruff documentation
   (S101) states that assertions should not be used for runtime validation of user input or to enforce
   interface constraints.
2. **The litmus test:** the assertion could be deleted without breaking the code. If removing it changes
   what the function does, it was a conditional and has to be a real `if` that raises.
3. **Raise a built-in exception that says what is wrong** (`ValueError` for a violated precondition), not a
   bare `AssertionError`.
4. **An assertion that documents a post-condition the code does not depend on is fine,** as is `assert` in
   pytest tests, where it is the mechanism. The Ruff rule exempts assertions inside a `TYPE_CHECKING`
   block, which exist only to satisfy a type checker; outside it, prefer a real check.

## 1.2 Naive datetimes
1. **`datetime.utcnow()` returns a naive datetime,** one that carries no timezone and so cannot be placed
   against other times unambiguously. Use `datetime.now(tz=UTC)` (`datetime.UTC` from Python 3.11, or
   `timezone.utc` before).
2. **`datetime.fromtimestamp(ts)` without `tz=` is also naive** (it uses the machine's local zone), so the
   same timestamp gives a different object on a different host. Pass `tz=`.
3. **Store and compare aware values in UTC and convert at the edges** for display. Comparing naive and aware
   values raises, which is the cheap failure; two naive values from different zones compare silently wrong.

## 1.3 File encoding
1. **`open()` in text mode without `encoding=` uses a locale-specific default,** not UTF-8 as many readers
   assume. A file written on one machine and read on another may decode differently or raise. The Ruff
   documentation (PLW1514) cites PEP 597, which recommends `encoding="utf-8"` as the default choice.
2. **If a locale encoding is intended, say so** (`encoding="locale"` on Python 3.10 and later), so the
   dependence is explicit.
3. **The same applies to `Path.read_text` and `write_text`,** which take an `encoding` argument.

## 1.4 Late-binding closures
1. **A lambda or nested function defined in a loop looks up the loop variable when it is called,** not when
   it is defined, so every callback sees the last value. Ruff documents the example: `[lambda x: x + i for
   i in range(3)]` called with 1 gives 3, 3, 3 (B023).
2. **Bind the value at definition:** a default argument (`lambda x, i=i: x + i`) or `functools.partial`.
3. **A callback registered in a loop and run later (a task, a button handler, a schedule) is the
   place this bites,** because by then the loop has finished.

## 1.5 Cached methods
1. **`functools.lru_cache` and `functools.cache` on a method keep a reference to `self` in the cache,** so
   the instance is never garbage collected while it is cached (B019). The cache is global to the function,
   not per instance, and it grows with every instance.
2. **Move the computation to a function that takes only its arguments** and call it from the method, or
   cache on the instance in an attribute. Enum methods are exempt, since members are singletons.
3. **A cache on a function of values (not objects with identity) is fine.** The settings loader cached
   once for the process is the legitimate use.

## 1.6 Mutable context variable defaults
1. **A `ContextVar` default is evaluated once, when the variable is defined,** and the same object is
   returned from every `get()` that has no value set. A mutable default (`[]`, `{}`) is therefore shared, and
   a change made in one request persists for the next (B039).
2. **Use `None` as the default and set a new object in the context when needed,** or use an immutable value.

## Verification
- The module's tests were run once with `python -O`.
- A timestamp created under one `TZ` setting was compared under another and agreed.
- A callback list built in a loop was called and each returned its own value.
- A method's instance was shown to be collectable after use, or the cache moved off the method.
