# § 4 — The ones with a concrete entry condition

> Section 4 of `skills/design-patterns`. Read it when one of these seven shapes is in front of you. The
> trigger is mechanical enough to state, which is what makes them reviewable rather than a matter of
> taste. Each still passes §1's second-real-case threshold first. `business/fintech-compliance`
> cites §4.5 here; `laravel-conventions` §4 and §8 cite §4.7 here.

1. **Strategy** — a `switch`/`match` on a `type`/`channel`/`provider`/`mode`/`kind` field with **3+ branches
   that keeps growing**, or sibling classes differing only in one method. The axis of variation must be
   **one**: two axes means you're about to build a matrix, and a map of functions keyed by the pair is
   smaller. Each strategy owns its tests. **Bridge** is the rare legitimate answer when both axes are real,
   growing independently, and each side already has several implementations (e.g. a notification
   abstraction with multiple channels *and* multiple formatters) — splitting into two hierarchies that
   compose beats a matrix of concrete classes. It's an escape valve for when the map-of-functions above
   stops being smaller, not a default.
   The counter-trigger is a `switch` with two branches that has been two branches for a year: that is an
   `if`, and turning it into a registry adds a lookup, a registration and a way to be missing at run time.
   And when the strategies are chosen by a value that arrives from outside — a request field, a webhook's
   `type` — the dispatch needs an explicit unknown-value branch, because the interesting failure is not a
   wrong strategy but no strategy at all.
2. **State** — one object moves through **named statuses** (`pending` → `approved` → `paid` → `refunded`) and
   its behaviour shifts at each step, with the `if`/`match` on that field repeated across **several**
   methods. The trigger is the repetition, not the existence of a status field: a status read in one place is
   a status field, not a state machine. What you're really buying is that an invalid transition becomes
   unrepresentable — if the transitions don't matter, this is over-abstraction.
   Two consequences decide the shape. The status is persisted, so the set of names is stored data: adding a
   state is a deployment where old rows carry old names, and renaming one is a migration. And the
   transitions are where concurrency bites — two requests both reading `pending` and both approving is the
   bug the state machine is supposed to prevent, which it only does if the transition is applied as a
   guarded write (a conditional update, a lock) rather than a read, a decision and a save.
3. **Null Object** — the same "is this collaborator absent?" branch repeats (`if ($logger)`, `if ($user)`,
   optional constructor arguments defaulted to null, a lookup returning null for an unknown key, a
   guest/anonymous case). Substitute an instance that does nothing, so the caller stops asking. It pays when
   the branch is **repeated**; a single null check is a null check.
   The trap is a null object that hides a failure instead of a legitimate absence: a no-op mailer in
   production sends nothing and reports success, and a guest user that answers "no" to every permission
   question is indistinguishable from a broken session. Use it where doing nothing is the correct
   behaviour for that case, and never as a way to stop a null from crashing.
4. **Object construction** — the honest answer to "this constructor has too many parameters", and the
   smallest fix wins: a **parameter object** (group the ones that travel together), a **named constructor**
   (`::fromX`, a `from_x` classmethod) when there are several distinct valid ways to build the thing, a
   **readonly class / dataclass / validated model** when it's really a value, and a **fluent builder** only
   when construction genuinely has many optional parts. Reach for the builder last: it's the most code and
   the least type safety of the four. Decide it **while the signature is being written** — reworking an
   existing wide constructor unprompted is `simplify`'s territory, not this one's.
   What makes a wide constructor dangerous rather than merely ugly is same-typed neighbours: four booleans
   or three strings in a row can be passed in the wrong order with no error anywhere, and the bug surfaces
   as wrong data rather than as a failure. That is the case where the parameter object pays immediately,
   because the fields are named at the call site.
5. **Value Object** — a domain value travels as a bare primitive: money as a float, an amount and a
   currency as two separate parameters nothing keeps together, the same email/phone/IBAN shape validated at
   2+ call sites, a start/end pair nothing keeps ordered, or raw ids from different tables passed
   interchangeably because they're all just integers. Wrap it in a small immutable value object that
   enforces its invariant **once**, in its constructor, instead of at every call site that touches it. Money
   is never a float — that one is close to a hard rule, not a judgment call.
   The invariant has to be unforgeable to be worth anything: a value object with a public setter, or one
   holding a mutable array, is validated at construction and wrong afterwards. And the boundaries are where
   it earns most — a value object constructed from request input rejects the bad value at the edge, with
   the field name still available for the error message, instead of three layers in where the only honest
   response is a 500.
6. **Pipeline** — one payload passes through an **ordered sequence of independent steps that keeps
   growing** (import, ETL, validation-then-enrichment, checkout) — model each step as a named stage class
   behind one interface, with an explicit ordered list, before the third step lands. The mechanical
   counter-trigger matters as much as the trigger: a **fixed** three-step sequence that will never grow is
   three named method calls in order, not a Pipeline — the abstraction has to earn its indirection against a
   growing list, or it's ceremony around three lines. Refactoring an existing god-method into one is
   `simplify`'s territory, not a drive-by here.
   Two things the ordered list must answer, or the pipeline is worse than the god-method it replaced: what
   happens when a stage fails — does the payload stop, skip, or carry an error the later stages have to
   check — and whether a stage may mutate the payload other stages already read. Decide both once, in the
   interface, because a pipeline where each stage answers differently cannot be reasoned about at all.
