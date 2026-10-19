# § 5 — Disposal, nullability, enumeration

> Section 5 of `skills/dotnet-conventions`. Read it when a disposable is created, a null is tested or
> silenced, or a sequence is enumerated or counted.

1. An `IDisposable` created locally is disposed on **every** path, exception paths included
   (`using`/`using` declaration) — CA2000. The leaked resource is usually a connection or file handle, so
   the symptom is not memory but a pool that runs dry under load, in a request unrelated to the leaking
   code.
2. The full `Dispose(bool)` pattern with `GC.SuppressFinalize` if `IDisposable` is implemented by hand
   (CA1063): never a partial `Dispose()`. Usually the better answer is not to implement it by hand — hold
   the disposable and let a `using` own it, or let the container own its lifetime (§2.11).
3. Nullable Reference Types enabled across the whole project, not partially. `!` (null-forgiving) is not a
   way to silence the compiler: every use must be justifiable. Partial enablement is the worst of the three
   states: annotations in enabled files make claims the disabled ones don't check, so the compiler is
   confident exactly where it shouldn't be.
4. A LINQ query re-enumerated several times on a deferred `IEnumerable` re-runs on every iteration:
   materialise it (`.ToList()`) if the source is expensive or has a side effect (CA1851 — known blind
   spots, so check by eye too). On a database source, "re-runs" means another round trip, and the results
   can differ, so a count and a loop over the same query can disagree.
5. An empty `catch {}` or a `catch (Exception) {}` with no log or rethrow swallows a real bug: never a
   silent catch. The visible result is a request reporting success having done nothing; the invisible one
   is no log entry when the incident happened.
6. **Null tested with the pattern form** (`is null` / `is not null`) rather than the equality operator, and
   the roundabout not-null spellings avoided. A preference in ordinary code, informed override accepted —
   except one place where it is no preference: **inside an equality-operator body, using the equality
   operator is infinite recursion.**
7. **One lookup per dictionary access.** Ask for the value and the existence together when you need the
   value, use the insert-if-absent call when inserting, and keep the pure existence check for when no value
   is read. The double probe is the one unambiguous performance claim in this section: the existence check
   and the indexer run the same hash-and-probe, so both run it twice. Never route a lookup through the keys
   or values projection — a linear scan wearing a lookup's clothes.
8. **Read the size from the receiver's own member** where its type exposes one, and reserve the LINQ count
   method for a sequence that has none. On a lazy sequence "is there anything in here" has its own call,
   which stops at the first element. The reason is intent, not micro-optimisation — the folklore version
   overstates the cost.
9. **Dispose what you own, and nothing else.** An injected dependency belongs to the container, and
   disposing it takes it from every other holder — a singleton disposed by the first request that used it
   fails for the second, with an object-disposed exception nobody can trace to a `using`. Mechanical rule:
   if this code created it, this code disposes it.
10. **The shared HTTP client is the standard case of point 9 in both directions.** One per request
    exhausts sockets, because the connection lingers after the object is gone; disposing one obtained from
    the factory breaks the pooling the factory provides. Take it from the factory and do not dispose it.
11. **An async resource needs `await using`, not `using`.** Disposing an `IAsyncDisposable` synchronously
    either blocks a thread on the flush or skips the async part of the cleanup, which is how a buffered
    write disappears without an error. The compiler won't tell you: the type usually implements both.
12. **Nullable annotations are compile-time only, and data from outside does not obey them.** A
    non-nullable property filled by a deserialiser, an ORM's materialiser or reflection can be null with no
    warning, so the null arrives three layers in, where the only honest response is a 500. Validate at the
    boundary that receives the data, and treat the annotation as documentation of intent, not a guarantee
    about input.
13. **A `default` struct bypasses its own constructor.** `default(T)` for a value type zeroes every field —
    including a non-nullable reference field, null despite its annotation, and an enum with no member
    valued `0` (§4.15). Where a struct has an invariant, it must hold for the zero value too, or the type
    wants to be a `sealed record`.
