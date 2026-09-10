# python-conventions §6 — Dependency injection and lifetimes

> Section 6 of `skills/python-conventions`. Read it when a binding is declared or a lifetime is chosen. The other sections and the guardrails stay in `SKILL.md`.

1. A binding's default is an application-lifetime singleton. Reach for a different lifetime **deliberately**:
   per-request scope for per-request state, transient for a fresh instance per resolution. The default is the
   right one because most collaborators are stateless behaviour, and one instance is then both cheaper and
   easier to reason about.
2. Per-request state in an app-lifetime singleton is the same captive-dependency bug as anywhere else: it
   leaks one request's data into the next. Under concurrency it is worse than a stale read — two requests
   interleave through the same object, so the data one user sees came from another's request (§4.12 is the
   same failure without a container).
3. **The lifetime of a dependency cannot exceed the lifetime of what it holds.** A singleton holding a
   request-scoped session, a connection or a user context captures the first one it is given and keeps using
   it after that request has ended — so the object is closed, the transaction is gone, and the failure
   appears in whichever unrelated request happens to hit that path next. The container will wire it happily;
   the constraint is yours to enforce.
4. **Scope is a design decision, and both wrong answers have a shape.** Too wide and you get point 2 and
   point 3. Too narrow and a "transient" cache, connection pool or client is rebuilt per resolution, so the
   pooling it existed to provide never happens and the cost shows up as latency nobody can attribute.
5. **A resource-owning singleton needs a shutdown path.** A pool, a client, a background task or an open
   file held for the application's lifetime has to be released when the application stops, or the process
   hangs on exit and connections are left open on the far side. The container's lifecycle hooks are where
   that belongs, not an `atexit` bolted on later.
6. **Nothing is resolved from the container inside business code.** Reaching for the container at a call
   site is a global lookup with extra steps: the dependency stops appearing in the signature, so a reader
   cannot see it, a test cannot substitute it without touching the container, and the class no longer states
   what it needs. Dependencies arrive through the constructor.
7. **Inject the collaborator, not the container.** A class that takes the container takes everything, which
   makes its real dependencies invisible and its tests a full application build — the same problem as
   point 6, moved into the constructor where it looks legitimate.
8. **Bind to a protocol, not to the concrete class** (§1.13). It is what lets a test or another environment
   substitute an implementation without inheriting anything, and it is what stops the graph quietly
   depending on a class's private surface.
9. **Six or more constructor dependencies is a god object** (`code-baseline` §2.9). The container makes that
   painless to write, which is precisely why the signal has to be read deliberately: nothing will complain,
   and the class will keep accumulating reasons to change.
10. **Constructors do no work.** A constructor that opens a connection, reads config or calls an API makes
    resolution expensive and failure-prone, and it happens during graph construction where the traceback
    names the container. Take the values, build nothing.
11. **A circular dependency in the graph is a design problem, not a wiring problem.** The usual workaround —
    a lazy provider or a setter after construction — makes it resolve and leaves two components that cannot
    be understood or tested apart. Extract the shared concern into a third.
12. Overriding or wrapping another module's binding is legitimate but explicit, in one place, so the effective
    graph stays readable. Scattered overrides mean the winning binding depends on import order, which is the
    least discoverable configuration in the system.
