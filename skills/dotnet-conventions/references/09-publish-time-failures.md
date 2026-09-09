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
