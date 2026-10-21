# terraform-ci-delivery-pitfalls §2 — Pipeline gates

A pipeline that reaches `apply` on any path without the gates has the gates only on the paths people remember.

## 2.1 Stages and gates
terrashark's baseline order: format and validate; lint and security scan; plan; policy checks against the plan
JSON; an approval gate; apply from a trusted branch and runner; post-apply drift check and evidence.
1. **Format and validate jobs run `init -backend=false`**, so they need no state access and no credentials
   (terrashark's templates).
2. **Policy checks run on every path that reaches apply.** The sources use `conftest` against `show -json`
   output. A pipeline that claims compliance with no policy stage, or with one that a path can skip, is listed as
   a model mistake (terrashark; terraform-skill).
3. **Production apply sits behind a protected environment with required reviewers.** On GitHub the protection is
   configured in the repository's environment settings, not in the workflow file (the deployment review page
   links to the environment setup and notes that an environment can forbid self-approval of a run you started, and
   that administrators can bypass protection unless the environment blocks it); on GitLab the sources use a
   manual job (terraform-skill; terrashark).
4. **Hardening around the gate** (terrashark): branch protection on the default branch, code-owner review for
   paths that affect production, apply jobs restricted to protected runners, and an audit trail holding the
   approver, the actor, the commit and the runtime version. Atlantis, where used, is restricted to approved pull
   requests and protected branches with its server-side locking on.

## 2.2 Cloud authentication
1. **Use OIDC or workload identity federation, not static cloud keys** (terrashark; terraform-skill). Static keys
   only where the CI cannot issue OIDC tokens.
2. **Pin the trust policy.** Pin `aud` to the exact value for the platform pair, and pin `sub` to a specific
   repository plus branch or environment. A wildcard `sub` such as `repo:*:*` lets any repository assume the role
   (terraform-skill).
3. **A mismatched `aud` is rejected with an opaque error. Fix the `aud`; do not relax `sub`** (terraform-skill).
4. **The expected `aud` per pair**, as terraform-skill states it. GitHub's documentation confirms the AWS value
   (`sts.amazonaws.com`, checked as the `aud` condition) and that the Azure login action defaults to
   `api://AzureADTokenExchange`; the GitHub default is otherwise the URL of the repository owner and can be
   set by the action. The GCP row was not checked; the GitLab row was corrected 2026-10-21 against GitLab's page (it does not name `$CI_SERVER_URL`):

| Pair | Expected `aud` |
|---|---|
| GitHub Actions to AWS | `sts.amazonaws.com` |
| GitHub Actions to Azure AD | `api://AzureADTokenExchange` |
| GitHub Actions to GCP | the value passed as the `audience` parameter |
| GitLab CI to AWS | the `aud` set in the job `id_tokens`, equal to the audience of the AWS identity provider (GitLab states it is often `sts.amazonaws.com` or the instance URL) |

5. **The job must be granted `id-token: write`** (at workflow or job level, with `contents: read` if it checks
   out) or no token can be requested; it grants no other write access.
6. **The `sub` format changed for new repositories.** Repositories created after 15 July 2026, and renamed or
   transferred ones, use an immutable subject carrying owner and repository IDs
   (`repo:OWNER@ID/REPO@ID:...`); older ones keep the name-based form unless they opt in. A trust policy copied
   from an old repository then silently matches nothing. Match the format your repository really uses.
7. **A wildcard `repo:ORG/REPO:*` lets any branch, pull request or environment of that repository assume the
   role** (own reading: GitHub's page, read 2026-10-21, does not discuss wildcards, it only requires at least one condition in the trust policy). Scope `sub` to a branch or, better, an environment
   that carries protection rules. Dependabot tokens carry the event name `dynamic`, so restrict event names where
   the provider can.
8. **For reusable workflows from outside your organisation, set `id-token: write` explicitly at the caller** so only
   intended callers get a token; `job_workflow_ref` and `job_workflow_sha` identify the called workflow.
9. Token permissions of the workflow and pinning of the actions it runs are in `ci-workflow-hardening`.

## 2.3 Concurrency and locks
1. **Serialize applies.** In GitHub Actions use a `concurrency` group with `cancel-in-progress: false`, so the
   later run waits and the earlier one is never cancelled mid-apply; GitLab has `resource_group` for the same
   (terraform-skill; terrashark).
2. **The group key decides what is serialized.** terraform-skill's examples key on the ref
   (`terraform-${{ github.ref }}`) or on the matrix environment. Own reasoning, not from the sources: a key on the
   ref serializes only runs on that ref, so when several refs can apply the same state the key has to name the root
   or the state instead.
3. **Set `-lock-timeout` for contended backends.** The default is `0s`, which fails on the first contention; the
   sources use `5m` and `10m` as examples (terraform-skill). The OpenTofu pages say only that the lock is retried
   for the given duration (a number and a unit such as `3s`), with no effect under `-lock=false`; they state no
   default, so the `0s` figure stays terraform-skill's. In GitHub Actions the concurrency group name is
   case-insensitive and a waiting run is replaced by a newer waiting run unless the queue is widened, so a run
   can be dropped silently rather than delayed (GitHub concurrency page). The backend lock itself is in
   `terraform-state-and-secrets-pitfalls` §1.4.
4. **Serialize applies for shared foundation, backend, identity and network roots** (terrashark), and never break a
   lock from the pipeline.
5. **`TF_IN_AUTOMATION: "true"`** is set in the sources' templates; what it changes is not described in them, so no
   claim is made here.
