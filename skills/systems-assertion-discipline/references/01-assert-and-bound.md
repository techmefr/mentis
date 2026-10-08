# systems-assertion-discipline §1 — What to assert and bound

The first four points rewrite the safety section of the TigerBeetle style document (Apache-2.0, tree of
2026-10-06). It is one project's discipline for a database written in Zig; where a number or a rule is that
project's own choice it is labelled so, and nothing here is a language requirement.

## 1.1 An assertion is not error handling
1. **Assertions detect programmer errors; operating errors are handled.** The document draws the line this
   way: a failure that is expected (bad input, a full disk, a peer that misbehaves) is returned and handled; a
   failure that means the code itself is wrong is not expected, and the only correct response to corrupt
   state is to stop. It argues that assertions turn a catastrophic correctness bug into a liveness bug, and
   that they multiply what fuzzing finds.
2. **Never assert on data you do not control.** Validate it and return an error (`security-hardening` §1).
   An assertion on external input turns a malformed message into a crash.
3. **All errors that can happen are handled.** The same document states that every error must be handled and
   cites a study of production failures in distributed systems that found most catastrophic failures came from
   incorrect handling of non-fatal errors (the study itself was not read here).

## 1.2 What to assert
1. **Assert arguments, return values, preconditions, postconditions and invariants at the function
   boundary.** A function should not operate blindly on data it has not checked. The project's own target is
   an average of two assertions per function; treat that figure as theirs, not as a threshold for yours.
2. **Pair assertions across code paths.** For each property, find two places that can check it: the document's
   example is validating data just before writing it to disk and again right after reading it back.
3. **Assert both spaces.** Assert what you expect (positive space) and what you do not expect (negative
   space), because the bugs live where data crosses between them; the document draws the same consequence for
   tests, which should exercise invalid data and data that turns invalid, not only valid data.
4. **Split compound assertions** (`assert(a); assert(b);` rather than one assertion with both conditions) so a
   failure says which condition broke; state an implication as a single-line `if (a) assert(b)`.
5. **A blatantly true assertion can replace a comment** where the condition is critical and surprising. This
   matches the house rule against comments in code: put the claim where it is checked, not beside it.
6. **An assertion does not replace understanding.** A fuzzer or simulator proves the presence of bugs, not
   their absence; build the mental model, encode it as assertions, then let the machinery test the model.

## 1.3 Put a limit on everything
1. **Every loop and every queue has an explicit upper bound**, so a runaway input shows up as a violated bound
   instead of an infinite loop or a latency spike. Where a loop is meant not to terminate, such as an event
   loop, assert that fact.
2. **No recursion where execution is meant to be bounded.** The document uses very simple control flow and
   forbids recursion to guarantee every bounded execution is bounded. The Zig 0.17.0 reference adds that Zig
   code is not yet protected from stack overflow, so a recursion bug there is not caught for you.
3. **Allocate everything at start-up and nothing afterwards** is that project's design choice, with the stated
   benefits of predictable behaviour and no use after free. It is a strong constraint, not a default: adopt it
   only where the whole memory budget can be known up front (own guidance on when).
4. **Declare variables at the smallest scope and keep few in scope**, and the document caps functions at 70
   lines. These are that project's style numbers; the reasoning, that long functions and wide scopes hide
   misuse, is what transfers.

## 1.4 Check constants at compile time
1. **Assert the relationships between compile-time constants and the sizes of types** so a design assumption
   fails the build instead of the run; the document points out this checks design integrity before the
   program executes.
2. **Zig:** `comptime { assert(...) }` evaluates at compile time, and a false condition is a compile error
   (Zig 0.17.0 reference: a `comptime` expression either evaluates at compile time or fails to compile).
3. **C++:** `static_assert(condition)` at namespace, block or class scope; if the condition is false the
   program is ill-formed and the compiler issues a diagnostic. The message argument is optional since C++17.
4. **C:** `_Static_assert(expression, message)` since C11, with the C23 form `static_assert(expression)`
   where the message is optional and `_Static_assert` is deprecated; before C23 `static_assert` was a
   convenience macro in `<assert.h>`. The expression must be an integer constant expression and a zero value
   is a compile-time error.
5. **Rust:** not covered here; no page on compile-time assertions was read for this block.
