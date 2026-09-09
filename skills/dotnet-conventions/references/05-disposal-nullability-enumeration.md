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
