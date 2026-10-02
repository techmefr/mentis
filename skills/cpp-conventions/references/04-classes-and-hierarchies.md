# cpp-conventions §4 — Classes and hierarchies

> Section 4 of `skills/cpp-conventions`. Read it when a class is designed, a constructor, destructor, copy
> or move operation is written or deleted, a virtual function or a base class appears, an operator is
> overloaded, or a union is used. Resource ownership at the object level is §2; exceptions thrown by
> constructors are §3. The other sections and the guardrails stay in `SKILL.md`.

1. **Prefer concrete, regular types over hierarchies.** A type that behaves like a built-in (copyable or
   movable, comparable where it makes sense, usable as a value) is easier to reason about than a class used
   through a base pointer. Use a hierarchy only to represent a concept with an inherent hierarchical structure.
   Group data that belongs together in a struct or class. A function becomes a member when it needs the
   representation itself; helpers live as free functions in the class's namespace. Const or reference data
   members break copying and moving, so leave them out of such types, and list members in the order their
   initialisation depends on.
2. **Rule of zero, otherwise rule of five.** If a class can rely on the compiler's copy, move and destructor,
   define none of them: its members already do the right thing. If you define or delete *any* of the
   destructor, copy and move operations, define or delete *all* of them, because the semantics are closely
   related and declaring one suppresses the implicit generation of others (declaring a destructor or a copy
   operation suppresses the implicit move; declaring a move makes the implicit copy deleted). Keep them
   consistent with each other, and use `=default` to be explicit about default semantics and `=delete` to forbid
   an operation without an alternative. A polymorphic class suppresses public copy and move and provides a
   virtual `clone` where copying is needed.
3. **Destructors.** Define one when the class needs an action at destruction; all resources a class acquires are
   released by its destructor, so a class with an owning raw pointer must have one. A destructor never fails
   and is `noexcept`. A base class destructor takes one of two shapes: public and virtual, or protected and non-virtual.
   Anything else makes deletion through a base pointer undefined. A class with a virtual function
   has one of those destructors.
4. **Copy, move, swap, equality.** A copy operation copies; a move operation moves and leaves the source valid;
   both are safe for self-assignment, non-virtual, and take and return the conventional types
   (`const T&` in and `T&` out for copy; `T&&` in for move). Move operations and `swap` are `noexcept` and
   never fail. `==` is symmetric in its operand types and `noexcept`; beware of `==` on a base class. A `hash`
   is `noexcept`. Rely on constructors and assignment, never `memset` or `memcpy`, to copy or clear an object
   that has a constructor.
5. **A class with an invariant is a class with a constructor.** Use `class` if the type has an invariant (some
   relation between its members that must always hold) and `struct` if the members can vary independently.
   Any non-public member also means `class`. An invariant calls for a constructor, and the constructor
   must produce a fully initialised object; if it cannot, it fails (§3.3, §3.9) rather than
   leaving a half-built object. Minimise the exposure of members, keep data members private, and make all
   non-const data members the same access level. Avoid protected data and trivial getters and setters.
6. **Constructors do not do surprising work.**
   - Single-argument constructors are `explicit` by default: an implicit conversion constructor is an
     unintended conversion waiting to be passed to a function.
   - Prefer default member initialisers to member initialiser lists for constant initialisers; do not write a
     default constructor whose only work is to initialise members. Define and initialise members in
     declaration order; prefer initialisation to assignment in the constructor body.
   - Do not call virtual functions in constructors and destructors: the call does not reach the derived class.
     If virtual behaviour is needed during initialisation, use a factory function.
   - Use delegating constructors for the actions common to all constructors.
   - A copyable class has a default constructor, simple and non-throwing where possible.
7. **Virtual functions are a deliberate choice.** Do not make a function virtual without a reason. A virtual
   function states exactly one of `virtual`, `override` or `final`. An interface is a pure abstract class,
   which usually needs no user-written constructor; distinguish interface inheritance from implementation
   inheritance, and prefer composition to implementation inheritance (a style guide asks for composition
   first, and for public inheritance only). Reserve multiple inheritance for combining separate interfaces, or for
   genuinely merging implementation traits, never for convenience. A virtual function and its override must
   not declare different default arguments. Use `final` on a class sparingly.
8. **Navigate a hierarchy rarely and explicitly.** Access polymorphic objects through pointers or references,
   not by value (slicing); prefer a virtual function to a cast; where navigation is unavoidable use
   `dynamic_cast` to a reference when failure is an error and to a pointer when failure is a valid
   alternative. Run-time type information is a last resort in code that you control.
9. **Operators mean their conventional meaning.** Overload operators to mimic conventional usage, only for
   operations that are roughly equivalent to the built-in one, define them in the namespace of their operands
   (and symmetric ones as non-members). Avoid implicit conversion operators, and overload unary `&` only in a
   system of smart pointers and references. Use `using` for customisation points.
10. **Unions.** Avoid naked unions; use a variant type or an anonymous union inside a tagged union class,
    and never use a union for type punning (copy the bytes into an object of the target type instead).
11. **Containers follow the standard.** A container type has value semantics, move operations, a default
    constructor that makes it empty and an initializer-list constructor.
