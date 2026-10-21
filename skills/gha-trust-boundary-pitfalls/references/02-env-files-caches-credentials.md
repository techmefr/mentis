# gha-trust-boundary-pitfalls §2 — Environment files, caches and the checkout credential

Three things carry state across a trust boundary inside GitHub Actions: the environment files a step
writes, the caches one workflow writes and another reads, and the credential checkout leaves behind.

## 2.1 `GITHUB_ENV` and `GITHUB_PATH`
1. **In a workflow with a dangerous trigger** (the page names `pull_request_target` and `workflow_run`),
   writing to `GITHUB_ENV` or `GITHUB_PATH` can be arbitrary code execution (zizmor's `github-env` entry).
2. **Through `GITHUB_ENV`**: an attacker who can set variables or their contents may set `LD_PRELOAD` or
   otherwise cause code to run implicitly in later steps.
3. **Through `GITHUB_PATH`**: an attacker who can add a directory to `PATH` can run code by shadowing an
   ordinary executable such as `ssh`.
4. **Avoid modifying either file in a sensitive, attacker-triggered workflow.** If it cannot be avoided, pass
   no attacker-controlled value into it: literal strings and values computed only from trusted sources.
5. **To pass state between steps, use `GITHUB_OUTPUT` instead** (the same entry).

## 2.2 Caches written by one run and read by another
In a cache-poisoning attack the attacker compromises a cache in one workflow (the "source") and uses it to
pivot into a higher-privilege one (the "sink"). zizmor's page says typical sources are workflows with a
dangerous trigger, or with cache writes enabled, that run external actors' code; typical sinks are release
workflows, which hold valuable credentials or can be used to pivot to other projects.
1. **A release workflow does not read from the Actions cache.** The page's first remedy is to disable
   caching entirely with `cache-mode: none` at workflow or job level, after which no other step in its list
   is needed. The platform's own announcement confirms the setting: it takes `read`,
   `write`, `write-only` or `none`, goes at workflow or job level (the job wins), and a reusable workflow cannot
   get more access than its caller gave. Low-trust events such as `pull_request_target` default to `read`, trusted ones
   such as `push` to `write`; declaring `write` on a low-trust event removes that protection and the platform
   adds a warning annotation. A blocked restore is a plain cache miss, not a failure.
2. **Without that setting**, take the cache out in one of three ways: remove cache-aware actions (such as the
   cache action) from workflows that produce releases; skip them with a step-level `if:` on the trigger; or
   set the action's own input that turns restoration off. The page lists three examples: `lookup-only: true`
   for Swatinem/rust-cache, `package-manager-cache: false` for actions/setup-node and `enable-cache: false`
   for astral-sh/setup-uv. These inputs are as of the page's date.
3. **A cache can be disabled only for the publishing case.** The page's example for a release triggered by a
   tag turns the cache on only when the ref is not a tag:

```yaml
with:
  enable-cache: ${{ !startsWith(github.ref, 'refs/tags/') }}
```

4. **A privileged trigger does not write a cache.** The audit flags jobs under a dangerous trigger that
   explicitly set `cache-mode: write` or `cache-mode: write-only`; detection of these writes is available
   from zizmor 1.31.0.
5. **Many setup-style actions have caching built in** (the page names setup-node, setup-java, setup-ruby,
   setup-uv and rust-cache), so a workflow can read a cache without a step that says "cache" (own
   reasoning from that list). The general rule on caches is in the caches subsection of section 1 of `ci-workflow-hardening`.

## 2.3 The checkout credential
1. **By default, checkout persists a credential on disk.** Versions below 6.0.0 of the action store it in
   `.git/config` of the checked-out repository; version 6.0.0 and later store it under `$RUNNER_TEMP`
   (zizmor's `artipacked` entry; the checkout action's own README states the same location change for 6.0.0 and
   that the default is `true`). Authenticated git from a Docker container action needs a runner of version
   2.329.0 or later.
2. **A later step can publish it by accident**, for example by uploading the checked-out directory as a
   public artifact. zizmor notes the newer location is more resistant to this misuse and reports lower
   severity for 6.0.0 and later, but it still calls persisting an unneeded credential non-ideal.
3. **Use `persist-credentials: false` unless a later step needs git operations with the token.** If it is
   needed, say so explicitly with `persist-credentials: true`. The rule is in `ci-workflow-hardening` §1.4
   point 3; this point adds the location change.

## 2.4 Forks restore, they do not save
Runs with read-only cache access, such as fork pull requests, can restore caches but their save step only logs
a warning and succeeds (the cache action's README). A green fork run therefore says nothing about whether
a cache was written; to learn it, look in the cache list, not the job status.

## 2.5 Verify
Search the workflows triggered by `pull_request_target` or `workflow_run` for `GITHUB_ENV` and `GITHUB_PATH`.
Run the release workflow and confirm in the log that no cache is restored. Check each checkout step for
`persist-credentials`.
