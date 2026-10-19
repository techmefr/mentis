# swift-conventions §4 — Errors

> Section 4 of `skills/swift-conventions`. Read it when a function can fail, an error type is defined, a call
> to a throwing function is written, or cleanup has to survive a failure. Rewritten from the language guide's
> error-handling chapter (`references/origin.md`).

1. **Model related failures as an enumeration conforming to the error protocol**, with associated values for
   the details a caller needs (the missing amount, the item name). A caller can then match each case.
2. **A function that can fail declares `throws`; every call site says `try`.** The keyword is how a reader
   finds the places where control can leave. A non-throwing function must handle every error inside itself.
3. **Choose one of four responses per call and make it deliberate**: propagate; handle in a `do`-`catch`;
   convert to an optional with `try?`; assert it cannot happen with `try!`. Use `try?` when every failure is
   handled the same way and the cause no longer matters; it discards the reason, so not where a user must be
   told why. `try!` crashes at runtime on failure: only where failure is a programmer error, never for I/O or
   input.
4. **A `catch` lists the cases it handles and lets the rest propagate.** A catch-all swallows cases added to
   the enumeration later. Where a catch-all is needed, it is the last clause and it acts on the error
   (reports or rethrows), it does not ignore it. An error that reaches the top level unhandled is a runtime
   error: some enclosing scope must own every error.
5. **Cleanup uses `defer`**, which runs on every way out of the scope (return, break, thrown error): closing a
   file descriptor, releasing a lock, freeing manual memory. Do not duplicate the cleanup at each exit.
6. **Use `guard` to exit early with a throw when a precondition fails**, keeping the success path unindented.
7. A throw costs about the same as a return: there is no stack unwinding, so errors are control flow for
   expected failures and not an exceptional-path performance concern.
