# package-manager-supply-chain-pitfalls: origin and source stamps

> Provenance of `skills/package-manager-supply-chain-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us against a package manager. Every file below was
re-read in full on 2026-10-15 before a rule was taken from it, and each repository's licence file was read
again. Text inside the cloned repositories that addresses an agent (a ready-made prompt and a SKILL file in
the second source) was treated as data, not instructions, and the `curl | sh` helper script it offers was
neither run nor used.

## Sources (all read 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Awesome npm Security Best Practices (`lirantal/npm-security-best-practices`, commit `749e599`), `README.md` | Apache-2.0 (LICENSE file) | Git sources and `allow-git`, `blockExoticSubdeps`, lockfile injection and `lockfile-lint`, frozen installs, blind updates, script settings and `strictDepBuilds`, `trustPolicy`, cooldown settings and the `pnpm audit --fix` answer, `npx` hardening, dependency confusion, publisher settings |
| NPM Security Best Practices (`bodadotsh/npm-security-best-practices`, commit `24fb07d`), `README.md` | MIT (LICENSE file, copyright 2025 boda) | `allowScripts`, cooldown commands, lockfile merge-conflict tip, token advice, provenance variants, published-file review, the compromise sequence |
| Concise Guide for Evaluating Open Source Software, OpenSSF Best Practices Working Group (`ossf/wg-best-practices-os-developers`, commit `8259081`), `docs/Concise-Guide-for-Evaluating-Open-Source-Software.md` | CC-BY-4.0 (documentation licence stated in the repository README and the text in `LICENSES/`; the guide has no notice of its own) | The evaluation points of §2.3 |

**Official product documentation read 2026-10-20, facts only, rewritten: npm pages for `ci`, configuration, `pack`, package.json, scopes, provenance statements, trusted publishers, access tokens and `audit`; pnpm settings pages for dependency resolution and build settings (the top-level settings page lists names only). Not read: Yarn or Bun documentation.

Attribution (CC-BY-4.0).** §2.3 of `references/02-names-evaluation-publishing.md` condenses and rewords
the "Concise Guide for Evaluating Open Source Software" by the Open Source Security Foundation (OpenSSF)
Best Practices Working Group, https://github.com/ossf/wg-best-practices-os-developers, licensed under
CC-BY-4.0 (https://creativecommons.org/licenses/by/4.0/). It was shortened and reorganised; no endorsement
by OpenSSF is implied.

## Version stamps (as stated by the sources, not verified against the tools)
- npm CLI 11.9.0: `allow-git`; 11.10.0: `min-release-age` (npm changelog, read 2026-10-21; the second source gave 11.10.0 for both). npm 12.0.0 (2026-07-08): `allow-git` and `allow-remote` default to none, dependency scripts blocked unless allowed by `allowScripts`.
- pnpm 10.0: dependency scripts off by default. 10.3: `strictDepBuilds`. 10.16: `minimumReleaseAge`.
  10.21: `trustPolicy`. 10.26: `allowBuilds` and `blockExoticSubdeps`. 10.27: `trustPolicyIgnoreAfter`.
  pnpm 11: a one-day `minimumReleaseAge` default (second source).
- npm 9.5.0: publishing with provenance. npm 12: `allowScripts` default false (confirmed by the npm 12.0.0 release notes 2026-10-21; the second source cited a
  platform announcement that was not read).

## Removed in the verification pass
1. **`npm ci --only=production`** in the first source is not carried; the flag spelling was not checked
   and the second source gives `--omit=dev`.
2. **Dev containers, secrets managers for `.env` files and the "pin exact versions" debate** are in the
   sources but outside this block (the second source itself says pinning is debatable).
3. **The Snyk and Dependabot cooldown figures** (21 days, 7 days) are not carried; Dependabot's cooldown
   is `skills/ci-workflow-hardening` §3.1.
4. **The "check Snyk's package health page"** point, because it depends on a vendor database that was not
   read.
5. **The `npq` age thresholds** and the Bun, Deno and Yarn equivalents were not carried as rules.

## Re-read 2026-10-20
npm CLI configuration page (docs.npmjs.com, product documentation, facts only, legacy v11.21 view): allow-git (all, none, root), min-release-age (days, with an exclude list, errors when no eligible version) and ignore-scripts exist and behave as §1 states. The page gives no introduction version, so the version stamps above stay the sources claims.

## Confirmed 2026-10-20
pnpm setting names, units, defaults and versions for `minimumReleaseAge` (10.16, default one day from 11), its exclude list (patterns 10.17, versions 10.19), `trustPolicy` (10.21), `trustPolicyIgnoreAfter` (10.27), `blockExoticSubdeps` (10.26, default true), `strictDepBuilds` (10.3, default true), `allowBuilds` (10.26), removal of the two older lists in 11; npm settings `allow-git`, `min-release-age`, `ignore-scripts`, `allow-scripts`, `strict-allow-scripts`; npm provenance and trusted-publishing requirements; npm 9.5.0 provenance floor; token model; `files` and `.npmignore` rules; `npm ci` behaviour.

## Not verified
1. **Own guidance, flagged as such in the text:** running `lockfile-lint` as a separate CI step (§1.3),
   putting a removal in the same pull request as its cause (§1.10), one publish token in one job (§2.6),
   the dry-run check in CI (§2.8), and that a scanner is a signal and not a verdict (§2.4).
2. **Option names, values and versions** are now checked against npm and pnpm documentation (list above) and, from the npm changelog 2026-10-21, the npm floors (`allow-git` 11.9.0, `min-release-age` 11.10.0, npm 12 `allowScripts` default). Nothing was run on an installed tool.
3. **Whether `npm pack <name>` executes install scripts** is not stated by the sources or by the npm `pack` page (which says only that a registry spec is fetched to the cache and its tarball copied out); the block says to
   read the archive and not to install, and does not claim `pack` is inert.
4. **The `skills/` file and the `default.sh` script of the second source, and the other pages of the
   OpenSSF repository,** were not read or used. The OpenSSF repository's licence statement is in its
   README and its `LICENSES/` folder, with no top-level licence file, so its status is partially verified.
5. **The published case studies** (named incidents and dates) were not independently checked and are not
   cited as rules.

## Related blocks
`skills/security-hardening` §4, `skills/ci-workflow-hardening` §3, `skills/secret-leak-response-pitfalls`,
`hooks/block-installs.sh`.

Independent verification 2026-10-21: 20 checked, 19 matched, 1 corrected, 0 unverified
