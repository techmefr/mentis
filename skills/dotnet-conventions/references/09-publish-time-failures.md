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
