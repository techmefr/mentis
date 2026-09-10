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
   The member is removed, so the symptom is a missing type or a missing method rather than a missing
   feature, and it names something you did not write. Either annotate the boundary so the trimmer keeps
   what the reflection needs, or don't reflect there — the second is usually the right call in application
   code.
3. **The publish is part of the build, and CI has to run it.** Building proves nothing about a trimmed or
   single-file publish, and the warnings the publish emits are the review surface: each one names a place
   where the analysis could not prove the code survives. A baseline of them is a list of things that will
   throw in production, which is the same trade as any suppressed analyser finding (this block's
   guardrail).
4. **Single-file and AOT change what the process knows about itself.** The assembly's location comes back
   empty, so anything resolving a path relative to it silently reads from the process's working directory
   instead — a configuration file, a template, a certificate. Ask the host for the content root or the
   application's base directory, which is what §6.3 means by not hardcoding a path.
5. **Test what you ship, at least once.** A suite that only ever runs against the ordinary build exercises
   a different code path from the published artefact: the tests are green and the binary throws. Where a
   trimmed or AOT publish is a real target, one smoke test runs the published thing and hits one endpoint
   that serialises — that single test is what turns every rule above from advice into a check.
6. **A publish warning suppressed is the root cause left in place, not removed.** Silencing a trim or AOT
   warning states that the code path is compatible when the analysis could not prove it — the warning was
   the one signal that the throw hadn't been found yet, and suppressing it deletes the signal, not the bug.
   Fix the code path or accept the limitation explicitly (a documented fallback, a feature disabled in this
   publish mode); never silence the warning to make the count go down.
