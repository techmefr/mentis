# gha-trust-boundary-pitfalls §1 — Conditions and references an attacker can shape

A workflow often decides "trust this" with a short expression or a short string: an actor name in an
`if:`, a version in `uses:`. Both can be made to say what the attacker wants.

## 1.1 `github.actor` is not the author
1. **Many workflows let a trusted bot bypass a check or act with privilege**, and test for it with
   `if: github.actor == 'dependabot[bot]'`.
2. **That condition is spoofable.** `github.actor` is the last actor to perform an action on the triggering
   context, not necessarily the actor who caused the trigger. An attacker can open a pull request whose head
   commit has `github.actor == 'dependabot[bot]'` while the rest of the branch history is attacker-controlled
   code, and the actor check passes.
3. **Check who created the pull request instead**: `github.event.pull_request.user.login` is the actor that
   created it, not the last one to modify it.
4. **Do not use `pull_request_target` for auto-merge workflows.** zizmor's page says GitHub's documentation
   recommends against it. The shape that page gives as the fix moves the trigger to `pull_request` and the
   condition to the author:

```yaml
on: pull_request

jobs:
  automerge:
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login == 'dependabot[bot]' && github.repository == github.event.pull_request.head.repo.full_name
    steps:
      - run: gh pr merge --auto --merge "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

   The URL reaches the shell through an environment variable (`ci-workflow-hardening` §1.4).
5. **The same applies to any actor name used as a gate**: a human maintainer's login in an `if:` has the same
   flaw. Own guidance, extending the page's bot example: treat any identity read from `github.actor` as a
   hint for logging, never as a gate.

6. **A re-run keeps the original actor's privileges.** GitHub's contexts page defines `github.actor` as the user
   who triggered the original run and `github.triggering_actor` as the one who started this run, which differs
   only on a re-run; the re-run uses the privileges of the original actor. So a maintainer's re-run of a
   run first triggered by someone else does not raise or lower what the run may do, and the two names must not
   be mixed in one condition.

## 1.2 `@v1` can be a branch or a tag
1. **A symbolic ref in `uses:` is ambiguous.** `@v1` can name a branch or a tag.
2. **An attacker can publish a branch or tag that takes precedence over the legitimate one.** The malicious
   action then reaches existing consumers of the action without anyone changing the consumers (zizmor's
   `ref-confusion` entry).
3. **The fix is a commit hash.** `ci-workflow-hardening` §1.1 already says to pin every third-party action to
   a full-length commit; this point adds the reason: a tag is not just mutable, it can also be shadowed by
   a branch of the same name.

## 1.3 Verify
Search the workflows for `github.actor` and for every `uses:` line whose ref is not 40 hexadecimal
characters. Own guidance: open a throwaway pull request from a non-bot account against a scratch copy of
the workflow and confirm the privileged job does not run.
