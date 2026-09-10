# § 7 — Language idioms

> Section 7 of `skills/dotnet-conventions`. Read it when writing new code that has a choice of form.
> Preferences rather than prohibitions, all of them: propose the form below, accept an informed override,
> and never rewrite existing code to them unprompted (`code-baseline` §0).

1. **Test and bind in one step.** A type pattern that checks and names the value at once, rather than a
   conversion followed by a null check, an existence test followed by a separate cast, or a runtime
   type comparison. Multi-field conditions fold into property and relational patterns instead of a chain of
   member accesses that each have to be re-read for null. What it removes is a specific class of bug: the
   test and the use can no longer disagree, because there is only one expression.
2. **The expression form of a `switch` when every arm yields a value** — every branch assigning the same
   local, or every branch returning. Keep the statement form when the branches do work: an expression whose
   arms have side effects is harder to read than the statement it replaced, not easier.
3. **A collection expression where the target type is written on the left.** The spread form is an opt-in
   rewrite rather than a default, because it changes *when* the sources are enumerated — which matters for a
   lazy or side-effecting source, and for nothing else.
4. **Arguments guarded at the top of the method**, through the platform's own throw-if helpers where they
   exist: the argument-exception family is the framework's vocabulary for "the caller passed something
   wrong", and a hand-rolled check throws the wrong type. Where a guard is still written by hand, the
   parameter is named symbolically rather than as a typed string. And **never turn a literal that is
   *data* — a wire field, a config key, a policy name — into a symbol reference just because it happens to
   match an identifier today**: the day the identifier is renamed, the data silently changes with it.
5. **`required` members for what must be set, rather than a comment saying so.** It gives a
   property-initialised type the same guarantee a constructor parameter has, at the point of construction,
   without forcing every optional field through the constructor. The caveat is the same as §5.12's: a
   deserialiser or an ORM materialiser can bypass it, so it is a guarantee about code that constructs the
   type, not about data arriving from outside.
6. **A raw string literal for anything that contains quotes or backslashes** — embedded JSON, a SQL
   fragment, a regex, a Windows path in a test fixture. The escaped version is unreadable and, worse,
   unverifiable: a reviewer cannot tell whether `\\d` was meant to be one backslash or two, and the two
   behave differently.
7. **A record's `with` expression is the right way to express a copy with one field changed — and it is a
   shallow copy.** The new instance shares every reference the original held, so a "copy" whose list is
   then mutated changes both. Records make the value semantics of the *record's own* fields free; they do
   not make what those fields point at immutable (the same shallowness as `clone` elsewhere).
8. **A `switch` expression with no fallback arm throws at run time for an unlisted value.** That is
   better than falling through silently, and it is still a run-time failure — so for a value that arrives
   from outside (a wire field, a database column, an enum widened by a later deploy), the unhandled case
   deserves a deliberate arm that says what happens, not an exception with the compiler's message. For a
   value that is entirely internal, the throw is the right outcome and needs no arm.
9. **Prefer the form that keeps the type visible at the point it is read.** That is the thread running
   through this section and through §4.6: target-typed `new`, a collection expression, a pattern that names
   its result all keep the type stated once on the line that declares it, which is what a diff review and
   a `git log -p` can actually see. An idiom that moves the type off the line — or off the screen — is the
   one to decline, however concise it is.
10. **The fallback arm exists for the compiler, not only for the unlisted value.** An enum's underlying
    type admits any integer, so a `switch` expression covering every named member is still not exhaustive:
    the compiler reports it and names the zero value — which §4.15's explicit numbering usually leaves
    unnamed — and that report is a build failure wherever warnings are errors. Point 8 holds with one
    correction: the arm is written even for a value that is entirely internal, and what matters is that it
    throws rather than returning a plausible default. §5.13 states the same fact for `default(T)`.
