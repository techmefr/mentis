# systems-assertion-discipline §2 — What an assertion does in a release build

Ask of every assertion: **does the build we ship still run it, and what happens if it is false?**

## 2.1 Rust
1. **`assert!` is always checked, in debug and release, and cannot be disabled** (standard library
   documentation). Unsafe code may rely on it to enforce a run-time invariant whose violation would be
   unsafe.
2. **`debug_assert!` runs only in non-optimised builds by default**; an optimised build skips it unless
   `-C debug-assertions` is passed. The expression is still type-checked. The documentation says swapping
   `assert!` for `debug_assert!` is encouraged only after thorough profiling, and only in safe code.
3. **Choose by consequence** (own guidance, built on the two points above): an invariant whose violation could
   cause memory unsafety or a wrong security decision is `assert!`; an expensive consistency check that only
   helps development is `debug_assert!`.

## 2.2 Zig
1. **`unreachable` panics in debug and safe modes; in fast and small modes the optimiser assumes it is never
   reached** (Zig 0.17.0 language reference). The reference states `std.debug.assert` is implemented as
   `if (!ok) unreachable`.
2. **So a false `std.debug.assert` in a fast or small build is not a check that fails, it is a promise the
   optimiser may use**, with unpredictable results. The same holds for `catch unreachable` (`zig-pitfalls`
   §1.1). Safety checks are on in debug and safe and off in fast and small (the reference's mode list).
3. **For a condition that must be enforced in a shipped fast or small build, write an explicit check that
   returns an error or calls `std.debug.panic`.** The reference says `std.debug.panic` is generally preferred
   over `@panic`, which it reserves for library code that defers to the programmer's panic function and for
   mixed C and Zig builds.
4. **`comptime` assertions are unaffected by the mode**, since they run during compilation (§1.4).

## 2.3 C and C++
1. **`assert` expands to nothing when `NDEBUG` is defined where the header is included**, and then the
   condition is not evaluated (cppreference; its C example asserts on a negative number before a square root and
   prints NaN instead of aborting once `NDEBUG` is defined). Whether a release build defines it depends on the
   project's build flags, so read them (own guidance) before counting on an assertion in production.
2. **Never put a side effect in an assertion condition**: with `NDEBUG` the side effect disappears (own
   inference from the previous point, labelled as such).
3. **Never use `assert` to validate input or to guard a security decision.** It is gone in the build that
   faces the input. Use a real check and an error path (`security-hardening` §1).
4. **`assert` takes one macro argument**, so a comma not protected by parentheses, as in template argument
   lists or brace initialisers, is a compile error in C++ before C++26; wrap the condition in an extra pair of
   parentheses or use `static_assert` for compile-time conditions.
5. **`static_assert` is not affected by `NDEBUG`**; it is a compile-time check (§1.4).

## 2.4 Make the build mode visible
State in the change which build runs the tests and which build ships (own guidance): a test suite that passes
only in debug has not exercised the checks the shipped build keeps, and one that passes only in release has
not exercised the debug assertions.
