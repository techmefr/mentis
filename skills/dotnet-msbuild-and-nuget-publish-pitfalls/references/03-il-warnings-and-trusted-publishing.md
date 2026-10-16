# dotnet-msbuild-and-nuget-publish-pitfalls §3 — IL warnings and trusted publishing

Sources: the dotnet/skills trimming and AOT compatibility skill and its NuGet trusted-publishing skill with its
workflow template (MIT, commit 6364668, read 2026-10-16), rewritten.

## 3.1 Never silence an IL warning
1. **A pragma that disables a warning hides it from the compiler's analyser only.** The linker and the AOT
   compiler still see the problem, so the code builds and then fails at trim or publish time.
2. **`UnconditionalSuppressMessage` is worse**: it tells both the analyser and the linker to ignore the
   warning, so the trimmer can no longer check safety and the failure moves to run time. The skill's position is
   that an error at build time is always preferable to a hidden one.
3. **Fix the cause instead.** Flow type information with `DynamicallyAccessedMembers` annotations, refactor the
   pattern that breaks the flow (boxing a `Type` into `object`, an untyped collection, a cast through an
   interface), or mark a method as fundamentally incompatible with `RequiresUnreferencedCode`,
   `RequiresDynamicCode` or `RequiresAssemblyFiles` so every caller has to acknowledge it.
4. **Work from the warnings, not from a survey of the code**: build with the analysers enabled, take one warning,
   open that file at that line, apply the fix, rebuild. The skill expects zero warnings on every target
   framework and a check that shared or linked source does not break a sibling project.

## 3.2 Trusted publishing to nuget.org
1. **Replace the long-lived API key with a short-lived token.** The publishing job requests an OIDC token
   (`id-token: write`, plus `contents: read` because setting permissions overrides the defaults), a login step
   exchanges it, and the push uses the key the login step outputs. Without the permission the login fails
   with a 403.
2. **The nuget.org policy needs the repository owner, the repository, the exact workflow file name and, when the
   job declares one, the environment.** Only the file name, no path; matching ignores case; the workflow's
   display name is not used. A private repository's policy is only temporarily active for seven days, until
   the first successful publish.
3. **The user creates the policy; the agent does not.** Do not run a publish or touch old secrets before the
   user confirms it exists. Drafting the workflow file earlier is fine.
4. **The login user is the nuget.org profile name, not an email address.** Keep it in an environment secret.
5. **Order matters**: the token is valid for about an hour, so run the login step right before the push, not
   early in a long job.
6. **Make the push idempotent with `--skip-duplicate`**, because a package id and version cannot be reused and a
   re-run of the same version otherwise fails.
7. **Trigger on a version tag and check the tag against the project version** before packing, so a mistyped tag
   fails early. Keep the CI workflow (build and test) separate from the publish workflow, since CI does not need
   the token permission.
8. **Pack locally first** (`dotnet pack` into an artifacts folder) and inspect the package before the first
   publish: a wrong first publish burns a version number and package ids are permanent.
9. **A re-run replays the workflow file of the original commit**, not the current branch. When a re-run fails on
   a release conflict, delete the conflicting release after confirmation and re-run; do not delete and re-create
   the tag. The skill advises omitting the release-creating step from the publish job, because a failure there
   blocks the push.
10. **Do not delete the old API key secret until a trusted publish has succeeded.** Removing it is one-way.
11. **If an auth or infrastructure step still fails after one fix attempt, stop and ask the user** rather than
    looping.
12. **Scope**: the flow is for nuget.org on a hosted workflow service named in the skill (GitHub Actions); a private
    feed or Azure Artifacts is not covered by it.