7. **Native AOT cannot generate code at run time, which is a different failure from trimming.** Anything
   building a new type, compiling an expression tree, or emitting IL at run time (a dynamic proxy, a
   hand-rolled expression compiler, some serializers' fallback path) has nothing to fall back to under AOT —
   it isn't trimmed away, it never worked to begin with. This is checked earlier than trimming: before
   adopting a library for an AOT target, confirm it publishes an AOT-compatibility statement rather than
   discovering the gap in the published binary.
8. **A third-party package's own trim/AOT compatibility is not assumed, it's read.** A package with no
   compatibility annotations can still build and pass tests locally while depending on reflection the
   trimmer cannot see; the project's publish warnings are where that dependency's own gap surfaces, one
   release behind whether the package's maintainers have caught up.
9. **`RegexOptions.Compiled` asks the runtime to emit IL for the pattern, which Native AOT cannot do** — the
   same failure as point 7, wearing a different name. It does not throw: the regex still runs, silently
   falling back to the interpreted engine, so the only symptom is a slower match nobody flagged as a
   regression because nothing failed. The source-generated regex (`[GeneratedRegex]` on a partial method)
   compiles the pattern at build time instead, which is the same trade this section keeps making — turn a
   run-time capability into a build-time artefact so the trimmer and the AOT compiler can both see it.
10. **A method that reflects on its own account has to say so, or its caller finds out at publish instead
    of at the call site.** `RequiresUnreferencedCodeAttribute` on a method that walks a type's members, and
    `DynamicallyAccessedMembersAttribute` on a parameter or generic type whose members that walk depends on,
    move the warning from "somewhere in the published output" to "at the line that calls this method" —
    which is the difference between a warning the author of the reflection sees and one the author of a
    call three layers away sees, if they ever publish trimmed at all. Framework and library code carries
    these annotations for exactly this reason; application code that reflects across a public boundary
    needs the same discipline or it has exported point 2's problem to whoever depends on it.
11. **Explicitly rooting an assembly cancels trimming for it, and that trade is not free.** A
    `TrimmerRootAssembly` (or an ILLink descriptor doing the same by hand) tells the trimmer to keep
    everything in that assembly reachable or not — which silences the warnings from a library with no
    trim annotations, but also keeps every unused type and method the trimmer would otherwise have removed,
    for that one assembly. It is the right escape hatch for a dependency you cannot fix and cannot avoid;
    it is the wrong first response to a warning, because it hides the specific member that was actually a
    problem behind "keep all of it."
12. **ReadyToRun and Native AOT solve different problems, and enabling one while expecting the other's
    guarantees is how this section's failures arrive as a surprise.** R2R precompiles IL to native code for
    faster startup while keeping the JIT, reflection and the full framework available — none of points 1–11
    apply to an R2R publish, because nothing was trimmed and nothing lost the ability to generate code.
    `PublishAot` removes the JIT entirely and pulls trimming in as a consequence; choosing it for "faster
    startup" without meaning to take on the trimming and no-codegen contract is the usual way a team
    discovers this whole section in production instead of in the release notes.
13. **Configuration binding reflects over the options type's properties, the same as any other
    reflection-based serialisation.** `IConfiguration.Bind` or `services.Configure<T>` populating a POCO
    walks its properties by name at run time; under trimming, a property the trimmer could not prove was
    read stays unset rather than throwing — the options object binds to defaults for exactly the members
    nobody explicitly kept, and the failure looks like a wrong value rather than a missing one. The
    configuration-binding source generator (`EnableConfigurationBindingGenerator`) produces a binding method
    per options type at build time, which puts the same list problem point 1 describes for serialisation
    under the compiler's eye instead of the trimmer's guess.
14. **Globalization-invariant mode is a separate switch from trimming, and it silently changes what a string
    comparison means rather than throwing.** With `InvariantGlobalization` enabled, every culture-aware
    comparison and case conversion falls back to ordinal behaviour regardless of the `CultureInfo` or
    `StringComparison` the caller actually asked for — a sort order or an uppercasing rule that depended on
    a specific culture (a Turkish `i`, an accent-insensitive sort) quietly changes shape in the published
    binary while the same code produced the expected order in every local run against the full ICU data.
    It shrinks the published size meaningfully (tens of megabytes in a container image), which is exactly
    why it gets turned on for the wrong reason on a service that does, in fact, localise something.
15. **Constructing any culture other than the invariant one throws once invariant mode is on, and it throws
    at the call site, not at startup.** `CultureInfo.GetCultureInfo("fr-FR")` or setting
    `CurrentCulture` to a named culture raises an exception the moment that line runs, which in practice
    means the first request that needs it, in production, after the switch was flipped for an unrelated
    size or startup-time win described in point 14 — the two failures travel together and are diagnosed
    separately unless whoever enabled the mode also grepped for named-culture use first.
16. **Native AOT does not support runtime marshalling for COM or Windows Runtime interop, which is a third
    kind of "invisible until publish" alongside reflection and codegen.** `[ComImport]` types, apartment-
    threaded COM objects and WinRT activation all depend on infrastructure Native AOT does not carry, so
    code exercising them builds and runs under the ordinary JIT and fails only in the trimmed, ahead-of-time
    compiled artefact — the same shape of gap as point 7's dynamic codegen, but for a dependency most
    projects only discover through a transitive package that happened to lean on COM for one code path.
17. **A source generator that emits attributes read by the trimmer only helps if it runs before the
    trimmer sees the code, and a generator disabled or misconfigured for one build configuration fails
    silently.** The JSON, configuration-binding, regex and logging source generators this section already
    relies on (points 1, 9, 13) are opt-in per project and can be quietly absent from a `Release` or
    publish-specific build configuration that never got the same `<PropertyGroup>` as `Debug` — the
    compile-time list they were meant to provide reverts to the reflection path they exist to replace, with
    no error, because reflection still compiles.
18. **`PublishReadyToRun` is restricted to publishing for the runtime identifier of the machine doing the
    publishing, unless cross-OS/architecture R2R is explicitly supported for that pair.** A CI machine that
    publishes R2R for a different target RID than its own silently produces IL-only output instead of the
    precompiled native code the setting promised — the artefact still runs, just with the JIT cold-start
    cost R2R exists to remove, and nothing in the build log calls this out as a failure because, by the
    letter of the setting, it isn't one.
19. **Blazor WebAssembly's default trimmer granularity is partial, and a library counted on to shrink only
    trims if it opted in.** Only framework libraries and packages that explicitly declare trimming support
    are trimmed by default; a third-party package with no trim annotations ships whole into the WASM payload
    regardless of how much of it the app actually calls, which is a silent size regression rather than a
    build failure — nothing reports "this package could have been smaller," the published bundle is just
    bigger than the code that uses it would suggest.
20. **A feature switch read through `AppContext.GetSwitch`/`AppContext.SetSwitch` is how the trimmer removes
    an entire code path at publish time, and setting the switch anywhere but the project file arrives too
    late to help.** The runtime libraries gate optional subsystems (globalization variants, diagnostics,
    some serializer fallbacks) behind switches the linker can evaluate at trim time when they're declared as
    `RuntimeHostConfigurationOption` MSBuild items — a switch instead flipped in `Main` at startup still
    changes behaviour, but the trimmer already made its keep/remove decision before that line ran, so it
    cannot shrink a path the switch turns off dynamically.
21. **A satellite resource assembly for a culture nobody publishes for is still built unless
    `SatelliteResourceLanguages` says otherwise.** Every culture a referenced package ships localised
    strings for gets its own resource DLL copied into the output by default, which is dead weight for an app
    that only ever runs in one language — restating the languages actually shipped is the same trade as
    point 14's invariant-globalization switch, one config line instead of a dozen unused assemblies riding
    along in every publish.
22. **A source generator that reads a project file, an embedded resource or another source file at compile
    time works from the compiler's snapshot, not from the file on disk when the published binary runs.** A
    generator that reads a `.json` or `.resx` sibling to bake its content into generated code has already
    finished by the time the application starts, so a config file edited after publishing without a rebuild
    changes nothing the generator produced — that is expected for a compile-time artefact, but it looks
    exactly like point 4's "reads from the wrong place" failure to whoever expected editing the deployed file
    to take effect, so a generator built this way needs the boundary stated once, near the generator.
23. **`DynamicDependencyAttribute` names exactly the member a trimmer-invisible call site needs kept, and is
    the narrower alternative to point 11's whole-assembly root.** Where a single method is reached through a
    string-built name — `Activator.CreateInstance` on a type name from configuration, a reflection call the
    trimmer genuinely cannot follow — the attribute states which member has to survive trimming without
    exempting the rest of the assembly from it, which keeps the warning point 10 describes scoped to the one
    place that actually needs the escape hatch instead of hiding an entire library behind it.
24. **MVC controllers are not a Native AOT target at all, which is a different failure from anything
    trimming produces on its own code that does run.** `AddControllers`, view compilation and the classic
    model-binding pipeline lean on reflection and runtime code generation deeply enough that the framework
    doesn't attempt to make them AOT-safe — the AOT project template ships minimal APIs only, and a project
    that adds MVC to an AOT-published host isn't looking at a warning list to work through, it's outside what
    the platform supports. The decision to target Native AOT is a decision to build on minimal APIs, made
    before the first controller is written, not discovered at the first publish.
25. **The Request Delegate Generator turns a minimal API's route handlers into source-generated code at
    compile time, and it only runs once trimming or AOT is actually turned on for the project.** A handler
    that works under the ordinary JIT build is compiled through the generator's own code path the moment
    `PublishAot` (or trimming) is enabled — which means a handler shape the generator can't express (one
    built from a runtime-computed delegate, for instance) surfaces as a build-time diagnostic from the
    generator rather than a run-time trim warning, the same shift from run time to build time this whole
    section keeps describing, just for routing instead of serialisation.
