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
