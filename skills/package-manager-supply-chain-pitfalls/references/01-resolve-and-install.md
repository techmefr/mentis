# package-manager-supply-chain-pitfalls §1 — Resolve and install

> Section 1 of `skills/package-manager-supply-chain-pitfalls`. Read it when an install configuration, a CI
> install step or an update policy changes. Versions and option names are as stated by the sources read on
> 2026-10-15 (lirantal/npm-security-best-practices at `749e599`, bodadotsh/npm-security-best-practices at
> `24fb07d`) and are not verified against the package managers themselves; confirm each against the
> installed version before writing it into a file.

1. **Block git sources.** A dependency written as a git URL bypasses the registry's checks, and the
   repository it fetches can ship its own `.npmrc` that re-enables lifecycle scripts, undoing `ignore-scripts`
   silently; its contents can also change at any time, because branches, tags and commits can be
   force-pushed. The source's npm setting is `allow-git`, available from npm CLI 11.9.0 (npm changelog; the source said 11.10.0), with three values:
   `all` (the default in npm 11, allows any git dependency; the npm 12 release notes change the default to `none`), `none` and `root` (only your own root `package.json`).
   Setting it to `none` (or `root` if you need one) is a configuration change, not a code change, so it
   belongs in the committed `.npmrc` and in CI.
2. **Block exotic sources below the top level.** pnpm has no direct equivalent of `allow-git`; the source
   says pnpm 10.26 and later offers `blockExoticSubdeps` (default true per the pnpm settings page), which lets only direct dependencies use git
   repositories or tarball URLs and requires every transitive one to come from the registry, local paths,
   workspace links or trusted GitHub repositories. A clean lockfile does not prevent a transitive
   dependency from pointing at such a source.
3. **A lockfile is input, so a pull request can inject into it.** The source describes the attack: a
   contributor edits `package-lock.json` or `yarn.lock` to add a package, or changes the `resolved` URL of an
   existing one and sets the integrity hash to match, so the next install fetches code from a host they
   control. `lockfile-lint` validates a lockfile against a policy: allowed hosts, HTTPS only, allowed URI
   schemes, that the resolved URL matches the package name, and that integrity uses SHA-512. Run it in CI
   on every change to a lockfile. The source's example runs it as a `preinstall` script; own guidance:
   run it as its own CI step before the install, because a script that the install policy disables, or a
   hostile change to the same `package.json`, cannot be the thing that guards the install. The source
   says it did not support Bun's lockfile formats, and that pnpm is not susceptible in the same way because
   it keeps no editable tarball sources, so check each for the lockfile you use.
4. **Install from the lockfile and fail when it disagrees.** The source's frozen commands are `npm ci`,
   `yarn install --immutable --immutable-cache`, `pnpm install --frozen-lockfile`,
   `bun install --frozen-lockfile` and `deno install --frozen`. The npm documentation confirms `npm ci` exits with an error when the two disagree, never writes either file, and deletes `node_modules` first; it also still runs install scripts unless told not to (npm `ci` page, read 2026-10-20), so a frozen install is not a scripts-off install. A plain `npm install` repairs a lockfile
   that does not match `package.json`, so the build gets versions nobody reviewed. Commit the lockfile
   for the manager you use. When a lockfile has a merge conflict, the second source says deleting it is not
   necessary and can upgrade ranged dependencies unexpectedly; check out the target branch's lockfile and
   run the install again.
5. **Never update blindly.** The source lists `npm update`, `npx npm-check-updates -u`, `pnpm update`,
   `yarn up` and `bun update` as anti-patterns when run without review: an automatic jump to the latest
   version is exactly the path a compromised release takes. Use update tooling that opens reviewable
   changes (`npx npm-check-updates --interactive`, Dependabot, Snyk, Renovate), and read the lockfile diff
   of each. The second source adds a warning that update bots can speed up delivery of malware when merged
   on green; the review rule is `skills/ci-workflow-hardening` §3.2.
