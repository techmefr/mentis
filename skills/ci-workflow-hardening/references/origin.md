# ci-workflow-hardening: origin and source stamps

> Provenance of `skills/ci-workflow-hardening`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real repository by us. No workflow was
executed and nothing was installed while writing it.

This block is meant to be folded into the same-topic block when PR 118 lands: its dependency supply-chain
section (§3) overlaps the Python supply-chain section that PR adds to `python-conventions`, which is not on
main and is not cited here. No block on main covers workflow hardening today. `devops-conventions` §1 holds the generic pipeline rules and `security-hardening`
§4 the dependency decision, and both are cross-linked rather than repeated.

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
| Paldom/python-skills: CI and supply-chain skills | MIT (copyright 2026), read 2026-10-08 | The aggregator pattern, matrix quoting, fail-fast, duplicate job names, bot pull request policy, slopsquatting, push protection plus backstop |
| scientific-python/cookie: security guide | BSD-3-Clause, read 2026-10-08 | Fork-addressable SHAs, no caching in release jobs, cooldown trade-off |

## Rewrite notes
The advice to keep bot pull requests under human review (§3.2) and the short-window figure are our guidance
drawn from the incident narrative in the MIT skill, not a platform fact. Verification lists were written
by us.

## Not verified
1. **`fail-fast` default and YAML float reading of `3.10`:** taken from the MIT skill and general YAML
   behaviour; the GitHub pages read did not state the default or the quoting.
2. **Required check context names, duplicate job names, "a pending check on a path-filtered workflow":** the
   duplicate-name claim is from the MIT skill only; the path-filter behaviour is from the GitHub
   troubleshooting page.
3. **Requiring approval for outside contributors, secret push protection coverage:** repository settings
   named in the MIT skill, not read in the GitHub settings documentation.
4. **Package registry behaviour for slopsquatting** and the practice of reading source on a registry viewer
   are from the MIT skill.
5. **Dependabot cooldown on transitive dependencies** was reported as unconfirmed upstream and is not
   claimed here.
6. **Version-dated platform changes** reported in the sources (a default cooldown, read-only cache tokens
   for untrusted triggers) were not confirmed in the official pages read and are not relied on.

## Related blocks
`devops-conventions` (pipeline reproducibility), `security-hardening` (dependencies and secrets),
`python-testing-strictness` (coverage gate settings), `python-container-runtime` (image pinning).
