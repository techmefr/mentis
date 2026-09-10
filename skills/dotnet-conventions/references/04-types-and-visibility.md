# § 4 — Types and visibility: the prohibitions

> Section 4 of `skills/dotnet-conventions`. Read it when a type is declared, a member's visibility is
> chosen, or one of the constructs below is about to be used. These are stated as prohibitions on purpose:
> "allowed but rare" is not a reviewable rule.

1. **No mutable global state**: no `public`/`internal static` mutable field or property, no singleton class
   with a static `.Instance` holding mutable state, no `[ThreadStatic]`. Ambient static reads
   (`DateTime.Now`, a static current-context accessor) are injected instead — that's also what makes them
   testable. The failure static state produces is the one that costs most to diagnose: state that survives
   between tests makes the order matter, so the suite fails in whichever test ran second and passes when
   run alone.
2. **No nested class**, with no private exception: it hides a type from search and from the file layout.
   Give it its own file. The concrete cost is that a reader looking for `OrderLine` finds nothing, because
   it is `Order.OrderLine` inside `Order.cs` — and the reader is usually looking because something about
   it is wrong.
3. **No local function** doing real work or capturing the enclosing method's locals: it's a method that
   avoided being named and tested. The capture is the part that hurts: the function reads a local the
   caller may reassign after it is declared, so its behaviour depends on where in the method it is called.
4. **No tuple returned across a public or internal boundary**: a tuple names no concept, carries no
   behaviour and validates nothing. Return a record. The positional access is the mechanical problem — two
   fields of the same type can be read in the wrong order at the call site with no error anywhere, and
   adding a third field silently changes what every existing destructuring means.
5. **No anonymous type crossing a boundary** — returned from a non-private method, serialised into a
   response, stored in a field that outlives the method, or passed as `object`/`dynamic`. It has no name to
   reference and no contract to check. Serialised into a response it is worse still: the wire contract is
   defined by whatever the projection happened to select, so a change to the query changes the API.
6. **Explicit types over `var`**, and `dynamic` not at all: an explicit type keeps a diff readable without an
   IDE and surfaces an API change at the call site. `var` stays acceptable where the type is stated on the
   same line (`new`, a cast). With `var`, a method whose return type changed still compiles at every call
   site and fails somewhere downstream — the diff review sees nothing.
7. **No `unsafe`**, no pointer types, no native allocators, no reinterpret-casts. Business code has no
   reason to leave the verifiable subset. What is being given up is not performance but the runtime's
   guarantees: a bug in this code is memory corruption rather than an exception, and it surfaces far from
   its cause.
8. **No `volatile`.** It's a memory-barrier hint, not synchronisation: it doesn't make `counter++` atomic and
   provides no mutual exclusion. Reach for the actual primitive (`lock`, `Interlocked`, a concurrent
   collection). The reason it keeps being reached for is that it makes a race *less likely*, which is the
   worst possible outcome — the bug survives testing and appears under load.
9. **No bitwise operators** in business code — they belong to cryptography, binary protocols and low-level
   systems work. `&`/`|` on `bool` operands is also a real bug source: they don't short-circuit, so both
   sides evaluate, side effects included. That is how a null check followed by a dereference on the same
   line throws despite reading correctly.
10. Every member starts at the **most restrictive** access modifier that works (default `private`) and is
    widened one rung only when a real caller requires it. Widening a member so a test can call it is a design
    smell: test it through its public surface. A widened member is also a promise: it can be called from
    anywhere in that scope from then on, and nothing will tell you when someone starts.
11. **Every new concrete class is `sealed` by default.** Inheritance is an explicit design decision made
    once, not a default left open "in case" — polymorphism runs through an interface, and a base class
    meant to be extended says so by being unsealed on purpose, not by omission. An unsealed class also
    makes every `protected` member and every internal call between its own methods part of its public
    behaviour, which is a contract nobody wrote down.
