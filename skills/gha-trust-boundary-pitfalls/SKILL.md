---
name: gha-trust-boundary-pitfalls
description: "Use when a GitHub Actions workflow decides trust from an identity or a reference, or passes state between runs and steps: an if condition on github.actor for a bot such as Dependabot (spoofable, use the pull request author), an action pinned to a tag or branch that an attacker can shadow, writes to GITHUB_ENV or GITHUB_PATH under pull_request_target or workflow_run, a release workflow that restores a cache or a privileged trigger that writes one, the checkout credential left on disk, and the optional checks on self-hosted runners and concurrency. A sibling of ci-workflow-hardening that adds only what it does not name."
---

# gha-trust-boundary-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the places where a workflow trusts something it should not. The
three sections share one premise: **a condition, a reference or a file is only a trust decision if the party
who writes it is the party you meant**. This is a sibling of `ci-workflow-hardening`, not a replacement:
its section 1 already covers pinning actions to a commit, untrusted triggers, script injection and
`persist-credentials`, and the general rule on caches, and none of that is repeated; this block adds the
reasons and the traps that block does not name.

## When
- Writing an `if:` that lets a bot, an author or a label skip a check or run a privileged step.
- Writing to `GITHUB_ENV` or `GITHUB_PATH` in a job started by a pull request or another workflow.
- Adding a cache to a workflow that publishes a release, or a cache write to a privileged trigger.
- Reviewing a workflow analyser's findings (zizmor is the one this block was read from) and deciding which
  are blocking and which are optional.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Spoofable conditions and confusable references: `github.actor`, bot checks, `@v1` as branch or tag | an `if:` names a bot or a user, or an action is referenced by a tag | [`01-conditions-and-refs.md`](./references/01-conditions-and-refs.md) |
| 2 | Environment files, caches and the checkout credential | a step writes `GITHUB_ENV`, a release job caches, or checkout is used | [`02-env-files-caches-credentials.md`](./references/02-env-files-caches-credentials.md) |
| 3 | Optional hardening: self-hosted runners and concurrency | a workflow runs on a self-hosted runner or runs pile up | [`03-runners-and-concurrency.md`](./references/03-runners-and-concurrency.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: no `github.actor` comparison remained and a pull request
from a non-bot account against a scratch workflow did not reach the privileged job (§1.1), the workflow analyser named in the analysis subsection of `ci-workflow-hardening` ran clean and no
`GITHUB_ENV` or `GITHUB_PATH` write remained in a privileged job (§2.1), and the release workflow ran with no
cache restored (§2.2). A workflow that was only read is not verified.

## Guardrails
- Never use `github.actor` as proof that a bot started the event (§1.1).
- Never reference an action by a tag or branch where a commit hash is possible (§1.2).
- Never write attacker-influenced content to `GITHUB_ENV` or `GITHUB_PATH` (§2.1).
- Never let a release workflow read a cache, and never enable cache writes in a privileged trigger (§2.2).
- Never present the pedantic findings (self-hosted runners, concurrency) as blocking (§3).
- This block states GitHub Actions behaviour as read from one analyser's audit documentation on the date in
  [`references/origin.md`](./references/origin.md); the platform and the analyser move, the GitHub secure-use
  page was not re-read for this block, and nothing was run while writing it.

## Origin
Rewritten from the audit documentation of zizmor (MIT: entries on bot conditions, GITHUB_ENV, cache
poisoning, ref confusion, self-hosted runners, concurrency limits and artipacked), read 2026-10-16. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
