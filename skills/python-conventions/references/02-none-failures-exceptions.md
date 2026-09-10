# python-conventions §2 — None, failures, exceptions

> Section 2 of `skills/python-conventions`. Read it when a failure is returned or raised, or a resource is opened. The other sections and the guardrails stay in `SKILL.md`.

1. **Never implicit truthiness where `None` is possible.** `if x:` is also false for `0`, `""`, `[]`, `{}` —
   so a valid empty value takes the missing-value branch. `if x is None:` / `is not None`, always. The bug it
   produces is the one that never reproduces on the developer's data: a quantity of zero, an empty note, a
   customer with no orders yet.
2. **The same trap wears other clothes.** `x or default` replaces a legitimate `0` or `""` with the default;
   `if not items` does not distinguish "no list" from "an empty list"; and a bare `if value` on a
   third-party object silently calls whatever truthiness that object defined. Ask the question actually
   being asked.
3. **A public boundary returns its failures as values**, so the type checker can see them: `T | None` for a
   binary present/absent, a result/option type for richer typed failures. A boundary that raises its failure
   modes silently makes every caller guess which exceptions exist.
4. **The reason is that Python's signature cannot state what a function raises.** There is no checked
   exception, so a raised failure is invisible to the caller, to the checker and to the reader — the only
   place it exists is the body, and the only way to learn it is to read every function the body calls.
   Returned in the type, the same failure is a thing the checker will not let the caller ignore.
5. **`T | None` says *that* it failed, not *why*.** For a lookup that is enough; for anything with more than
   one failure mode — rejected, expired, rate-limited, conflicting — a `None` collapses them and the caller
   has to guess or ask again. Carry a typed failure with the fields the caller needs to act.
6. Inside a tightly-coupled module, helpers may raise freely — only the boundary is held to the rule. The
   whole benefit of point 3 is at the seam; applying it to every private helper produces plumbing that
   unwraps and rewraps a result five times on the way out.
7. Truly exceptional conditions still raise. Results are for **recoverable** failures; wrapping a
   programming error in a result type just delays the crash. A missing configuration key at boot, a broken
   invariant, an unreachable branch: those should stop the process while the cause is still on the stack.
8. A raised exception is a specific class inheriting from `Exception`, never a bare
   `except Exception:` that swallows everything indiscriminately. Catching by type is what survives a
   refactor; matching on a message breaks the day somebody improves the wording, and catching everything
   also catches your own typo and reports it as the failure you were expecting.
9. **Catch the narrowest scope, not the paragraph.** A `try` wrapped around a block that contains the risky
   call *and* your logic converts a null dereference or a wrong argument into the exception you had planned
   for. Wrap the call.
10. An `except` with no rethrow and no log hides a real bug: never silent, even as a last resort. A bare
    swallow is indistinguishable from a forgotten branch, and it leaves no evidence anywhere that the
    failure happened — which is the most effective way to make something undiagnosable.
11. **Preserve the cause when you wrap.** Raising a domain exception from inside an `except` without
    chaining it keeps the meaning and throws away the traceback, so the log says "import failed" and
    nothing about the encoding error underneath. The `from` clause is the whole difference between a name
    and a diagnosis.
12. **Log-and-reraise at every layer reports one failure five times**, with five tracebacks to read before
    finding the origin. Report where the decision is made — once, at the boundary that knows what to do —
    and let the failure travel untouched in between.
13. **Nothing sensitive in an exception message.** The message reaches the log and the error tracker, which
    have different readers and different retention than the request did — so a token, a password or a
    personal detail interpolated into it has left the system that was governing it.
14. A context manager (`with`) for every resource that has to be closed (file, connection, lock): never a
    manual close an intermediate exception can skip. The failure is invisible at low volume and only shows
    up under load, because it needs failures to accumulate before the handles or the connections run out.
15. **A `finally` that can itself fail loses the original exception.** Cleanup code raising on the way out
    replaces the failure being reported with its own, so the thing that actually went wrong never reaches
    the log — which is why the cleanup belongs in a context manager written once rather than open-coded at
    each site.
16. **An expected failure is not a defect.** Reporting every rejected input and every stale link alongside
    real exceptions raises the volume until the real ones cannot be found, which is the same harm as
    reporting nothing. Decide per failure class whether it is monitored or merely logged.
17. **The failure path is asserted** (`skills/tdd`), or the first refactor turns the returned result back
    into a raise — exactly the thing point 3 forbids — and nothing anywhere goes red.
18. **A sentinel is not `None` wearing a different name, and reaching for one usually means the signature
    already lied.** A dedicated `_MISSING = object()` default distinguishes "the caller passed nothing" from
    "the caller passed `None` on purpose" in a function where both are meaningful — but where that
    distinction does not matter, a sentinel is a second spelling of point 7's `T | None`, harder to discover
    and with no checker support telling a reader it exists.
