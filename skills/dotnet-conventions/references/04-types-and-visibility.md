# § 4 — Types and visibility: the prohibitions

> Section 4 of `skills/dotnet-conventions`. Read it when a type is declared, a member's visibility is
> chosen, or one of the constructs below is about to be used. These are stated as prohibitions on purpose:
> "allowed but rare" is not a reviewable rule.

1. **No mutable global state**: no `public`/`internal static` mutable field or property, no singleton class
   with a static `.Instance` holding mutable state, no `[ThreadStatic]`. Ambient static reads
   (`DateTime.Now`, a static current-context accessor) are injected instead, which also makes them
   testable. Static state is the costliest to diagnose: state surviving between tests makes order matter,
   so the suite fails in whichever test ran second and passes alone.
2. **No nested class**, with no private exception: it hides a type from search and from the file layout.
   Give it its own file. A reader looking for `OrderLine` finds nothing because it is `Order.OrderLine`
   inside `Order.cs` — and is usually looking because something about it is wrong.
3. **No local function** doing real work or capturing the enclosing method's locals: it's a method that
   avoided being named and tested. The capture hurts: the function reads a local the caller may reassign
   after it is declared, so its behaviour depends on where in the method it is called.
4. **No tuple returned across a public or internal boundary**: a tuple names no concept, carries no
   behaviour and validates nothing. Return a record. Positional access is the mechanical problem: two
   fields of the same type can be read in the wrong order with no error, and adding a third silently
   changes what every existing destructuring means.
5. **No anonymous type crossing a boundary** — returned from a non-private method, serialised into a
   response, stored in a field that outlives the method, or passed as `object`/`dynamic`. It has no name to
   reference and no contract to check. Serialised into a response it is worse: the wire contract is
   whatever the projection selected, so a change to the query changes the API.
6. **Explicit types over `var`**, and `dynamic` not at all: an explicit type keeps a diff readable without
   an IDE and surfaces an API change at the call site. `var` stays acceptable where the type is stated on
   the same line (`new`, a cast). With `var`, a method whose return type changed still compiles at every
   call site and fails downstream, and diff review sees nothing.
7. **No `unsafe`**, no pointer types, no native allocators, no reinterpret-casts. Business code has no
   reason to leave the verifiable subset. What is given up is not performance but the runtime's
   guarantees: a bug here is memory corruption rather than an exception, surfacing far from its cause.
8. **No `volatile`.** It's a memory-barrier hint, not synchronisation: it doesn't make `counter++` atomic
   and gives no mutual exclusion. Use the actual primitive (`lock`, `Interlocked`, a concurrent
   collection). It keeps being reached for because it makes a race *less likely*, the worst outcome — the
   bug survives testing and appears under load.
9. **No bitwise operators** in business code — they belong to cryptography, binary protocols and low-level
   work. `&`/`|` on `bool` operands is also a real bug source: they don't short-circuit, so both sides
   evaluate, side effects included. That is how a null check followed by a dereference on the same line
   throws despite reading correctly.
10. Every member starts at the **most restrictive** access modifier that works (default `private`) and is
    widened one rung only when a real caller requires it. Widening a member so a test can call it is a
    design smell: test through the public surface. A widened member is also a promise: callable from
    anywhere in that scope from then on, and nothing tells you when someone starts.
11. **Every new concrete class is `sealed` by default.** Inheritance is an explicit design decision made
    once, not left open "in case" — polymorphism runs through an interface, and a base class meant to be
    extended says so by being unsealed on purpose. An unsealed class also makes every `protected` member
    and internal call between its own methods part of its public behaviour, a contract nobody wrote down.
