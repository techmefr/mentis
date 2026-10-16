---
name: release-changelog-pitfalls
description: "Use when releases are cut by a release-pull-request tool (release-please) or a changelog is generated or maintained from commits: squash-merge and a linear history, commit prefixes and what counts as a releasable unit, extra changes in one commit, forcing a version, a release pull request that never appears, a stale pending label, testing the configuration on a real branch, how the previous release is found; plus what the Keep a Changelog 2.0 text adds (urgency order of the six types, Fixed versus Changed, Security entries, the breaking marker, what CI may and may not do for a changelog), and build provenance attestations in GitHub Actions (plan limits, public versus private signing, the v4 wrapper)."
---

# release-changelog-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the mechanics between a merged commit and a published release. The
premise: **a release tool reads your commit history literally, so the shape of the history is the interface,
and a changelog is a record written for readers that a tool can only draft**. How to write the notes
themselves (net outcomes, entry wording, the verification gate, the baseline file layout) is in
`release-notes-writing-pitfalls`; the mechanics of removing something that is in use are in
`deprecation-migration`; pinning and hardening the workflow that runs all this is in `ci-workflow-hardening`.

## When
- A repository adopts release-please, or its release pull request does not appear, or the version is wrong.
- Pull requests are merged in ways that change what the release notes say.
- A changelog is generated from commit messages and nobody edits it.
- A workflow signs build output with attestations.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Release-please: history shape, commit prefixes, footers, forcing a version, missing release pull requests, testing, previous release | a release-pull-request tool is set up or misbehaves | [`01-release-pull-requests.md`](./references/01-release-pull-requests.md) |
| 2 | The Keep a Changelog 2.0 text: curation, type order, Fixed versus Changed, Security, breaking marker, CI role | a changelog file is generated, edited or checked | [`02-changelog-conventions.md`](./references/02-changelog-conventions.md) |
| 3 | Build provenance attestations: what they bind, where they are signed, plans, the v4 wrapper | a workflow attests build output | [`03-build-attestations.md`](./references/03-build-attestations.md) |

## Output / checkpoint
Each rule was exercised, not read off the page: the tool was run in dry-run mode against a branch of the real
repository and its output read (1.5), a squash-merged `feat` and `fix` pair produced the entries expected
(1.2), a forced version produced a release pull request (1.3), the generated changelog section was edited by
a person before release (2.1), and an attestation was verified with the command-line tool after the workflow
ran (3.4). A configuration that was only read is not verified.

## Guardrails
- Never merge with rebase or a plain merge commit in a repository whose notes come from commit messages (1.2).
- Never put the extra change messages of a commit anywhere but the bottom of it (1.3).
- Never test a release configuration on a fork (1.5).
- Never remove an `autorelease` label before looking for the release pull request it belongs to (1.4).
- Never publish a generated changelog section unread (2.1).
- Never fold a dependency bump into a changelog as its own type (2.2).
- Never make a changelog edit a required check on every change (2.5).
- Never assume attestations work in a private repository on a plan that lacks them (3.2).
- This block states documentation as of the commits in [`references/origin.md`](./references/origin.md); no
  tool was run and no workflow executed (🟡).

## Origin
Rewritten from the release-please documentation (googleapis/release-please, Apache-2.0), the Keep a Changelog
2.0.0 text (olivierlacan/keep-a-changelog, MIT) and the `actions/attest-build-provenance` README (MIT), read
2026-10-16. 🟡: never run by us; open points and own guidance are in [`references/origin.md`](./references/origin.md).
