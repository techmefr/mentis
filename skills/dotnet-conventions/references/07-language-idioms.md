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
