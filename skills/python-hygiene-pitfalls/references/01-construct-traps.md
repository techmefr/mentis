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
   against other times unambiguously. The datetime page marks it deprecated since 3.12 and says to use
   `datetime.now()` with `UTC`: `datetime.now(tz=UTC)` (`datetime.UTC` is an alias added in 3.11, `timezone.utc`
   works before).
2. **`datetime.fromtimestamp(ts)` without `tz=` is also naive** (it uses the machine's local zone), so the
   same timestamp gives a different object on a different host. Pass `tz=`. `utcfromtimestamp()` is
   deprecated since 3.12 for the same reason.
3. **Store and compare aware values in UTC and convert at the edges** for display. Comparing naive and aware
   values with `<` or `>` raises `TypeError`, which is the cheap failure; but `==` between a naive and an aware
   value does not raise, it is simply always `False`, so an equality check hides the mix-up. Two naive values from
   different zones compare silently wrong.

## 1.3 File encoding
1. **`open()` in text mode without `encoding=` uses a locale-specific default** (what `locale.getencoding()`
   returns) **unless UTF-8 mode is on,** not UTF-8 as many readers assume. The `open()` page of the Python 3.15.0
   documentation records that 3.15 makes UTF-8 the default (PEP 686); up to 3.14 the
   locale default applies, so state the encoding for as long as the project supports those releases. A file written on one machine and read on another may decode differently or raise. The Ruff
   documentation (PLW1514) cites PEP 597, which recommends using UTF-8 for text files and opening them with
   `encoding="utf-8"`.
2. **If a locale encoding is intended, say so** (`encoding="locale"` on Python 3.10 and later; PEP 597 says
   older versions raise `LookupError`), so the dependence is explicit. `-X warn_default_encoding` (3.10) makes
   the interpreter emit an `EncodingWarning` wherever the argument is omitted, which finds the sites.
3. **The same applies to `Path.read_text` and `write_text`,** which take `encoding`, `errors` and `newline`
   with the meaning they have in `open()`.

## 1.4 Late-binding closures
1. **A lambda or nested function defined in a loop looks up the loop variable when it is called,** not when
   it is defined, so every callback sees the last value. Ruff documents the example: `[lambda x: x + i for
   i in range(3)]` called with 1 gives 3, 3, 3 (B023).
2. **Bind the value at definition:** a default argument (`lambda x, i=i: x + i`) or `functools.partial`.
3. **A callback registered in a loop and run later (a task, a button handler, a schedule) is the
   place this bites,** because by then the loop has finished.

## 1.5 Cached methods
1. **`functools.lru_cache` and `functools.cache` on a method keep a reference to `self` in the cache,** so
   the instance is never garbage collected while it is cached (B019; the `functools` page says the `self`
   argument is part of the cache key and that the cache keeps references to arguments and results until they
   age out or the cache is cleared). The cache is global to the function, not per instance, and `cache` never
   evicts.
2. **Move the computation to a function that takes only its arguments** and call it from the method, or
   cache on the instance in an attribute. Enum methods are exempt, since members are singletons.
3. **A cache on a function of values (not objects with identity) is fine.** The settings loader cached
   once for the process is the legitimate use.

## 1.6 Mutable context variable defaults
1. **A `ContextVar` default is evaluated once, when the variable is defined,** and the same object is
   returned from every `get()` that has no value set. A mutable default (`[]`, `{}`) is therefore shared, and
   a change made in one request persists for the next (B039). A default passed to `get()` itself wins over the
   one given at creation.
2. **Create the variable once at module level,** as the documentation requires, never inside a function or a
   closure: contexts hold strong references to their variables, so they are never collected.
3. **Use `None` as the default and set a new object in the context when needed,** or use an immutable value.

## Verification
- The module's tests were run once with `python -O`.
- A timestamp created under one `TZ` setting was compared under another and agreed.
- A callback list built in a loop was called and each returned its own value.
- A method's instance was shown to be collectable after use, or the cache moved off the method.