12. **A data-carrying type (DTO, wire payload, command/query payload, value object) defaults to a `sealed`
    positional record**, or a `readonly record struct` for a small value type — value equality and
    immutability come from the language instead of hand-rolled `Equals`/`GetHashCode`/mutable setters. This
    is also where a primary constructor is the right tool (point 02.1's carve-out): a record's parameters
    become public init-only properties, not a hidden mutable field.
13. **File-scoped namespaces** (`namespace Foo;` on its own line) on every new file, never the braced
    wrapper — one indentation level saved on every type, no loss of information.
14. **No `#region`.** It's unenforced structure: a region can silently stop matching its contents after a
    few edits, and invites cramming unrelated things under one folded heading instead of splitting the
    file. Split into a smaller type instead of folding.
15. **Every enum member carries an explicit numeric value.** The implicit ordinals are what the ORM writes
    to the database and the serialiser puts on the wire, so inserting a member mid-list or reordering two
    silently changes the meaning of existing data — no migration, no error, no failing test. Pinning the
    values costs one line per member and makes a reorder harmless.
    The analyser set agrees only if one member holds zero: the design-rule analyser for enums
    (CA1008, on under `AnalysisMode All`) rejects an enum whose numbering starts at one. Name the zero
    member (`None`, `Unknown`) as the explicit "unset" sentinel, so `default(T)` is a value you chose
    rather than an unnamed one (§5.13, §7.10).
16. **A member that returns a sequence declares the read-only interface**, not the concrete list or array.
    It is a **view, not a barrier**: the caller can't add or remove through it, but it is not a defensive
    copy. The half with no override is the other one: private collection state is never exposed through a
    mutable declared type, which hands out a live handle on the object's own invariant.
17. **One casing per kind, one role suffix per type**, applied to new code and to renames you were asked to
    make. Existing names stay: renaming a public type is a contract change, never a drive-by cleanup.
    Consistency earns its place because of search: where the same kind of thing is named the same way, a
    grep finds all of them, and grep is the tool everybody uses.
18. **The `file` access modifier for a type meant to exist in exactly one file** — a small helper generated
    beside a source generator's output, or a scratch implementation type backing one feature that nothing
    else should reference. Where the language version supports it, `file` gives that type a scope narrower
    than `internal` without nested-class's cost of hiding it from a top-level search (point 2): it still
    appears in the file listing under its own name, merely can't be named from another file, and two
    unrelated `file` types can reuse an identifier with no collision.
19. **A struct that never mutates its own state is declared `readonly struct`.** The modifier is a promise
    the compiler checks — every field read-only, every member non-mutating — and the payoff is that passing
    it by `in` needs no defensive copy before each call. A struct only conventionally immutable gets that
    copy on every `in` parameter and readonly-field access silently, a performance cliff nobody sees in a
    diff.
20. **A generic algorithm shared across numeric types goes through the platform's numeric interfaces**
    (`INumber<T>`, `IBinaryInteger<T>` and neighbours) and their static abstract members, rather than an
    overload per concrete type or run-time dispatch on `typeof`. A static abstract member is resolved at
    compile time from the type parameter, so `Sum<T>(IEnumerable<T> values) where T : INumber<T>` written
    once compiles to a direct call per instantiation — no boxing, no reflection — for `int`, `decimal` or a
    custom value type, which a hand-written overload set can't offer without duplicating the body per type.
21. **A partial property or indexer pairs a generated backing implementation with a hand-written
    declaration**, as partial classes already do for methods. Where the language version supports it, the
    declaring part states the signature and the implementing part (often a source generator's output)
    supplies the body, so the property can be backed by generated storage without either side knowing the
    other's file. As with any generated pairing, the hand-written half never reaches into what the
    generator owns, and the generated half is never hand-edited: the next build silently discards the edit.
22. **A `ref struct` that will implement an interface or flow through a generic method says so on
    purpose.** Since C# 13, a `ref struct` can implement an interface and be a type argument for a generic
    parameter constrained with `allows ref struct` — but the ordinary restrictions still apply: no boxing,
    no field of a class or non-`ref` struct, no capture by a lambda or local function. Use it when the type
    genuinely wraps a stack-only buffer (a `Span<T>`-backed parser, a pooled accumulator), not as a general
    performance switch: once the type must outlive the call or be stored, the restrictions become rewrites.
23. **A discriminated union of a fixed, closed set of shapes is a `sealed` base with a private constructor
    and a `sealed` record per case, matched with `switch` — never an `enum` carrying an "extra data" field
    on the side.** The enum-plus-payload version has one field meaning something different depending on
    another, which nothing enforces; the sealed hierarchy makes the compiler's exhaustiveness check (§7.10)
    mean something, since each case is its own type rather than a discriminator column cross-referenced by
    hand.
24. **`protected internal` and `private protected` are two different intersections, and the wrong one
    silently widens the member.** `protected internal` means "protected OR internal" — reachable from any
    derived class in any assembly, and from anywhere in this assembly without inheriting. `private
    protected` means "protected AND internal" — a derived class gets in only if it also lives in this
    assembly. Using the first when the second was meant hands the member to every internal caller in the
    project, not only the intended subclasses.
25. **A conversion operator (`implicit`/`explicit`) is declared only where the conversion cannot lose
    information or throw, and is `explicit` the moment it can.** An `implicit` operator runs at every
    assignment and call site with no syntax marking it, so a lossy or throwing one surfaces as a bug with no
    visible cause. A value object wrapping a primitive (§4.12) is the common temptation — prefer a named
    factory or accessor over an implicit conversion back to the primitive, so unwrapping stays visible.
26. **An operator overload changes what `+`, `==` or `<` mean for the type, and is reserved for a type where
    that operation already has one unambiguous mathematical or domain meaning** — a `Money` addition, a
    `Vector` sum, a value object's equality. Overloading `+` to mean "merge" or "combine" on a type with no
    single obvious meaning trades a greppable, hoverable named method for a symbol that silently means
    something different than on every built-in type.
27. **Generic variance (`in`/`out` on a generic interface's type parameter) is declared only when every
    member of the interface respects it** — `out T` only where `T` appears solely in return position, `in
    T` only solely in parameter position. Forcing variance onto an interface exposing `T` the other way
    doesn't compile, but forcing it onto one that merely compiles hides a subtler cost:
    `IEnumerable<Derived>` assigned to `IEnumerable<Base>` (covariance) means the consumer can no longer be
    handed something that writes into it — the actual trade, not a free upcast.
28. **The `required` modifier (C# 11) states which properties a caller must set, and is the boundary check
    a constructor parameter was the only way to express on an object-initializer-built type.** A positional
    record's constructor already enforces this (§4.12); a class or record built through object initializers
    relied on every caller remembering the field, with nothing catching the one that forgot until a null or
    default surfaced downstream. `required` moves the check to the construction site and the compiler, at
    the cost that a `required` member cannot be `private` — it exists to be seen by whoever constructs the
    type, not to replace a constructor for members nobody outside should set.
29. **`SetsRequiredMembersAttribute` on a constructor is a promise the compiler can only trust.** It tells
    the compiler this constructor already assigns every `required` member, so callers through it are exempt
    from setting them in an object initializer — correct for a constructor that does the assignment, a
    silent hole in point 28's guarantee for one that doesn't, since nothing re-checks the body against the
    claim.
30. **An interface default implementation changes behaviour for every existing implementer the moment it's
    added, the opposite of what adding an interface member used to mean.** Adding a method used to be a
    breaking change every implementer handled explicitly; a default implementation makes it compile
    silently for types that don't override it — the intended evolution path for a published interface — but
    using a default body to avoid touching implementers of an interface owned entirely within this codebase
    hides a decision (what should the untouched implementers do) behind a fallback nobody chose per type.
31. **A `static` member on an interface, reachable through a generic constraint, is a different mechanism
    from a default implementation and answers a different question.** Point 20 covers static abstract
    members for numeric-style algorithms; a plain `static` (non-abstract) interface member is shared code
    called through the interface type, not an instance — useful for a factory method or a constant common
    to every implementer, and confusing when a reader expects `IFoo.Create()` to dispatch polymorphically
    when it resolves to exactly one implementation chosen at the call site.
32. **A `readonly` member on a mutable struct is a promise about that one member, not the struct.** Marking
    a method or accessor `readonly` inside a struct that is not itself `readonly` (point 19) states that
    this member doesn't mutate the instance, letting the compiler skip the defensive copy for that member
    alone on an `in` parameter or `readonly` field — other members can still mutate, so the type-level
    guarantee of point 19 and this member-level one are not interchangeable, and marking every member
    `readonly` individually is not marking the struct `readonly`.
33. **`params` accepting any collection type or span (C# 13), not only an array, changes what a caller can
    pass without changing what the method promises.** A `params ReadOnlySpan<T>` accepts a stack-allocated
    buffer with no heap array — a real win on a hot path — but a span parameter can't be stored past the
    call (it's a `ref struct`, point 22's restrictions apply), so a `params` method that let its array
    argument be captured or returned changes its contract when the parameter moves from array to span, and
    every caller relying on the old array's identity must be checked, not just recompiled.
34. **A type alias (`using Alias = Namespace.Type;`, or a global one) renames a type for the file or project
    declaring it, and a reader who only sees the alias has no path back to the real type without finding
    the `using` line.** It earns its place for a generic instantiation reused so often that spelling it out
    hides the surrounding code, or for disambiguating two same-named types from different namespaces in one
    file. As a shorthand for an ordinary type with an inconvenient name it trades the type's searchable
    identity (point 17's reasoning) for a nickname greps for the real name will never find.
35. **A `sealed` or `abstract` modifier declared on any one part of a partial class applies to the whole
    type, and the other parts do not repeat it.** The compiler merges the parts into one declaration before
    point 11's inheritance reasoning applies, so a type split across two files is sealed once either file
    says so — a reviewer checking whether a partial type is extensible must find every part, because the
    file in front of them may be the one that left the modifier off.
36. **An interceptor substitutes a different method body for a specific call site at compile time, with
    nothing at that call site's source marking it.** The mechanism exists for source generators — replacing
    a LINQ-to-objects call with a pre-translated one, as EF Core's AOT query compilation does — and is
    scoped by `InterceptorsNamespaces`, the project setting listing which namespaces may contain one. That
    scope is its only visibility control: widening it carelessly makes "what does this call actually run"
    unanswerable from the call site, the search-defeating cost point 2 charges a nested class, paid for an
    entire compilation instead of one type.
37. **`UnsafeAccessorAttribute` reaches a private member from outside the type with no reflection and no
    run-time lookup cost, which is why it is no routine substitute for widening the member (point 10).** It
    exists for a narrow set of cases — a serializer or test harness that must reach a field on a type it
    doesn't own and can't change, where reflection's cost or incompatibility with trimming and Native AOT
    rules it out. Every other case is still point 10's question — does a real caller need this member
    widened? — answered honestly, not routed around through an attribute that hides the access from the
    type's own file.
38. **`UnsafeAccessorType` names the target type by an assembly-qualified string instead of a compile-time
    type reference, trading point 37's compile-time-checked binding for one resolved at run time.** It
    serves the case point 37 can't reach — a private member on a type not referenceable from the caller's
    compilation (one in a dynamically loaded assembly, or one whose public surface doesn't expose the
    type) — and inherits the trade's costs: a typo in the string, or a rename in the target assembly,
    fails at run time with no compiler catching it, where the ordinary form fails the build.
39. **`[DynamicallyAccessedMembers]` states, for a type or generic parameter reached only through
    reflection, which members a trimmer or AOT compiler must keep though nothing in the visible call graph
    references them.** A generic method calling `.GetProperties()` on `typeof(T)` has no static reference to
    any of `T`'s properties, so a trimmed build removes them unless the parameter is annotated with the
    member kinds the reflection needs. The annotation is a visibility contract read by tooling, not the
    compiler, and an unannotated reflection path is where point 10's access-modifier discipline is
    invisible to the thing that most needs to see it.
40. **Sealing a class also lets the JIT devirtualize a call through it — resolve which method runs at
    compile time instead of by virtual dispatch — and that payoff reaches only call sites the compiler can
    see are sealed.** Point 11 states `sealed` as the default for its own design reason; performance is a
    second, independent argument, and it is why a class left unsealed "just in case" costs more than an
    open design question: every call through it, in every referencing assembly, pays a virtual-dispatch
    cost point 11's inheritance argument alone wouldn't have made visible.
41. **A record's positional equality is anchored on a compiler-generated `EqualityContract` property, not
    the fields alone, and a derived record that fails to override it inherits the base's contract.** Two
    records with identical field values compare unequal across different types because `EqualityContract`
    differs by design — the guard against one type's instance equalling another's — but a derived record
    not participating correctly in that override (a rare hand-written `Equals`, or a base declared
    unintentionally without the usual record machinery) can compare equal to a sibling type with the same
    fields, which no generic constraint catches since there is no `where T : record` (point 12's default
    gets this right automatically; only a hand-rolled override can lose it).
42. **Sealing only the `ToString()` override on an otherwise-unsealed record locks the format contract for
    every derived type without sealing the type, a narrower decision than point 11's "seal the class by
    default."** A base record meant to be extended (point 11's carve-out, applied to a record) can still
    guarantee that `ToString()`'s output shape — the property list a derived type inherits — isn't silently
    reshaped by a subclass override; the modifier applies member by member, as point 32 states for a
    `readonly` member on an otherwise-mutable struct.
43. **There is no generic constraint for "must be a record"** — a `record class` satisfies an ordinary
    `class` constraint and a `record struct` an ordinary `struct` constraint, and nothing at the constraint
    level distinguishes either from a hand-written type. A generic algorithm assuming point 12's value
    semantics (structural equality, immutability) because its parameter is *usually* a record has no
    compiler-enforced guarantee: a caller can supply an ordinary mutable class satisfying the same `class`
    constraint, and the assumption silently stops holding for that instantiation with no error.
44. **A static abstract interface member (point 20) cannot carry a default body as an ordinary default
    interface member (point 30) can — the two look like one feature applied to statics but answer different
    questions about who must implement what.** An instance default implementation exists so an existing
    implementer compiles unchanged (point 30); a static abstract member has no instance to fall back on and
    no implementer predating it in point 30's sense, so every type declaring it satisfies the constraint
    must supply its own implementation — expecting point 30's "safe to add without breaking anyone" gets a
    compile error for every type already implementing the interface.
45. **`UnsafeAccessorAttribute` (§4.37) targeting a closed generic type resolves differently from targeting
    the open generic definition, and a version upgrade can change which one a declaration means.**
    Accessing a private member on `Repository<Order>` is not the same request as on `Repository<T>` in the
    abstract — the runtime's rules for matching a closed-generic target changed between .NET releases
    without the attribute's syntax changing, so code written against one release's resolution is worth
    re-verifying after an SDK upgrade, the same read-the-current-behaviour discipline §9.38 states for the
    same attribute from the publish side.
46. **`in`/`out` variance declared on a generic interface (point 27) is invariant by default and must be
    requested on each type parameter individually, not inherited from a base interface that declared it.**
    An interface extending a covariant `IReadOnly<out T>` with its own additional generic parameter does
    not make that parameter variant — point 27 checks each parameter's own usage, so a derived interface
    adding an invariant-shaped member reintroduces the "can no longer be handed something that writes into
    it" trade, scoped to the parameter never declared variant.
47. **An application project (an executable, a web host) makes every type `internal`, and the analyser set
    says so by itself.** Under `AnalysisMode All` the rule on unneeded public types (CA1515) fails the
    build on every `public` type in a project nothing references, which is point 10 enforced rather than
    advised. The same set then reports every `internal` class that only the container constructs as
    never instantiated (CA1812), since a registration by generic argument is not a `new` the analyser can
    see: that finding is false by construction here, so scope it off in the project's editor configuration
    beside the naming rules (Guardrails), and do not widen the type or add a dummy construction to
    silence it. The test project that needs the types reaches them through `InternalsVisibleTo`, not by
    re-widening.
