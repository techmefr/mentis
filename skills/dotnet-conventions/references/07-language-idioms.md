# § 7 — Language idioms

> Section 7 of `skills/dotnet-conventions`. Read it when writing new code that has a choice of form.
> Preferences rather than prohibitions, all of them: propose the form below, accept an informed override,
> and never rewrite existing code to them unprompted (`code-baseline` §0).

1. **Test and bind in one step.** A type pattern that checks and names the value at once, rather than a
   conversion followed by a null check, an existence test followed by a separate cast, or a runtime type
   comparison. Multi-field conditions fold into property and relational patterns instead of a chain of
   member accesses each re-read for null. It removes a class of bug: test and use can't disagree, because
   there is one expression.
2. **The expression form of a `switch` when every arm yields a value** — every branch assigning the same
   local, or every branch returning. Keep the statement form when branches do work: an expression whose
   arms have side effects is harder to read than the statement it replaced.
3. **A collection expression where the target type is written on the left.** The spread form is an opt-in
   rewrite, not a default, because it changes *when* the sources are enumerated — which matters for a lazy
   or side-effecting source, and nothing else.
4. **Arguments guarded at the top of the method**, through the platform's throw-if helpers where they
   exist: the argument-exception family is the framework's vocabulary for "the caller passed something
   wrong", and a hand-rolled check throws the wrong type. Where a guard is still hand-written, name the
   parameter symbolically rather than as a typed string. And **never turn a literal that is *data* — a wire
   field, a config key, a policy name — into a symbol reference because it matches an identifier today**:
   rename the identifier and the data silently changes with it.
5. **`required` members for what must be set, rather than a comment saying so.** It gives a
   property-initialised type a constructor parameter's guarantee at the point of construction, without
   forcing optional fields through the constructor. Caveat as §5.12: a deserialiser or ORM materialiser can
   bypass it, so it guarantees code that constructs the type, not data arriving from outside.
6. **A raw string literal for anything containing quotes or backslashes** — embedded JSON, a SQL fragment,
   a regex, a Windows path in a test fixture. The escaped version is unreadable and unverifiable: a
   reviewer can't tell whether `\\d` meant one backslash or two, and they behave differently.
7. **A record's `with` expression is the right way to copy with one field changed — and it is a shallow
   copy.** The new instance shares every reference the original held, so a "copy" whose list is then
   mutated changes both. Records make value semantics of the *record's own* fields free; they don't make
   what those fields point at immutable (the same shallowness as `clone` elsewhere).
8. **A `switch` expression with no fallback arm throws at run time for an unlisted value.** Better than
   silent fall-through, yet still a run-time failure — so for a value arriving from outside (a wire field,
   a database column, an enum widened by a later deploy), the unhandled case deserves a deliberate arm
   saying what happens, not the compiler's exception message. For an entirely internal value the throw is
   right and needs no arm.
9. **Prefer the form that keeps the type visible where it is read.** This is the thread through this
   section and §4.6: target-typed `new`, a collection expression, a pattern naming its result all state
   the type once on the declaring line, which is what a diff review and `git log -p` can see. Decline an
   idiom that moves the type off the line or off the screen, however concise.
10. **The fallback arm exists for the compiler, not only for the unlisted value.** An enum's underlying
    type admits any integer, so a `switch` expression covering every named member is still not exhaustive:
    the compiler reports it naming the zero value — which §4.15's explicit numbering usually leaves
    unnamed — and that report is a build failure wherever warnings are errors. Point 8 holds with one
    correction: the arm is written even for an entirely internal value, and what matters is that it throws
    rather than returning a plausible default. §5.13 states the same fact for `default(T)`.
11. **The backing-field keyword removes a declaration, not a decision.** Where the language version
    supports it, a property whose accessor needs the stored value names it directly instead of declaring a
    private field beside it — the right form, since the field existed only to pair with the property. Two
    mechanical cautions: in a type already having a member of that name the keyword wins, silently changing
    what the accessor reads; and it makes a validating setter cheap, which is no licence to put behaviour
    in a property whose failure the caller can't see (§4.12's data-carrying types stay data).