14. **`IAsyncDisposable.DisposeAsync` is one call, and a type owning several async resources still exposes
    one.** The pattern is `DisposeAsyncCore` doing the async teardown, called from `DisposeAsync` alongside
    disposing any synchronous fields — never two public dispose entry points on one type, which moves point
    9's ownership question onto the caller instead of answering it.
15. **A double dispose has to be a no-op, not a second failure.** A `using` around code that already
    handled an earlier failure, or two paths that both think they own the cleanup, call `Dispose` on an
    already-disposed object under real conditions — guard the body with a disposed flag rather than assuming
    a single call site.
16. **A nullable type parameter needs its own constraint, not an assumption from the call site.** A generic
    method over `T` without `where T : notnull` (or an explicit `T?`) inherits whatever nullability the
    caller's type argument has — its own contract about null says nothing until the constraint states it.
17. **`ArgumentNullException.ThrowIfNull` is the guard clause, and the null-forgiving operator after it is
    what a reviewer should never see.** Checking a parameter and writing `param!` two lines later says the
    check exists to satisfy an analyser and nobody trusted its result. The compiler narrows after a
    `ThrowIfNull` as after an `is null` check, so the following `!` is redundant or a sign the check was
    copied in unread.
18. **An `IAsyncEnumerable<T>` disposes its enumerator through `await foreach`, and breaking out early
    still runs that disposal.** A `break` or `return` inside the loop triggers the compiler's implicit
    `finally` calling `DisposeAsync`, as a synchronous `foreach` would. The trap is code that stores the
    enumerator itself (`GetAsyncEnumerator()` called by hand, outside a `foreach`) and exits without a
    matching `DisposeAsync`, leaving the connection or cursor behind the sequence open for the life of the
    process.
19. **A `SafeHandle` wraps the OS resource so a `Dispose` running during finalization can still release it
    correctly; a raw `IntPtr` field cannot.** A type storing a native handle as `IntPtr` and closing it in a
    hand-written finalizer risks the handle being reused by another allocation between the object becoming
    garbage and the finalizer running, so the wrong resource is closed under load. Wrap it in a `SafeHandle`
    derivative, whose release path is interlocked against that race — the reason to prefer it over a
    hand-rolled finalizer (point 2).
20. **A struct with a nullable value-type field defaults that field to `null` like any other default, and
    equality then depends on both sides agreeing.** `Nullable<T>` inside a `default` struct or a
    zero-initialized array element compares equal to another unset instance — invisible until the struct is
    a dictionary key or a record's equality member, where two "empty" instances collapse to one bucket or
    one duplicate-looking entry, matching point 13's warning about the zero value carrying real meaning
    whether or not anyone designed it.
21. **Re-enumerating a sequence twice does not always give two identical results, and the risky case isn't
    always visible at the call site.** Point 4 covers deferred-and-expensive; the sharper case is a source
    that mutates between enumerations — a queue drained by a background reader, a stream whose position the
    first pass advanced — where the second enumeration silently sees less. `.ToList()` where a sequence
    stops being "just produced" and starts being "read more than once" turns that gap into a value that
    can't move under the caller.
22. **`ConditionalWeakTable<TKey, TValue>` attaches data to an object's lifetime without extending it,**
    and a normal `Dictionary` keyed by the same object turns "extra state for this instance" into a leak:
    every reference-keyed entry keeps its key alive as long as the dictionary exists, effectively forever
    for anything long-lived. Where the requirement is "clean up when the object is collected, and not
    before," the conditional table is the framework collection that gives it, instead of a `Dispose` you
    must remember.
