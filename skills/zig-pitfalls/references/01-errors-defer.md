# zig-pitfalls §1 — Errors and defer

Rules from the Zig 0.17.0 language reference unless a rule says otherwise.

## 1.1 Propagate with try, handle on purpose
1. **`try` returns the same error from the current function** and otherwise unwraps the value. It is the
   default way to pass a failure up. The reference notes that error return traces keep that practical: an
   error that bubbles out of the program still shows every place it was returned through.
2. **`catch` with a default value** needs a right-hand side of the unwrapped type or of type `noreturn`.
   Use it only when the default is a correct answer, not to make the error go away.
3. **`catch unreachable` is an assertion, not a discard.** The reference says `unreachable` is
   safety-checked illegal behaviour: in debug and safe modes it panics, and in fast and small modes the
   optimiser may assume the branch is never reached (see `systems-assertion-discipline` §2). Write it only
   where the error cannot happen, such as parsing a literal you control; an error that can occur at run time
   must be returned or handled.
4. **Handle some errors and pass the rest** with `if (...) |value| ... else |err| switch (err)` and a final
   `else => |leftover| return leftover`. The reference shows this form and notes the error capture is
   mandatory in the `else` branch; capture with `_` when the value is not needed.
5. **The reference says the error primitives make it practical for a missed error check to be a compile
   error**, and that a deliberate ignore is spelled `catch unreachable`, which then crashes in debug and safe
   modes if the assumption was wrong. Do not work around the compiler with a silent discard.

## 1.2 Release next to the acquire
1. **`defer` runs at scope exit, in reverse order of the defers.** A `defer` that was never reached does not
   run, so a defer written inside an `if` that is not taken releases nothing.
2. **`errdefer` runs only when the block is left with an error.** Put it on the line after the acquire it
   undoes. The reference example pairs `errdefer` for the value that is returned on success with plain `defer`
   for a temporary buffer that must always be freed, and says the point is that deallocation code always
   directly follows the allocation code.
3. **Order matters for a second fallible step.** An `errdefer` only covers what was acquired before it; a
   fallible acquire placed before its `errdefer` leaks on the failure of the next one. Write the acquire, then
   its `errdefer`, then the next fallible call (own guidance, derived from the scope rule above).
4. **No `return` or `try` inside a defer expression.** The compiler rejects it with "cannot return from defer
   expression", so cleanup that can fail has to handle its own error inside the block.
5. **Zig 0.17.0: the `errdefer |err|` capture was removed.** The release notes migrate a use by splitting the
   function in two and catching the error from the inner one at the call site (`catch |err| ...`). Code that
   still writes the capture does not compile on 0.17.0.

## 1.3 Name the error set
1. **Avoid `anyerror`.** The reference says the global error set stops the compiler knowing which errors are
   possible, which hurts generated documentation and messages such as a forgotten value in a `switch`.
   Coercing to it is free; casting back inserts a language-level assertion.
2. **An inferred error set (`!T`) makes the function generic.** The reference lists the consequences:
   harder to take a function pointer, no consistent set across targets, and incompatibility with recursion.
   In those cases it recommends an explicit set, starting from an empty one and letting compile errors fill it
   in.
3. **Inferred is fine for ordinary internal functions**, where none of those situations applies (own
   guidance; the reference only says inference is supported and lists the limits above).

## 1.4 Related
Allocation failure is an error value, not a crash: `error.OutOfMemory` (§2.5). Assertion and bound rules for
the same code: `systems-assertion-discipline`.
