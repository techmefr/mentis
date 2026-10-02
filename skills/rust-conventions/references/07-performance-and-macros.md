# rust-conventions §7 — Performance and macros

> Section 7 of `skills/rust-conventions`. Read it when a hot path, an allocation pattern, a collection, a
> benchmark or a macro is written or reviewed. The measure-first doctrine is `skills/webperf`; the rule here is
> the same one stated for this language. The other sections and the guardrails stay in `SKILL.md`.

**None of the micro-rules below applies before a profile says the code is hot.** A change justified by a
number in a rule and not by a measurement of this program is the exact mistake the first point forbids.

1. **Decide early whether the crate is performance-relevant; if it is, make the hot path measurable.**
   Identify the hot paths, put benchmarks around them (wall time and, where the tooling allows, CPU time across
   all threads), profile CPU and allocations regularly, and write down which areas are performance-sensitive so
   the next contributor does not undo it. Keep debug symbols in the benchmark profile so a profiler has names.
2. **Optimise for throughput: items per CPU cycle.** Batch the work, partition it ahead of time, let each
   thread or task process its slice, sleep or yield when there is none, expose batched APIs and use them.
   Do not spin hot to get single items faster, do not process one item at a time when batching is possible, and
   do not balance by work-stealing single items. Shared state is worth it only when sharing costs less than
   recomputing.
3. **Reuse allocations on the hot path.** A core API lets the caller own the output buffer and pass it in
   (`get_in(id, &mut value)`), with a `clear()` to reset, so a loop does not allocate per element. The
   allocating convenience form may exist, but as the secondary API.
4. **Size collections when the size is known.** Create a `Vec`, `String`, map or set with a capacity when the
   final or approximate size is known at construction, which avoids repeated reallocation and copying. After
   building a large long-lived collection without an exact reservation, shrink it to fit before storing, since
   growth can leave nearly half the memory unused.
5. **Immutable, frequently created sequences are boxed slices.** Internal data that is never resized and is
   instantiated thousands of times is stored as a boxed slice or a shared string instead of a growable `Vec` or
   `String`, which drops the capacity field and saves a third of the handle. Only when it is immutable, very
   numerous and not visible to users.
6. **Avoid reflexive nested sharing.** Wrapping every nested type in a reference-counted pointer, a habit from
   garbage-collected languages, makes each field access a chain of dependent memory loads. Start with embedded
   data and lift the hot, cache-friendly fields; keep shared ownership for types that really have several owners.
7. **The default hasher is safe, not fast.** For trusted internal keys, a fast non-cryptographic hasher is
   often a significant gain; for keys an attacker can craft, keep the default, which resists hash flooding.
8. **Applications can tune what libraries cannot.** A binary may choose a faster global allocator and, for a
   server with a known fleet, a more specific CPU target. Benchmark both on the real workload first.
9. **Macros are the last resort.** Use the language first: a macro is opaque, raises compile time for projects
   that otherwise have none, and can break across edition changes. The more complex the structure a macro
   generates, the worse the idea. A good macro makes its user think "I know exactly what this generates, I just
   do not want to type it".
10. **When a macro is justified, prefer a declarative one over a procedural one**, since its expansion is easy
    to inspect and it compiles faster. Its input syntax looks like the output (a `struct` keyword before a
    struct name, semicolons after constants), it accepts attributes on each generated item and visibility
    specifiers, it works in module scope and in function scope, and its type fragments accept primitives,
    relative and absolute paths, `super` paths and generics. Test it in both scopes.
11. **A macro does not lie about what is written.** It does not turn a struct into an enum, change a function
    signature, flip `async`, or define hidden magic types. A procedural macro is a thin shim in its own crate
    that calls a normal library crate holding the logic and its snapshot tests. The macro crates are pinned to
    the exact version of the main crate and published together. Generated code refers to third-party items
    through a hidden re-export module of the main crate, and assumes the macro is used through the main crate,
    not under a renamed import.
