# § 9 — What only breaks at publish

> Section 9 of `skills/dotnet-conventions`. Read it when the project targets a trimmed, single-file or
> ahead-of-time publish, or when reflection, serialisation or a path relative to the executable is written
> in a project that might. Everything here compiles, runs locally and passes the tests: the failure appears
> in the published artefact, which is the one nobody ran.

1. **Reflection-based serialisation is disabled in a trimmed or AOT publish**, and the code that used it
   throws at the first request rather than failing the build — an explicit "reflection-based serialisation
   has been disabled for this application", on the path that worked all through development. The answer is
   the serialisation source generator, a context declaring the types it must handle, which makes the list a
   build-time artefact: a payload type added later and not declared is the same failure again, in the one
   endpoint nobody exercised.
2. **Trimming keeps what it can see, and reflection over a name computed at run time is invisible to it.**
   The member is removed, so the symptom is a missing type or method rather than a missing feature, and it
   names something you did not write. Either annotate the boundary so the trimmer keeps what the reflection
   needs, or don't reflect there — usually the right call in application code.
3. **The publish is part of the build, and CI has to run it.** Building proves nothing about a trimmed or
   single-file publish, and the warnings the publish emits are the review surface: each names a place where
   the analysis could not prove the code survives. A baseline of them is a list of things that will throw
   in production, the same trade as any suppressed analyser finding (this block's guardrail).
4. **Single-file and AOT change what the process knows about itself.** The assembly's location comes back
   empty, so anything resolving a path relative to it silently reads from the working directory instead — a
   configuration file, a template, a certificate. Ask the host for the content root or the application's
   base directory, which is what §6.3 means by not hardcoding a path.
5. **Test what you ship, at least once.** A suite that only runs against the ordinary build exercises a
   different code path from the published artefact: the tests are green and the binary throws. Where a
   trimmed or AOT publish is a real target, one smoke test runs the published thing and hits one endpoint
   that serialises — that test turns every rule above from advice into a check.
6. **A publish warning suppressed is the root cause left in place, not removed.** Silencing a trim or AOT
   warning states that the code path is compatible when the analysis could not prove it — the warning was
   the one signal that the throw hadn't been found yet. Fix the code path or accept the limitation
   explicitly (a documented fallback, a feature disabled in this publish mode); never silence the warning
   to make the count go down.
7. **Native AOT cannot generate code at run time, which is a different failure from trimming.** Anything
   building a new type, compiling an expression tree, or emitting IL at run time (a dynamic proxy, a
   hand-rolled expression compiler, some serializers' fallback path) has nothing to fall back to under AOT —
   it isn't trimmed away, it never worked. Before adopting a library for an AOT target, confirm it publishes
   an AOT-compatibility statement rather than discovering the gap in the published binary.
8. **A third-party package's own trim/AOT compatibility is not assumed, it's read.** A package with no
   compatibility annotations can build and pass tests while depending on reflection the trimmer cannot see;
   the project's publish warnings are where that gap surfaces, one release behind whether the maintainers
   have caught up.
9. **`RegexOptions.Compiled` asks the runtime to emit IL for the pattern, which Native AOT cannot do** — the
   same failure as point 7. It does not throw: the regex silently falls back to the interpreted engine, so
   the only symptom is a slower match nobody flagged because nothing failed. The source-generated regex
   (`[GeneratedRegex]` on a partial method) compiles the pattern at build time, the trade this section keeps
   making — turn a run-time capability into a build-time artefact the trimmer and AOT compiler can see.
10. **A method that reflects on its own account has to say so, or its caller finds out at publish instead
    of at the call site.** `RequiresUnreferencedCodeAttribute` on a method that walks a type's members, and
    `DynamicallyAccessedMembersAttribute` on a parameter or generic type whose members that walk depends on,
    move the warning from "somewhere in the published output" to "at the line that calls this method" —
    so the author of the reflection sees it, not someone three layers away. Application code that reflects
    across a public boundary needs the same annotations or it exports point 2's problem.
11. **Explicitly rooting an assembly cancels trimming for it, and that trade is not free.** A
    `TrimmerRootAssembly` (or an ILLink descriptor doing the same by hand) keeps everything in that assembly
    reachable or not — silencing warnings from a library with no trim annotations, but also keeping every
    unused type and method. The right escape hatch for a dependency you cannot fix or avoid;
    the wrong first response to a warning, since it hides the offending member behind "keep all of it."
12. **ReadyToRun and Native AOT solve different problems, and enabling one while expecting the other's
    guarantees is how this section's failures arrive as a surprise.** R2R precompiles IL to native code for
    faster startup while keeping the JIT, reflection and the full framework — none of points 1–11 apply to
    an R2R publish, because nothing was trimmed and nothing lost the ability to generate code. `PublishAot`
    removes the JIT entirely and pulls trimming in as a consequence; choosing it for "faster startup"
    without meaning to take on the trimming and no-codegen contract is how a team discovers this section in
    production instead of in the release notes.
13. **Configuration binding reflects over the options type's properties, the same as any other
    reflection-based serialisation.** `IConfiguration.Bind` or `services.Configure<T>` walks properties by
    name at run time; under trimming, a property the trimmer could not prove was read stays unset rather
    than throwing — the options object binds to defaults for the members nobody kept, and the failure looks
    like a wrong value rather than a missing one. The configuration-binding source generator
    (`EnableConfigurationBindingGenerator`) produces a binding method per options type at build time,
    putting point 1's list problem under the compiler's eye instead of the trimmer's guess.
14. **Globalization-invariant mode is a separate switch from trimming, and it silently changes what a string
    comparison means rather than throwing.** With `InvariantGlobalization` enabled, every culture-aware
    comparison and case conversion falls back to ordinal behaviour regardless of the `CultureInfo` or
    `StringComparison` the caller asked for — a sort order or uppercasing rule that depended on a specific
    culture (a Turkish `i`, an accent-insensitive sort) quietly changes in the published binary while the
    same code produced the expected order in every local run against the full ICU data. It shrinks the
    published size (tens of megabytes in a container image), which is why it gets turned on for the wrong
    reason on a service that does localise.
15. **Constructing any culture other than the invariant one throws once invariant mode is on, and it throws
    at the call site, not at startup.** `CultureInfo.GetCultureInfo("fr-FR")` or setting `CurrentCulture` to
    a named culture raises an exception the moment that line runs — the first request that needs it, in
    production, after the switch was flipped for the size or startup win of point 14. Grep for named-culture use before enabling the mode.
16. **Native AOT does not support runtime marshalling for COM or Windows Runtime interop, which is a third
    kind of "invisible until publish" alongside reflection and codegen.** `[ComImport]` types, apartment-
    threaded COM objects and WinRT activation depend on infrastructure Native AOT does not carry, so code
    exercising them builds and runs under the JIT and fails only in the AOT artefact — point 7's gap, usually
    discovered through a transitive package that leaned on COM for one code path.
17. **A source generator that emits attributes read by the trimmer only helps if it runs before the
    trimmer sees the code, and a generator disabled or misconfigured for one build configuration fails
    silently.** The JSON, configuration-binding, regex and logging source generators this section relies on
    (points 1, 9, 13) are opt-in per project and can be absent from a `Release` or publish configuration
    that never got the `Debug` `<PropertyGroup>` — the list reverts to the reflection path with no error,
    because reflection still compiles.
18. **`PublishReadyToRun` is restricted to publishing for the runtime identifier of the machine doing the
    publishing, unless cross-OS/architecture R2R is explicitly supported for that pair.** A CI machine
    publishing R2R for a different target RID than its own silently produces IL-only output instead of the
    promised precompiled native code — the artefact still runs, with the cold-start cost R2R exists to remove, and
    nothing in the build log calls it a failure.
19. **Blazor WebAssembly's default trimmer granularity is partial, and a library counted on to shrink only
    trims if it opted in.** Only framework libraries and packages that explicitly declare trimming support
    are trimmed by default; a third-party package with no trim annotations ships whole into the WASM payload
    however little the app calls — a silent size regression, not a build failure.
20. **A feature switch read through `AppContext.GetSwitch`/`AppContext.SetSwitch` is how the trimmer removes
    an entire code path at publish time, and setting the switch anywhere but the project file arrives too
    late to help.** The runtime libraries gate optional subsystems (globalization variants, diagnostics,
    some serializer fallbacks) behind switches the linker can evaluate at trim time when declared as
    `RuntimeHostConfigurationOption` MSBuild items — a switch flipped in `Main` still changes behaviour, but
    the trimmer made its keep/remove decision before that line ran, so it cannot shrink a path the switch
    turns off dynamically.
21. **A satellite resource assembly for a culture nobody publishes for is still built unless
    `SatelliteResourceLanguages` says otherwise.** Every culture a referenced package ships localised
    strings for gets its own resource DLL in the output by default, dead weight for an app that runs in one
    language — restating the languages shipped is the same trade as point 14's invariant-globalization
    switch, one config line instead of a dozen unused assemblies in every publish.
22. **A source generator that reads a project file, an embedded resource or another source file at compile
    time works from the compiler's snapshot, not from the file on disk when the published binary runs.** A
    generator that reads a `.json` or `.resx` sibling to bake its content into generated code has finished
    by the time the application starts, so a config file edited after publishing without a rebuild changes
    nothing the generator produced — expected, but it looks like point 4's failure to whoever expected
    editing the deployed file to work, so state the boundary once, near the generator.
23. **`DynamicDependencyAttribute` names exactly the member a trimmer-invisible call site needs kept, and is
    the narrower alternative to point 11's whole-assembly root.** Where a single method is reached through a
    string-built name — `Activator.CreateInstance` on a type name from configuration, a reflection call the
    trimmer cannot follow — the attribute states which member must survive without exempting the rest of the
    assembly, keeping point 10's warning scoped to the one place that needs the escape hatch instead of
    hiding an entire library behind it.
24. **MVC controllers are not a Native AOT target at all, which is a different failure from anything
    trimming produces on its own code that does run.** `AddControllers`, view compilation and the classic
    model-binding pipeline lean on reflection and runtime code generation deeply enough that the framework
    doesn't attempt to make them AOT-safe — the AOT project template ships minimal APIs only, and a project
    that adds MVC to an AOT-published host is outside what the platform supports, not working through a
    warning list. Targeting Native AOT is a decision to build on minimal APIs, made before the first
    controller is written, not discovered at the first publish.
25. **The Request Delegate Generator turns a minimal API's route handlers into source-generated code at
    compile time, and it only runs once trimming or AOT is actually turned on for the project.** A handler
    that works under the JIT build goes through the generator's code path the moment `PublishAot` (or
    trimming) is enabled — a handler shape the generator can't express (one built from a runtime-computed
    delegate, for instance) surfaces as a build-time diagnostic rather than a run-time trim warning.
