# cpp-conventions §1 — Types, initialisation and conversions

> Section 1 of `skills/cpp-conventions`. Read it when a variable is declared, an enumeration defined, a cast or
> a conversion written, a string or array parameter chosen, signed and unsigned values mixed, or a null
> pointer spelled. The C-side arithmetic rules (`skills/c-conventions` §1) apply in full to the arithmetic
> here. The other sections and the guardrails stay in `SKILL.md`.

1. **Express the idea in the type system and let the compiler check it.** What is stated in code has defined
   meaning and can be verified by tools; a comment cannot. Prefer the compiler as the checker; whatever it cannot
   verify should fail loudly at run time, as early as possible. A function
   that returns a month is a `month()` that cannot change anything, not an `int month()`.
2. **Interfaces are precisely typed.** A parameter list of several `int`s or `bool`s documents nothing and
   invites a transposed call. Give a distinct type to a distinct concept (a strong type, an enumeration, a
   small class), and do not put two parameters side by side when swapping them would still compile
   and mean something else.
3. **Always initialise.** An object read before it is written is undefined; initialising at the declaration
   also makes refactoring and reading easier. Do not declare a variable before you have its value, and do not
   introduce it before you need it. Prefer the brace form of initialisation, which has simpler rules, rejects
   narrowing conversions and avoids the parsing ambiguity of parentheses; use `=` only when no narrowing can
   occur (with `auto` for arithmetic types). Declare an object `const` or `constexpr` unless it must change.
   Use a lambda to initialise a `const` object that needs several statements.
4. **Keep scopes small and names honest.** Declare names in the init part of a `for` or a condition, do not
   reuse a name in a nested scope, do not use a variable for two unrelated purposes, declare one name per
   declaration, keep common local names short and uncommon non-local names longer, and avoid names that look
   alike. Do not use `ALL_CAPS` for anything but macros (§6.7), enumerators included.
5. **Enumerations are scoped.** Prefer an enumeration to a macro for related named constants, and a scoped
   (`enum class`) one to a plain one: plain enumerators convert to `int` freely and share their enclosing
   scope, so two enumerations can clash and a value can be passed where a different enumeration was meant.
   Specify the underlying type or the values only when you must (for serialisation, for example), define the
   operations that make the enumeration safe to use, and do not leave an enumeration unnamed.
6. **Signed for arithmetic, unsigned for bits, never mixed.** Mixing signed and unsigned operands in one
   expression silently converts the signed one, and `x - y` becomes a huge number when the result "should" be
   negative. Use signed types for arithmetic and subscripts and unsigned types only for bit manipulation; do
   not use `unsigned` to say "never negative". Do not overflow, underflow or divide by zero (§1 of
   `skills/c-conventions` for the checks). A style guide that treats integers the same way asks to use plain
   `int` for ordinary quantities, the exact-width types when the size matters, a 64-bit type whenever a value
   could reach two to the power of 31, and the unsigned types only for bit patterns or defined modular
   arithmetic; follow the project's choice between the two formulations, they agree on the substance.
7. **No lossy conversions, and casts are rare and named.** Avoid narrowing and truncating arithmetic
   conversions (a brace initialiser rejects them). A cast is a known source of errors and defeats some
   optimisations: avoid it; when it is needed use a named cast (`static_cast` for a defined conversion, and the
   others only with a reason) and brace-initialisation for arithmetic type changes, never the C cast form
   (`(int)x`), and never cast away `const`. Do not slice a derived object into a base object by value.
8. **Null is `nullptr`.** Not `0`, not `NULL`: it has a precise type, so overload resolution and template
   deduction behave. Keep pointer use simple and straightforward; do not dereference an invalid pointer and
   do not compare pointers into different arrays.
9. **Strings and ranges.** Own character data with `std::string`. Refer to character data with
   `std::string_view` (or a span of characters when it must be mutated); a view never outlives the string it
   views. Pass a range as a `span`, not as a pointer and a separate length, and never as an array parameter
   that decays to a pointer. Use `std::byte` for raw bytes that are not characters. Prefer `std::array` or
   `std::vector` to a C array; `vector` is the default container unless a reason is shown. Never use
   `memset` or `memcpy` on objects that are not trivially copyable.
10. **Bounds errors are avoided, not hoped away.** Access ranges through spans, `at()` or an algorithm; the
    library precondition checks of `c-conventions` §5.4 turn the remaining violations into aborts in
    production. Avoid needing range checks at all by using range-`for` and the standard algorithms.
11. **Prefer the standard library** to handcrafted code or another library, and a suitable abstraction to a
    direct use of a language feature. Use support libraries where one exists instead of rewriting it.
12. **Magic constants get names.** A number whose meaning is not obvious becomes a named constant (`constexpr`),
    never a macro (§6.7).
13. **Loops and branches.** Prefer the range-`for` to the indexed `for`, a `for` to a `while` when there is an
    obvious loop variable and a `while` when there is not, a `switch` to a chain of `if` on the same value;
    avoid `do`, `goto` and heavy use of `break` and `continue`; never rely on implicit fall-through (the
    warning of `c-conventions` §5.2 enforces it) and use `default` for the common case only. Do not modify a
    loop control variable in the body of a raw `for`. Avoid complicated expressions, parenthesise when in
    doubt about precedence, and do not depend on the order of evaluation of function arguments.