6. **Know what runs at install time.** `ignore-scripts=true` disables every lifecycle script, including your
   own project's and every dependency's, with no per-package exception. pnpm disables dependency scripts by
   default from version 10 and lets you allow named packages: the source names `onlyBuiltDependencies` and
   `ignoredBuiltDependencies`, replaced from pnpm 10.26 by one map, `allowBuilds`, and `strictDepBuilds`
   (pnpm 10.3 and later) makes an install fail when a dependency wants to run a script that is not
   allowed. The pnpm settings pages confirm these: unlisted packages are not allowed to build by default, `strictDepBuilds` defaults to true (otherwise it only warns), `dangerouslyAllowAllBuilds` exists and defaults to false, and the two older lists were removed in pnpm 11 in favour of `allowBuilds` (pnpm settings pages, read 2026-10-20). The second source describes an npm `allowScripts` setting, and says that from npm 12 it defaults
   to false, with `ignore-scripts` taking precedence when both are set. The npm configuration page (11.21 view) confirms the setting and the precedence: `allow-scripts` is for one-off and global runs, project policy goes in the `allowScripts` field of `package.json` or `.npmrc`, a project-scoped install with the flag is an error, `--ignore-scripts` and the dangerous allow-all flag override it, and `strict-allow-scripts` makes an uncovered dependency with scripts fail the install; the npm 12 default was not found on any page.
   Allow scripts by package and version, and treat each entry as a decision
   (`skills/security-hardening` §4.11).
7. **A trust policy catches a package whose publisher evidence got worse.** Per the source, pnpm 10.21 and
   later has `trustPolicy: no-downgrade` (off by default; it compares by publish date, not by version number, per the pnpm settings page, read 2026-10-20), which refuses a version whose publishing trust is weaker than an
   earlier release of the same package, an early sign of a taken-over account. The trust levels it
   recognises, strongest first: a trusted publisher (OIDC from CI), a provenance attestation, a registry
   signature, no evidence. `trustPolicyExclude` lists packages or versions to let through, and
   `trustPolicyIgnoreAfter` (pnpm 10.27 and later, in minutes) ignores the check for packages published
   longer ago than that, for old packages that predate provenance. Keep the exclude list short and
   reviewed.
8. **A short cooldown and an exception for fixes.** The Dependabot and uv delay is
   `skills/ci-workflow-hardening` §3.1. For the package managers themselves, the sources name npm
   `min-release-age` (npm 11.10.0 and later, given in days) and pnpm `minimumReleaseAge` (pnpm 10.16 and
   later, in minutes, with `minimumReleaseAgeExclude`, which takes patterns from 10.17 and exact versions from 10.19; it covers transitive dependencies too, per the pnpm page). npm also has `min-release-age-exclude`: it exempts only the named package, whose own dependencies still follow the age rule, and an install errors when no eligible version exists (npm configuration page); the second source says pnpm 11 defaults it to one
   day. Security fixes should not wait out the window: the first source's answer is `pnpm audit --fix`,
   which keeps the policy but adds a per-package exclusion for the version that fixes a vulnerability, and
   Renovate's support for the same policy. Record each exclusion with its advisory.
9. **`npx` and `dlx` run unpinned code with your credentials.** The source's point is that `npx` resolves,
   downloads and executes a package in one step, with no lockfile and no cooldown, so a compromised release
   runs on the next invocation; this matters most for tools that hold your filesystem or environment, such
   as MCP servers and formatters launched through it. The source's fix is to install the tool once in a
   dedicated workspace with a lockfile, then run it with `--include-workspace-root --workspace <dir> --no
   --offline <package>`, so `--no` refuses to download and `--offline` forbids the network. Update by
   running `npm update` in that workspace and reading the lockfile diff before the next run. The same
   pattern goes into a tool's configuration file in place of the bare `npx` command.
10. **Reduce what can be attacked.** Each dependency adds its own tree; both sources say to prefer built-in
    platform features where they are enough and to remove what is unused, which is
    `skills/security-hardening` §4.12 for the decision. Own guidance: put the removal in the same pull
    request as the feature that made the dependency unnecessary.
