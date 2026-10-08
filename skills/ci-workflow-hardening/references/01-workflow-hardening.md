# ci-workflow-hardening §1 — Workflow hardening

A workflow runs with a token and, often, secrets, on the strength of a YAML file anyone with write access
can edit and on code a stranger can propose. Each rule below says what an attacker or a mistake does when
it is missing.

## 1.1 Pin what you execute
1. **Pin every third-party action to a full-length commit SHA.** A tag or a branch is a mutable reference:
   whoever controls the action's repository can move it, and your next run executes the new code with your
   token. The GitHub documentation calls a full-length SHA the only way to use an action as an immutable
   release. Keep the human-readable version as a trailing comment so a reviewer and an update bot can see
   what the hash means.
2. **A SHA is only trustworthy if it belongs to the repository you meant.** A commit from a fork is
   addressable through the upstream repository's name, so a hash copied from an issue or a blog post can
   point at code the maintainers never published. Take hashes from a tool or resolve them yourself
   from the upstream tags, and let a static analyser check that the hash matches a tag where it can.
3. **Pin reusable workflows the same way**, and the tools a step downloads and runs (a pinned version in the
   command, not the latest). An unpinned `uvx some-tool` in a workflow executes whatever was published
   minutes ago, with the job's permissions.
4. **First-party actions are lower risk, not zero.** The pin matters most for third-party ones; the cost of
   pinning all of them is a bot that proposes the bumps (§3.1).

## 1.2 Least privilege on the token
1. **Set the repository default for the workflow token to read-only on contents**, then raise permissions
   per job where a job needs more. The GitHub documentation recommends read-only as the default because
   anyone with write access to the repository can read every configured secret, so the token is the one
   thing you can still narrow.
2. **Declare `permissions` in every workflow.** Once any permission is listed, the ones not listed drop to
   none, so a top-level `contents: read` is a floor and a job lists only what it adds (`pull-requests: write`
   for the job that comments, `id-token: write` only for the job that publishes).
3. **A quality-gate job verifies, it does not mutate.** Lint, type check and tests need to read the code
   and nothing else. A job that commits, tags or comments back is a separate job with its own, named
   permissions.

## 1.3 Untrusted triggers
1. **`pull_request_target` runs in the context of the base repository's default branch**, with access to
   secrets and a token that can write, while being started by content from outside. The GitHub documentation
   warns that running untrusted code on it can lead to cache poisoning and unintended access to write
   privileges or secrets. The same holds for any trigger that runs in the privileged context.
2. **Do not check out or run the pull request's code in such a workflow.** The documentation states that
   these workflows must not explicitly check out untrusted code, including from forks. Labelling and
   commenting need only the event payload.
3. **The quality gate uses `pull_request`**: it runs the fork's code with a read-only token and no secrets,
   which is everything a lint, type and test job needs.
4. **Set the repository to require approval before workflows run for outside contributors.** It is a
   setting, not a file, which is why it is missing from most reviews.

## 1.4 Script injection
1. **A `${{ }}` expression in a `run:` step is pasted into the shell script before it runs.** A pull request
   title, a branch name or a commit message containing a shell fragment becomes code, with the job's
   permissions. Pull request titles, issue bodies, branch names and commit messages are all
   attacker-controlled strings.
2. **Pass the value through an environment variable and read it as a shell variable.** The GitHub
   documentation names the intermediate environment variable as the preferred approach; using a dedicated
   action instead of an inline script also avoids it.
3. **Check out with `persist-credentials: false`** when the job does not push, so the token is not left in
   the repository configuration for later steps to read.

## 1.5 Caches are an input
1. **A cache entry a low-trust run can write and a trusted job restores is a code injection path.** Release
   and publish jobs do not restore caches, and they do not build: they take an artifact produced by an
   earlier, reviewed job and upload it.
2. **Never put a secret or a token in a cached path.** Key caches on the lockfile hash.
3. **The GitHub documentation lists cache poisoning among the risks of `pull_request_target`;** design as
   if any cache a fork can write is hostile, whatever the current platform default is.

## 1.6 Analyse the workflows
1. **Run a workflow static analyser in CI** (zizmor is the one the sources use), with its version pinned.
   It reports template injection, dangerous triggers, excessive permissions and unpinned references: the
   items above. A new release can add rules, so bump the pin on purpose.
2. **Triage findings, do not silence them wholesale.** A per-line ignore with a reason is fine; a blanket
   ignore removes the check.
3. **Review a pull request that touches CI as a change to the gate.** The watch-list: `continue-on-error`
   or `|| true` added to a check, a deleted step, a narrowed trigger or a new path filter that skips the gate,
   a threshold lowered. Make the paths that define automation require a code owner's review (§3.5).

## Verification
- A scratch pull request whose title contains `$(id)` ran the workflow and the title was not executed.
- The analyser exits 0 on the final tree, and every `uses:` line in the diff ends in a 40-character hash.
- A workflow with no `permissions` block does not exist in the repository.
