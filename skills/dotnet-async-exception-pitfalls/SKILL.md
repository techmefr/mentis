---
name: dotnet-async-exception-pitfalls
description: "Use when writing or reviewing C# that rethrows, wraps or logs exceptions, registers cancellation callbacks, uses ContinueWith, Lazy of Task, TaskCompletionSource, async lambdas or timers, ConcurrentDictionary.GetOrAdd factories, returns tasks from inside a using block, validates arguments in async or iterator methods, locks, event subscriptions, struct dictionary keys, Math.Round, DateTime to DateTimeOffset, Regex on untrusted input or Process.Start."
---

# dotnet-async-exception-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the C# traps that compile cleanly, pass a happy-path test and
fail only in production: an exception that arrives without its stack, an argument error that surfaces a
line late, a task that was never awaited, a lock that anyone can take. The premise: **a trap here is a rule
the compiler does not enforce, so the rule has to be a habit or an analyzer**. The general async,
disposal and exception rules are in `dotnet-conventions` §1 and §5 and `dotnet-no-swallow-exceptions`; this
block holds only the narrow traps they do not name.

## When
- Writing a `catch`, a `throw`, a wrapper exception or a log line for a caught exception.
- Using `ContinueWith`, `Lazy<Task<T>>`, `TaskCompletionSource`, `Task.WhenAll` over a lazy sequence.
- Passing an async lambda to something that takes `Action`, or giving a `Timer` an async callback.
- Adding a `lock`, an event handler, a struct dictionary key, rounding, a date conversion or a regex.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Exception hygiene: rethrow, logging, inner exceptions, finally, cancellation registrations | a catch block, a wrapper or an error log is written | [`01-exception-hygiene.md`](./references/01-exception-hygiene.md) |
| 2 | Async traps: deferred validation, null tasks, ContinueWith, Lazy, TaskCompletionSource, async void in disguise, GetOrAdd, using and tasks, deferred sequences | an async method, a task combinator or a concurrent cache is written | [`02-async-traps.md`](./references/02-async-traps.md) |
| 3 | Runtime hygiene: lock targets, event leaks, struct keys, rounding, date offsets, regex timeouts, Process.Start | a lock, handler, key type, rounding, conversion or process launch is added | [`03-runtime-hygiene.md`](./references/03-runtime-hygiene.md) |

## Output / checkpoint
Each rule was exercised: the rethrow test asserts the original frame is in the stack trace (§1), the
async method was called with a bad argument and the error was seen at the call, not at the await (§2), the
lock target is private and was shown to be (§3). A rule applied by reading the diff only is not verified.

## Guardrails
- Never write `throw ex;` (§1.1).
- Never log a caught exception as its message alone (§1.2).
- Never pass an async lambda where the delegate type is `Action` (§2.5).
- Never lock on `this`, a public member, a string or a `Type` (§3.1).
- Versions: the rules apply to .NET 6 and later unless a rule names a version. Nothing was compiled or run
  while writing this block.
- When the project already enforces the rule through an analyzer, trust the analyzer and skip the section.

## Origin
Rewritten from the Microsoft .NET documentation (CC-BY-4.0) and from the rule descriptions of two MIT
analyzer packages (read 2026-10-08). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). It is meant to be folded into the same-topic references
of `dotnet-conventions` when the branch `feat/antislop-lot` (PR 118) lands.
