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
