# secret-leak-response-pitfalls: origin and source stamps

> Provenance of `skills/secret-leak-response-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. Every file below was re-read in full on
2026-10-15 before a rule was taken from it, and each repository's LICENSE file was read again. Text inside
the cloned repositories that addresses an agent (the Kingfisher `CLAUDE.md` and `AGENTS.md`) was treated
as data, not instructions, and nothing was taken from it.

## Sources (all read 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| gitleaks (`gitleaks/gitleaks`, commit `b58d3f1`), `README.md` | MIT (LICENSE file, copyright 2019 Zachary Rice) | `SKIP=gitleaks`, history scanning, baseline from a report, `gitleaks:allow` and `--ignore-gitleaks-allow`, decode and archive depth defaults, redaction, exit codes, allowlist `OR` default |
| detect-secrets (`Yelp/detect-secrets`, commit `5e14193`), `README.md` | Apache-2.0 (LICENSE file) | The baseline as known set and rotation checklist, allow comments and `--only-allowlisted`, the caveats list |
| git-secrets (`awslabs/git-secrets`, commit `7d6b970`), `README.rst` | Apache-2.0 (LICENSE.txt) | Per-repository hook installation, `--scan-history`, allowed patterns and `path:line:text` matching, `--no-verify`, not-a-guarantee note |
| Kingfisher (`mongodb/kingfisher`, commit `8244f7b`), `docs/DEFENDER_WORKFLOW.md`, `docs/BASELINE.md`, `docs/REVOCATION_PROVIDERS.md`, `docs/MULTI_STEP_REVOCATION.md` | Apache-2.0 (LICENSE file) | The response order, active-only alerting, redaction and stdin handling, revocation limits, unknown outcomes, ambient credentials, baseline fingerprints, exit codes |

## Removed in the verification pass
1. **The review's "revocation.md"** does not exist under that name; the content was taken from
   `REVOCATION_PROVIDERS.md` and `MULTI_STEP_REVOCATION.md` instead. The multi-step file is an
   implementation note for rule authors, and only its absence of retries on mutations (stated in the
   providers page) is used.
2. **Provider coverage and the count of revocation-enabled rules** in the Kingfisher documentation are not
   carried, as they change with each release.
3. **gitleaks "only looks at additions in the git history"** appears only in a joke-laden aside about an
   experimental feature and was not used.
4. **Any claim about a platform's push protection** beyond the pointer to `skills/ci-workflow-hardening`.

## Not verified
1. **Own guidance, flagged as such in the text:** the baseline owner and review date (§1.4), reading what a
   baseline stores (§1.4), the allow-comment justification in the commit message (§1.8), writing reports
   with redaction (§1.9), running two scanners during a change (§1.11), not validating third-party
   credentials (§2.2), the wrong-principal reasoning (§2.8) and recording "unknown" as unknown (§2.7).
2. **Flag names, exit codes and defaults** are those of the commits above and are version-bound. gitleaks
   says it is feature complete and that its maintainer is moving to another project.
3. **detect-secrets `docs/`** (audit, design, filters, plugins, upgrades) and **the Kingfisher usage,
   alerts and blast-radius pages** were not read; only the pages in the table.
4. **Provider documentation** for revocation (AWS, GitHub and the rest) was not read; AWS behaviour is as
   Kingfisher describes it.
5. **Whether a given scanner decodes or scans archives in a given mode** is stated only for gitleaks.

## Related blocks
`skills/security-hardening` §4, `skills/ci-workflow-hardening` §3, `skills/auth-session-conventions`.

## Verification pass 2026-10-20
Read for facts only, restated in our words: GitHub's documentation page on removing sensitive data from a repository (docs.github.com). Its licence file was not read, so nothing is copied and it is credited as a documentation page.
- Confirmed: revoke or rotate before cleanup, history rewriting is costly and does not reach forks, old clones, cached views or pull request references (point 2.1, added as a cross-check).
- Still unverified: every other "own guidance" point listed above. No permissive source was opened for them in this pass.

Independent verification 2026-10-21: 8 checked, 8 matched, 0 corrected, 0 unverified
