# rust-conventions §2 — Errors and panics

> Section 2 of `skills/rust-conventions`. Read it when a function can fail, when `unwrap`, `expect`, an index
> or an arithmetic operator appears on a value that comes from outside, or when an error type is introduced.
> `unsafe` and FFI panics are §3. The other sections and the guardrails stay in `SKILL.md`.

1. **A failure the caller could meet returns a `Result`; a panic is a stop.** A panic means "this program
   should halt now". It is not an exception, it is not a way to report a bad input upward, and nothing may
   assume it will be caught: a binary built with abort-on-panic turns any panic into a process exit. The valid
   reasons to panic are a programming error (an invariant that cannot be false), a context evaluated at compile
   time, an `unwrap`-style method the user explicitly asked for, and a poisoned lock (another thread already
   panicked).
2. **A detected programming bug panics instead of returning an error.** When a contract is violated, by the
   library or by the caller, there is nothing a caller could do at runtime with an error value, so none is
   introduced. What counts as a violation is situational and an API does not have to go out of its way to find
   them: dividing by a zero the caller passed may panic, a `parse` function fed a malformed string must return
   an error because parsing is fallible by nature. If in doubt, copy what the standard library does for the
   analogous function.
3. **Prefer making the bad call impossible.** Before settling for a panic on a bad input or a bad calling
   order, check whether a type removes the case (a non-zero type, a builder that cannot be built incomplete,
   a state encoded in the type). The panic is the least bad option, not the goal.
4. **A panic carries a message with the values.** `assert!`, `unreachable!`, `todo!` and `expect` say what was
   violated and print the actual numbers or names involved. A bare assertion on a length tells whoever reads
   the crash log nothing. In tests the message is optional.
5. **In library code, `unwrap`, `expect` and `assert!` stay inside what the function's specification forbids.**
   The operations that panic on a bad argument are well known: an unchecked index, an overflowing add in a
   debug build, a division by zero, a huge allocation, and `format!` on a faulty `Display`. Index with `get`
   and handle the `Option`, or test the index; do the arithmetic with an explicit mode (§2.8).
6. **`catch_unwind` is a last resort and is followed by a restart.** A caught panic can leave shared or
   thread-local state half-updated, and the damage is hard to see. A library never catches a panic to carry
   on. A server may catch it once per request so that one handler does not kill the process, but it still
   plans to restart after a handler panicked.
7. **A destructor never fails and never blocks.** `Drop` runs during a panic; a second panic there aborts the
   process. Offer an explicit `close()` that returns a `Result` for teardown that can fail, and make `Drop` do
   the best-effort teardown, logging or ignoring errors. Blocking inside `Drop` makes hangs hard to debug.
8. **Integer arithmetic on external or unbounded values names its overflow mode.** Plain operators wrap in a
   release build and panic in a debug build unless the profile says otherwise, so the same code behaves
   differently. Where an overflow is possible, use `checked_*` (returns `None`), `saturating_*`,
   `wrapping_*` or `overflowing_*`, or the `Wrapping` and `Saturating` types, so the behaviour is the same
   everywhere. Do not override the overflow-check and debug-assertion settings of the development and test
   profiles; if a release build must keep overflow checks, say so in the profile.
9. **Error types.** A library exposes an error type per kind of operation, as a struct carrying the cause
   and, where the capture is cheap enough, a backtrace, with helper methods that let a caller decide what to
   do (which file, which kind). A simple crate has one `Error`; a larger one has several, but one giant enum
   shared by every function is the thing to avoid, as is a different type for every function. Mixed
   operations may keep an `ErrorKind`. An application, or a crate used by one application only, may use an
   application-level error crate and should then use it everywhere rather than mixing several. The universal
   "box anything" wrapper does not belong in a library, because the caller can no longer match on the cause.
10. **An error type is a proper error.** It implements `std::error::Error`, `Debug` and `Display`, and is
    `Send + Sync + 'static` so it crosses threads, goes in an `Arc` and can be wrapped by an I/O error. Never
    use `()` or a bare string as an error type: it cannot be displayed, matched, converted with `?` or
    downcast. `Display` text is lowercase, concise and has no trailing punctuation. Do not implement the
    deprecated `description`.
11. **Convert once, with `From`.** When you own the error type, implement `From<Other>` for it and let `?`
    apply it, instead of a `map_err` at every call site. `map_err` is for foreign error types and for adding
    context at one specific spot.
12. **Validate at the boundary, in this order of preference.** First a type that rules out the bad input
    (§1.1, §1.2). Then a check inside the function, whose downsides are runtime cost and late detection. Do not
    be "liberal in what you accept" the way network protocols are: reject invalid input where it enters.
13. **Do not ignore a `Result`.** A discarded error is a hidden panic waiting for a different input. If it is
    truly irrelevant, bind it to `_` on purpose.
