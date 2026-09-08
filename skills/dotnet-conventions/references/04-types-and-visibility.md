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
