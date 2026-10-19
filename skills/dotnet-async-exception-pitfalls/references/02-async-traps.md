# dotnet-async-exception-pitfalls §2 — Async traps

Traps that survive code review because each line looks correct. The broad async rules are in
`dotnet-conventions` §1.

## 2.1 Argument validation arrives late
1. **In a public `async` method, a thrown argument exception is not raised at the call.** It is raised when
   the returned task is awaited, which may be much later. Validate eagerly in a non-async public method
   that then calls a private async one.
2. **A method with `yield` defers its whole body, validation included, until the first enumeration.**
   Validate arguments immediately in a wrapper and keep only the iteration deferred.
3. **Never return `null` where a `Task` is expected.** Awaiting a null task throws a
   `NullReferenceException`. Return `Task.CompletedTask`, `Task.FromResult`, or make the method `async`.
4. **Never write `await x?.DoAsync()`.** When `x` is null the expression is null and the await throws
   `NullReferenceException`. Test for null first.

## 2.2 Tasks that are not awaited
1. **Do not put a `Task` in a `using` statement.** A task does not need disposing; when it is there, the
   author usually forgot to await it (`using (await t)` is the intended form for a task of a disposable).
2. **Await a task before the resource it uses is disposed.** A method that returns a task from inside a
   `using` block disposes the resource before the task finishes; `await` inside the block, or make the
   method `async`.
3. **Use `Unwrap()` on a `Task<Task>` instead of awaiting twice.**
4. **A `Task` converted to a string is a missing `await`:** the text is the type name, not the result.

## 2.3 Lazy and completion sources
1. **`Lazy<Task<T>>` can deadlock.** The value factory inherits the context of the first caller; if it
   needs a thread the first caller did not have, or a later caller blocks on `.Value`, the code stalls. Use
   an async lazy type (the vs-threading library provides `AsyncLazy<T>`) and never block on it.
2. **Create a `TaskCompletionSource` with `TaskCreationOptions.RunContinuationsAsynchronously`.** Without
   it, continuations run synchronously on the thread that completes the task, which can cause deadlocks.

## 2.4 Fan-out
**Materialise a lazy `IEnumerable<Task>` once.** `ids.Select(async id => ...)` is deferred: awaiting
`Task.WhenAll(tasks)` and then enumerating `tasks` again starts the whole work a second time. Call
`ToList()` or `ToArray()` first.

## 2.5 Async void in disguise
**An async lambda or method group passed where the delegate type is not task-returning is `async void`.**
An exception in it cannot be caught by the caller and can crash the application. Give the API a
`Func<Task>` overload, or catch everything inside the lambda and log it.

## 2.6 Concurrent dictionaries
1. **`GetOrAdd(key, value)` and `AddOrUpdate(key, addValue, ...)` evaluate the value before the call,**
   even when the key exists. When computing it is expensive, use the overload that takes a factory.
2. **Keep a factory free of side effects.** This is our own guidance: a factory may be called under
   contention, so a factory that sends, writes or starts something should store a lazy value instead.

## Verification
- Call each public async method and each iterator with an invalid argument and assert the exception at
  the call line.
- Run the fan-out with a counter in the work item and assert it equals the item count, not twice that.
- Enable the matching analyzer rules where the project has an analyzer package; they cover most of this
  section.
