# ci-workflow-hardening §3 — Dependency supply chain

The lockfile pins what you resolved (`security-hardening` §4.9), but three things still decide what lands in
your build: how soon you adopt a new release, who or what opens the pull request that adopts it, and whether
the audit looks at your dependencies or at itself.

## 3.1 A delay before adopting a new release
1. **Malicious releases are usually found and pulled within a day or two**, so a short wait before
   adopting a new version removes a class of attack for the price of getting fixes a little later. Keep it
   short (a few days) and expect fixes for known vulnerabilities to be slower than they could be.
2. **Dependabot: set `cooldown` in each `updates` entry.** `default-days` sets the window; the
   documentation says the default cooldown does not apply to security updates, which is the property that
   makes this the right layer for the delay. The bump-type options (`semver-major-days` and the others)
   exist only for some ecosystems, so check the ecosystem table before using them. `include` and `exclude`
   scope it by name; `exclude` wins.
3. **uv: `exclude-newer` in `[tool.uv]` limits resolution to files uploaded before a point in time**, as an
   RFC 3339 timestamp or a duration such as `3 days`; durations are fixed numbers of seconds and calendar
   units like months are rejected. The comparison is on the upload time of each file, not the release date.
   `exclude-newer-package` sets a per-package value or turns it off for one package. It also delays
   security fixes, which Dependabot's cooldown does not, so use both with the window you can live with.
4. **pip has an equivalent** (`--uploaded-prior-to`, or an environment variable); use a full timestamp with
   time-of-day if pip and uv must agree, or they will be a day apart.
5. **A fixed timestamp freezes resolution in the past** until someone moves it. A duration moves by itself.

## 3.2 Bot pull requests are pull requests
1. **A dependency bot's pull request gets the same required checks and a human review as any other.** Merging
   on green turns a malicious release into a merged change within hours of its publication; the bot adds
   speed, not trust. This is our guidance, not a platform fact.
2. **Keep the bot, drop the noise another way:** group minor and patch updates into one pull request, leave
   majors individual, keep the schedule weekly.
3. **Keep the actions ecosystem in the bot configuration** so the commit pins of §1.1 are bumped by a
   reviewable pull request rather than left to rot.
4. **One bot, not two.** Two tools opening competing pull requests doubles the review load and the risk.

## 3.3 Audit the lockfile, not the tool
1. **A vulnerability audit with no input audits the current environment**, per the pip-audit documentation.
   Run through an ephemeral tool runner without an input, that environment is the tool's own, and the
   result is a clean report about the wrong thing.
2. **Export the lockfile and pass it in**: `uv export --format requirements-txt --no-emit-project` to a
   file, then `pip-audit -r <file> --no-deps`. The documentation says `-r` audits the given requirements
   file and `--no-deps` skips resolution and requires every requirement pinned to an exact version, which
   an export is.
3. **Pin the audit tool's own version** for the reason in §1.1.3, and run it on a schedule as well as on
   pull requests: a dependency does not have to change for a new advisory to apply to it.
4. **Do not use the tool's auto-fix in automation.** It changes the environment it ran in, not your
   lockfile.

## 3.4 A name from a suggestion is a dependency decision
1. **A package name suggested by a model, a snippet or a chat may not exist, or may have been registered by
   someone who read the same suggestion.** Before adding it, open its registry page: the exact name, the
   linked repository, the release history and the age. This is the check `security-hardening` §4.3 asks for
   with one extra reason.
2. **Installing a package runs its build and install code**, so never install one only to inspect it; read
   it on the registry's source view first.

## 3.5 Code owners and leaked secrets
1. **Code owners: the last matching pattern wins.** A catch-all `*` line placed after the specific lines
   overrides them. Put the catch-all first and the paths that define automation (workflows, the bot
   configuration, the agent-instruction files) after it.
2. **A code owners file enforces nothing by itself.** The GitHub documentation says approval is only
   required when a branch rule or ruleset requires code owner review, and that owners need explicit write
   access. Check both, or the file is decoration.
3. **Turn on push protection for secrets** so a detected secret is blocked before it enters history, and
   keep a CI scan as the backstop for what the protection misses and for a bypassed local hook.
4. **Rotate first, then clean.** A secret that was pushed once is in every clone and fork
   (`security-hardening` §4.6); removing the line without rotating the credential changes nothing.

## Verification
- The audit was run against the exported file and its output listed packages from your lockfile.
- A freshly published test version of a dependency was not proposed inside the cooldown window.
- A pull request touching the workflow directory requested the code owner it should, and could not merge
  without that approval.
