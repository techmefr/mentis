# Review transports: where the diff comes from, where the findings go

> **A review has two ends, and only these two vary.** In: how the diff reaches the reader. Out: what happens to
> the findings. Everything between — what counts as a finding, the cross-cutting axes, the comment register —
> is the same review whatever the transport, and lives in the agents plus `references/review-axes.md`.
>
> **The local transport is the default.** It needs git and nothing else: no forge, no account, no token, no
> network. A reader that only worked against a merge request would be useless to anyone not on that forge, and
> useless on the change you have not pushed yet.
>
> Cited by: the eight readers and `skills/review`.

## The three transports

| Transport | In | Out | Needs |
|---|---|---|---|
| **Local** (default) | `bin/prefetch_local.py` on a git range | a report you read and fix yourself | git |
| **CI** | same script, on the pipeline's checkout | a report as a job artefact/log, optionally a failing job | git + a runner |
| **Forge** | `bin/prefetch_mr.py` against a merge request | the same report, or inline comments if explicitly asked | git + `glab`, GitLab |

Same dump shape in all three — `mr.json`, `diffs.json`, `discussions.json`, `files/` — so **the reader's
instructions do not change between them**. That is the whole point of the split: one review, three ways in.

## 1. Local: the default, and what most people should use

```bash
python3 bin/prefetch_local.py                 # this branch vs where it forked from
python3 bin/prefetch_local.py origin/main     # explicit base
python3 bin/prefetch_local.py main..feature/x # explicit range
python3 bin/prefetch_local.py --staged        # what you are about to commit
```

Then run the reader for the stack (`aragorn`, `gimli`, `legolas`, `frodo`, `boromir`, `theoden`, `samwise`,
`faramir`) or `elrond` to route by stack, pointing it at the dump. It returns findings — file, line, what is
wrong, the fix where there is one — **and you apply them yourself**. Nothing is posted anywhere, because there
is nowhere to post to.

**This is the mode to use if you generate a lot of code and read little of it.** The reader is not there to
make the code prettier: correctness first, then the cross-cutting axes (an unvalidated input reaching a query,
new behaviour with no test, a control no keyboard can reach, a swallowed failure nobody can diagnose). Run it
before you commit, fix, run it again. The value comes from the loop, not from one pass.

Two habits that decide whether it is useful:

- **Review small ranges.** A reader on 60 files returns a wall of text nobody acts on. `--staged`, or one
  feature branch against its base.
- **Fix or reject, explicitly.** A finding you neither apply nor dismiss is a finding you will read again next
  run and skim past. Rejecting is a legitimate answer — the reader is often wrong about intent, never about
  what the code says.

## 2. CI: the same review, unattended

The pipeline already has the checkout, so the same script produces the same dump. What changes is that nobody
is there to read a chat: the findings go to a file the job publishes, and the job's exit code decides whether
the pipeline cares.

```yaml
# GitLab CI
review:
  image: node:22
  script:
    - npm i -g @anthropic-ai/claude-code
    - git fetch --depth 50 origin "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - python3 bin/prefetch_local.py "origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - claude -p "Review the dump in $MR_SCRATCH, REPORT mode, follow agents/<reader>.md" > review.md
  artifacts: { paths: [review.md], when: always }
```

```yaml
# GitHub Actions
- uses: actions/checkout@v4
  with: { fetch-depth: 50 }
- run: npm i -g @anthropic-ai/claude-code
- run: python3 bin/prefetch_local.py "origin/${{ github.base_ref }}"
- run: claude -p "Review the dump in $MR_SCRATCH, REPORT mode, follow agents/<reader>.md" > review.md
- uses: actions/upload-artifact@v4
  with: { path: review.md }
```

Three rules that keep a CI review from being turned off within a week:

1. **Never fail the pipeline on style.** If the job blocks, it blocks on the categories a human would also
   block on — a real bug, a trust-boundary hole, new behaviour with no test. Everything else is a report.
2. **A model call in CI costs money and time on every push.** Scope it: merge requests only, changed files
   only, and skip it on a branch that is still churning.
3. **The report is written for someone who is not in the conversation.** File, line, consequence. No "as
   discussed above".

Honest status: the local transport is tested (`bin/test_scripts.py`, `bin/test_local.py`); **the CI recipes
above are written, not yet run in a real pipeline**. Treat them as a starting point, not as proven.

## 3. Forge: GitLab merge requests

Everything specific to that transport — the API-first dump, batched searches, restricted scope, REPORT vs
POST, replying in an existing discussion, and the four traps of posting an inline comment — is in
`references/mr-review-plumbing.md`. It is the only transport that can post, and it posts **only** on an
explicit instruction.

**GitHub pull requests are not implemented.** The gap is small and deliberate rather than hidden: `gh` exposes
the same three primitives (`gh pr diff`, `gh pr view --json`, `gh api .../comments` with a `line` + `side`
position), so a `prefetch_pr.py` writing the same four files would make every reader work unchanged. Until
someone needs it, the local transport already covers a GitHub repo — you review before you push, which is
earlier and free.

## Choosing, in one line

Reviewing your own change before it leaves your machine → **local**. Enforcing a floor on everything that
reaches a branch → **CI**. Commenting on someone else's merge request → **forge**.

## Origin
Written 2026-08-06, after the readers were found to assume a GitLab merge request as the only way in — which
made the whole review layer unusable for anyone on another forge, or on a change not yet pushed. The dump
shape was already the right seam: it was invented for the API transport, and it turned out to describe a local
diff just as well, so the local transport is a second producer of the same four files rather than a second
review path. `bin/test_local.py` checks that the position resolver written for the forge transport works
unchanged on a locally produced diff, which is the property the whole design rests on.
