# rust-async-unsafe-pitfalls §3 — Unsafe

Sources: the Rustonomicon (exception safety, unchecked uninitialised memory, FFI and unwinding), the standard
library documentation for `mem::zeroed` and `mem::uninitialized`, the Miri README, and the Clippy lint
documentation for `missing_safety_doc` and `undocumented_unsafe_blocks`.

## 3.1 A panic must not leave memory unsafe
1. **Unsafe code has to be exception safe to the point of not violating memory safety**, which the Rustonomicon
   calls minimal exception safety. Almost anything can panic (an unwrap, an index, an overflow in a debug
   build, and any caller-supplied `Clone`, `Ord` or closure), and unsafe code must assume safe code will panic
   at the worst moment.
2. **While a state is transiently unsound, run only code that cannot panic, or hold a guard whose destructor
   restores a safe state.** The book's two examples: a `Vec` extension that raised the length before cloning
   (a panicking `Clone` leaves the vector claiming uninitialised elements, so fix it by setting the length
   after the loop or on each iteration), and a heap sift that keeps two copies of a value (a panicking
   comparison causes a double drop, so move the user-defined comparisons ahead of the unsafe moves, or keep a
   guard struct whose `Drop` puts the value back).
3. **The state a panic exposes need not be coherent, only safe.** An inconsistent heap is acceptable after a
   panic; a double drop is not.
4. **Do not use `catch_unwind` as control flow.** The book says unwinding is optimised for the case where it
   does not happen and is expensive when it does, and that panics should be for programming errors or
   extreme problems.

## 3.2 Uninitialised and zeroed memory
1. **Use `MaybeUninit<T>` for memory that is not yet initialised.** Dropping a `MaybeUninit` does nothing, so
   assigning to an element of an array of them does not drop the old, uninitialised value; writing through a
   raw pointer with `*p = value` to a place that is really uninitialised drops garbage and is the book's
   "WRONG" example.
2. **Do not call `mem::uninitialized`.** It is deprecated since Rust 1.39.0; its documentation says it is
   immediate undefined behaviour for nearly all types, including integers and arrays of integers, even when
   the result is unused.
3. **`mem::zeroed` is valid only if all-zero bytes are a valid value of the type.** It is immediate undefined
   behaviour for references and function pointers. Zero is fine for integers; check every other field of a
   struct before zeroing it, and prefer `MaybeUninit::zeroed` with an explicit `assume_init` at the point the
   claim is made (own guidance on the second half).
4. **Converting an array of `MaybeUninit<T>` to `[T; N]` is allowed with `transmute`, but a container of
   `MaybeUninit<T>` is not generally the same layout as the container of `T`**: the book's example is
   `Option<bool>`, which uses niche values a `bool` has and an uninitialised one may not.

## 3.3 FFI and unwinding
1. **Most ABI strings have an `-unwind` variant.** If you expect a Rust panic or a foreign (for instance C++)
   exception to cross a boundary, the boundary must use the `-unwind` string; if you do not, use the plain
   one. The `Rust` ABI always permits unwinding.
2. **What happens when unwinding meets a boundary that does not allow it:** a Rust `panic` aborts the process
   safely; a foreign exception entering Rust is undefined behaviour. Building with `panic=abort` aborts on
   any panic whatever the ABI.
3. **The interaction of `catch_unwind` with foreign exceptions, and of `panic` with C++ `try` and `catch`, is
   undefined.** Do not mix them.
4. **The Rustonomicon's two chapters differ.** Its unwinding chapter, in older wording, says unwinding across
   FFI is undefined and a panic must always be caught at the boundary; its FFI chapter describes the
   `-unwind` ABIs above. Follow the FFI chapter, and where the boundary must not unwind, catch the panic at the
   boundary or abort rather than let it escape (own reconciliation of the two chapters).

## 3.4 Miri
1. **Run unsafe-heavy tests under Miri**: on the nightly toolchain with the `miri` component, `cargo miri
   test`; flags go in `MIRIFLAGS`. It detects out-of-bounds access, use after free, invalid uninitialised
   reads, violated intrinsic preconditions, misaligned access, invalid values (a `bool` that is not 0 or 1),
   data races and some weak-memory behaviour, and memory leaks. Aliasing checks (Stacked Borrows, Tree
   Borrows) are experimental.
2. **A green Miri run is not a proof of soundness.** It runs one execution of your test, so it only reports UB
   on that input and interleaving; vary `-Zmiri-seed` and the inputs to widen it. It follows its own
   approximation of undefined behaviour, so consult the Reference for the definition.
3. **Miri does not support most platform APIs and FFI.** Gate unsupported tests with `cfg(miri)` and
   `#[cfg_attr(miri, ignore)]`, and say in the change which tests were excluded. For intricate atomics, use
   `loom` (`rust-test-supply-chain-ci` §1) as the Miri README itself advises.
4. **Its isolation is not a sandbox and its random numbers are fake**, so do not run Miri on code that handles
   real keys or generates cryptographic material.
5. **State the Miri flags used and the toolchain** in the change, since the aliasing model and the flag set
   move between nightly versions (own guidance, from the README's statement that Miri follows the compiler).

## 3.5 Documenting unsafe
1. **Every public `unsafe fn` carries a `# Safety` section** stating what the caller must guarantee. Clippy's
   `missing_safety_doc` (group `style`, since Clippy 1.39.0) flags its absence.
2. **Clippy's `undocumented_unsafe_blocks` (group `restriction`, off by default) wants a `// SAFETY:` line
   comment on every unsafe block**, which conflicts with the house rule against comments in code. Under that
   rule do not enable it; keep each unsafe block as small as one operation, put it behind a safe function, and
   state the invariant the function upholds in its docblock (own guidance reconciling the two).
