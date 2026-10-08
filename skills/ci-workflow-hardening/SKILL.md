---
name: ci-workflow-hardening
description: "Use when a GitHub Actions workflow is written or changed, a required status check or branch rule is set up, or a dependency-update bot, lockfile audit or release-age delay is configured: pinning actions to a commit, token permissions, untrusted triggers and script injection, caches, an aggregator job as the only required check (skipped counts as success, merge queue trigger, matrix names), and dependency supply-chain hygiene (cooldown on new releases, bot pull requests, auditing the lockfile rather than the tool, code owners)."
---

# ci-workflow-hardening

Step 6 of the pipeline (`WORKFLOW.md`), for the CI file itself. The three sections share one premise: **the
workflow is production code that runs with your token on code you have not read, and a green check is only
as strong as the rule that requires it**. Examples are GitHub Actions and Python tooling because that is
where the sources were read; the mechanisms (pin what you execute, least privilege, one stable required
check, a delay before adopting a new release) apply to any CI. Generic pipeline reproducibility is in
`devops-conventions` §1, and the dependency decision itself is in `security-hardening` §4; this block adds
what they do not say.

## When
- Creating or editing anything under `.github/workflows/`, or a reusable workflow.
- Choosing which check is required before merge, or a PR is green and will not merge.
- Adding or tuning a dependency-update bot, a vulnerability audit of the lockfile, or a release-age delay.
- Letting a workflow or a bot act on a pull request from a fork.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Workflow hardening: pinned actions, token permissions, untrusted triggers, script injection, caches, static analysis | a workflow file is written or reviewed | [`01-workflow-hardening.md`](./references/01-workflow-hardening.md) |
| 2 | Required checks: aggregator job, skipped jobs, merge queue trigger, matrix versions and names, bot-created events | a check is made required, renamed, or a green PR is blocked | [`02-required-checks.md`](./references/02-required-checks.md) |
| 3 | Dependency supply chain: release-age delay, bot pull requests, auditing the lockfile, code owners, leaked secrets | a bot, an audit, a lockfile command or a dependency name is added | [`03-dependency-supply-chain.md`](./references/03-dependency-supply-chain.md) |

## Output / checkpoint
The rule was exercised, not read off the file: a workflow linter or static analyser ran clean on the final
tree (§1), a pull request with one job deliberately failed showed the aggregator red and one with a job
skipped did not show it green (§2), and the audit was run against the exported lockfile and its output
named a project dependency (§3). A workflow that was only reviewed by eye is not verified.

## Guardrails
- Never check out or execute code from a pull request in a workflow that has secrets or a write token (§1.3).
- Never put an untrusted expression directly in a shell step (§1.4).
- Never make a matrix leg the required check (§2.2).
- Never turn on auto-merge for bot pull requests as a way to reduce noise (§3.2).
- This block states GitHub and uv behaviour as of the documentation read on the date in
  [`references/origin.md`](./references/origin.md); platform settings move often, so check a setting
  against the current docs before relying on it. Nothing was run while writing it.
- Installing the analysers and auditors named here is the user's step, in their own terminal; this block
  names them and stops.

## Origin
Rewritten from the official GitHub Actions documentation (secure use, events, required checks, code
owners, Dependabot options), the uv and pip-audit documentation, one MIT agent-skill repository for
Python CI and supply chain and one BSD scientific-Python template's security guide (read 2026-10-08). 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