12. **A data-carrying type (DTO, wire payload, command/query payload, value object) defaults to a `sealed`
    positional record**, or a `readonly record struct` for a small value type — value equality and
    immutability come from the language instead of a hand-rolled `Equals`/`GetHashCode`/mutable setters. This
    is also where a primary constructor is the right tool (point 1's carve-out): a record's parameters become
    public init-only properties, not a hidden mutable field.
13. **File-scoped namespaces** (`namespace Foo;` on its own line) on every new file, never the braced wrapper
    — one indentation level saved on every type in the file, for no loss of information.
14. **No `#region`.** It's unenforced structure nothing checks — a region can silently stop matching what's
    actually inside it after a few edits, and it invites cramming unrelated things under one folded heading
    instead of splitting the file. Split into a smaller type instead of folding it.
15. **Every enum member carries an explicit numeric value.** The implicit ordinals the compiler assigns are
    what the ORM writes into the database and what the serialiser puts on the wire, so inserting a member in
    the middle or reordering two of them silently changes the meaning of data that already exists — with no
    migration, no error and no test failing. Pinning the values costs one line per member and makes the
    reorder harmless.
16. **A member that returns a sequence declares the read-only interface**, not the concrete list or array.
    Understand what it buys before over-claiming: it is a **view, not a barrier** — the caller can't add or
    remove through it, but it is not a defensive copy. The half with no override is the other one: private
    collection state is never exposed through a mutable declared type, because that hands out a live handle
    on the object's own invariant.
17. **One casing per kind, one role suffix per type**, applied to new code and to renames you were asked to
    make. Existing names stay: renaming a public type is a contract change, never a drive-by cleanup. The
    reason consistency earns its place here rather than being taste is search: a codebase where the same
    kind of thing is named the same way is one where a grep finds all of them, and that is the tool
    everybody actually uses.
18. **The `file` access modifier for a type meant to exist in exactly one file** — a small helper generated
    alongside a source generator's output, or a scratch implementation type that backs one feature and has
    no business being referenced from anywhere else. Where the language version supports it, `file` gives
    that type a scope narrower than `internal` without paying nested-class's cost of hiding it from a
    top-level search (point 2): it still appears in the file listing under its own name, it simply cannot be
    named from another file, and two unrelated `file` types across the project can reuse the same identifier
    with no collision.
19. **A struct that never mutates its own state is declared `readonly struct`.** The modifier is a promise
    the compiler checks — every field is enforced read-only and every member enforced non-mutating — and
    the concrete payoff is that passing it by `in` no longer needs a defensive copy before each call, because
    the compiler already knows the callee cannot change it. A struct that is only conventionally immutable,
    with the keyword left off, gets that defensive copy on every `in` parameter and every readonly field
    access silently, which is a performance cliff nobody sees in a diff.
20. **A generic algorithm shared across numeric types goes through the platform's numeric interfaces**
    (`INumber<T>`, `IBinaryInteger<T>` and neighbours) and their static abstract members, rather than a
    separate overload per concrete type or a run-time dispatch on `typeof`. A static abstract interface
    member is resolved at compile time from the generic type parameter, so a `Sum<T>(IEnumerable<T> values)
    where T : INumber<T>` written once compiles to a direct call per instantiation — no boxing, no
    reflection — for `int`, `decimal` or a custom value type that implements the interface, which a
    hand-written overload set cannot offer without duplicating the body once per type.
21. **A partial property or indexer pairs a generated backing implementation with a hand-written
    declaration**, the same split partial classes already have for methods. Where the language version
    supports it, the declaring part states the signature and the implementing part supplies the body — most
    often the implementing part is what a source generator emits, so the property can be backed by
    generated storage without either side needing to know the other's file. The rule is the same as any
    other generated pairing: the hand-written half never reaches into what the generator owns, and the
    generated half is never hand-edited, because the next build silently discards the edit.
22. **A `ref struct` that will implement an interface or flow through a generic method says so on purpose.**
    Since C# 13, a `ref struct` can implement an interface and be used as a type argument for a generic
    parameter constrained with `allows ref struct` — but the ordinary restrictions still apply everywhere
    else: it cannot be boxed, cannot sit in a field of a class or of a non-`ref` struct, and cannot be
    captured by a lambda or a local function. Reach for it when the type genuinely wraps a stack-only buffer
    (a `Span<T>`-backed parser, a pooled accumulator) — not as a general performance switch, because the
    moment the type needs to outlive the call or be stored anywhere, the restrictions turn into rewrites.
23. **A discriminated union of a fixed, closed set of shapes is a `sealed` base with a private constructor
    and a `sealed` record per case, matched with `switch` — never an `enum` carrying an "extra data" field
    on the side.** The enum-plus-payload version has one field meaning something different depending on
    another field's value, which nothing enforces; the sealed hierarchy makes the compiler's exhaustiveness
    check (§7.10) mean something, because each case is its own type instead of a discriminator column a
    reader has to cross-reference by hand.
24. **`protected internal` and `private protected` are two different intersections, not two spellings of the
    same idea, and the wrong one silently widens the member.** `protected internal` means "protected OR
    internal" — reachable from any derived class in any assembly, and from anywhere in this assembly even
    without inheriting. `private protected` means "protected AND internal" — a derived class only gets in if
    it also lives in this assembly. Reaching for the first when the second was meant hands the member to
    every internal caller in the project, not only to the subclasses it was scoped for.
25. **A conversion operator (`implicit`/`explicit`) is declared only where the conversion cannot lose
    information or throw, and is `explicit` the moment it can.** An `implicit` operator runs at every
    assignment and every call site with no syntax marking that a conversion happened at all, so a lossy or
    throwing one surfaces as a bug with no visible cause in the calling code. A value object wrapping a
    primitive (§4.12) is the common case tempted into this — prefer a named factory or accessor over an
    implicit conversion back to the wrapped primitive, so unwrapping stays visible at the call site.
26. **An operator overload changes what `+`, `==` or `<` mean for the type, and is reserved for a type where
    that operation already has one unambiguous mathematical or domain meaning** — a `Money` addition, a
    `Vector` sum, a value object's equality. Overloading `+` to mean "merge" or "combine" on a type with no
    single obvious meaning for it trades a named method a reader can grep and hover over for a symbol that
    silently means something different than it does on every built-in type.
27. **Generic variance (`in`/`out` on a generic interface's type parameter) is declared only when every
    member of the interface actually respects it** — `out T` only where `T` appears solely in return
    position, `in T` only where it appears solely in parameter position. Forcing variance onto an interface
    that also exposes `T` the other way doesn't compile, but forcing it onto one that merely happens to
    compile hides a subtler cost: `IEnumerable<Derived>` assigned to `IEnumerable<Base>` (covariance) means
    the consumer can no longer be handed something that writes into it, which is the actual trade being
    made, not a free upcast.
