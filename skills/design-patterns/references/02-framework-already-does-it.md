# § 2 — Check the framework doesn't already do it

> Section 2 of `skills/design-patterns`. Read it before writing any pattern by hand. This is where most
> of the catalogue goes in our stacks: the structures below already exist in the framework or the
> language, and re-implementing one gets less capability and no upgrades.

1. **Object construction and wiring** — the DI container resolves and configures. A hand-written factory
   usually reimplements it with less capability, and a hand-written **Singleton** replaces a managed
   lifetime with a hidden global that tests can't reset. The lifetime is the part that hurts: a
   container's singleton is scoped to the process and swappable in a test, while a static instance
   survives between test cases, so the failure shows up in whichever test ran second.
2. **Notification / decoupling** — the framework's events, listeners and queued jobs are Observer and
   Command, already instrumented and already testable. What "already instrumented" buys is concrete: the
   framework's own test helpers can assert an event was dispatched without running its listeners, and
   the queue gives retries, backoff and a failed-jobs record that a hand-rolled subscriber list does not.
3. **Wrapping behaviour around a call** — middleware, pipelines and interceptors are Decorator when each
   layer always runs and adds behaviour; the same stack is **Chain of Responsibility** when a layer can
   decide to short-circuit (an auth guard that stops the chain, a handler that claims the request and the
   rest never runs). Framework middleware already gives you both; naming which one you mean only matters
   in the ADR, not in new code. The distinction that does matter in code is ordering: a stack whose
   order is implicit breaks when someone inserts a layer, so the order belongs in one explicit list.
4. **Interchangeable behaviour** — in a typed language, a map of functions or a discriminated union does
   what a Strategy class hierarchy does, in a fraction of the lines. Reach for classes when the behaviours
   carry state. The same discriminated union with an exhaustive `switch`/`match` is also what **Visitor**
   buys in an untyped OOP language (dispatch per node type without touching the node classes) — the
   compiler's exhaustiveness check is the "you forgot a case" guarantee Visitor exists to give you. Which
   means the class hierarchy loses the guarantee: a new subclass that forgets to override a method
   inherits the parent's, silently, where a new union member fails the build.
5. **Iteration, state machines, templates** — generators/iterables exist; and a state machine is better
   modelled as data (`domain-modeling` §states-not-flags) than as a class per state. Template Method is
   the third one here: a function parameter, a closure or a hook is the same "vary one step of a fixed
   algorithm" with no inheritance, and without the subclass's obligation to know the order its parent
   calls things in.
6. **Cloning** — `structuredClone`, object/array spread, `Object.create`, PHP's `clone`: **Prototype** is
   the language, not a pattern to hand-roll. The one thing to know is which of them is shallow — most are
   — because a hand-rolled prototype usually exists to paper over exactly that, and the honest fix is an
   immutable value rather than a deeper copy.
7. **Reactivity and composition** — Vue's `ref`/`reactive` already are a **Proxy** (JS `Proxy` under the
   hood: property access is intercepted to track dependencies); the component tree, parent and child
   addressed the same way through props/slots, already is a **Composite**. Writing either by hand on top
   of the framework duplicates what it does for free — and worse, a hand-rolled proxy over reactive state
   usually breaks the dependency tracking it sits on, so the UI stops updating for reasons no stack trace
   explains.
8. **Rarely earned in a GC'd web app**: **Flyweight** (sharing state to cut memory pressure) is a
   rendering-engine/game-dev answer to a problem the garbage collector already solves at our scale; if
   you're reaching for it, measure the allocation first (`sparks`), don't assume it. The same test
   applies to any object pool: a pattern justified by performance has to be justified by a measurement,
   and it has to be re-measured when the runtime is upgraded, because the reason can disappear.
9. **A Repository over an ORM is the recurring local case.** It pays only when there's a genuine second
   implementation or a real intention to swap the store. Otherwise it's a one-caller wrapper over an API
   that was already the abstraction, and it hides the query optimiser you'll want later (`tank`). The
   concrete loss: eager loading, the query builder's own composition, and the ability to see the query
   that ran — all of which end up re-exposed through the wrapper one method at a time, until it is the
   ORM with a different spelling.
10. **How to check is a search for the capability, not for the pattern name.** Frameworks do not
    advertise "we have Observer" — they advertise events, listeners, hooks, middleware, pipelines,
    scopes, lifetimes, resolvers. Read that list before writing a structure, because the version you
    write by hand starts one framework release behind and stays there.
11. **A hand-rolled structure does not get the framework's upgrades, and that is the compounding cost.**
    The container gains contextual bindings, the queue gains a backoff strategy, the middleware stack
    gains a way to be tested in isolation — and the hand-written equivalent gains nothing, while every
    new developer has to learn both. Re-check the hand-rolled ones at each major upgrade: the reason
    they existed is frequently gone.
12. **Subtraction is the skill this section is teaching.** The output of the pass is usually "delete the
    plan", not "write a smaller pattern": two thirds of the classic catalogue is already present in a
    modern framework, so the honest answer to most pattern proposals is the name of the framework
    feature that already does it. That answer is also the most useful thing to write in the review.
