# cpp-conventions §2 — Resources and ownership

> Section 2 of `skills/cpp-conventions`. Read it when `new` or `delete` appears, a raw pointer or a smart
> pointer is in a signature, a resource (memory, file, lock, handle) must be released, or an object is shared.
> The error side of the same problem is §3, the class-level rules (destructors, copy, move) are §4. The other
> sections and the guardrails stay in `SKILL.md`.

1. **A resource is owned by an object, and the object's destructor releases it (RAII).** Every acquire/release
   pair (open/close, lock/unlock, allocate/free) is wrapped in a handle whose constructor acquires and whose
   destructor releases, so release happens on every exit path, exceptions included. Calling `fclose` by hand
   at the end of a function is a leak on every early return.
2. **Raw pointers and references do not own.** A raw pointer or a reference in an interface denotes access to
   one object, never ownership; ownership is stated with a type. Never transfer ownership through a raw
   pointer or reference: if there is doubt about who frees a returned pointer, the code leaks or frees early.
   Return an owning smart pointer or the object by value, and a raw pointer only to designate a position.
3. **Do not heap-allocate unnecessarily.** A scoped object (a local, a member) is simpler, faster and safe. Use
   `new` and `delete` only inside the functions that implement a resource handle; avoid `malloc` and `free`
   (they do not run constructors or destructors); never allocate in the middle of an expression with other
   side effects, and give the result of an explicit allocation to a manager object in the same statement.
   Overload allocation and deallocation operators in matched pairs.
4. **Smart pointers say what they mean.** `unique_ptr` represents exclusive ownership and is the default: it is
   simpler, predictable (you know when destruction happens) and does not pay for a reference count.
   `shared_ptr` only when ownership is genuinely shared, and `weak_ptr` to break cycles. Construct them with
   `make_unique` and `make_shared`. Do not hold a pointer in a local without a smart pointer owning the object.
5. **Take smart pointers as parameters only to express lifetime.** A function that uses an object takes a raw
   pointer or a reference to it, so callers are free to own it however they like. A `unique_ptr` by value means
   "this function takes ownership"; by non-const reference it means "this function may reseat it"; a
   `shared_ptr` by value means "this function shares ownership"; by non-const reference it may reseat the
   pointer. Do not hand a function a raw pointer or reference taken from a smart pointer that something else can
   reset during the call.
6. **If a class holds a raw pointer or reference, decide whether it might own.** If it owns, it has a
   destructor and the copy rules of §4.2; if it does not, the type says so (a view, a `not_null`-style
   wrapper) and the owner outlives it.
7. **Never return a pointer or reference to a local**, and never return an rvalue reference. Do not write
   `return std::move(local)`: it prevents the optimisation. Write `std::move` only when you really move an
   object to another scope. Return multiple values in a struct.
8. **Arrays and `delete[]`.** Delete arrays with `delete[]` and single objects with `delete`; better, use
   a container so the question never arises. Indexing an array of derived objects through a base pointer
   steps by the wrong size, so keep that conversion out of the code.
9. **Avoid mutable global state and singletons.** A non-constant global hides dependencies and is subject to
   unpredictable change; a singleton is a global in disguise. Pass the state in. Avoid complex initialisation of
   global objects, whose order across translation units is not defined.
10. **Locks are RAII objects** (§5.2). A mutex is never locked and unlocked by hand.
11. **Encapsulate the rule violations you cannot avoid.** When a raw `new`, a cast or an unsafe call is
    unavoidable, confine it to one small function behind a safe interface, and name it, so the rest of the code
    does not spread the mess and a reviewer has one place to read.
12. **A resource handle with pointer semantics provides `*` and `->`;** a type that acts like a container
    follows the standard container interface (value semantics, move operations, an initializer-list
    constructor, a default constructor that makes it empty).
