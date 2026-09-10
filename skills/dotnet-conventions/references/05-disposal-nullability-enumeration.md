# § 5 — Disposal, nullability, enumeration

> Section 5 of `skills/dotnet-conventions`. Read it when a disposable is created, a null is tested or
> silenced, or a sequence is enumerated or counted.

1. An `IDisposable` created locally is disposed on **every** path, exception paths included
   (`using`/`using` declaration) — CA2000. The resource being leaked is usually a connection or a file
   handle, so the symptom is not memory: it is a pool that runs dry under load, in a request that has
   nothing to do with the code that leaked.
2. The full `Dispose(bool)` pattern with `GC.SuppressFinalize` if `IDisposable` is implemented by hand
   (CA1063): never a partial `Dispose()`. In practice the better answer is usually not to implement it by
   hand at all — hold the disposable and let a `using` own it, or let the container own its lifetime
   (§2.11).
3. Nullable Reference Types enabled across the whole project, not partially. `!` (null-forgiving) is not a
   way to silence the compiler: every use has to be justifiable. Partial enablement is the worst of the
   three states: the annotations in the enabled files make claims the disabled ones don't check, so the
   compiler is confident about exactly the boundary where it shouldn't be.
4. A LINQ query re-enumerated several times on a deferred `IEnumerable` re-runs on every iteration:
   materialise it (`.ToList()`) if the source is expensive or has a side effect (CA1851 — known blind spots,
   so check by eye too). On a database source, "re-runs" means a second round trip, and the two results can
   differ — so a count and a loop over the same query can disagree with each other.
5. An empty `catch {}` or a `catch (Exception) {}` with no log or rethrow swallows a real bug: never a
   silent catch. The visible consequence is a request that reports success having done nothing, and the
   invisible one is that the log has no entry at the moment the incident happened.
6. **Null tested with the pattern form** (`is null` / `is not null`) rather than the equality operator, and
   the roundabout not-null spellings avoided. Preference in ordinary code, informed override accepted — with
   one place where it is not a preference at all: **inside an equality-operator body, using the equality
   operator is infinite recursion**, not a style choice.
7. **One lookup per dictionary access.** Ask for the value and the existence together when you need the
   value, use the insert-if-absent call when inserting, and keep the pure existence check for the case where
   no value is read. The double probe is the one unambiguous performance claim in this section: the
   existence check and the indexer run the same hash-and-probe, so doing both runs it twice. Never route a
   lookup through the keys or values projection — that is a linear scan wearing a lookup's clothes.
8. **Read the size from the receiver's own member** where its type exposes one, and reserve the LINQ count
   method for a sequence that genuinely has none. On a lazy sequence the question "is there anything in
   here" has its own call, which stops at the first element instead of walking the whole thing. The honest
   reason is intent, not micro-optimisation — the folklore version of this rule overstates the cost.
9. **Dispose what you own, and nothing else.** An injected dependency belongs to the container, and
   disposing it takes it away from every other holder — a singleton disposed by the first request that used
   it fails for the second, with an object-disposed exception nobody can trace to a `using`. The rule is
   mechanical: if this code created it, this code disposes it.
10. **The shared HTTP client is the standard case of point 9 in both directions.** Creating one per request
    exhausts sockets, because the connection lingers after the object is gone; disposing one obtained from
    the factory breaks the pooling the factory exists to provide. Take it from the factory and do not
    dispose it.
11. **An async resource needs `await using`, not `using`.** Disposing an `IAsyncDisposable` synchronously
    either blocks a thread on the flush or skips the async part of the cleanup entirely, which is how a
    buffered write disappears without an error. The compiler will not tell you: the type usually implements
    both.
12. **Nullable annotations are compile-time only, and data from outside does not obey them.** A
    non-nullable property filled by a deserialiser, an ORM's materialiser or reflection can be null with no
    warning anywhere, so the null arrives three layers in where the only honest response is a 500. Validate
    at the boundary that receives the data, and treat the annotation as documentation of intent rather than
    a guarantee about input.
13. **A `default` struct bypasses its own constructor.** `default(T)` for a value type produces every field
    zeroed — including a non-nullable reference field, which is then null despite its annotation, and
    including an enum that has no member with the value `0` (§4.15). Where a struct has an invariant, the
    invariant has to hold for the zero value too, or the type wants to be a `sealed record` instead.
14. **`IAsyncDisposable.DisposeAsync` is one call, and a type owning several async resources still exposes
    one.** The pattern is `DisposeAsyncCore` doing the actual async teardown, called from `DisposeAsync`
    alongside disposing any synchronous fields — never two public dispose entry points on the same type,
    which just moves the ownership question in point 9 onto the caller instead of answering it.
