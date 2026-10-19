# swift-conventions §5 — Reference ownership and memory access

> Section 5 of `skills/swift-conventions`. Read it when a class holds another class, a closure is stored or
> escapes, a delegate or parent link is declared, or an in-out argument is passed. Rewritten from the
> language guide's reference-counting and memory-safety chapters (`references/origin.md`).

1. **Two class instances that hold each other strongly are never freed.** The same happens between an
   instance and a closure stored on it that mentions `self`. A leak shows as a deinitialiser that never runs.
2. **Break the cycle with the weaker reference that matches the lifetimes.** Use `weak` when the other side can
   be freed first (it is optional and becomes nil automatically). Use `unowned` when the other side has the
   same lifetime or a longer one and is always present; accessing it after it is freed is a runtime error, so
   only when that is certain. A weak reference is no cache: with reference counting a value is freed the
   moment its last strong reference goes.
3. **A closure that is stored and captures a class instance declares a capture list.** Capture `self`
   unowned when the closure and the instance always die together; capture it weak when it can become nil, and
   unwrap inside. If the captured reference can never be nil, prefer unowned over weak. The unsafe unowned
   form disables the runtime check and is a conscious exception.
4. **Ownership is a design statement.** The parent holds children strongly; the child's back-reference
   (delegate, parent, owner) is the weak or unowned one.
5. **Do not give two simultaneous in-out arguments the same variable, and do not read a variable while it is
   being passed as in-out.** An in-out access lasts for the whole call, so reading the original (a global used
   inside the function) or passing it twice is a conflicting access, reported at compile time or run time even
   on one thread. Copy the value first when the read is wanted.