23. **An `IAsyncEnumerable<T>` producer accepts a `CancellationToken` through `[EnumeratorCancellation]`,
    not an ordinary parameter.** A plain parameter on an `async IEnumerable<T>` iterator is never populated
    by `await foreach`'s `WithCancellation`; the attribute tells the compiler to wire the caller's token
    into the one the method reads. Without it the enumeration looks cancellable and never stops — worse
    than offering no cancellation, because it hides behind code that appears to support it.
24. **A `CancellationTokenSource` created locally is disposed like any `IDisposable` (point 1), and a linked
    source doubly so.** `CancellationTokenSource.CreateLinkedTokenSource` allocates a second object to
    dispose independently of the tokens it links — left undisposed in a hot path it is a steady handle leak
    showing as memory growth with no single large allocation, since each is small and repeats per call.
25. **A nullable value-type parameter tested with `HasValue`/`Value` rather than compared to `null` through
    the equality operator once inside a hot path.** Both compile to the same result, but `.Value` without a
    preceding check throws `InvalidOperationException` naming neither parameter nor call site — matching
    point 6's pattern-form preference, `is { } bound` names and binds the value in the one expression that
    proved it present, removing a separate `.Value` access that can drift from the check justifying it.
26. **An object pool's `Return` path resets every field the pooled instance accumulated, or the pool leaks
    state across unrelated callers instead of memory.** `ObjectPool<T>` and `ArrayPool<T>` hand the same
    instance to the next renter with none of the framework's cleanup — a buffer returned uncleared carries
    the previous caller's data into a path that never wrote those slots, and a pooled object with a
    mutable field carries state between two unrelated requests.
27. **Nullable reference type warnings from a third-party package's own (possibly incomplete) annotations
    are not silenced with a project-wide `#nullable disable` around the call.** A dependency that annotated
    its public surface incompletely produces a false warning at the call site — fix it with a narrow
    `!`-suppression or a local `#pragma warning disable CS86xx` on that one line, with a comment naming the
    package whose annotation is wrong, because disabling nullable checks for the surrounding code silences
    every real warning in the block with the false one.
28. **Several `IDisposable` resources acquired in one method are disposed in reverse acquisition order, and
    the compiler enforces that only for nested `using` statements or declarations, never for fields
    disposed by hand in a written-out order.** A resource depending on another staying open — a transaction
    wrapping a connection, a stream wrapping a file handle — must close first, so a hand-rolled `Dispose`
    tearing down fields in declaration order rather than dependency order can close the connection while
    the transaction is still flushing. Nested `using` declarations get this free; a type owning several
    disposables by hand must state the order deliberately, because nothing checks it.
29. **`WeakReference<T>` and `TryGetTarget` exist for a cache entry that shouldn't itself keep an object
    alive; any other use trades a `Dispose` you forgot for a value that vanishes on its own schedule.** Right
    for a genuinely optional cache — a second lookup recomputes what a collected entry lost — wrong for a
    resource that must be released deterministically, because `TryGetTarget` returning `false` means "the
    GC already ran," not "explicitly released"; treating a weakly-held handle as if closing it still
    mattered reinvents point 22's `ConditionalWeakTable` case without its guarantee.