12. **An extension member is a call-site convenience, not a place for a dependency.** Where the language
    version supports extension properties, operators and static members, they follow the same judgement as
    the extension method they generalise: they read as if the type declared them, so the reader looks in
    the type first and finds nothing. Use them to make a *foreign* type read naturally (a package type, a
    generated client), never for a type we own, where the member goes on the type. An extension reaching a
    service, a clock or a database is the worst of both: an invisible dependency behind a member that looks
    like data (§2.1, §6.4).
13. **`nameof` for any name that must stay in sync with the declaration it names** — a guard's parameter
    name, a `PropertyChanged` argument, a log template's placeholder. With the extended scope a parameter's
    name is reachable from an attribute on the method, the parameter or a type parameter, so there is no
    reason to fall back to a literal "because the name isn't in scope here." A renamed parameter that used a
    literal compiles clean and silently breaks the message; with `nameof` it fails at the rename, in the
    same file, where the fix is cheapest.
14. **A list pattern for a check that is about shape, not a single element.** `[var first, .., var last]`
    or `[_, _, ..]` states "exactly one item", "at least two" or "this exact sequence" as one expression —
    §7.1's test-and-bind applied to a sequence. A length check followed by indexed access has the
    disagreement risk point 1 describes for a cast: the checked length and the read index can drift apart
    across an edit, and nothing catches it until the index throws.
15. **A `u8` suffix for a string literal that is going to be bytes anyway** — a fixed HTTP header name, a
    magic-number prefix in a binary format, a constant compared against a `ReadOnlySpan<byte>` off the
    wire. The literal is stored pre-encoded as UTF-8 and compared without allocation, where
    `Encoding.UTF8.GetBytes(...)` at every call, or in a hot loop, allocates a new array to compare against
    a constant that never changes. It is a wire-level literal, not a replacement for `string`: business
    text stays `string`, since it needs comparison, formatting and culture rules a byte span lacks.
