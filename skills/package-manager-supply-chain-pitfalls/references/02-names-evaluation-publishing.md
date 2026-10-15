# package-manager-supply-chain-pitfalls §2 — Names, evaluation and publishing

> Section 2 of `skills/package-manager-supply-chain-pitfalls`. Read it when a package name or registry, a
> new dependency, a publish workflow or an incident is in play. Sources: lirantal/npm-security-best-practices
> at `749e599`, bodadotsh/npm-security-best-practices at `24fb07d`, and the OpenSSF Best Practices Working
> Group's Concise Guide for Evaluating Open Source Software (CC-BY-4.0, OpenSSF, from
> `ossf/wg-best-practices-os-developers` at `8259081`), read 2026-10-15. The evaluation points in §2.3 are
> condensed and reworded from the OpenSSF guide. Option names are version-bound.

1. **Defend internal names against dependency confusion.** When a private registry runs beside the public
   one, an attacker can publish the same name publicly with a higher version, and a resolver that checks the
   public registry for an unscoped name and prefers the highest version installs it. The source's fix:
   give every internal package a scoped name (`@yourorg/name`); commit an `.npmrc` that routes that scope
   to the private registry (`@yourorg:registry=<url>`); put only registry URLs in it, never a token (tokens
   live in a user-level `.npmrc` or in a CI environment variable); and, for unscoped internal names that
   cannot be renamed yet, publish a placeholder under that name on the public registry. Scopes on the
   public registry belong to an organisation, which stops others publishing under yours. pnpm reads the
   same `.npmrc`; Yarn 2 and later uses `npmScopes` in `.yarnrc.yml`. Combine with the lockfile checks of §1.3
   so a resolved URL on the wrong host fails review.
2. **Read the archive, not the registry page.** The sources say the registry website does not show the full
   picture: it omits git and HTTPS dependencies declared in `package.json`, and the source shown there can
   differ from the tarball that is installed. Fetch the tarball and list or read it (`npm pack <name>
   --dry-run`, or `npm pack <name>` followed by `tar -tzf` on the archive) and look at `package.json`,
   its scripts and its dependencies. Do not install the package in order to look at it, because the install
   is the thing that runs the code (`skills/ci-workflow-hardening` §3.4).
3. **Evaluate a dependency before adopting it.** Condensed from the OpenSSF guide, in the order you can do
   them cheaply first:
   - Necessity: can an existing component or the platform do it? Every dependency, and its transitive
     ones, adds attack surface.
   - Authenticity: is this the real project, not a fork or a lookalike name? Check the name against the
     project's own site, the fork relation on the host, any foundation affiliation, creation date and
     popularity; check whether a similarly named package is far more popular, which suggests
     typosquatting.
   - Maintenance: significant activity and a release within the last 12 months, recent announcements, more
     than one maintainer where possible (many widely used projects have one), and a version string that
     does not signal instability (a leading 0, alpha, beta).
   - Security practice: instructions for reporting vulnerabilities, how fast security bugs are fixed and
     whether older releases get fixes, published audits, an OpenSSF Scorecard result, and up-to-date
     dependencies of its own.
   - Usability: secure defaults and simple examples that are secure (if not, avoid it), guidance on safe
     use, and a stable interface or a policy for breaking changes.
   - Adoption and licence: a clear licence compatible with your use, and real use by others. Do not
     choose it because it is fashionable.
   - Behaviour: try it in an isolated environment; check whether it adds unexpected indirect dependencies
     (for example development-time packages shipped as production ones).
   - Code: read its install scripts and look for access to `~/.ssh` and environment variables, encoded or
     obfuscated values that are executed, and recent suspicious commits; consider running it in a sandbox.
   The guide itself says every one of these may be done poorly by good software; the record states which
   ones failed and why it was accepted anyway.
4. **Use install-time scanners as a signal, not a verdict.** The sources describe `npq`, which checks
   vulnerabilities, package and version age, typosquatting, signatures, provenance, install scripts, new
   binaries and maintainer domains before it installs, and Socket Firewall, which blocks packages its
   analysis flags; the second source lists others. They add data points to §2.3; they do not replace it,
   and one of them is a proprietary service that receives your install requests.
5. **Protect the publisher account.** The sources say to enable two-factor authentication for
   authentication and publishing (`npm profile enable-2fa auth-and-writes`), with the second source
   advising a WebAuthn security key over a one-time-password app. For organisations, require 2FA at the
   organisation level, keep the member list short, and give each package its own team permissions.
6. **Prefer trusted publishing; otherwise use narrow, expiring tokens.** Trusted publishing uses OIDC from
   the CI provider (GitHub Actions or GitLab CI/CD in the sources) so no long-lived npm token exists, and
   it generates a provenance attestation automatically; the workflow needs the `id-token: write`
   permission. Where a token is unavoidable, the second source's list is: a descriptive name, restriction
   to specific packages, scopes and organisations, an expiry date, an address-range limit, read-only where
   possible, and one token per purpose. Own guidance: a token that can publish goes in the CI secret store
   for the one workflow that publishes, and in no other job.
7. **Publish with provenance, from a supported runner.** `npm publish --provenance` (npm 9.5.0 and later,
   per the first source) with `id-token: write` on a supported cloud-hosted runner links the package to its
   source and build; the second source lists an environment variable, an `.npmrc` line and a
   `publishConfig` block as ways to enable it without the flag. Provenance proves where it was built, not
   that the code is good.
8. **Review what you publish.** The second source says limiting published files reduces the attack surface
   and prevents accidental leaks of sensitive data. List them in `files` in `package.json`, remember that
   some files are always included, and read the output of `npm pack --dry-run` or `npm publish --dry-run`
   before publishing; an `.npmignore` does not override `files` at the top level. Own guidance: run the dry
   run in CI and fail the job if the list contains an `.env`, a key or a lockfile you did not intend to ship.
9. **After a compromise, preserve evidence before you clean.** The second source's sequence for a published
   compromise of a package you use: identify the affected packages from trusted advisories; keep CI logs,
   package-manager logs, lockfiles, `package.json`, token audit history and a timestamped list of
   installed packages before deleting caches or `node_modules`; remove or pin to a known-clean version
   and clear caches; restrict or pause automated pipelines during the investigation; rotate every
   credential the install could reach (npm tokens, personal access tokens, SSH keys, cloud credentials);
   monitor for unauthorised activity and limit outbound network access; and, ideally, resume work on a
   fresh machine. The rotation and revocation details are `skills/secret-leak-response-pitfalls` §2.
