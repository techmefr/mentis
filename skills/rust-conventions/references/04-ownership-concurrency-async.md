# rust-conventions §4 — Ownership, concurrency and async

> Section 4 of `skills/rust-conventions`. Read it when a smart pointer or a trait object appears in a
> signature, when a `static` or thread-local is added, when a collaborator has to be replaceable in tests, or
> when a task or a future is public or runs for a long time. `unsafe` threading primitives are §3. The other
> sections and the guardrails stay in `SKILL.md`.

1. **The caller decides where data is copied and placed.** A function that needs ownership takes the value;
   a function that only reads it takes a borrow. Taking a borrow and cloning inside hides a copy the caller
   could have avoided, and taking ownership just to drop it forces the caller to clone. Do not put a `Copy`
   bound on a generic unless the body truly needs it.
2. **Wrappers stay inside.** `Rc`, `Arc`, `Box`, `RefCell` and `Mutex` in a public signature leak an
   implementation choice, and the caller can end up unable to satisfy two crates that disagree on the wrapper.
   The public API takes `&T`, `&mut T` or `T`. Exceptions are the cases where the pointer is the purpose of
   the API (a new container) and a benchmark shows the gain justifies the complexity.
3. **Abstractions do not visibly nest.** What a user writes in a field should be one level of type parameter
   at most (`Service` or `Service<Backend>`, not `Service<Backend<Store>>`). Parameters spread to every holder
   of the type, drag trait hierarchies with them and produce long error messages.
4. **Replaceable collaborators climb a ladder.** Start with a concrete type. If a second implementation exists
   only so tests can avoid real I/O, make the type an enum with a real variant and a mock variant (§4.5). If
   users must supply their own implementations, define narrow traits (`LoadObject`, `StoreObject`), implement
   them on top of inherent methods, and accept them as generics. Only when generics start to nest, reach for a
   trait object, and wrap it in your own type (`DynamicDataAccess(Arc<dyn DataAccess>)`) so the pointer does not
   show. Porting an interface-per-service design from another language one for one is the mistake this ladder
   prevents. Generics give static dispatch and reuse at the price of code size; trait objects give
   heterogeneity at the price of an indirection and no generic methods; decide early which a trait is for.
5. **Anything non-deterministic is mockable.** A type that does I/O, reads a clock, draws entropy or calls the
   system takes its effect source as input and offers a way to substitute it for tests. A library does not
   open files on its own, does not create its own I/O core, and does not offer a `default()` that wires itself
   to the real world. Allocations are exempt (treat them as deterministic) but unbounded input still needs
   bounded or chunked operations. Test-only hooks live behind one feature named `test-util` so that production
   builds cannot reach a bypass such as skipping certificate checks.
6. **Avoid statics where consistency matters.** Two versions of one crate can both be linked into a build
   (every `0.x` is a separate major version), each with its own copy of the static, so a global counter or
   registry silently splits in two. A static is fine only for a pure optimisation whose loss would change
   nothing but speed. Statics also get in the way of unit tests and of thread-per-core designs.
7. **Heavy services are cheap to clone.** A shared service type implements `Clone` with shared-ownership
   semantics, so one instance is created per thread and handed to many consumers.
8. **Public types are `Send`.** In particular every future a public function returns, since a runtime may
   move tasks between threads. A single non-`Send` value (an `Rc`) held across an `.await` makes the whole
   future non-`Send`. Pin the property with a compile-time assertion for the main entry points; you do not need
   to test every method.
9. **Declare `async fn` rather than returning `impl Future`** unless the trait context or a hot-path size
   concern requires the explicit form.
10. **A long computation yields.** A loop of pure CPU work inside a task starves its neighbours on the same
    runtime. Await a yield point at regular intervals, between chunks of a batch or inside a long item. Work
    that already awaits I/O in the loop is preempted by those awaits and needs nothing more.
11. **In a hot async path, watch the size of the future.** Values that live across an `.await`, and the
    parameters captured at construction, become part of the future and are moved around with it. Reduce the
    size of what is held across awaits, shrink parameter and return types, and extract setup out of the async
    block when a profile shows the copying.
12. **Cycles of reference counts are leaks.** A recursive type linked with `Rc` or `Arc` together with interior
    mutability can keep itself alive forever; break the cycle with a weak reference or restructure (§3.9).
13. **One shape for I/O in tests.** Functions written against `Read` and `Write` (§1.14) are driven in tests
    by in-memory buffers; those written against a concrete file or socket need a temp directory and a server.
    Prefer the first.