26. **A pre-compiled EF Core query (point 21's compiled model taken one step further) needs the same
    "regenerate when the model changes" discipline, and skipping it produces a stale artefact that still
    builds.** Pre-compiled queries generate the SQL and materialisation code for a specific LINQ expression
    at build time so nothing about executing it depends on reflecting over the model at run time — which is
    exactly what makes it viable under trimming and AOT, and exactly why a query changed without
    regenerating the artefact keeps compiling against the old generated code instead of failing, silently
    running the previous version of the query against the current model.
27. **A container base image chosen for size (a "chiseled" or distroless variant) can be missing pieces an
    AOT-published binary still calls into, and the gap is invisible until the container actually starts.**
    Native AOT removes the managed runtime's own dependency on globalization and TLS libraries being present
    as .NET components, but the published binary still links against native ICU, OpenSSL or equivalent
    platform libraries at the OS level — a minimal image trimmed of those shared libraries builds and starts
    the ordinary framework-dependent image fine while the AOT one crashes at startup with a missing native
    library, because the two publish modes depend on the host image differently and a size optimisation
    tuned for one silently breaks the other.
28. **`PublishTrimmed` without `PublishAot` still runs the IL trimmer alone, and every failure mode in this
    section that comes from trimming (points 1, 2, 8, 10, 11, 17, 19, 23) applies to it independently of
    Native AOT's no-codegen restriction (points 7, 9, 16).** A project can be trimmed and still keep the JIT
    and reflection-based code generation available, which means point 12's distinction cuts a third way, not
    two: R2R changes nothing this section warns about, trimming alone brings the "invisible member removed"
    class of failure without the "cannot generate code at all" class, and full AOT brings both — treating
    "trimmed" and "AOT" as one setting when reasoning about which of this section's twenty-plus points
    actually applies is how a team fixes the wrong half of the list.
29. **A file-based app (`dotnet run app.cs`, .NET 10) publishes Native AOT by default, which means a script
    nobody meant to harden against this section inherits every one of its rules the day it's published rather
    than merely run.** The single-file entry point that felt like a throwaway script during `dotnet run`
    reflects, serialises or reads a culture the same as any other code, and `dotnet publish` on it turns on
    `PublishAot` without being asked — so the first sign of points 1, 7 or 15 applying at all is the publish
    step itself, for a file that was never reviewed as an AOT target because it never looked like one.
30. **Packing a .NET tool as self-contained, trimmed or Native AOT (.NET 10) exposes the same failures this
    section already describes, the day the packaging choice changes rather than the day the code does.** A
    global tool authored against the ordinary framework-dependent build can be packed several different ways
    without a source change; switching the pack target to trimmed or AOT surfaces points 1, 2 and 7 for code
    that compiled and ran identically under every previous packaging choice — the failure is entirely in the
    publish configuration, which is exactly why point 3's rule to run the actual publish in CI has to cover
    every packaging variant that ships, not just the default one.
31. **The AOT and trim analyzers catch more of this section at build time than they used to, and that
    coverage is still opt-in per project, per warning wave — point 3's rule about running the publish is not
    superseded by better tooling.** A newer SDK's diagnostics flag a wider slice of points 1, 2 and 7 during
    an ordinary build without a publish step at all, which narrows the gap between "compiles" and "publishes
    safely" but does not close it — a warning wave introduced after a project's `TreatWarningsAsErrors`
    baseline was set can sit unenforced, silently, the same way point 6 already warns a suppressed individual
    warning does.
32. **The feature-switch attribute model (.NET 9) declares a switch's trim behaviour in the same place as its
    name, which point 20's bare `AppContext` switch left to be documented separately or not at all.** A
    library author states, next to the switch itself, both the friendly configuration name an app sets in its
    project file and what the trimmer should assume when it's off — so a consumer reading the switch's own
    declaration knows whether flipping it actually removes code (point 20's condition for the trimmer to act
    on it) without cross-referencing separate documentation that can drift from what the linker configuration
    actually says.
33. **Hybrid globalization mode is a third point on the axis points 14 and 15 already describe as two, not a
    safer version of either.** Full ICU keeps every culture-aware behaviour; invariant mode (point 14) flattens
    all of it to ordinal; hybrid keeps culture-aware casing and comparison but still throws or falls back for
    the operations that need the full ICU data files it deliberately doesn't ship — so code exercising exactly
    the subset hybrid mode omits fails the same way point 15 describes for invariant mode, just for a smaller
    and less obviously-invariant-shaped set of operations, which makes the gap easier to miss in testing
    precisely because most culture-aware code keeps working under it.
34. **`[DllImport]` depends on the runtime's own marshalling engine to build the interop stub at load time,
    which Native AOT does not carry — `[LibraryImport]` generates that same stub at compile time instead, the
    same list-as-build-artefact trade point 1 makes for serialisation.** A `[DllImport]` method that worked
    under the ordinary JIT throws at the call site under AOT with no build-time signal that it would, because
    nothing about the attribute declares which marshalling shapes it needs ahead of time; the source-generated
    partial method surfaces an unsupported parameter or return shape as a compiler error on the method
    declaration itself, before publish, which is the difference point 3's "publish warnings are the review
    surface" is arguing for one layer earlier.
35. **`IsAotCompatible` (.NET 10) is an assembly-level claim a package makes about itself, and reading it as
    proof rather than as a starting point repeats point 8's mistake with a metadata flag instead of a missing
    one.** The attribute exists to cut warning noise from a dependency that has actually been checked, which
    only helps once something checked it — a package that sets the flag without exercising every code path
    under a real trimmed/AOT publish produces the same silent gap point 8 describes for a package with no
    annotation at all, just with a marker now actively suppressing the one signal (the publish warning) that
    would have caught it.
36. **`EnableAotAnalyzer`/`EnableTrimAnalyzer` run as ordinary build-time diagnostics, not only at publish, and
    turning them on in every build is what makes point 3's "CI has to run the publish" affordable rather than
    the only line of defence.** A warning from either analyser appears on `dotnet build` the same as any other
    compiler diagnostic — under `TreatWarningsAsErrors` (this block's guardrail) it fails the ordinary CI build
    a pull request already runs, well before a dedicated trimmed/AOT publish job exists to catch it, which
    catches the regression on the commit that introduced it instead of on the next scheduled publish.
37. **The framework annotating its own APIs for trim/AOT compatibility narrows where the next warning comes
    from without narrowing whose job it is to read it.** .NET 10 removed a large share of the IL2xxx/IL3xxx
    warnings that used to originate inside ASP.NET Core's own minimal-API and serialisation code paths — which
    means a warning that still appears after upgrading is now overwhelmingly likely to trace back to
    application code or a third-party dependency rather than to the framework, not that the application has
    become AOT-safe by association; point 8's "read, don't assume" applies to the framework's own compatibility
    exactly as much as to any package's.
38. **A generic method reached through `UnsafeAccessorAttribute` (§4.37) behaves differently for a closed
    generic than for an open one, and that difference changed between .NET versions without changing the
    attribute's syntax.** A private member accessed this way on a specific closed instantiation (`Repository
    <Order>` rather than `Repository<T>`) resolves against that exact closed type, so code written and tested
    against one .NET version's resolution rules for the generic case is a compatibility check worth rerunning
    after an SDK upgrade — the same "read the publish warnings, don't assume the last release's behaviour still
    holds" discipline point 3 already asks for, now triggered by a runtime version bump instead of a publish.
39. **A trimmed build's IL2xxx warning and an AOT build's IL3xxx warning name different failure classes even
    when they point at the same line, and fixing the code path for one does not necessarily fix it for the
    other.** Points 1–6 and 17 are the trimming class — a member removed because nothing visible referenced it;
    points 7, 9 and 16 are the codegen class — an operation Native AOT cannot perform at all, present or absent
    from the trimmed output. A warning suppressed or "fixed" by keeping the member alive (point 11's rooting,
    for instance) answers the first class and leaves the second exactly as broken, which is point 28's
    twenty-plus-point list read as two separate checklists rather than one.