15. **A double dispose has to be a no-op, not a second failure.** A `using` around code that already caught
    and handled an earlier failure, or two code paths that both think they own the cleanup, both call
    `Dispose` on an already-disposed object under real conditions — guard the body with a disposed flag
    rather than assuming a single call site.
16. **A nullable type parameter needs its own constraint, not an assumption from the call site.** A generic
    method typed over `T` without `where T : notnull` (or the reverse, an explicit nullable annotation on
    `T?`) inherits whatever nullability the caller's type argument happens to have — the method's own
    contract about null says nothing until the constraint states it.
17. **`ArgumentNullException.ThrowIfNull` is the guard clause, and the null-forgiving operator afterwards is
    what a reviewer should never see next to it.** Checking a parameter and then writing `param!` two lines
    later is not a mistake in isolation — each half is fine — but together they say the check exists purely
    to satisfy an analyser and nobody trusted its own result. Let the throw be the whole story: the
    compiler narrows the type after a `ThrowIfNull` the same way it narrows after an `is null` check, so the
    `!` that follows is either redundant or a sign the check was copied in without reading what it does.
18. **An `IAsyncEnumerable<T>` disposes its enumerator through `await foreach`, and breaking out of the loop
    early still has to run that disposal.** A `break` or a `return` inside the loop triggers the compiler's
    implicit `finally` calling `DisposeAsync` on the enumerator the same as a normal `foreach` would for a
    synchronous one — the trap is code that stores the enumerator itself (`GetAsyncEnumerator()` called by
    hand, outside a `foreach`) and then exits without a matching `DisposeAsync`, which leaves whatever
    connection or cursor backs the sequence open for as long as the process runs.
19. **A `SafeHandle` wraps the OS resource so a `Dispose` running during finalization can still release it
    correctly; a raw `IntPtr` field cannot.** A type that stores a native handle as `IntPtr` and closes it
    in a hand-written finalizer is exposed to the handle being reused by another allocation between the
    object becoming garbage and the finalizer running, so the wrong resource gets closed under load. Wrap
    the handle in a `SafeHandle` derivative instead — its release path is already interlocked against
    exactly that race, which is the reason to prefer it over rolling a finalizer by hand at all (point 2).
20. **A struct with a nullable value-type field defaults that field to `null` the same as any other default,
    and equality then depends on whether both sides agree on that.** `Nullable<T>` inside a `default`
    struct or a zero-initialized array element compares equal to another unset instance, which is normally
    invisible — until the struct is used as a dictionary key or a record's equality member, where two
    "empty" instances now silently collapse to one bucket or one duplicate-looking entry, matching point 13's
    warning about the zero value carrying real meaning whether or not anyone designed it to.
21. **Re-enumerating a sequence twice does not always mean two identical results, and the risky case is not
    always visible at the call site.** Point 4 covers the deferred-and-expensive case; the sharper version
    is a source that mutates between enumerations — a queue drained by a background reader, a stream whose
    position advanced by the first pass — where the second enumeration doesn't repeat the work, it silently
    sees less of it. `.ToList()` at the boundary where a sequence stops being "just produced" and starts
    being "read more than once" turns that silent gap into a value that can't move under the caller.
22. **`ConditionalWeakTable<TKey, TValue>` attaches data to an object's lifetime without extending it,** and
    reaching for a normal `Dictionary` keyed by the same object instead is how "extra state associated with
    this instance" turns into a leak: every entry keyed by reference in an ordinary dictionary keeps that
    key alive as long as the dictionary exists, which for anything long-lived is effectively forever. Where
    the requirement is genuinely "clean up when the object is collected, and not before," the conditional
    table is the one collection in the framework that gives you that instead of a `Dispose` you have to
    remember to call.
23. **An `IAsyncEnumerable<T>` producer accepts a `CancellationToken` through `[EnumeratorCancellation]`, not
    through an ordinary parameter.** A plain parameter on an `async IEnumerable<T>` iterator method is never
    populated by `await foreach`'s own `WithCancellation` — the attribute is what tells the compiler to wire
    the token the caller passed into the one the method reads. Without it the enumeration looks cancellable
    from the call site and simply never stops, which is a worse failure than not offering cancellation at
    all, because it hides behind code that appears to support it.
24. **A `CancellationTokenSource` created locally is disposed the same as any other `IDisposable` (point 1),
    and a linked source doubly so.** `CancellationTokenSource.CreateLinkedTokenSource` allocates a second
    object that has to be disposed independently of the tokens it links — a linked source left undisposed in
    a hot path is a steady handle leak that shows up as memory growth with no single large allocation to
    point at, because each one is small and the pattern repeats on every call.