13. **An override in a test is undone after the test.** A container mutated in place and not restored makes
    the next test's graph depend on this one's, so the suite passes in the order it was written and fails in
    the order the runner chooses — read as flakiness rather than as the coupling it is (§8.8 covers doing
    this through the container's own seam).
14. **A registration with no consumer is an unenforced guarantee** (`code-baseline` §8). A binding nothing
    resolves, or an interface with one implementation and no substitution, reads as an extension point and
    provides none — and it consumes the attention that would have noticed the missing one.
15. **The graph is worth reading back rather than assumed.** The failure mode of a container is that a
    misconfiguration is silent: the wrong lifetime, the shadowed binding, the module never registered all
    produce a working application that is subtly wrong. Where the container can print its graph, printing it
    once after a change is cheaper than diagnosing point 3 in production.
16. **Per-request state belongs in a `contextvars.ContextVar`, not a thread-local.** A thread-local is keyed
    to the OS thread, and an async application serves many requests on the same thread, interleaved at every
    `await` — so a thread-local set for one request is read by whichever request runs next on that thread,
    the same captive-dependency shape as point 2 without a container in sight. A `ContextVar` is copied into
    each task at creation, so one request's value cannot leak into a sibling's.
17. **A factory is the honest answer to "this needs a runtime argument".** A binding built once at
    application start cannot take a tenant id, a request path or a user supplied at call time — reaching for
    the container mid-request to get a fresh one is point 6's global lookup again. Register a callable that
    builds the object from its argument, and inject the factory itself, which keeps the dependency visible
    in the constructor while deferring the one value that cannot be known yet.
18. **Lazy initialisation of a singleton needs a lock or a double-checked read, or two requests race to build
    it.** Under concurrency, the interpreter can switch threads between the "is it built" check and the
    assignment, and both requests observe "not built" and construct their own instance — one of which is
    then silently discarded, along with whatever it opened. The container's own lazy-singleton support has
    usually solved this once; a hand-rolled `if not self._instance:` next to a resource open has not.
19. **A cache or connection pool with a lifetime the container does not own should hold weak references to
    what it caches**, or the cache itself becomes the reason an object nobody else references is never
    collected. A `weakref.WeakValueDictionary` lets an entry disappear once its last real owner does, so the
    cache reflects what is actually alive instead of pinning every value it has ever seen for the life of
    the process.
20. **A readiness or liveness check is a consumer of the graph, not a parallel one.** A health endpoint that
    opens its own connection to "check the database" rather than resolving the same pooled client the
    application uses can report healthy while the pool it did not check is exhausted, or unhealthy while a
    transient blip on its private connection has nothing to do with the real one. Wire it through the
    container so it observes what requests actually observe.
21. **A binding overridden for a test should be overridden through the container's own seam, not by
    reassigning the module attribute it was read from.** Patching the attribute directly works until two
    tests import it under different names, or until the container already cached the pre-patch value in a
    singleton — at which point the override is invisible to the object that matters and point 13's
    order-dependent failure returns wearing a different cause.
22. **A per-request scope is not automatically torn down at the end of the request unless the framework
    integration says so.** A scoped session or connection left open past its request because the scope's
    exit hook was never wired leaks exactly like point 3's captive dependency, except the leak is in the
    container's own bookkeeping rather than in application code, which is why it tends to be found as a
    slow file-descriptor or connection-count climb rather than as a wrong answer.
23. **A framework's own DI (FastAPI's `Depends`, a test runner's fixtures) is still a container, and points
    1 through 22 still apply to it.** `Depends(get_session)` cached per request is the same per-request scope
    as point 1's default; a `Depends` that opens a connection inline is point 10's constructor doing work; the
    rules do not relax because the container is built into the framework rather than a separate library.
24. **A default argument evaluated once at function definition (`def handler(service=Service())`) is a
    de facto singleton binding with none of a container's visibility.** It is built at import time, shared
    across every call, and mutable state on it behaves exactly like point 2's captive dependency — except
    nothing that reads the signature would guess a singleton is hiding there, because it looks like an
    ordinary default.
25. **Constructor injection and property/attribute injection answer different questions about when a
    dependency must exist.** A required collaborator belongs in `__init__`, where its absence is a
    construction-time error the type checker can already see (§1.7); an attribute set after construction
    can be forgotten, leaving an object that instantiates successfully and then fails the first time the
    attribute is used, which is strictly worse than failing at construction.
26. **A binding chosen by decorating a class (`@injectable`) still has to be discoverable by reading the
    class, not only by knowing the container's scan configuration.** A decorator that silently omits
    registering the class when a naming convention isn't matched, or a container that only picks up classes
    under a configured module path, turns "why isn't this resolving" into a container-configuration hunt
    instead of a two-line diagnosis from the class definition itself.
27. **Environment-specific bindings (a fake email sender in tests, an in-memory store in local dev) belong
    in one composition root per environment, not in `if os.environ.get(...)` branches inside the binding
    itself.** A binding that inspects the environment to decide what to construct hides the substitution
    point 8's protocol was supposed to make explicit — the environment should choose which composition root
    runs, not which object a single binding quietly returns.
28. **A dependency resolved lazily through a `Provide[...]` marker at the call site still has to be typed as
    what it resolves to, not as the marker itself**, or the signature lies to both the reader and the checker
    about what the parameter actually is once the framework's wiring step substitutes the real value —
    the same visibility argument as point 6, applied to a marker-based container rather than a lookup call.
