# § 3 — Where they do earn their place

> Section 3 of `skills/design-patterns`. Read it when a pattern has survived §1's threshold and §2's
> subtraction pass. Not a rejection of the catalogue — these are the cases that hold up in our stacks.

1. **Adapter and Facade at a third-party boundary.** This is rule B in code: an external API gets one
   wrapper we own, so a breaking change upstream is one file. Even here, one caller is fine — the
   justification isn't reuse, it's containment. The test of whether the wrapper works is whether the
   vendor's shape leaks through it: if the caller handles the vendor's error class, reads its response
   object or knows its field names, the breaking change is still spread across the codebase and the
   wrapper bought nothing. Convert at the boundary, into our own types.
2. **Strategy when the branches are real and growing**, and each has its own tests. The tests are half
   the point: three branches inside one function share one test file and one set of fixtures, so the
   coverage of the third branch is nobody's responsibility. Three objects behind one interface each have
   an obvious place for their own cases, including the ones only that provider gets wrong.
3. **Builder when construction genuinely has many optional parts** and the alternative is a constructor
   nobody can read. "Many" is the operative word — §4.4 lists the three cheaper fixes to try first, and
   the builder is last because it is the most code and the least type safety of the four: a builder can
   always be called with a required part missing, and the failure is at run time.
4. **Command when work must be queued, retried or audited** — usually meaning the framework's job
   abstraction (`background-jobs-conventions`). Each of the three words is a real requirement rather
   than a nicety: queued means the caller does not wait, retried means the operation has to be
   idempotent, audited means the command's inputs are recorded somewhere a human can read afterwards. A
   command object with none of the three is a function with extra steps.
5. **State when the transitions are the domain** and getting them wrong is the bug you're preventing.
   What you buy is that an invalid transition cannot be expressed — a refunded order cannot be shipped
   because there is no method on that state to call. Where the transitions are not the thing that goes
   wrong, this is over-abstraction; §4.2 states the mechanical trigger.
6. **Mediator when components must stay decoupled from each other, not just from the framework** — a
   central event bus/store two features go through instead of importing each other directly. It earns
   its place once a third participant needs to react to the same event; two callers with a direct
   reference are simpler and don't need it. The cost to weigh against it is traceability: with a
   mediator, finding out what happens when an event fires means searching for subscribers rather than
   reading a call, so the indirection has to be buying real independence.
7. **Memento when the requirement is explicitly "undo" or "restore a previous state"** — a multi-step
   wizard's back button, a draft auto-saved before an edit, an optimistic UI update rolled back on a
   failed save. Without that explicit requirement, don't snapshot state "just in case". When it is
   required, the question that decides the design is what a snapshot contains: a shallow copy of a
   mutable object restores a reference to something that has since changed, which reads as undo doing
   nothing.
8. **The common thread is containment, not reuse.** Every case above is justified by a boundary that
   already exists — a vendor's API, a growing set of providers, a queue, a set of domain transitions,
   two features that must not import each other, a snapshot the product asked for. None of them is
   justified by "we might need it twice". When the justification you can write down is reuse and there
   is exactly one caller, the pattern is §1.2 wearing a name.
9. **Each of these still owes the net-line test.** Earning a place in this section is not a bypass:
   `over-engineering-review`'s question — is the code smaller with the pattern than without — applies to
   an Adapter and a Strategy the same as to anything else. The usual honest outcome for a first Adapter
   is that it adds lines and is still right, because the lines it adds are the containment; say that
   explicitly rather than pretending the count improved.
10. **What this section owes at review time is one sentence per named pattern.** Which boundary it
    contains, and where the second real case is. If that sentence cannot be written, the diff is a
    `simplify` candidate — and if it can, it belongs in the ADR (§5.2 here) rather than being rediscovered by
    the next reader.
11. **Chain of Responsibility earns its place when a request must pass through an ordered set of handlers
    and any one of them may resolve it and stop the rest** — a support ticket escalated L1 to L2 to L3 until
    someone has the authority to close it, an approval that climbs a management chain until it finds a
    signer, a validation pipeline where the first failing rule stops the remaining ones from even running.
    What justifies naming it separately from plain middleware (§2.3) is exactly that stopping condition:
    once a caller writes "if this handler claims it, nothing after it runs," the shape is Chain of
    Responsibility rather than a fixed sequence of steps that always all execute.
12. **Bridge earns its place when an abstraction and its implementation each vary independently and both
    need to grow without a combinatorial explosion of subclasses** — a shape hierarchy (circle, square)
    that must be renderable through several unrelated drawing back-ends (canvas, SVG, print), where
    `Circle`/`Square` times `CanvasRenderer`/`SvgRenderer` would otherwise need one subclass per pairing.
    It is the rarest earned pattern in most of our stacks because the condition — two axes of variation,
    both real, both growing — is uncommon outside rendering and driver-style code; reach for it only when
    a second axis of variation is already forcing subclasses to multiply, not in anticipation of one.
13. **Visitor earns its place when new operations on a fixed set of node types are added more often than
    new node types are.** A compiler's AST, a document processor walking HTML/XML elements, a reporting
    step that walks a fixed schema — each adds a new visitor (export to PDF, validate, pretty-print)
    without touching the node classes themselves. The condition that has to hold is the inverse of most
    OOP design: the type hierarchy is closed and stable, and it is the set of operations that is open — get
    that condition backwards and Visitor turns every new node type into an edit of every visitor, which is
    strictly worse than a method per node.
14. **Composite earns its place when the client code must treat a single item and a group of items
    through the same call, recursively** — a UI component tree where a container and a leaf both expose
    `render()`, a filesystem where a folder and a file both expose `size()`, a permission rule that can be
    a single check or a group of checks combined with AND/OR. What it buys is that calling code never
    special-cases "is this a group or a single item" — the recursion is the whole payoff, so a "composite"
    with only one level of nesting is a plain collection wearing a bigger name.
