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

## Not verified
1. **`cache-mode`** is a GitHub workflow setting that zizmor's page links to; the page that defines it was
   not read, so the setting name, placement and values are as zizmor states them (version-bound to zizmor
   1.31.0 and later).
2. **Per-action inputs** (`lookup-only`, `package-manager-cache`, `enable-cache`) are as the page lists them
   and are version-bound to those actions.
3. **Checkout's credential location** (below 6.0.0 versus 6.0.0 and later) is as the `artipacked` entry
   states it; the checkout action was not read.
4. **Written by us, not sourced:** the verification paragraphs, the extension of the actor point to human
   logins (§1.1), the statement that setup-style actions can cache without a visible step (§2.2), and the
   advice not to cancel a release or deployment run in progress (§3.2).
5. **The GitHub documentation** on secure use, `pull_request_target` and `cache-mode` was not read; the
   statement that it recommends against `pull_request_target` for auto-merge is zizmor's, relayed.

## Related blocks
`ci-workflow-hardening`, `security-hardening`, `devops-conventions`, `credential-lifecycle-pitfalls`.