26. **A pre-compiled EF Core query (point 21's compiled model taken one step further) needs the same
    "regenerate when the model changes" discipline, and skipping it produces a stale artefact that still
    builds.** Pre-compiled queries generate the SQL and materialisation code for a specific LINQ expression
    at build time so nothing depends on reflecting over the model at run time — what makes them viable
    under trimming and AOT, and why a query changed without regenerating keeps compiling against the old
    generated code, silently running the previous version of the query against the current model.
27. **A container base image chosen for size (a "chiseled" or distroless variant) can be missing pieces an
    AOT-published binary still calls into, and the gap is invisible until the container actually starts.**
    The binary still links against native ICU, OpenSSL or equivalent libraries at the OS level — a minimal
    image without those shared libraries runs the framework-dependent publish fine while the AOT one crashes
    at startup with a missing native library, because the two modes depend on the host image differently.
28. **`PublishTrimmed` without `PublishAot` still runs the IL trimmer alone, and every failure mode in this
    section that comes from trimming (points 1, 2, 8, 10, 11, 17, 19, 23) applies to it independently of
    Native AOT's no-codegen restriction (points 7, 9, 16).** A trimmed project keeps the JIT and code
    generation, so point 12's distinction cuts three ways: R2R changes nothing this section warns about,
    trimming alone brings the "invisible member removed" class without the "cannot generate code" class, and
    full AOT brings both — treating "trimmed" and "AOT" as one setting is how a team fixes the wrong half of
    the list.
29. **A file-based app (`dotnet run app.cs`, .NET 10) publishes Native AOT by default, which means a script
    nobody meant to harden against this section inherits every one of its rules the day it's published
    rather than merely run.** `dotnet publish` on it turns on
    `PublishAot` without being asked — so the first sign of points 1, 7 or 15 is the publish step itself,
    for a file never reviewed as an AOT target.
30. **Packing a .NET tool as self-contained, trimmed or Native AOT (.NET 10) exposes the same failures this
    section already describes, the day the packaging choice changes rather than the day the code does.** A
    global tool authored against the framework-dependent build can be packed several ways without a source
    change; switching the pack target to trimmed or AOT surfaces points 1, 2 and 7 for code that compiled
    and ran identically under every previous packaging choice — so point 3's CI publish must
    cover every packaging variant that ships.
31. **The AOT and trim analyzers catch more of this section at build time than they used to, and that
    coverage is still opt-in per project, per warning wave — point 3's rule about running the publish is not
    superseded by better tooling.** A newer SDK flags a wider slice of points 1, 2 and 7 during an
    ordinary build, narrowing the gap between "compiles" and "publishes safely" without closing it — a
    warning wave introduced after a project's `TreatWarningsAsErrors` baseline was set can sit unenforced.
32. **The feature-switch attribute model (.NET 9) declares a switch's trim behaviour in the same place as its
    name, which point 20's bare `AppContext` switch left to be documented separately or not at all.** A
    library author states, next to the switch, both the friendly configuration name an app sets in its
    project file and what the trimmer should assume when it's off — so a consumer knows from the declaration
    whether flipping it removes code (point 20's condition) without cross-referencing documentation that can
    drift from what the linker configuration says.
33. **Hybrid globalization mode is a third point on the axis points 14 and 15 describe as two, not a safer
    version of either.** Full ICU keeps every culture-aware behaviour; invariant mode (point 14) flattens
    all of it to ordinal; hybrid keeps culture-aware casing and comparison but still throws or falls back
    for the operations that need the full ICU data files it deliberately doesn't ship — so code exercising
    exactly that subset fails the way point 15 describes, for a smaller and less obviously
    invariant-shaped set of operations, easy to miss in testing because most culture-aware code keeps
    working under it.
34. **`[DllImport]` depends on the runtime's own marshalling engine to build the interop stub at load time,
    which Native AOT does not carry — `[LibraryImport]` generates that same stub at compile time instead,
    the list-as-build-artefact trade of point 1.** A `[DllImport]` that worked under the JIT throws at the
    call site under AOT with no build-time signal; the source-generated partial method surfaces an
    unsupported parameter or return shape as a compiler error on the declaration, before publish.
35. **`IsAotCompatible` (.NET 10) is an assembly-level claim a package makes about itself, and reading it as
    proof rather than as a starting point repeats point 8's mistake with a metadata flag instead of a missing
    one.** The attribute exists to cut warning noise from a dependency that has actually been checked; a
    package that sets the flag without exercising every code path under a real trimmed/AOT publish produces
    point 8's silent gap, with a marker now suppressing the one signal (the publish warning) that would have
    caught it.
36. **`EnableAotAnalyzer`/`EnableTrimAnalyzer` run as ordinary build-time diagnostics, not only at publish, and
    turning them on in every build is what makes point 3's "CI has to run the publish" affordable rather than
    the only line of defence.** A warning from either appears on `dotnet build` like any compiler
    diagnostic — under `TreatWarningsAsErrors` (this block's guardrail) it fails the ordinary CI build a
    pull request already runs, catching the regression on the commit that introduced it instead of on the
    next scheduled publish.
37. **The framework annotating its own APIs for trim/AOT compatibility narrows where the next warning comes
    from without narrowing whose job it is to read it.** .NET 10 removed a large share of the IL2xxx/IL3xxx
    warnings that used to originate inside ASP.NET Core's own minimal-API and serialisation code paths — a
    warning that still appears after upgrading now overwhelmingly traces back to application code or a
    third-party dependency, not the application having become AOT-safe by association; point 8's "read,
    don't assume" applies to the framework's own compatibility as much as to any package's.
38. **A generic method reached through `UnsafeAccessorAttribute` (§4.37) behaves differently for a closed
    generic than for an open one, and that difference changed between .NET versions without changing the
    attribute's syntax.** A private member accessed on a specific closed instantiation (`Repository
    <Order>` rather than `Repository<T>`) resolves against that exact closed type, so code written and tested
    against one .NET version's resolution rules is a compatibility check worth rerunning after an SDK
    upgrade — point 3's "don't assume the last release's behaviour still holds", triggered by a runtime
    version bump instead of a publish.
39. **A trimmed build's IL2xxx warning and an AOT build's IL3xxx warning name different failure classes even
    when they point at the same line, and fixing the code path for one does not necessarily fix it for the
    other.** Points 1–6 and 17 are the trimming class — a member removed because nothing visible referenced
    it; points 7, 9 and 16 are the codegen class — an operation Native AOT cannot perform at all, present or
    absent from the trimmed output. A warning "fixed" by keeping the member alive (point 11's rooting) answers
    the first class and leaves the second exactly as broken — point 28's list read as two checklists, not
    one.
