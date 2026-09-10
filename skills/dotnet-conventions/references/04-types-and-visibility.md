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
28. **The `required` modifier (C# 11) states which properties a caller must set, and is the boundary check
    a constructor parameter used to be the only way to express on an object-initializer-built type.** A
    positional record's constructor already enforces this (§4.12); a class or a record built through object
    initializers instead relied on every caller remembering to set the field, with nothing catching the one
    that forgot until the missing value surfaced downstream as a null or a default. Marking the property
    `required` moves that check to the construction site and to the compiler, at the cost that a `required`
    member cannot be `private` — it exists specifically to be seen by whoever constructs the type, not to
    replace a constructor for members nobody outside the type should set at all.
29. **`SetsRequiredMembersAttribute` on a constructor is a promise the compiler cannot verify, only trust.**
    Applying it tells the compiler that this particular constructor already assigns every `required` member,
    so callers going through it are exempt from setting them again in an object initializer — which is
    correct for a constructor that genuinely does the assignment and a silent hole in point 28's guarantee
    for one that doesn't, because nothing re-checks the body against the claim once the attribute is present.
30. **An interface default implementation changes behaviour for every existing implementer the moment it's
    added, which is the opposite of what adding a member to an interface used to mean.** Before default
    interface members, adding a method to an interface was a breaking change every implementer had to
    handle explicitly; a default implementation instead makes it compile silently for types that don't
    override it, which is the intended migration path for a published interface's evolution — but reaching
    for a default body as a shortcut to avoid touching implementers on an interface owned entirely within
    this codebase hides a decision (what should the untouched implementers actually do) behind a fallback
    nobody chose per type.
31. **A `static` member on an interface, reachable through a generic constraint, is a different mechanism
    from a default implementation and answers a different question.** Point 20 already covers static
    abstract members for numeric-style generic algorithms; a plain `static` (non-abstract) interface member
    is instead shared code called through the interface type itself, not through an instance — useful for a
    factory method or a constant genuinely common to every implementer, and a source of confusion the moment
    a reader expects `IFoo.Create()` to dispatch polymorphically the way an instance call would, when it
    resolves to exactly one implementation chosen at the call site.
32. **A `readonly` member on a mutable struct is a promise about that one member, not about the struct.**
    Marking an individual method or property accessor `readonly` inside a struct that is not itself
    `readonly` (point 19) states that this specific member doesn't mutate the instance, which lets the
    compiler skip the defensive copy for that member alone when called on an `in` parameter or a `readonly`
    field — the rest of the struct's members can still mutate, so the type-level guarantee point 19
    describes and this member-level one are not interchangeable, and marking every member `readonly`
    individually is not the same declaration as marking the struct itself `readonly`.
33. **`params` accepting any collection type or span (C# 13), not only an array, changes what a caller can
    pass without changing what the method promises.** A `params ReadOnlySpan<T>` parameter accepts a stack-
    allocated buffer at the call site with no heap array allocated to hold the arguments, which is a real
    allocation win for a hot path — but a span parameter cannot be stored past the call (it's a `ref struct`,
    point 22's restrictions apply), so a `params` method that used to let its array argument be captured or
    returned changes its own contract the moment its parameter type moves from array to span, and every
    caller relying on the old array's identity has to be checked, not just recompiled.
34. **A type alias (`using Alias = Namespace.Type;`, or a global one project-wide) renames a type for the
    file or project that declares it, and a reader who only ever sees the alias has no path back to the real
    type without knowing to look for the `using` line.** It earns its place for a generic instantiation
    reused often enough that spelling it out every time hides the code around it, or for disambiguating two
    same-named types from different namespaces in one file — reached for instead as a shorthand for an
    ordinary type with an inconvenient name, it trades the type's own searchable identity (point 17's
    reasoning) for a local nickname that greps for the real name will never find.
35. **A `sealed` or `abstract` modifier declared on any one part of a partial class applies to the whole
    type, and the other parts do not repeat it.** The compiler merges the parts into one declaration before
    any of point 11's reasoning about inheritance applies, so a type split across two files is sealed the
    moment either file says so — which also means a reviewer checking whether a partial type is extensible
    has to find every part before concluding it isn't, because the file in front of them may simply be the
    one that left the modifier off.
36. **An interceptor substitutes a different method body for a specific call site at compile time, with
    nothing at that call site's own source marking that it happened.** The mechanism exists for source
    generators — replacing a LINQ-to-objects call with a pre-translated one, the way EF Core's AOT query
    compilation does — and it is scoped by `InterceptorsNamespaces`, the project setting that lists which
    namespaces are trusted to contain one. That scope is the only visibility control it has: a project that
    widens it carelessly makes "what does this call actually run" unanswerable by reading the call site,
    which is the same search-defeating cost point 2 already charges a nested class for, paid here for an
    entire compilation instead of one type.
37. **`UnsafeAccessorAttribute` reaches a private member from outside the type with no reflection and no
    runtime lookup cost, and that is precisely why it is not a routine substitute for widening the member
    (point 10).** It exists for a narrow, named set of cases — a serializer or a test harness that must reach
    a field on a type it does not own and cannot change, where reflection's cost or its incompatibility with
    trimming and Native AOT rules it out — and every other case is still point 10's question: does a real
    caller need this member widened, answered honestly, not routed around through an attribute that makes the
    access invisible in the type's own file.
38. **`UnsafeAccessorType` names the target type by an assembly-qualified string instead of by a compile-time
    type reference, which trades point 37's compile-time-checked binding for one resolved at run time.** It
    exists for the case point 37 cannot reach at all — a private member on a type that isn't referenceable
    from the caller's compilation, such as one in an assembly loaded dynamically or one whose public surface
    doesn't expose the type itself — and it inherits every cost that trade implies: a typo in the string, or
    a rename in the target assembly, fails at run time with no compiler catching it, where the ordinary
    attribute form fails the build instead.
39. **`[DynamicallyAccessedMembers]` states, for a type or a generic parameter reached only through
    reflection, which of its members a trimmer or an AOT compiler must keep even though nothing in the
    visible call graph references them.** A generic method that calls `.GetProperties()` on `typeof(T)` has
    no static reference from that call to any of `T`'s actual properties, so a trimmed build removes them
    unless the parameter is annotated with which member kinds the reflection code needs — the annotation is a
    visibility contract read by the tooling rather than the compiler, and an unannotated reflection path is
    the one place point 10's access-modifier discipline is invisible to the thing that most needs to see it.
40. **Sealing a class is also what lets the JIT devirtualize a call through it — resolve which method runs at
    compile time instead of through a virtual dispatch — and that payoff only reaches call sites the compiler
    can actually see are sealed.** Point 11 already states `sealed` as the inheritance default for its own
    design reason; the performance case is a second, independent argument for the same default, and it is why
    a class kept unsealed "just in case" costs more than an open design question — every call through it, in
    every assembly that references it, pays the virtual-dispatch cost point 11's inheritance argument alone
    would not have made visible.
41. **A record's positional equality is anchored on a compiler-generated `EqualityContract` property, not on
    the fields alone, and a derived record that fails to override it inherits the base's contract instead of
    getting its own.** Two records with identical field values compare unequal across different types
    precisely because `EqualityContract` differs by design — the guard against one type's instance silently
    equalling another's — but a derived record that doesn't participate correctly in that override (a rare
    hand-written `Equals`, or a base declared unintentionally without the usual record machinery) can end up
    comparing equal to a sibling type sharing the same fields, which no generic constraint catches because
    there is no `where T : record` to enforce it (point 12's default gets this right automatically; only a
    hand-rolled override can lose it).
42. **Sealing only the `ToString()` override on an otherwise-unsealed record locks the format contract for
    every derived type without sealing the type itself, which is a narrower and different decision from point
    11's "seal the class by default."** A base record meant to be extended (point 11's carve-out, applied to a
    record) can still guarantee that `ToString()`'s output shape — the property list a derived type inherits —
    isn't silently reshaped by a subclass overriding it for its own purposes; the modifier applies member by
    member here, the same way point 32 already states for a `readonly` member on an otherwise-mutable struct.
43. **There is no generic constraint for "must be a record"** — a `record class` satisfies an ordinary `class`
    constraint and a `record struct` satisfies an ordinary `struct` constraint, and nothing distinguishes
    either from a hand-written type at the constraint level. A generic algorithm written assuming point 12's
    value semantics (structural equality, immutability) because its type parameter is *usually* instantiated
    with a record has no compiler-enforced guarantee of that — a caller can supply an ordinary mutable class
    satisfying the same `class` constraint, and the algorithm's assumption about equality or immutability
    silently stops holding for that instantiation with no error anywhere.
44. **A static abstract interface member (point 20) cannot carry a default body the way an ordinary default
    interface member (point 30) can — the two mechanisms look like the same feature applied to statics but
    answer different questions about who is required to implement what.** An instance default implementation
    exists precisely so an existing implementer compiles unchanged (point 30); a static abstract member has no
    instance to fall back on and no implementer predates it in the way point 30 addresses, so every type that
    declares it satisfies the constraint has to supply its own implementation — reaching for a static abstract
    member expecting point 30's "safe to add without breaking anyone" property gets a compile error instead,
    for every type that already implements the interface.
45. **`UnsafeAccessorAttribute` (§4.37) targeting a closed generic type resolves differently from targeting the
    open generic definition, and a version upgrade can change which one a given declaration actually means.**
    Accessing a private member on `Repository<Order>` specifically is not the same request as accessing it on
    `Repository<T>` in the abstract — the runtime's rules for matching a closed-generic target changed between
    .NET releases without the attribute's own syntax changing, so code written against one release's resolution
    behaviour is worth re-verifying after an SDK upgrade rather than assumed still correct, the same
    read-the-current-behaviour discipline §9.38 states for the same attribute from the publish side.
46. **`in`/`out` variance declared on a generic interface (point 27) is invariant by default and has to be
    requested on each type parameter individually, not inherited from a base interface that already declared
    it.** An interface extending a covariant `IReadOnly<out T>` with its own additional generic parameter of
    its own does not automatically make that new parameter variant — each parameter's own usage inside the
    interface is what point 27 checks, so a derived interface adding an invariant-shaped member reintroduces
    exactly the "can no longer be handed something that writes into it" trade point 27 describes, scoped to
    the parameter that was never declared variant in the first place.
