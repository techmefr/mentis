# ci-workflow-hardening: origin and source stamps

> Provenance of `skills/ci-workflow-hardening`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real repository by us. No workflow was
executed and nothing was installed while writing it.

Overlaps with `skills/devops-conventions` §1, `skills/security-hardening` §4 and the Python supply-chain section of `skills/python-conventions` (2026-10-19); cross-referenced, not merged. Its dependency supply-chain section (§3) is the part that overlaps most. `devops-conventions` §1 holds the generic pipeline rules and `security-hardening` §4 the dependency decision, and both are cross-linked rather than repeated.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| GitHub Actions documentation: secure use | official docs, read 2026-10-08 | Full-length SHA as the immutable reference, read-only default token, untrusted checkout in privileged triggers, intermediate environment variable for untrusted input |
| GitHub documentation: events that trigger workflows | official docs, read 2026-10-08 | `merge_group` trigger requirement, `pull_request_target` context and its cache and secret risks, events created with the workflow token |
| GitHub documentation: troubleshooting required status checks | official docs, read 2026-10-08 | Skipped by a conditional reports success, merge queue trigger |
| GitHub documentation: workflow syntax | official docs, read 2026-10-08 | Unlisted permissions drop to none once any is listed |
| GitHub documentation: Dependabot options reference | official docs, read 2026-10-08 | Cooldown options, security updates not delayed, `exclude` precedence, ecosystem support for bump-type options |
| GitHub documentation: about code owners | official docs, read 2026-10-08 | Last matching pattern wins, enforcement only through a branch rule, owners need write access |
| uv documentation: settings reference, projects sync | MIT or Apache-2.0, read 2026-10-08 | `exclude-newer` formats and semantics, `--locked` raising on a stale lockfile |
| pip-audit repository documentation | Apache-2.0, read 2026-10-08 | Default environment audit, `-r`, `--no-deps` |
| GitHub documentation: managing Actions settings for a repository | official docs, read 2026-10-20 | Approval setting for fork pull request workflows (first-time, new-to-GitHub or all external contributors); `pull_request_target` runs regardless of it |
| GitHub documentation: troubleshooting required status checks (Enterprise Server 3.19 copy) | official docs, read 2026-10-20 | Re-confirmed: conditional skip reports success, path-filtered workflow stays pending, check and status of one name must both pass, `always()` with `needs` |
| GitHub documentation: secret scanning push protection | official docs, read 2026-10-20 | Coverage (CLI, web UI, API), repository-level protection off by default, bypass with a reason creating an alert |
| GitHub documentation: secure use (re-read) | official docs, read 2026-10-20 | Pin to a SHA taken from the action's own repository, environment variable for untrusted input, self-hosted runner risk |
| Paldom/python-skills: CI and supply-chain skills | MIT (copyright 2026), read 2026-10-08 | The aggregator pattern, matrix quoting, fail-fast, duplicate job names, bot pull request policy, slopsquatting, push protection plus backstop |
| scientific-python/cookie: security guide | BSD-3-Clause, read 2026-10-08 | Fork-addressable SHAs, no caching in release jobs, cooldown trade-off |

## Rewrite notes
The advice to keep bot pull requests under human review (§3.2) and the short-window figure are our guidance
drawn from the incident narrative in the MIT skill, not a platform fact. Verification lists were written
by us.

## Verified 2026-10-20
- Outside-contributor approval is a repository Actions setting with three levels; confirmed in the settings page.
- Push protection exists at repository level (off by default) and can be bypassed with a recorded reason; so it is a net, with a backstop scan, as §3 says.
- Skipped-by-conditional reports success, path-filtered workflows stay pending, and `always()` with `needs` is the documented remedy for dependent jobs: confirmed.

## Not verified
1. **`fail-fast` default and YAML float reading of `3.10`:** the workflow-syntax and job-variations pages read on 2026-10-20 did not state the default or the quoting; still from the MIT skill and general YAML behaviour.
2. **Duplicate job names across workflows:** the troubleshooting page does not address it; still from the MIT skill only.
3. **Package registry behaviour for slopsquatting** and reading source on a registry viewer: MIT skill only.
4. **Dependabot cooldown on transitive dependencies** was reported as unconfirmed upstream and is not claimed here.
5. **Version-dated platform changes** (a default cooldown, read-only cache tokens for untrusted triggers) were not confirmed in the official pages and are not relied on.

## Related blocks
`devops-conventions` (pipeline reproducibility), `security-hardening` (dependencies and secrets),
`python-testing-strictness` (coverage gate settings), `python-container-runtime` (image pinning).
