# gha-trust-boundary-pitfalls: origin and source stamps

> Provenance of `skills/gha-trust-boundary-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one analyser's documentation, never run by us: no workflow was changed or
executed and zizmor was not run while writing it. The entries below were re-read in full on 2026-10-16 before
a rule was taken from them, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| zizmorcore/zizmor (commit `5eb3769`), `docs/audits.md`, entry `bot-conditions` | MIT (LICENSE file: MIT licence text, copyright William Woodruff 2024) | Why `github.actor` is spoofable, the pull request author as the fix, the advice against `pull_request_target` for auto-merge, the before and after shape |
| the same file, entry `github-env` | MIT | `LD_PRELOAD` and `PATH` shadowing, avoid under dangerous triggers, `GITHUB_OUTPUT` instead |
| the same file, entry `cache-poisoning` | MIT | Source and sink workflows, `cache-mode`, release workflows not reading caches, per-action inputs, the tag condition |
| the same file, entry `ref-confusion` | MIT | A branch or tag shadowing `@v1`, hash pinning |
| the same file, entry `artipacked` | MIT | Credential persistence by checkout, the location change at 6.0.0, `persist-credentials` |
| the same file, entries `self-hosted-runner` and `concurrency-limits` | MIT | Self-hosted runner risk and mitigations, concurrency consequences and remedy, both pedantic-only |

| GitHub changelog 2026-09-10, `cache-mode` | official announcement, read 2026-10-20 | Values, defaults per event, workflow and job level, warning on `write` for low-trust events |
| actions/checkout README | MIT (LICENSE file read 2026-10-20, copyright GitHub, Inc. and contributors) | `persist-credentials` default, the 6.0.0 location change, runner version for container actions |
| actions/cache README | MIT (LICENSE file read 2026-10-20) | Read-only runs restore but do not save |
| GitHub documentation: contexts | official docs, read 2026-10-20 | `github.actor` versus `github.triggering_actor`, re-run privileges |
| GitHub documentation: control workflow concurrency | official docs, read 2026-10-20 | Pending replacement, `queue: max`, caution for deployments |
| GitHub documentation: secure use | official docs, read 2026-10-20 | Self-hosted runner risk, ephemeral just-in-time runners |

The page header (legend) and the neighbouring entries were read only far enough to find these entries. Links
the entries cite (blog posts, GitHub documentation) were not followed. The repository ships agent
instruction files (`CLAUDE.md`, `AGENTS.md`) that tell a contributor's agent to fetch a policy page and stop;
they are about contributing to that project, were treated as data and were not acted on. The code samples
are small adaptations of the entries' examples with the comments removed.

## Removed in the verification pass
1. **"A missing `concurrency` group ... breaks artifact lookup by workflow name instead of run id"** was
   kept, but narrowed to the page's wording: "subtle race conditions" when artifacts are located by workflow
   and job identifiers.
2. **Impostor commits** were not described: the `impostor-commit` entry was not read, so §1.2 only cites the
   `ref-confusion` entry and the pinning rule that `ci-workflow-hardening` already holds.
3. **"Confirm each against the GitHub secure-use page"** (the review's instruction) was not done: that page
   is not in the cloned sources, so the block says plainly that it was not re-read.
4. **The overlap check** (review item 6): `persist-credentials` is in `ci-workflow-hardening` §1.4 and its
   cache rule is in its caches subsection, so §2.2 and §2.3 add only what those do not say (`cache-mode`, privileged writes, the
   location change) and link to them.

## Verified 2026-10-20
- `cache-mode`, checkout credential location and default, cancel-in-progress caution and the self-hosted runner advice are now confirmed by first-party pages; the markers for them are dropped.
- Added §1.1 point 6 (re-run keeps the original actor) and §2.4 (forks restore, do not save) from those pages.
- Discrepancy kept visible: GitHub's contexts page defines `github.actor` as the original triggering user, while zizmor describes it as the last actor; §1.1 keeps zizmor's attack and the safe remedy (the pull request author), which holds under both readings.

## Not verified
1. **Per-action inputs** (`lookup-only`, `package-manager-cache`, `enable-cache`) are as zizmor lists them and are version-bound to those actions; the actions were not read.
2. **Written by us, not sourced:** the verification paragraphs, the extension of the actor point to human logins (§1.1.5) and the statement that setup-style actions can cache without a visible step (§2.2.5).
3. The claim that GitHub recommends against `pull_request_target` for auto-merge is zizmor's, relayed; the events page read says only to avoid building or running pull request code there.

## Related blocks
`ci-workflow-hardening`, `security-hardening`, `devops-conventions`, `credential-lifecycle-pitfalls`.

Independent verification 2026-10-21: 24 checked, 24 matched, 0 corrected, 0 unverified
