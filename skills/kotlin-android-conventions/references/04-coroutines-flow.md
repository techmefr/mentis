# kotlin-android-conventions §4 — Coroutines and Flow

> Section 4 of `skills/kotlin-android-conventions`. Read it when a coroutine is launched, a suspending
> function is written, a flow is built or collected, shared state is touched from several coroutines, or a
> dispatcher is chosen. Rewritten from the coroutines library documentation and the platform vendor's
> coroutine best-practices page (`references/origin.md`).

1. **Every coroutine has an owner and a lifetime.** New coroutines start only from a scope whose lifecycle
   is stated: a screen-bound scope for work that ends with the screen, an application-level scope passed in
   for work that must outlive it. A parent waits for its children and cancelling it cancels them, so the tree
   is what makes cancellation and failure predictable. Do not launch from an initialiser with a scope nobody
   owns.
2. **No global scope.** It is a delicate API: it has no lifecycle, hardcodes the context and blocks controlled
   execution in tests. The one legitimate use, a root coroutine for the whole application, is opted into
   explicitly. Inject a scope instead.
3. **A suspending function is safe to call from the main thread.** It switches to its own dispatcher
   internally (a context switch inside the function), so callers never have to know which thread the work
   needs. Dispatchers are injected, not named in the body, so a test can replace them.
4. **Cancellation is cooperative.** A coroutine stops at its next suspension point; code that runs long
   without suspending never stops. In a long computation or a loop call the periodic yield, or check the
   active flag or the ensure-active call. Blocking calls that support thread interruption are wrapped in the
   interruptible helper, or cancellation will not interrupt them. A custom suspending bridge built with the
   non-cancellable primitive ignores cancellation: use the cancellable one.
5. **Never swallow the cancellation exception.** Catching a broad exception type around a suspending call also
   catches it and breaks propagation; if it must be caught, rethrow it. Catch the specific failure types the
   call can raise.
6. **Cleanup that suspends runs in a non-cancellable context, used narrowly.** Closing a resource with a
   suspending close after cancellation is the use case; apply the non-cancellable context through a context
   switch inside the cleanup, never as an argument to a launch or async, which detaches the child from its
   parent.
7. **Failure goes up the tree.** A child failing with anything other than cancellation cancels its parent, and
   the original exception is handled once all children have terminated. Cancelling a child does not cancel its
   parent. A handler installed on a child of a regular scope has no effect; handlers belong on root
   coroutines and cannot recover. For an async result the exception is held until it is awaited.
8. **Use a supervisor only when sibling failure must be independent**, such as sub-tasks of a screen where one
   failing should not cancel the others. Do not reach for it to hide an exception.
9. **Shared mutable state needs a real mechanism.** A volatile flag does not make an increment atomic. Choose
   one: a thread-safe structure or atomic for a simple counter, confinement of the state to a single
   dispatcher in coarse chunks (fine-grained switching per update is very slow), or a mutex for critical
   sections.
10. **A flow keeps its context.** Do not change the context with a context switch inside a flow builder or
    emit from another coroutine; set the upstream context with the flow-on operator, and collect in the
    caller's context. An exception thrown by the collector surfaces inside the builder: if the builder
    catches it, it rethrows it, so the caller of collect handles it (exception transparency). Failures of the
    upstream flow are handled with the flow's own catch operator.
11. **Expose read-only types.** A view model or repository holds the mutable state or flow privately and
    exposes the read-only state flow or flow, so every change goes through one class. The data and business
    layers expose suspending functions and flows, so the caller decides when the work runs and can cancel it.
12. **A view model creates the coroutines for its screen**, so the logic is unit-testable and the work
    survives configuration change; exceptions of those coroutines are caught at that boundary.
