# dotnet-msbuild-and-nuget-publish-pitfalls §2 — Duplicate project instances

Source: the dotnet/skills MSBuild anti-pattern catalogue, entries on forking an instance and on
`SetTargetFramework` (MIT, commit 6364668, read 2026-10-16), rewritten.

## 2.1 What a project instance is
1. **An MSBuild project instance is identified by its path plus its global properties.** Passing one extra
   global property to the MSBuild task creates a distinct instance of the target project.
2. **If that property does not change the output path, the two instances share `bin` and `obj`.** The graph
   already builds the project with no global properties; the forked one builds it again into the same folders,
   and in a parallel build both write the same files (debug symbols, `project.assets.json`, native-AOT
   intermediates). The symptom is "the process cannot access the file because it is being used by another
   process", often intermittent and retry-flaky.

## 2.2 Forking with the MSBuild task
1. **Do not make a project call the MSBuild task on itself with a flag such as `_IsPublishing=true`.** Set the flag
   as an ordinary property, run the publish target in the same instance through `DependsOnTargets`, and guard it
   with a captured copy of the original global value so that `dotnet publish` (which sets the flag as a global
   property) does not re-trigger the target in a loop.
2. **Do not make project A call Build or Publish on project B with a path-neutral property** either. Let B publish
   as part of its own build, reference it from A only to sequence the build (`ReferenceOutputAssembly="false"`),
   and read B's output.
3. **Extra global properties are fine when the output path encodes them**: `RuntimeIdentifier`,
   `TargetFramework`, `Configuration`, `Platform` each give the instance its own folders. If a path-neutral
   property is unavoidable, give that build its own intermediate and output path.

## 2.3 SetTargetFramework on a project reference
1. **`SetTargetFramework` injects `TargetFramework` as a global property.** It exists so a consumer can pick one
   framework of a multi-targeting project; each framework has its own folders, so it is safe there.
2. **On a single-targeting project, injecting the framework it already targets is path-neutral**, so it forks
   the same clash as 2.1. The catalogue notes that the reference protocol itself omits the property for a
   non-multi-targeting reference, and `SetTargetFramework` is what reintroduces it.
3. **Injecting a different framework into a single-targeting reference is a legitimate override**, because the
   output path changes.

## 2.4 References between incompatible frameworks
1. **When the two projects target incompatible frameworks, set both `SkipGetTargetFrameworkProperties="true"` and
   `ReferenceOutputAssembly="false"`.** The first bypasses the negotiation that would fail; the second stops the
   build from trying to consume an assembly it cannot reference.
2. **Stop the referencing project's own `TargetFramework` from leaking into a single-targeting reference.** With
   the negotiation bypassed nothing prevents it, and the reference then builds under the wrong framework. Either
   pin the framework with `SetTargetFramework` (needed for a multi-targeting reference) or strip it with
   `UndefineProperties="TargetFramework"`; use one or the other, not both.

## 2.5 Checking
The catalogue points to a separate skill that compares two evaluations of a project for a path-neutral
difference; it was not read for this block. Without it, compare the project's output path under both instances
by evaluating the properties for each, and treat equal paths with different global properties as the clash.
That evaluation advice is own guidance.
