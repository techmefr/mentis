# § 11 — Build hygiene: shared settings and package versions

> Section 11 of `skills/dotnet-conventions`. Read it when a project file, a shared build file or a package
> reference changes, or when the same property or version appears in several projects.

1. **A build setting lives at one level of inheritance.** A property that three or more project files repeat
   (nullable context, warnings as errors, implicit usings, analyzers, package metadata) moves to a shared
   file at the repo or source-folder root. The project files keep only what is unique to them.
2. **Two shared files, two jobs.** The props file is imported before the project, so a project can override
   what it sets: defaults, metadata, common analyzer references go there. The targets file is imported after
   the SDK and the project, so it has the last word: custom targets and any value that depends on a property
   the SDK defines go there.
3. **A condition on the target framework does not work in a props file for a single-target project**: the
   property is still empty when the file is evaluated, and the condition silently never matches. Put such
   properties in the targets file; conditions on items and targets are not affected.
4. **Only the nearest shared file is imported automatically.** To chain a source-folder file to the repo file,
   the inner file imports its parent at the top, guarded by an existence check. Without it, the repo-level
   settings vanish for that folder with no error.
5. **Package versions are central.** One central file enables central package management and lists every
   version once; a project reference then carries no version. A version written inline in a project file is a
   bypass and is flagged, since two projects can then resolve the same package to different versions.
   Analyzers that every project needs can be declared once as global references there.
6. **Analyzer and build-tool packages are marked private** so they do not flow to consumers of a library as
   transitive dependencies.
7. **Use the built-in build tasks, not a shell command in an exec task.** Make-directory, copy and delete
   tasks are cross-platform, incremental and logged; an exec task is opaque and breaks on another operating
   system. Paths are built from the file's own directory or a discovered root, never an absolute path.
8. **Quote both sides of every build condition** (`'$(Configuration)' == 'Release'`): an unquoted empty value
   makes the condition wrong or a parse error.
9. **Do not restate SDK defaults, and do not list source files by hand in an SDK-style project.** Restated
   values hide the real overrides and pin an old default; hand lists cause merge conflicts and missed files.
   Opt out with a remove entry. (A project in a language that compiles in declaration order lists files in
   dependency order and is the exception.)
10. **A target does one job.** A long target mixing unrelated steps cannot be skipped incrementally or
    extended; split it and give each target its inputs and outputs.
11. **When a setting is not where you think, preprocess the project** (the build command's preprocess switch
    writes the fully merged project with every import expanded) rather than guessing which file wins.
12. A repository-level build-arguments file can fix the shared command-line flags (parallelism, console
    logger options) so local and CI builds agree.

**Checks, by command:** search project files for an inline package version when a central file exists, for
the same property block in several projects, for exec tasks calling copy, delete or mkdir, for absolute
drive paths, and for unquoted conditions.