11. **The backing-field keyword removes a declaration, not a decision.** Where the language version
    supports it, a property whose accessor needs the stored value can name it directly instead of declaring
    a private field beside it — which is the right form, because the field existed only to be paired with
    the property and nothing else could see it. Two cautions, both mechanical: in a type that already has a
    member of that name the keyword wins, silently changing what the accessor reads; and the keyword makes
    a validating setter cheap to write, which is not a licence to put behaviour in a property that the
    caller cannot see failing (§4.12's data-carrying types stay data).
12. **An extension member is a call-site convenience, not a place for a dependency.** Where the language
    version supports extension properties, operators and static members, they belong to the same judgement
    as the extension method they generalise: they read as if the type declared them, so the reader looks in
    the type first and does not find them. Use them to make a *foreign* type read naturally — a type from a
    package, a generated client — and never for a type we own, where the member simply goes on the type. An
    extension that reaches a service, a clock or a database is the worst case of both: an invisible
    dependency behind a member that looks like data (§2.1, §6.4).
13. **`nameof` for any name that must stay in sync with the declaration it names** — a guard's parameter
    name, a `PropertyChanged` argument, a log template's placeholder. The extended scope means a
    parameter's name is reachable from an attribute on the method, on the parameter itself, or on a type
    parameter, so there is no longer a reason to fall back to a string literal "because the name isn't in
    scope here." A renamed parameter that used a literal compiles clean and silently breaks the message; one
    written with `nameof` fails at the rename, in the same file, which is where the fix is cheapest.
14. **A list pattern for a check that is really about shape, not a single element.** `[var first, .., var
    last]` or `[_, _, ..]` states "exactly one item", "at least two", or "this exact sequence" as one
    expression, the same test-and-bind move as §7.1 applied to a sequence instead of a single value. The
    alternative — a length check followed by indexed access — has the same disagreement risk point 1
    describes for a cast: the length that was checked and the index that is read can drift apart across an
    edit, and nothing catches it until the index throws.
15. **A `u8` suffix for a string literal that is going to be bytes anyway** — a fixed HTTP header name, a
    magic-number prefix in a binary format, a constant compared against a `ReadOnlySpan<byte>` read off the
    wire. The literal is stored pre-encoded as UTF-8 and compared without an allocation, where the
    alternative — `Encoding.UTF8.GetBytes(...)` at every call, or worse, in a hot loop — allocates a new
    array to compare against a constant that never changes. It is a wire-level literal, not a general
    replacement for `string`: business text stays `string`, because it still needs comparison, formatting
    and culture rules a byte span doesn't have.
16. **A `global using` for a namespace that is imported by nearly every file in the project** — the
    framework namespace, the project's own root namespace, a handful of primitives everyone touches. It
    removes the same boilerplate `using` line from every file, which is a real gain; it also means a type's
    dependency list is no longer visible by opening that one file, which is the trade a nested class avoids
    by being findable at all (§4.2's complaint, one level up). Reserve it for the small set that really is
    ambient, and resist the temptation to promote every namespace to global just to shorten a diff — the
    file's own `using` list is still the fastest way to answer "what does this file talk to."
17. **A `params` parameter typed as a collection or interface rather than only `T[]`.** Where the language
    version supports it, `params IReadOnlyList<T>` or `params ReadOnlySpan<T>` accepts the same call-site
    spread as an array parameter but lets the callee declare the narrower contract §4.16 already asks for on
    a return type — the caller still writes `Method(a, b, c)` with no array literal in sight, and a
    `ReadOnlySpan<T>` overload skips the array allocation entirely for the common case. Overload resolution
    then has to pick between candidates that differ only in the `params` collection type, so keep at most
    one `params` overload per call shape rather than several competing on element type.
18. **The index and range operators (`array[^1]`, `items[1..^1]`) over hand-computed offsets.** `^1` states
    "last element" directly instead of `array.Length - 1`, and a range slices without a manual `Skip`/`Take`
    pair or a `Substring(start, length)` where `length` has to be recomputed from two ends by hand. What it
    removes is the usual off-by-one: `Length - 1` transcribed as `Length` or `Length + 1` compiles and throws
    or silently truncates, where `^1` has no arithmetic left to get wrong.
19. **A `using` declaration (`using var resource = ...;`) over the braced form, unless the disposal has to
    happen before other code in the same block runs.** It disposes at the end of the enclosing scope, same
    guarantee as §5.1, with one less indentation level and one less place for the closing brace to end up in
    the wrong spot after an edit. Reach for the braced form only when the resource must be released partway
    through the method, before later statements run.
20. **A target-typed conditional expression (`cond ? new Foo() : new Bar()` inferring a common type, or both
    branches converting to the target the assignment already states) over repeating the type on each arm.**
    The idiom this section keeps returning to — state the type once — applies here too: when the surrounding
    context already states the target type, letting both arms convert to it removes a second, redundant
    statement of a type already visible one token to the left.
21. **A primary constructor's parameters used directly in the body, not copied into a field the class already
    has room for.** Where a type takes a primary constructor (§4.12's carve-out), reading the parameter
    directly in a method body is the point of the feature; re-declaring `private readonly Foo _foo` and
    assigning it in a manually written constructor right next to a primary one is the anti-pattern — pick
    one, because a type with both a primary constructor and a hand-written one that also sets fields is two
    competing explanations for how the object gets built.
22. **`ArgumentOutOfRangeException.ThrowIfNegative`/`ThrowIfZeroOrNegative`/`ThrowIfGreaterThan` and the rest
    of the numeric guard family, for the same reason §4's argument-exception rule exists.** They read as the
    condition they check rather than as an `if` a reader has to evaluate, and they throw the exact exception
    type analyzers and callers expect for a range violation — a hand-written `if (value < 0) throw new
    ArgumentException(...)` gets both the condition-reading cost and the wrong exception type at once.
23. **A collection-initializing target-typed `new()` (`Dictionary<string, int> counts = new();`) over
    repeating the generic argument list on the right-hand side.** Same principle as point 9 and §4.6 stated
    from the other direction: when the left-hand side already names the full closed generic type, restating
    it on the right adds a second place that has to change together if the type ever does, for a form the
    compiler already resolves unambiguously from the declaration.
24. **A custom interpolated string handler for an interpolation that only sometimes needs to run.** A
    logging call already gets this for free from the framework's own handler (§2.9); the same shape applies
    to any API that accepts a formatted string behind a condition it controls — a debug-only assertion
    message, a diagnostic appended only past a verbosity threshold — where the handler's `AppendFormatted`
    calls are only invoked at all once the condition is checked, so an expensive `ToString()` or a boxed
    value never gets produced on the path where the message is discarded unread. Reach for a hand-written
    handler only where the call site is hot enough for that to matter; an ordinary string interpolation is
    the right default everywhere else.
25. **A `checked` block or a `checked` operator for arithmetic where an overflow means the calculation is
    wrong, not where wraparound is the intended behaviour.** The project-wide default is unchecked, so
    `int.MaxValue + 1` silently wraps to a negative number with no exception and no compiler warning at
    either the addition or the point the wrong value is later used — wrapping a specific expression (an
    array index computed from user-supplied lengths, a checksum accumulator) in `checked` turns that class
    of bug into an `OverflowException` at the moment it happens instead of a wrong answer discovered several
    calls downstream. A hash or a bitmask that relies on wraparound as its actual algorithm stays unchecked
    on purpose, and that choice is worth a comment precisely because it looks like the bug the checked form
    exists to catch.
26. **`StringSyntaxAttribute` on a parameter that is going to hold a regex, a JSON fragment, or a route
    template gives the editor syntax highlighting and inline diagnostics on a plain `string`, without
    changing what the parameter accepts.** It is a documentation mechanism, not a validation one — annotating
    a method's `pattern` parameter with `[StringSyntax(StringSyntaxAttribute.Regex)]` does nothing at run
    time and nothing the compiler enforces, but it is what turns an editor's generic string literal into one
    that is coloured, linted and completed as the embedded language it actually is, which is the same
    reviewer-legibility goal raw string literals (point 6) serve for the escaping problem rather than the
    syntax-awareness one.
27. **Extended property patterns nest a member access inside the pattern instead of a chain of `&&`
    conditions each re-reading the same path.** `{ Address.City: "Paris" }` states the nested check as one
    pattern the same way point 1 already prefers for a single level, and it composes with a `null` guard for
    free: the nested member is only read if the outer one is non-null, where a hand-written
    `x.Address != null && x.Address.City == "Paris"` needs the guard spelled out explicitly and drifts the
    moment someone edits one side without the other.
28. **A tuple deconstructed directly in a `foreach` header removes the `.Item1`/`.Item2` or `.Key`/`.Value`
    access that would otherwise repeat inside the loop body.** `foreach (var (id, name) in pairs)` over a
    sequence of tuples or `KeyValuePair<TKey, TValue>` binds both names once at the loop's own declaration,
    which is the same test-and-bind principle point 1 states for a single value applied to the two halves of
    a pair — the alternative, indexing into `.Key` and `.Value` on every line that needs them, is not wrong,
    it is simply the chain of repeated member access point 1 already argues against, one collection type
    later.
29. **`in` parameters pass a large `readonly struct` by reference without letting the callee mutate it, and
    passing anything else by `in` buys nothing but the annotation.** The parameter modifier only avoids a
    copy for a struct large enough that copying it costs more than passing a reference — for a small struct
    or a reference type, `in` adds a defensive-copy risk of its own (the compiler copies on any call that
    might mutate through the reference, silently, to preserve the readonly guarantee) with no size benefit
    to offset it. Reserve it for a struct genuinely too large to pass by value on a hot path, the same
    circumstance §4's `readonly struct` point exists for, not as a blanket default on every struct parameter.
30. **A discard (`_`) in a pattern or a deconstruction states "this position exists and is deliberately
    unused," which is a different claim from naming it and never reading the name.** `if (dict.TryGetValue(k,
    out _))` or `var (_, count) = Summarize(items)` tells a reader the second value was considered and
    rejected on purpose, where a named-but-unused variable leaves the same question open that an unused
    private field does — was this forgotten, or intentional — with a compiler warning as the only way to
    find out, and only if the warning is enabled. The discard makes the answer part of the code itself
    instead of something a linter has to notice on your behalf.
