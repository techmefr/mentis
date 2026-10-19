---
name: dotnet-msbuild-and-nuget-publish-pitfalls
description: "Use when writing or reviewing .csproj, Directory.Build.props or custom MSBuild targets, ProjectReference metadata, trimming or AOT warnings, or a NuGet publish workflow: Exec versus built-in tasks, condition quoting, PrivateAssets, properties conditioned on the target framework, duplicate project instances, never suppressing IL warnings, and trusted publishing."
---

# dotnet-msbuild-and-nuget-publish-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for .NET build files and the workflow that ships the package. The premise:
**an MSBuild file that evaluates cleanly on the author's machine can be wrong in three quiet ways: a property that
is empty at the moment its condition is read, a project built twice under two identities that share one output
folder, and a warning silenced for the analyser but not for the linker.** None of them fails a local build.
Language-level C# rules are `dotnet-conventions`; supply-chain rules for CI workflows in general are
`ci-workflow-hardening`; test-side seams are `dotnet-testcontainers-and-time-seam-pitfalls`.

## When
- A `.csproj`, `.props`, `.targets` or `Directory.Build.*` file is added or changed, or a custom target is written.
- A `ProjectReference` carries metadata (`SetTargetFramework`, `ReferenceOutputAssembly`, `UndefineProperties`).
- A trimming, AOT or other IL warning appears and someone proposes to silence it.
- A workflow pushes a package to nuget.org, or an API key secret is still in use for it.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Project-file smells: Exec, conditions, paths, SDK defaults, PrivateAssets, shared settings, property timing | any project or props file is written or reviewed | [`01-project-file-smells.md`](./references/01-project-file-smells.md) |
| 2 | Duplicate project instances: forked MSBuild calls, `SetTargetFramework`, incompatible-framework references | a target calls the MSBuild task or a reference carries framework metadata, or a build fails with a file-in-use error | [`02-duplicate-instances.md`](./references/02-duplicate-instances.md) |
| 3 | IL warnings and trusted publishing | a trim or AOT warning is on screen, or a NuGet push is added or migrated | [`03-il-warnings-and-trusted-publishing.md`](./references/03-il-warnings-and-trusted-publishing.md) |

## Output / checkpoint
Every finding names the file and the element, says whether it is a defect or a style preference (a backslash in an
imported path is the second, a backslash in an `Exec` command is the first), and gives the replacement. A claim
that a build "works" without naming the operating system and the invocation is not verified. A publish change is
not finished until the user has created the policy on nuget.org and one publish succeeded.

## Guardrails
- Never silence an IL warning with a pragma or `UnconditionalSuppressMessage` to get a build green (part 3).
- Never inject a framework into a reference to a single-targeting project that already targets it (part 2).
- Never condition a property on `$(TargetFramework)` in a `.props` file (part 1).
- Never delete the old API key secret before a trusted-publishing publish has succeeded (part 3).
- No block and no agent installs a tool or a package: the blocks name it and the user installs it
  (`CONVENTIONS.md`).
- Versions: rules come from the .NET skills repository at the commit stamped in `references/origin.md`. Nothing
  was built, packed or published while writing this block.

## Origin
Rewritten from the dotnet/skills repository (MIT: the MSBuild anti-pattern catalogue, the trimming-compatibility
skill and the NuGet trusted-publishing skill), read 2026-10-16. Overlaps with `skills/dotnet-conventions` (2026-10-19); cross-referenced, not merged. 🟡: never run by us;
open points are in [`references/origin.md`](./references/origin.md).