30. **A boxed value-type enumerator loses the mutation a `foreach` over a `struct`-based collection depends
    on, and the boxing happens where the code looks generic.** `List<T>.Enumerator` and similar are structs
    so a `foreach` against the concrete type allocates nothing per iteration; the same loop against the
    `IEnumerable<T>` interface (a generic helper, a LINQ operator) boxes the struct, invisible in the source
    and visible only as an allocation-profile difference. It matters on a hot path (point 8's territory)
    and is not worth chasing elsewhere.
31. **`GC.SuppressFinalize` in a hand-written `Dispose(bool)` (point 2) is called from the public
    `Dispose()` overload, not the protected one both paths share.** Calling it inside
    `Dispose(bool disposing)` whatever invoked it suppresses finalization even when the object was being
    finalized — backwards, since the call tells the GC "already cleaned up through `Dispose`, skip the
    finalizer"; a finalizer thread calling it on itself needs no such promise.
32. **`IMemoryOwner<T>`'s `Memory<T>` stays valid only until `Dispose` runs, and a slice or copy of the
    reference taken earlier does not extend that.** Renting through `MemoryPool<T>.Rent` and disposing the
    owner returns the array to the pool for the next renter — point 26's `ArrayPool<T>` state leak — so a
    `Memory<T>` handed to another component and read after the owner's `Dispose` reads whatever the next
    renter wrote. Whoever calls `Dispose` on the owner must be the last reader, and that ordering must be
    explicit at the API boundary, not assumed from how long the reference happens to live.
33. **A record's positional `with` expression and a hand-written property setter disagree about whether a
    change is visible to `Equals`; `init`-only properties keep that from happening silently.** A record
    property with a plain `set` instead of `init` can be mutated after construction outside a `with`
    expression, so two records equal at one point can drift apart with no copy ever made — the value
    semantics point 07.7 ascribes to `with` hold only while every property stays `init`-only; a settable one
    makes the record a class with generated equality members riding on state they no longer compare.
34. **`[MemberNotNull]` and `[MemberNotNullWhen]` tell the compiler what a guard method already proves;
    without them a validation helper resets the flow analysis point 3 depends on at every call site.** A
    method that throws when a field is null, or returns `false` exactly then, communicates nothing unless
    annotated: the inline `if (x is null) throw` narrows the field for the rest of the method, while the
    same check in a helper leaves the compiler at "might be null" when it returns, and the codebase
    accumulates redundant `!` (point 17) because the guard lives one call away from where its result is used.
35. **`[NotNullIfNotNull]` states a pass-through contract a return-type annotation alone can't express, and
    skipping it reverts to point 12's "annotation as documentation only."** A method returning its input
    unchanged when non-null, null only when the input was — a normaliser, an optional mapper — must have a
    nullable return type, forcing a null-check on every caller even for the branch that never produces one;
    naming the linked parameter lets the compiler narrow the *result* as it narrows the input, instead of
    every caller re-deriving the guarantee by eye.
36. **A `ref struct` implementing an interface (C# 13's `allows ref struct` constraint) can now be disposed
    through generic code, so the disposal discipline built around `IDisposable` (points 1, 9) reaches types
    that couldn't opt in.** `Lock`'s scope, a pooled buffer wrapper or any stack-only type had to be
    disposed by a caller knowing its concrete type, since a `ref struct` couldn't implement `IDisposable`
    for a generic `using`-over-`T`; a method declared `where T : IDisposable, allows ref struct` can now own
    that disposal as for a heap type — new surface for point 9's "dispose what you own", not a new rule.
37. **A collection expression's spread element enumerates its source once to build the target and disposes
    nothing it walked.** `[.. source]` calls `GetEnumerator()`/`MoveNext()` as a `foreach` would, but the
    generated code has no `using` around it — for a source that is an `IEnumerable<T>` backed by a
    disposable enumerator (a database cursor wrapped as a sequence, a custom iterator holding a handle) the
    copy finishes and leaves the handle open: point 1's leak through syntax that doesn't look like
    enumeration.
38. **A `using` declaration's scope is the rest of the enclosing block, not its statement, and two
    declared back-to-back stay open longer than equivalent nested `using` statements.** `using var a = ...;
    using var b = ...;` disposes both at the end of the method or block, in reverse order (point 28) —
    usually wanted, but a resource that should close well before the method returns (a short-lived
    transaction opened partway through) silently outlives its useful scope as a declaration instead of a
    braced `using` statement, holding a connection or lock for everything after in the block.
39. **`ArgumentOutOfRangeException.ThrowIfZero`/`ThrowIfNegative` and siblings are point 17's guard clause
    for a numeric range, and the same rule about what follows applies.** The framework's static
    throw-helpers for a parameter that must be positive, non-zero or in range read like
    `ArgumentNullException.ThrowIfNull` — one line, no `if` block — and nothing should re-check afterwards
    what the helper established: a defensive re-test says the check wasn't trusted the first time.
40. **A `struct` with an `init`-only auto-property still has a parameterless constructor the runtime can
    call through `default` or array allocation, and point 13's zeroed-struct warning applies to `init`
    members as to mutable ones.** `init` changes when a property can be *set from outside the type* — after
    construction, only from an object initializer — not the all-zeroed value every value type has whether
    or not its declared constructor ran; an invariant expressed only in a parameterised constructor must
    still hold for the value nobody constructed that way — point 13's trap through a modifier that looks
    like it should have closed it.
41. **A `ref struct` that implements `IDisposable` (point 36) is disposed through pattern-based resolution
    first, not the interface method, when both exist.** Since C# 13 a `ref struct` can carry both a
    duck-typed `public void Dispose()` and an explicit `IDisposable.Dispose()`; `foreach` and `using`
    resolve the pattern method in preference, falling back to the interface only when none matches — a type
    with both, written expecting the interface method to run, silently runs the other, which matters when
    they differ (a diagnostic counter incremented in only one).
42. **`Span<T>`/`ReadOnlySpan<T>` cannot be written as `Span<T>?`, because a `ref struct`'s nullability
    can't be expressed as point 3's reference-type annotations express it.** An API needing "no span"
    distinct from "an empty span" — point 21's "ran and produced nothing" versus "didn't run" — has no
    nullable-annotation route for a span-typed parameter or return; the two alternatives are
    `Span<T>.Empty` carrying the meaning by convention (documented, since nothing enforces it) or a
    separate `bool` beside the span, neither compiler-checked like an ordinary nullable reference.
43. **A `Dispose` that throws leaves the object in a state nothing can safely retry, and thrown while
    unwinding from another exception it replaces the original.** An exception escaping `Dispose` while a
    `using` block is already propagating a different one discards the first — the caller sees only the
    disposal failure and never learns what went wrong inside the block, a worse point-5 swallow because the
    original fired but never reaches anyone. `Dispose` catches what it can handle internally and treats an
    unrecoverable failure as a logged fact, not a throw.
44. **A finalizer runs on a thread with no guaranteed ordering relative to other finalizers, and calling a
    method on another managed object inside one risks calling an already-finalized object.** The full
    `Dispose(bool disposing)` pattern point 2 asks for keeps the finalizer path (`disposing == false`) from
    touching anything but this object's own unmanaged handles — a finalizer walking into a referenced
    object's method because "the reference is still not null" is wrong about what that guarantees once
    finalization has started, which is why the pattern splits managed and unmanaged cleanup into two
    branches instead of one body from both entry points.
45. **`IAsyncDisposable`'s `DisposeAsync` returns a `ValueTask`, which is single-consumption as point 01.20
    (async, cancellation, threading) states — awaiting it twice, or after checking `IsCompleted`, is
    undefined for the same reason.** A double-dispose guard `if (!_disposed) { await DisposeAsync(); }` on a
    resource whose `DisposeAsyncCore` (point 14) returns a pooled `ValueTask` is safe only if the guard
    actually prevents the second call — reasoning about the awaited result afterwards, or re-awaiting the
    stored task in a retry path, revisits a `ValueTask` the first await may have invalidated.
46. **A `using` declaration or statement disposes exactly what its expression evaluates to, and a method
    returning a *new* wrapper around an existing disposable each call defeats point 9's "dispose only what
    you own" by making ownership look local.** `using var reader = GetReader();` disposes the variable's
    value — if `GetReader()` returned a wrapper over a connection the caller doesn't own (a pooled
    connection, a shared stream sliced into a view), the `using` disposes the wrapper as intended but can
    cascade into the shared resource if the wrapper's `Dispose` propagates, a design decision on the
    wrapper's side the call site can't see from the `using`.