16. **A `global using` for a namespace imported by nearly every file** — the framework namespace, the
    project's root namespace, a handful of primitives everyone touches. It removes the same boilerplate
    line from every file, a real gain; but a type's dependency list is then no longer visible in that one
    file (§4.2's complaint, one level up). Reserve it for the small set that is really ambient, and don't
    promote every namespace to global to shorten a diff — the file's own `using` list is still the fastest
    answer to "what does this file talk to."
17. **A `params` parameter typed as a collection or interface rather than only `T[]`.** Where the language
    version supports it, `params IReadOnlyList<T>` or `params ReadOnlySpan<T>` accepts the same call-site
    spread as an array but lets the callee declare the narrower contract §4.16 asks for on a return type —
    the caller still writes `Method(a, b, c)`, and a `ReadOnlySpan<T>` overload skips the array allocation
    in the common case. Overload resolution must then pick between candidates differing only in the
    `params` collection type, so keep at most one `params` overload per call shape, not several competing
    on element type.
18. **The index and range operators (`array[^1]`, `items[1..^1]`) over hand-computed offsets.** `^1` states
    "last element" instead of `array.Length - 1`, and a range slices without a manual `Skip`/`Take` pair or
    a `Substring(start, length)` with a hand-recomputed `length`. It removes the off-by-one: `Length - 1`
    transcribed as `Length` or `Length + 1` compiles and throws or silently truncates, where `^1` leaves no
    arithmetic to get wrong.
19. **A `using` declaration (`using var resource = ...;`) over the braced form, unless disposal must happen
    before other code in the same block runs.** It disposes at the end of the enclosing scope, the same
    guarantee as §5.1, with one less indentation level and one less place for the closing brace to land
    wrong after an edit. Use the braced form only when the resource must be released partway through the
    method.
20. **A target-typed conditional expression (`cond ? new Foo() : new Bar()` inferring a common type, or both
    branches converting to the target the assignment states) over repeating the type on each arm.** The
    idiom this section keeps returning to — state the type once: when the surrounding context states the
    target type, letting both arms convert removes a redundant restatement one token to the left.
21. **A primary constructor's parameters used directly in the body, not copied into a field the class
    already has room for.** Where a type takes a primary constructor (§4.12's carve-out), reading the
    parameter directly is the point of the feature; re-declaring `private readonly Foo _foo` and assigning
    it in a hand-written constructor beside a primary one is the anti-pattern — pick one, since a type with
    both is two competing explanations of how the object is built.
22. **`ArgumentOutOfRangeException.ThrowIfNegative`/`ThrowIfZeroOrNegative`/`ThrowIfGreaterThan` and the
    rest of the numeric guard family, for the reason §4's argument-exception rule exists.** They read as the
    condition they check rather than an `if` to evaluate, and throw the exception type analyzers and
    callers expect for a range violation — a hand-written `if (value < 0) throw new ArgumentException(...)`
    pays the condition-reading cost and the wrong exception type at once.
23. **A target-typed `new()` (`Dictionary<string, int> counts = new();`) over repeating the generic
    argument list on the right.** Point 9 and §4.6 from the other direction: when the left names the full
    closed generic type, restating it on the right adds a second place to change together if the type ever
    does, for a form the compiler resolves unambiguously.
24. **A custom interpolated string handler for an interpolation that only sometimes needs to run.** A
    logging call gets this free from the framework's handler (§2.9); the same shape applies to any API
    accepting a formatted string behind a condition it controls — a debug-only assertion message, a
    diagnostic appended past a verbosity threshold — where `AppendFormatted` is called only once the
    condition is checked, so an expensive `ToString()` or boxed value is never produced where the message
    is discarded unread. Write a handler by hand only where the call site is hot enough to matter; ordinary
    interpolation is the right default elsewhere.
25. **A `checked` block or operator for arithmetic where overflow means the calculation is wrong, not where
    wraparound is intended.** The project-wide default is unchecked, so `int.MaxValue + 1` silently wraps
    negative with no exception or compiler warning at the addition or where the wrong value is later used —
    wrapping a specific expression (an array index computed from user-supplied lengths, a checksum
    accumulator) in `checked` turns that bug class into an `OverflowException` at the moment it happens
    instead of a wrong answer found several calls downstream. A hash or bitmask relying on wraparound as its
    algorithm stays unchecked on purpose, worth a comment because it looks like the bug `checked` catches.
26. **`StringSyntaxAttribute` on a parameter that will hold a regex, a JSON fragment or a route template
    gives the editor syntax highlighting and inline diagnostics on a plain `string`, without changing what
    it accepts.** It is documentation, not validation — `[StringSyntax(StringSyntaxAttribute.Regex)]` on a
    `pattern` parameter does nothing at run time and nothing the compiler enforces, but makes the editor
    colour, lint and complete the literal as the embedded language it is: the reviewer-legibility goal raw
    string literals (point 6) serve for escaping, applied to syntax-awareness.
27. **Extended property patterns nest a member access inside the pattern instead of a chain of `&&`
    conditions re-reading the same path.** `{ Address.City: "Paris" }` states the nested check as one
    pattern as point 1 prefers for a single level, and composes with a `null` guard free: the nested member
    is read only if the outer is non-null, where `x.Address != null && x.Address.City == "Paris"` spells
    the guard out and drifts when someone edits one side.
28. **A tuple deconstructed directly in a `foreach` header removes the `.Item1`/`.Item2` or `.Key`/`.Value`
    access that would repeat in the loop body.** `foreach (var (id, name) in pairs)` over tuples or
    `KeyValuePair<TKey, TValue>` binds both names once at the loop's declaration — point 1's test-and-bind
    applied to the halves of a pair. Indexing `.Key` and `.Value` on every line is not wrong, just the
    repeated member access point 1 argues against, one collection type later.
29. **`in` parameters pass a large `readonly struct` by reference without letting the callee mutate it, and
    passing anything else by `in` buys only the annotation.** The modifier avoids a copy only for a struct
    large enough that copying costs more than passing a reference — for a small struct or a reference type,
    `in` adds a defensive-copy risk (the compiler silently copies on any call that might mutate through the
    reference, to preserve the readonly guarantee) with no size benefit. Reserve it for a struct too large
    to pass by value on a hot path, the circumstance §4's `readonly struct` point exists for, not a blanket
    default on every struct parameter.
30. **A discard (`_`) in a pattern or deconstruction states "this position exists and is deliberately
    unused", a different claim from naming it and never reading the name.** `if (dict.TryGetValue(k,
    out _))` or `var (_, count) = Summarize(items)` tells a reader the second value was considered and
    rejected on purpose; a named-but-unused variable leaves the question an unused private field leaves —
    forgotten or intentional? — answerable only by a compiler warning, if enabled. The discard puts the
    answer in the code instead of leaving a linter to notice.
31. **The null-conditional assignment (`obj?.Prop = value`, `obj?.Prop += value`) replaces an
    `if (obj is not null) obj.Prop = value` that existed only to guard the write, not to branch on anything
    the caller cares about.** It composes with the compound-assignment forms — `+=`, `-=`, `??=` and the
    rest — but not `++`/`--`, so a counter increment still needs the explicit guard. Use it where point 1's
    test-and-bind applies: when the null check and the single write are the whole statement, one expression
    removes a branch that added no information.
32. **A partial constructor or partial event pairs a declaring part with an implementing part, the split
    partial properties have (point 04.21's sibling).** The declaring part states the signature — parameters,
    or the event's type and name — and a generator or hand-written second file supplies the body, under
    point 04.21's discipline: the hand-written half never reaches into what the generated half owns, and the
    generated half is never hand-edited because the next build discards the edit. Use it when a
    constructor's real body is generated (a source generator wiring injected fields) and the declaring part
    is what the type's file wants to show a reader not looking for generator output.
33. **A lambda parameter carrying `ref`, `in`, `out` or `scoped` states the same by-reference contract a
    method parameter does, instead of forcing a named local method to get it.** A delegate type declaring a
    `ref` parameter can now be satisfied by a lambda repeating the modifier, without inferring it silently
    — where before a lambda needed an explicit delegate type spelled out by hand. Stating the modifier on
    the parameter is point 9's "keep the type and its contract visible on the declaring line", applied to a
    parameter modifier instead of a type name.
34. **`nameof` now resolves an unbound generic type (`nameof(List<>)`, not only `nameof(List<int>)`), the
    form a diagnostic or log template wants when the message is about the generic type itself, not one
    closed instantiation.** Before, naming a generic type in a string meant picking an arbitrary type
    argument to make `nameof` compile, or a literal `"List"` a rename silently stops matching — point 13's
    rename-safety, extended to a type that had no safe spelling.
35. **The widened implicit conversions to `Span<T>` and `ReadOnlySpan<T>` mean an API written to accept a
    span takes an array, a `string` (for `ReadOnlySpan<char>`) or another span-convertible type with no
    explicit `.AsSpan()` — a call-site simplification, not a licence to treat every span-typed parameter as
    interchangeable with what used to be passed by hand.** A method changed from `string` to
    `ReadOnlySpan<char>` to avoid an allocation still changes what the callee can do with the value (no
    boxing, no capturing past the call, point 04.22's `ref struct` restrictions) — the conversion hides the
    syntax, not the contract, so an unchanged call site is no evidence the semantics are unchanged.
36. **A user-defined compound assignment operator (`operator +=` declared directly, rather than `operator
    +` plus the compiler's expansion to `x = x + y`) is for a type where the in-place form is measurably
    cheaper than "compute a new value, then assign" — a large mutable buffer, an accumulator that would
    allocate a new instance on every `+=` in a loop.** It is the compound counterpart to point 04.26's rule
    for `+`/`==`/`<`: reserved for an operation with one unambiguous domain meaning, used only when in-place
    mutation is the actual optimisation, not as a shorter spelling of an existing operator overload.
37. **EF Core's `LeftJoin`/`RightJoin` query operators replace the `GroupJoin` + `SelectMany` +
    `DefaultIfEmpty` sequence that was the only way to express an outer join in LINQ.** The three-step form
    compiles to the same SQL, but nothing in its shape says "outer join": a grouped join, a flattening and
    a default-substitution whose combination must be recognised rather than read. `orders.LeftJoin(customers,
    o => o.CustomerId, c => c.Id, (o, c) => new { o, c })` states the join kind as a word — "prefer the form
    that states what it means" — and the right side of a `LeftJoin` (the left of a `RightJoin`) is nullable
    in the projection, the one thing to check against a leftover null-forgiving `!` from the old pattern's
    workaround.
