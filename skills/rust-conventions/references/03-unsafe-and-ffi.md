# rust-conventions §3 — Unsafe and FFI

> Section 3 of `skills/rust-conventions`. Read it when an `unsafe` block or function, a raw pointer, a manual
> `Send`/`Sync` implementation, a `Drop` implementation or a binding to (or from) another language appears.
> The general security background is `skills/security-hardening`. The other sections and the guardrails stay in
> `SKILL.md`.

1. **`unsafe` needs one of three reasons, and a reason is not "it was shorter".** The accepted reasons are a
   new low-level abstraction (a smart pointer, an allocator), a measured performance need, and a call across a
   language or platform boundary. Not accepted: shortening safe code with a `transmute`, bypassing a `Send`
   bound with `unsafe impl Send`, stretching a lifetime with a `transmute`. A crate with no accepted reason
   declares `#![forbid(unsafe_code)]` in its root so the compiler enforces it.
2. **Undefined behaviour is not allowed, including the theoretical kind.** A function that looks safe (no
   `unsafe` in its signature) but can cause undefined behaviour in any calling mode, however contrived, is
   *unsound*, and unsound code is never acceptable. There is no "good enough reason" exception to this one. If
   a thing cannot be encapsulated safely, expose an `unsafe fn` and document the conditions.
3. **`unsafe` means "misuse can cause undefined behaviour", nothing else.** A function that deletes a database
   is dangerous, not unsafe. Marking it `unsafe` dilutes the keyword and breeds warning fatigue.
4. **The soundness boundary is the module.** Inside one module a safe function may rely on what another
   function of the same module guarantees (a pointer set by `new`). Outside the module nothing may be assumed,
   so every public safe function must be correct for every caller. A new `unsafe` abstraction is kept minimal
   and testable, and is checked against adversarial inputs: closures that panic, and safe traits (`Deref`,
   `Clone`, `Drop`) that misbehave.
5. **Every `unsafe` use has its safety reasoning written down, in a place the house no-comment rule
   allows.** An `unsafe fn` or `unsafe impl` you provide (including an `_unchecked` variant) lists its
   preconditions in its declaration docblock. A call site of an `unsafe fn` is kept to one line inside a small
   safe function whose own docblock says why the preconditions hold, so the reasoning sits on a declaration
   and not in an inline comment; where a project's rule insists on an inline justification, that rule wins.
   All `unsafe` code is encapsulated so that it either exposes a safe behaviour that no safe
   caller can turn into undefined behaviour, or exposes `unsafe` items whose usage conditions (preconditions,
   ordering) are documented exhaustively.
6. **A performance `unsafe` comes after a benchmark.** Without the measurement the `unsafe` is a guess with
   a security cost. With it, the measurement is the justification.
7. **Run the interpreter-level check on code that contains `unsafe`.** The project's undefined-behaviour
   checker for Rust (Miri) must pass on the unsafe code and its adversarial tests; the checkpoint names whether
   it ran. If the tool is not installed, say "not run" and ask; do not report a pass.
8. **Manual `Send` and `Sync` are rare and justified in writing.** The compiler derives them correctly. A type
   with raw pointers needs a compile-time assertion that it is (or is not) `Send`/`Sync`, so a refactor cannot
   change it silently.
9. **`Drop` is justified, never panics, and is not the only security step.** Implement it for a real resource.
   A key erased only in `Drop` is not erased if the value is leaked or the process aborts, so a security-
   relevant cleanup also has an explicit step. A value with `Drop` is never part of a reference-counted cycle,
   and reference-counted recursive types do not combine with interior mutability.
10. **In a security-critical profile, leaks are banned.** `mem::forget`, `Box::leak` and an unreleased
    `ManuallyDrop` are not used there; every `into_raw` is matched by exactly one `from_raw`, and `from_raw`
    is called only on a pointer that came from `into_raw`. `std::mem::uninitialized` is never used and each
    `MaybeUninit` is justified. Outside that profile, `Box::leak` for a true process-lifetime singleton is a
    judgment call to name in review, not a default.
11. **A foreign library is wrapped in two layers.** A thin module (or a `-sys` crate when exposed) mirrors the
    C API in `extern` blocks; a second, safe module restores the invariants. Prefer an established interop
    library or an automatic binding generator to hand-written declarations, and document which call patterns
    the generated bindings allow. The core business logic lives in an ordinary safe crate; the FFI crate only
    translates, and the core does not take on interop shapes.
12. **Only C-compatible types cross the boundary**, with the same size and alignment on both sides, and with
    the portable aliases for platform-dependent types (`c_int`, `c_long`) instead of fixed Rust integers.
    Function pointers at the boundary are marked `extern` with an ABI and `unsafe`, and a function pointer that
    came from outside is checked before it is called.
13. **Never trust an incoming value.** A foreign value of a type with invalid bit patterns (a Rust `enum`, a
    `bool`, a reference) is read as a raw value and checked before it becomes the Rust type. Do not accept a
    Rust `enum` from the foreign side unless it is opaque there or maps to a safe enumeration of that language.
    Every foreign pointer is checked non-null before use, and stronger checks (range, alignment, tagging) are
    better where possible. Incoming pointers are held as raw pointers, not as references, until validated.
14. **One side allocates and frees.** Data that crosses without a copy is allocated and released by the same
    language; the other side calls dedicated functions instead of freeing directly. Foreign data owned by the
    foreign language gets a `Drop` wrapper that calls its release routine. A type with a Rust `Drop` is not
    passed by value across the boundary. Opaque foreign types are modelled as dedicated Rust types, and opaque
    Rust types are exposed to C as pointers to incomplete structs.
15. **A panic never unwinds into foreign code.** Rust code called from another language either cannot panic or
    wraps its body in the panic-catching mechanism (or a panic hook or handler) so the program neither aborts
    unexpectedly nor returns in an inconsistent state. The exported API is a dedicated C-compatible surface, not
    the internal Rust API with attributes added.
16. **Provide `unsafe` escape hatches for native handles.** A type wrapping a native handle offers an `unsafe`
    constructor from a raw handle and an accessor, with the safety requirements documented, because users meet
    handles you did not create.
