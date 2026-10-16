# dotnet-msbuild-and-nuget-publish-pitfalls §1 — Project-file smells

Source: the dotnet/skills MSBuild anti-pattern catalogue (MIT, commit 6364668, read 2026-10-16), rewritten. Where
a point is not in the catalogue it says "own guidance".

## 1.1 Use built-in tasks, guard what is platform-specific
1. **Prefer the built-in task over `Exec` for file operations.** `MakeDir`, `Copy`, `Delete`, `Move`,
   `WriteLinesToFile` and `Touch` are cross-platform, take part in incremental builds and log structurally;
   an `Exec` running `mkdir`, `copy` or `del` is opaque to MSBuild and breaks on the other operating system.
2. **Prefer property functions over `Exec` for string and path work.** `$(Version.Replace('-preview', ''))` or
   `$([MSBuild]::NormalizeDirectory(...))` needs no shell and its result is already a property; capturing shell
   output back into a property is the slow, shell-dependent route.
3. **An `Exec` that only works on one operating system needs a condition** such as
   `!$([MSBuild]::IsOSPlatform('Windows'))` around the target, or it fails on the others.

## 1.2 Conditions and paths
1. **Quote both sides of `==` and `!=` with single quotes**: `'$(Configuration)' == 'Release'`. An unquoted side
   that is empty or contains a space evaluates wrongly or throws a parse error.
2. **No absolute paths in project files.** Build them from `$(MSBuildThisFileDirectory)`,
   `$(MSBuildProjectDirectory)`, `$([MSBuild]::GetDirectoryNameOfFileAbove(...))` or
   `$([MSBuild]::NormalizePath(...))`, so the file works on another machine, in CI and on another system.
3. **A backslash is a defect only where MSBuild does not normalise the path.** The catalogue's test: does the
   string flow through the evaluator (an `Import`, an item `Include`, a built-in task's file argument) or is it
   handed verbatim to something else (an `Exec` command line, a file written for another tool, a custom task
   calling file APIs directly)? The first is a style preference (forward slashes are still preferred in new
   code), the second breaks on Unix because the shell reads the backslash as an escape.
4. **Guard an `Import` only when the file is optional.** An unguarded import of a missing file fails with a
   confusing error, so wrap local-override or environment-specific imports in `Exists(...)`; a required import
   should fail fast and stays unguarded. A forwarding import inside a package's `build` or `buildTransitive`
   folder is a package contract, so resolve it against the packed layout before flagging it.

## 1.3 Do not restate what the SDK already does
1. **Properties equal to the SDK default are noise** and silently pin old behaviour if the default later
   changes: `OutputType` Library, `EnableDefaultItems`, a `RootNamespace` or `AssemblyName` equal to the project
   name. Keep only the non-default values.
2. **Do not list source files in an SDK-style project**: the SDK globs them, and an explicit list creates merge
   conflicts and silently misses new files. Use `Remove` or `Exclude` to opt out. The exception is F#: its
   compiler is order-dependent, so every file is listed in dependency order and a signature file sits directly
   before its implementation.
3. **A `Reference` with a `HintPath` into a `packages` folder is the old `packages.config` pattern**: it has no
   transitive resolution and no restore. Use `PackageReference`.
4. **Do not reference a project that an existing reference already brings in transitively**, unless you use its
   types directly; extra edges only blur the graph.

## 1.4 Packages and shared settings
1. **Analyzers, source generators, SourceLink packages, versioning tools and build-only tools take
   `PrivateAssets="all"`**, otherwise they flow to every consumer of your library as a transitive dependency.
2. **A property block repeated in three or more project files belongs in `Directory.Build.props`** at the
   repository or source root (nullable, warnings as errors, implicit usings in the catalogue's example).
3. **Different versions of one package across projects is version drift.** The catalogue's fix is Central
   Package Management through `Directory.Packages.props`; its conversion procedure was not read for this block,
   so follow the NuGet documentation for that step.
4. **A property set unconditionally in both the shared props file and a project is a silent last-write-wins.**
   Give the shared value a condition (`'$(OutputPath)' == ''`) so an override is deliberate.

## 1.5 Timing: props versus targets, evaluation versus execution
1. **Defaults go in `.props`, logic goes in `.targets`.** A `.targets` file is imported late, so a default set
   there may be read as empty by something that ran earlier.
2. **Never condition a property on `$(TargetFramework)` in a `.props` file.** A single-targeting project sets
   it in its own body, after the props file is read, so the condition silently never matches. Item and target
   conditions are safe there, because items and targets evaluate after all properties; the same property
   condition belongs in `Directory.Build.targets` or the project.
3. **No side effect during property evaluation.** A property function that writes a file or touches the network
   runs on every evaluation, including design-time evaluations by an IDE. Put it in a target.
4. **A custom target with no `Inputs` and `Outputs` runs on every build** and defeats incremental builds; give
   it both and register what it writes. Split a target that does several unrelated things so each step can be
   skipped on its own.
5. **Do not put an `Include` and an `Update` of the same item type in one item group**, because `Update` only
   sees items already in the set; use two groups.

## 1.6 Review shape
For a review request the catalogue asks for prioritised findings grounded in the supplied file, separating
confirmed defects from conditional risks and patterns that are already correct, with no edits unless the user
asked for fixes. Order by consequence: an unquoted condition, a side effect in evaluation, a `TargetFramework`
property condition in props and a forked instance (part 2) before duplication and style.
