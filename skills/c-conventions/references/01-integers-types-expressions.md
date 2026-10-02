# c-conventions §1 — Integers, types and expressions

> Section 1 of `skills/c-conventions`. Read it when arithmetic is done on a size, an index or an untrusted
> number, when a conversion or a shift is written, when an object may be read before it is written, or when a
> pointer is cast. Rule identifiers in brackets point at the published secure-coding standard in
> `references/origin.md`, for tracing, not for applying. The other sections and the guardrails stay in
> `SKILL.md`.

1. **Arithmetic on a value from outside is checked before it is done, not after.** Unsigned arithmetic wraps
   silently by definition [INT30]; signed overflow is undefined behaviour [INT32], and a compiler is allowed to
   delete a later test that "can only be true if the overflow happened". A bound check such as
   `offset + len > max` computed after the addition proves nothing once the addition may have overflowed. Write
   the check so no overflow can occur (`len > max - offset` once both are known non-negative), or use the
   compiler's checked-arithmetic builtins and test the flag they return.
2. **Conversions are deliberate.** Converting between sizes or between signed and unsigned can lose a value or
   reinterpret it [INT31]: a negative `int` turned into a `size_t` becomes a huge length, and a long truncated
   into an `int` becomes a small one. Keep sizes and counts in `size_t` end to end, keep offsets that can be
   negative in a signed type of the right width, and make each narrowing explicit after a range test. Enable the
   conversion warnings (§5.2) so the compiler lists the implicit ones.
3. **Never divide or take a remainder without knowing the divisor is non-zero** [INT33]; the minimum signed
   value divided by minus one overflows too.
4. **A shift count is in range.** Shifting by a negative number, or by the width of the type or more, is
   undefined [INT34]. Shift an unsigned operand when you mean bits; shifting a negative signed value is also
   a trap. Use the exact precision of the type when computing masks [INT35].
5. **Pointer and integer conversions are rare and justified** [INT36]. Store addresses in the dedicated
   pointer-sized integer type when they must be integers at all, and never assume their size.
6. **Read nothing before it is written** [EXP33]. An automatic variable without an initialiser holds garbage,
   and reading it is undefined. Initialise at the declaration, with the real value where it is known and with a
   zero initialiser for aggregates. Padding bytes of a structure are not initialised either, so do not compare
   structures byte for byte [EXP42] and do not send them across a trust boundary without clearing them first
   [DCL39] (they leak stack contents).
7. **Never dereference a pointer that may be null** [EXP34]. A function that can return null from a library
   call is tested at once (§3.1); a function that accepts null documents it, and a pointer parameter that is read or
   written through is described with the access attribute and its size argument (§5.10) so the compiler can
   diagnose a bad call.
8. **Respect types and alignment when reading through a pointer.** Do not access an object through a pointer of
   an incompatible type [EXP39] and do not cast to a more strictly aligned pointer type [EXP36]. For type
   punning use `memcpy` into an object of the target type; the compiler optimises it away. Do not cast away
   `const` to modify a constant object [EXP40], and do not access a `volatile` object through a non-volatile
   reference [EXP32].
9. **One expression, one side effect, one order.** Two writes to the same object, or a write and a read, without
   a sequence point between them are undefined [EXP30]; argument evaluation order is unspecified. Do not put an
   assignment in a condition [EXP45], and do not use a bitwise operator where a Boolean one was meant [EXP46].
   Do not put side effects inside `sizeof` or `_Generic` operands; they are not evaluated [EXP44].
10. **Floating point.** No floating-point loop counter [FLP30], since the increment is inexact; check the range
    before converting a float to an integer or to a narrower float [FLP34]; check domain and range errors from
    math functions [FLP32]; compare floating-point values with the arithmetic comparison, not by their bytes
    [FLP37].
11. **Identifiers.** Never declare or define an identifier the implementation reserves (a leading underscore
    followed by an uppercase letter or another underscore, and names from the standard library) [DCL37].
    Declare every identifier before use [DCL31] and give a function a single declaration visible to all its
    callers, so a call with the wrong argument types is a compile error, not undefined behaviour [EXP37,
    DCL40]. Do not declare variables between `switch` and the first `case` [DCL41]. Every non-void function
    returns a value on every path [MSC37].
12. **Random numbers.** Never use `rand()` for anything with a security meaning [MSC30]; use the operating
    system's cryptographic random source.
    A non-security generator is seeded properly [MSC32]. Never hard-code a secret, a key or a password in
    the source [MSC41].
