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
   configured in the repository's environment settings, not in the workflow file; on GitLab the sources use a
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
4. **The expected `aud` per pair**, as terraform-skill states it (platform documentation not read; re-check):

| Pair | Expected `aud` |
|---|---|
| GitHub Actions to AWS | `sts.amazonaws.com` |
| GitHub Actions to Azure AD | `api://AzureADTokenExchange` |
| GitHub Actions to GCP | the value passed as the `audience` parameter |
| GitLab CI to AWS | matches `$CI_SERVER_URL` |

5. Token permissions of the workflow and pinning of the actions it runs are in `ci-workflow-hardening`.

## 2.3 Concurrency and locks
1. **Serialize applies.** In GitHub Actions use a `concurrency` group with `cancel-in-progress: false`, so the
   later run waits and the earlier one is never cancelled mid-apply; GitLab has `resource_group` for the same
   (terraform-skill; terrashark).
2. **The group key decides what is serialized.** terraform-skill's examples key on the ref
   (`terraform-${{ github.ref }}`) or on the matrix environment. Own reasoning, not from the sources: a key on the
   ref serializes only runs on that ref, so when several refs can apply the same state the key has to name the root
   or the state instead.
3. **Set `-lock-timeout` for contended backends.** The default is `0s`, which fails on the first contention; the
   sources use `5m` and `10m` as examples (terraform-skill). The backend lock itself is in
   `terraform-state-and-secrets-pitfalls` §1.4.
4. **Serialize applies for shared foundation, backend, identity and network roots** (terrashark), and never break a
   lock from the pipeline.
5. **`TF_IN_AUTOMATION: "true"`** is set in the sources' templates; what it changes is not described in them, so no
   claim is made here.
