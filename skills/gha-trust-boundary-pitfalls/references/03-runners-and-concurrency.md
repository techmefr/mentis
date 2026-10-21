# gha-trust-boundary-pitfalls §3 — Optional: self-hosted runners and concurrency

zizmor marks both of these audits as pedantic-only, meaning they are noisy for the average user. They are
real risks, but they belong on a review list, not in a blocking gate. Present them that way.

## 3.1 Self-hosted runners
1. **Self-hosted runners are very hard to secure by default**, which is why GitHub does not recommend them
   on public repositories (zizmor's `self-hosted-runner` entry). The audit is pedantic-only because
   zizmor cannot analyse a runner's configuration itself.
2. **Use them on private repositories only.** Exposing a self-hosted runner to potential public use is always
   a security risk, according to the page.
3. **When a public repository genuinely needs one**, the page lists two mitigations: require manual approval
   for workflows from all external contributors (configurable at repository, workflow or enterprise
   level), and use only ephemeral just-in-time runners, created for one job and destroyed afterwards. It
   says this makes persistence harder, not impossible. GitHub's secure-use page agrees: it advises against
   self-hosted runners on public repositories and notes they are not isolated between jobs like hosted ones.
4. **Runner services from third parties count too**: the audit flags runners provided by services such as
   runs-on and namespace, since they are also client-managed compute.

## 3.2 Concurrency
1. **By default several instances of the same workflow run at once**, even when a new run fully supersedes
   an old one (zizmor's `concurrency-limits` entry).
2. **Two consequences**: a resource-waste vector for attackers, particularly on billed runners; and subtle
   race conditions when artifacts are located by workflow and job identifiers rather than by run
   identifier.
3. **Add a `concurrency` group and set `cancel-in-progress`** to `true` or to an expression that is true in
   most cases. `false` lets separate instances run concurrently:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

4. **Do not cancel a deployment mid-run.** GitHub's concurrency page advises caution with
   `cancel-in-progress: true` for deployments and shows `queue: max` (up to 100 waiting runs, first in first
   out) to process each one in order; the two cannot be combined, and group names are case insensitive.
   Keep release jobs in a group with `cancel-in-progress` false.

## 3.3 Verify
List the runners named in `runs-on` and confirm each self-hosted one is on a private repository or is
ephemeral with approval required. Push twice quickly to a branch and confirm the first run is cancelled.
