---
name: python-hygiene-pitfalls
description: "Use when writing or reviewing Python that validates input with assert, creates or compares datetimes, opens text files, builds closures in a loop, caches a method, defaults a ContextVar, writes log calls or error messages, shares data between threads, relies on __del__ for cleanup, or writes a pytest.raises block: bugs that pass every test and fail under -O, in another timezone or locale, after the first loop iteration, or under load."
---

# python-hygiene-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for small Python habits whose failure is silent: the code runs,
the tests pass, and the wrong thing happens later or elsewhere. The three sections share one premise:
**each of these constructs works in the case you tried and behaves differently in a case you did not** (an
interpreter flag, a locale, a second iteration, a second thread). The broader rules (None handling,
exceptions, typing, structure) are in `python-conventions` §1 to §5; what a handler may block on is in
`python-async-no-blocking-calls`. This block adds the traps those sections do not list.

## When
- Writing a check on an argument or an invariant, or reaching for `assert`.
- Writing code that creates, stores or compares times, or reads and writes text files.
- Writing a lambda or nested function inside a loop, a cached method, or a context variable.
- Writing a log call or the message of an exception.
- Sharing a value between threads, or relying on object destruction to release a resource.
- Writing a `pytest.raises` block.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Construct traps: `assert`, naive datetimes, file encoding, late-binding closures, cached methods, mutable context variable defaults | one of those constructs is written | [`01-construct-traps.md`](./references/01-construct-traps.md) |
| 2 | Logs and error messages: literal patterns, messages that state the true condition | a log call or an exception message is written | [`02-logs-and-messages.md`](./references/02-logs-and-messages.md) |
| 3 | Threads, cleanup and tests: atomicity, queues and locks, `with` over `__del__`, a single statement in `pytest.raises` | threads, a resource or a raises-test is involved | [`03-threads-cleanup-tests.md`](./references/03-threads-cleanup-tests.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the module was run once with `python -O` and behaved the
same (§1.1), a value created in one timezone was compared in another (§1.2), the loop's callbacks were all
called and each saw its own value (§1.4), and the raises-test was made to fail on a different line than the
one under test (§3.3). A diff that was only read is not verified.

## Guardrails
- Never use `assert` to validate input or to guard a branch the code depends on (§1.1).
- Never create a naive datetime for a point in time (§1.2).
- Never format a log message before passing it to the logger (§2.1).
- Never rely on a finalizer to release a resource (§3.2).
- These rules are stated for CPython 3.11 and later where a version matters, and for the tool and standard
  library documentation read on the date in [`references/origin.md`](./references/origin.md); a linter rule
  code is named only as a pointer to where the same trap is detected. Nothing was run while writing this
  block.

## Origin
Rewritten from the Python style guide published by Google (CC-BY-3.0, attribution kept in
[`references/origin.md`](./references/origin.md)) and the rule documentation of the Ruff linter (MIT), read
2026-10-08. This block is meant to be folded into the same-topic sections of `python-conventions` when
PR 118 lands. 🟡: never run by us; open points are in the origin file.