25. **A nullable value-type parameter tested with `HasValue`/`Value` rather than compared against `null`
    through the equality operator once inside a hot path.** Both compile to the same result, but `.Value`
    used without a preceding check throws `InvalidOperationException` with a message naming neither the
    parameter nor the call site — matching point 6's pattern-form preference, `is { } bound` names and binds
    the underlying value in the one expression that already proved it was there, which removes the separate
    `.Value` access that can drift from the check that justified it.
26. **A object pool's `Return` path resets every field the pooled instance accumulated, or the pool leaks
    state across unrelated callers instead of leaking memory.** `ObjectPool<T>` and `ArrayPool<T>` hand the
    same instance to the next renter with none of the framework's own cleanup — a buffer returned without
    clearing carries the previous caller's data into a code path that never wrote to those slots, and a
    pooled object with a mutable field carries state across two requests that have no other relationship to
    each other.
27. **Nullable reference type warnings from a third-party package's own (possibly incomplete) annotations
    are not silenced with a project-wide `#nullable disable` around the call.** A dependency that annotated
    its public surface incompletely produces a false warning at the call site — the fix is a narrow
    `!`-suppression or a local `#pragma warning disable CS86xx` on that one line with a comment naming which
    package's annotation is wrong, because disabling nullable checking for the surrounding code silences
    every real warning in that block along with the one false one.
28. **Several `IDisposable` resources acquired in one method are disposed in the reverse of the order they
    were acquired, and the compiler enforces that automatically only when they're nested `using` statements
    or declarations, never when they're fields disposed by hand in a written-out order.** A resource that
    depends on another one still being open — a transaction wrapping a connection, a stream wrapping a
    file handle — has to close before the resource it depends on, so a hand-rolled `Dispose` that tears down
    fields in declaration order rather than dependency order can close the connection while the transaction
    built on it is still trying to flush. Nested `using` declarations get this for free; a type owning
    several disposables by hand has to state the order deliberately, because nothing checks it for you.
29. **A `WeakReference<T>` and `TryGetTarget` exist for a cache entry that should not itself be the reason
    an object stays alive, and using them for anything else trades a `Dispose` you forgot to call for a
    value that vanishes on its own schedule.** The pattern is right for a genuinely optional cache — a
    second lookup recomputes what a collected entry lost — and wrong for a resource that must be released
    deterministically, because `TryGetTarget` returning `false` is "the GC already ran," not "explicitly
    released," and code that treats a weakly-held handle as if closing it were still meaningful has
    reinvented point 22's `ConditionalWeakTable` case without its actual guarantee.
