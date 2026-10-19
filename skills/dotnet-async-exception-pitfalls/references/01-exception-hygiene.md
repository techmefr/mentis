# dotnet-async-exception-pitfalls §1 — Exception hygiene

An exception is evidence. These rules keep it intact from the throw site to the log line. Each says what
you see when it is missing. They apply to all supported .NET versions.

## 1.1 Rethrowing
1. **Rethrow with a bare `throw;`, never `throw ex;`.** An explicit rethrow replaces the original stack
   trace with a new one, so the frames that actually failed disappear.
2. **Rethrow only when the catch added something.** A catch that logs and rethrows produces the same error
   twice in the logs; log at the boundary that handles it (see `dotnet-no-swallow-exceptions`). This is our
   own guidance.
3. **When you throw a different exception from a `catch`, pass the caught one as the inner exception.**
   Without it the original cause is lost and debugging is harder.

## 1.2 Logging a caught exception
1. **A catch block that observes only `Message` is suspicious.** The message is often generic; the useful
   data is in the exception object and its inner exceptions. Pass the exception object to the logger so
   type, stack and inner exceptions are recorded.
2. **Do not put the exception text in a user-facing response.** It exposes internals; return a stable error
   code and log the detail with a correlation id. This is our own guidance.
3. **Log once per failure.** The layer that handles the error logs it; layers that only propagate do not.
   This is our own guidance.

## 1.3 Cleanup paths
1. **Never throw from a `finally` block.** It may hide an exception thrown in the `try` or `catch` block.
   Keep cleanup non-throwing, or catch and log inside the `finally`.
2. **Store and dispose the registration returned by `CancellationToken.Register`.** If the token outlives
   the object that registered the callback, an undisposed registration leaks memory.

## Verification
- A test throws from the innermost frame and asserts that frame's method name appears in the stack of the
  exception that reaches the caller.
- A grep for `throw ex` and for catch blocks that read only `Message` returns nothing.