19. **`contextlib.suppress` names the exceptions it swallows where a bare `try`/`except: pass` does not.**
    `with suppress(FileNotFoundError):` reads as a decision — this specific, expected condition is not an
    error here — while an empty `except:` block reads as point 10's silent swallow with better formatting;
    the tool does not change the rule, it only removes the excuse that the boilerplate was in the way.
20. **`except*` and `ExceptionGroup` exist because structured concurrency can fail more than once at a
    time**, and a single `try`/`except` can only ever catch one exception per attempt. A `TaskGroup` (§4)
    that fails two children in the same window raises one `ExceptionGroup` wrapping both; `except*
    ValueError:` pulls out every `ValueError` in the group while leaving the rest to propagate, which a
    plain `except ValueError:` cannot express — it would see only whichever exception the group presents
    first.
21. **A retry is a decision about which failures are worth repeating, not a loop around the call.** Retrying
    on every exception retries a `TypeError` from a bug in the retried code itself, which just delays the
    same crash a fixed number of times; retrying without a backoff turns a struggling dependency into one
    hammered by every caller's immediate next attempt. The exception type list and the delay between
    attempts are both part of the design, not incidental to wrapping the call.
22. **The walrus operator moves the `is None` check next to the value it guards, without changing what point
    1 requires.** `if (row := fetch(id)) is not None:` reads as one condition instead of a fetch followed by
    a separate check on a variable declared above it, but it is still an explicit `is None`/`is not None`
    comparison underneath — `if (row := fetch(id)):` reintroduces the exact truthiness bug point 1 exists to
    forbid, now harder to spot because the assignment draws the eye.
23. **A resource opened inside a generator is not closed by returning early — it is closed when the generator
    is garbage-collected or explicitly closed**, which under `asyncio` cancellation may not happen
    promptly. An async generator holding a connection open across a `yield` should be wrapped so
    cancellation while suspended still runs its cleanup, rather than trusting that the caller will always
    exhaust or explicitly close it (§4 covers the same gap from the cancellation side).
24. **A custom exception's `__init__` should still accept the base class's arguments, or `raise ... from`
    loses the message.** An exception subclass that overrides `__init__` to take only its own typed fields
    and never calls `super().__init__()` prints as a blank line in a traceback and nothing in a log that
    formats exceptions by their string form — the fields are there on the object, but nothing standard
    reads them without knowing the specific class first.
25. **`raise ... from None` says a cause was deliberately hidden, and that claim has to be true.** It reads
    as "this is not an implementation detail leaking through, it is the actual error" — appropriate at a
    boundary translating a low-level failure into a domain one the caller should not need to unwrap. Reaching
    for it because the original traceback was noisy, rather than because the cause is genuinely irrelevant,
    throws away the one piece of evidence that would have explained the failure.
26. **An exception hierarchy is a tool for callers to catch selectively, not a taxonomy for its own sake.** A
    single flat `AppError` forces every caller to inspect a code or a message to decide what happened,
    exactly what point 8 exists to avoid; a base `AppError` with `NotFoundError`, `ConflictError`,
    `ValidationError` beneath it lets a caller catch the one it can handle and let the rest propagate, without
    the module publishing every leaf class it might ever raise.
27. **A library's public exceptions are as much its contract as its return types.** A caller reasonably
    writes `except LibrarySpecificError:` once the library documents raising it, so renaming, removing or
    quietly no-longer-raising that class is a breaking change to every consumer, even though nothing about a
    call signature changed — the same discipline point 8's inheritance chain assumes but from the other side
    of the boundary.
28. **`except (ValueError, TypeError):` and two stacked `except` clauses answer different questions.** A
    tuple says both exceptions get the same handling; separate clauses say they don't, even if today's bodies
    happen to look alike. Collapsing two clauses that will diverge the moment one needs its own logging or
    recovery just to save a line reads as intentional and has to be undone later.
29. **`BaseException` is not `Exception`, and catching it catches `SystemExit` and `KeyboardInterrupt`
    alongside real errors.** A bare `except:` (no class at all) is broader than even point 8 warns about — it
    swallows the process's own shutdown signals, so a script that should exit on Ctrl-C instead logs "unknown
    error" and keeps running. Name `Exception`, never leave the class off entirely.
30. **A context manager that only wraps setup and teardown, with nothing between, is a fixture in disguise
    — and pytest already has that concept** (`skills/python-conventions` §8). Hand-writing `__enter__`/
    `__exit__` for "create a temp resource, yield it, clean it up" inside test code duplicates what a
    `pytest.fixture` with a `yield` statement already does with lifecycle management the runner understands,
    including teardown on a failed test.
31. **A `TimeoutError` from point-in-time code and one from `asyncio` share a name but not always a cause.**
    Catching `TimeoutError` around a call that can time out for either reason without checking which
    operation actually raised it can mask a hung dependency as a slow one, or vice versa — the same
    "caught by type, wrong assumption about what it means" trap as catching too broad a class in point 8.