7. **Transaction boundaries** — a single business operation performs **two or more writes that must succeed
   or fail together** (create a parent then its children, decrement stock after creating an order,
   multi-model writes in one action). One explicit transaction wraps **all** of that operation's writes, and
   the boundary sits on the action/use-case — never on the model, never on the controller. Side effects that
   aren't the database (mail, an outbound HTTP call, a queue dispatch, a broadcast event) move **outside**
   the transaction and fire only after commit — inside it, a slow vendor call holds the lock, and a
   rolled-back transaction can't un-send an email. Not for a read-only path, a single atomic statement, or
   code that's already inside a caller's transaction.
   The failure this prevents is specific and common: a queued job dispatched inside the transaction can be
   picked up by a worker before the commit, so it reads a row that does not exist yet — and on a rollback,
   never will. The same applies to a broadcast the frontend reacts to. And a transaction that wraps more
   than one operation because it was easier to put it higher up holds locks for the duration of everything
   inside it, which is how one slow report starts timing out unrelated writes.
   Three more things a first implementation of this boundary gets wrong, each of them silent. **Writing
   is not committing**: sending the statements to the database — a flush, a save, a persist — makes the
   rows visible to *this* connection and to nobody else, so a test that asserts through the same
   connection passes on an operation that never committed. **A transaction inside a transaction is
   usually a savepoint, not a transaction**: the inner rollback undoes the inner part and the outer
   commit keeps going, so an inner failure that was supposed to abort the operation leaves it half
   applied — and where the driver has no savepoints, the inner commit ends the *outer* one early.
   **The framework's own model events fire inside your boundary**: a listener on created or saved runs
   before the commit, so anything it does — a mail, a dispatch, an external call — is the failure above
   with no dispatch of yours anywhere near the transaction. Where an effect must happen exactly when the
   commit happens, the only shape that survives a crash between the two is writing the intent as a row
   in the same transaction and having something else deliver it afterwards; that is a real mechanism with
   a real cost (a table, a worker, an ordering question), so it earns its place when losing the effect
   is worse than building it — and not before (`skills/background-jobs-conventions`).

8. **An illegal transition is an exception, not a boolean.** Once §4.2's states exist, the question
   "may this move to that?" has two possible answers in code: a method returning false, which every
   caller may ignore and one of them will, or a refusal that stops the operation. Only the second makes
   the lifecycle a guarantee rather than a convention, and it is mapped to a response once, at the
   boundary, rather than caught per call site — a domain refusal is not a 500 and not a validation error
   on a field the caller did not send.
9. **The status stays; the pattern is what happens next.** Introducing §4.2's states does not remove the
   enum or the column: the name of the state is still data, still queryable, still what a report groups
   by. What moves out is the behaviour behind each name. A first implementation that deletes the enum in
   favour of a class hierarchy breaks every query and every filter, and then reintroduces the enum as a
   mapping — with two sources of truth for the same name.
10. **A resolver needs a verdict for a key it does not know, decided by where the key comes from.** §4.1's
    lookup is total for the keys we ship and partial for everything else: a key from our own code that
    misses is a bug and throws, a key from a request or a third-party payload that misses is input and
    gets the boundary's ordinary rejection, and a key whose absence is legitimate — an optional
    integration nobody configured — is where §4.3's Null Object earns its place rather than a null.
    Deciding this once, in the resolver, is what stops each call site from inventing its own answer.
11. **Halting a pipeline has two meanings and they need two signals.** §4.6's ordered sequence stops for
    one of two reasons: there is nothing left to do, which is success, or the run must fail, which is
    not. Collapsing them into one "stop" return makes a rejected payload indistinguishable from a
    finished one, and the caller reports success. State both in the stage contract, and state which of
    the two leaves the earlier stages' effects in place — because a pipeline that has already written
    something is a transaction question (§4.7), not a control-flow one.
12. **Several ways to build one thing are named constructors, not a factory class.** §4.4's answer to a
    constructor with too many parameters is usually not another type: it is one honest constructor plus a
    named entry point per way the thing is legitimately created — from a request, from a row, from a
    default. The word *factory* is what turns this into a class, because the vocabulary suggests one; a
    class earns its place only when construction needs a collaborator the object must not hold.
13. **A boolean parameter that changes what a method does is two methods.** A flag threaded through a
    constructor or a use case is a second implementation hidden inside the first, and it is the shape
    §4.1's Strategy exists for once there are two of them — but the first move is not a pattern, it is
    two named entry points with no flag. The tell is a body whose first statement is a branch on the
    flag, and whose two halves share nothing but the signature.
14. **A value object stays out of the wire format.** §4.5's type is the domain's shape, not the payload's:
    serialising it directly makes the API's contract change every time the domain's does, in a way no
    consumer asked for, and deserialising into it skips its own validation — the one thing it exists to
    guarantee. The boundary translates in both directions, which is `skills/code-baseline` §4's typed
    wrapper rule applied to something we own on both sides.