30. **A boxed value-type enumerator loses the mutation a `foreach` over a `struct`-based collection depends
    on, and the boxing happens exactly where the code looks generic.** `List<T>.Enumerator` and similar are
    structs so that a `foreach` compiled against the concrete type avoids an allocation per iteration; the
    same loop written against the `IEnumerable<T>` interface instead — a generic helper, a LINQ operator —
    boxes that struct to satisfy the interface, which is invisible in the source and shows up only as an
    allocation profile difference between "the same loop" written two ways. It matters for a hot path
    (point 8's territory) and is not worth chasing anywhere else.
31. **`GC.SuppressFinalize` in a hand-written `Dispose(bool)` (point 2) has to be called from the public
    `Dispose()` overload specifically, not from the protected one both paths share.** Calling it from inside
    `Dispose(bool disposing)` regardless of which branch invoked it suppresses finalization even when the
    object was actually being finalized — which is backwards, since the point of the call is to tell the GC
    "the object already cleaned up through `Dispose`, skip the finalizer," and a finalizer thread calling
    it on itself does not need that promise and shouldn't be making it look redundant.
32. **`IMemoryOwner<T>`'s `Memory<T>` stays valid only until `Dispose` runs, and a slice or a copy of the
    reference taken before disposal does not extend that.** Renting a buffer through `MemoryPool<T>.Rent`
    and disposing the owner returns the underlying array to the pool for the next renter to receive — the
    same `ArrayPool<T>` state-leak point 26 warns about — so a `Memory<T>` handed to another component and
    read after the owner's `Dispose` call reads whatever the next renter has since written into the same
    backing array. Whoever calls `Dispose` on the owner has to be the last reader of the memory it produced,
    and that ordering has to be explicit at the API boundary, not assumed from how long the reference happens
    to live in practice.
33. **A record's positional `with` expression and a manually written property setter disagree about whether a
    change is visible to `Equals`, and `init`-only properties are what keeps that from happening silently.**
    A record property declared with a plain `set` instead of `init` can be mutated after construction outside
    a `with` expression entirely, which means two records considered equal at one point in the program can
    drift apart from each other with no copy ever having been made — the value semantics point 7 already
    ascribes to `with` only holds while every property stays `init`-only; a settable one turns the record
    into a class with generated equality members riding on top of state that no longer matches what those
    members compare.
34. **`[MemberNotNull]` and `[MemberNotNullWhen]` tell the compiler what a guard method already proves, and
    without them a validation helper resets the flow analysis point 3 depends on at every call site.** A
    method that throws when a field is null, or returns `false` precisely when one is, doesn't communicate
    that to a caller unless annotated — so the same check written inline (`if (x is null) throw`) narrows the
    field for the rest of the method while the identical check moved into a helper leaves the compiler back
    at "might be null" the instant the helper returns, and the codebase accumulates redundant `!` (point 17)
    purely because the guard lives one call away from where its result is used.
35. **`[NotNullIfNotNull]` states a pass-through contract a return-type annotation alone can't express, and
    skipping it silently reverts to point 12's "annotation as documentation only."** A method that returns
    its own input unchanged when that input is non-null, and null only when the input was — a normaliser, an
    optional mapper — has a return type that has to be nullable to cover the second case, which then forces a
    null-check on every caller even for the branch that provably never produces one; naming the parameter the
    nullability is linked to is what lets the compiler narrow the *result* the same way it already narrows
    the input, instead of every caller re-deriving the guarantee by eye.
36. **A `ref struct` implementing an interface (C# 13's `allows ref struct` constraint) can now be disposed
    through generic code, and the disposal discipline this section builds around `IDisposable` (points 1, 9)
    finally reaches types that couldn't opt into it before.** `Lock`'s scope, a pooled buffer wrapper, or any
    stack-only type previously had to be disposed by a caller that knew its concrete type, because a `ref
    struct` could not implement `IDisposable` in a way a generic `using`-over-`T` could call; a generic method
    declared `where T : IDisposable, allows ref struct` can now own that disposal the same way it would for a
    heap type, which is new surface for point 9's "dispose what you own" to apply to rather than a new rule
    in itself.
37. **A collection expression's spread element enumerates its source once to build the target and disposes
    nothing it walked through.** `[.. source]` calls `GetEnumerator()`/`MoveNext()` on `source` the way a
    `foreach` would, but the compiler-generated code has no `using` around that enumeration — for a spread
    source that is itself an `IEnumerable<T>` backed by a disposable enumerator (a database cursor wrapped to
    look like a sequence, a custom iterator holding a handle), the collection expression finishes the copy
    and leaves that handle open, which is point 1's leak arriving through syntax that doesn't look like
    enumeration at the call site at all.
38. **A `using` declaration's scope is the rest of the enclosing block, not the statement it sits on, and two
    declared back-to-back stay open together for longer than the equivalent nested `using` statements would.**
    `using var a = ...; using var b = ...;` disposes both at the end of the method (or block) they're
    declared in, in reverse order (point 28) — which is usually what's wanted, but a resource that should
    close well before the method returns (a short-lived transaction opened partway through a longer method)
    silently outlives its useful scope if written as a declaration instead of a braced `using` statement,
    holding a connection or a lock for everything that runs afterward in the same block.
39. **`ArgumentOutOfRangeException.ThrowIfZero`/`ThrowIfNegative` and their siblings are point 17's guard
    clause for a numeric range instead of a null check, and the same rule about what comes after applies.**
    The framework's static throw-helpers for a parameter that must be positive, non-zero, or within a range
    read the same way `ArgumentNullException.ThrowIfNull` does — one line, no `if` block — and a reviewer
    should see the same thing after them that point 17 asks for after a null guard: nothing that re-checks
    what the throw-helper already established, because a defensive re-test right after says the check wasn't
    trusted the first time either.
40. **A `struct` with an `init`-only auto-property still has a parameterless constructor the runtime can call
    through `default` or array allocation, and point 13's zeroed-struct warning applies to `init` members the
    same as to a mutable one.** `init` changes when a property can be *set from outside the type* — after
    construction, only from an object initializer — it does not remove the all-fields-zeroed value every
    value type has whether or not its declared constructor ever ran; an invariant expressed only in a
    parameterised constructor still has to hold for the value nobody constructed that way, which is the same
    trap point 13 names, now reached through a property modifier that looks like it should have closed it.
