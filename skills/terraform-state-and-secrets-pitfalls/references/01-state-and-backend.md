# terraform-state-and-secrets-pitfalls §1 — State and backend

State is what lets Terraform match configuration to live resources. Everything that goes wrong with a backend
shows up later and elsewhere: a plan that wants to recreate the estate, a double apply, a secret read by someone
who never had the secret.

## 1.1 What state is
1. **State is the source of truth for live resource identity and often contains sensitive values.** Backend
   mistakes can leak secrets, orphan resources, disable locking, or make a routine refactor look like a destructive
   replacement (terrashark).
2. **It stores more than resources.** Resource attributes including computed values, variable values and output
   values all land in it, so database passwords, API keys, SSH keys and certificate private keys can be in there
   (terraform-skill).
3. **State readers are secret readers.** Keep backend read and write permissions separate when the platform allows
   it, and keep plan and state exports out of public or broadly readable CI logs (terrashark).
4. **State is not source code.** A `*.tfstate` file in git has no locking and produces merge conflicts, and editing
   it by hand is likely to corrupt it: use `state mv`, `state rm` and import instead (terraform-skill).

## 1.2 The backend baseline
1. **Remote state for every shared, CI or production environment; `local` is a solo prototype only** (terrashark;
   terraform-skill). A local backend has no locking, no backup and no versioning.
2. **Locking on every apply path, encryption at rest and in transit, and versioning or point-in-time recovery where
   the backend supports it** (terrashark).
3. **The backend bucket, container or table and its lock primitives live in a bootstrap root with their own
   lifecycle, never in the root that uses them as its active backend** (terrashark). A root that manages its own
   backend can destroy it. The terraform-skill bootstrap example also puts `prevent_destroy` on the state bucket
   and the lock table; that guard only blocks a plan that destroys them, so it is a second layer, not a substitute
   for the separate root.
4. **Backend credentials never go in checked-in HCL.** Use workload identity or partial backend configuration
   supplied at `init` time (terrashark; terraform-skill). The backend block does not support interpolation or
   environment variables, so the per-run values come through `-backend-config` (terraform-skill).
5. **One state per environment and component, with an access role per environment.** Split the key by environment
   and root (terrashark); workspace-only isolation is listed as a mistake when it replaces backend-level access
   separation (terraform-skill).

## 1.3 S3 specifics
1. **`encrypt = true` alone is SSE-S3**: an AWS-managed key with no per-request audit trail in CloudTrail. Because
   state often holds secrets, pair it with `kms_key_id` pointing at a customer-managed key (terraform-skill).
2. **Native S3 locking, `use_lockfile = true`, is stated as Terraform 1.10+ and replaces the DynamoDB lock table.**
   The lock is a regular object in the state bucket, deleted when the operation ends. Before 1.10, or on an
   existing setup, the table uses a string hash key named exactly `LockID` (terraform-skill). The sources state no
   OpenTofu floor for it. Writing a DynamoDB lock on a 1.10+ runtime is listed as a model mistake.
3. **Migrating the lock mechanism**: set both `dynamodb_table` and `use_lockfile` while workflows still run on
   older versions, then remove `dynamodb_table` once every workflow is on 1.10+ (terraform-skill).
4. **Bucket checks** (terrashark): versioning, encryption, public access block, narrow IAM, a lock mechanism, and
   the state key split by environment and root. terraform-skill adds a TLS-only deny statement and notes that
   `s3:ListBucket` targets the bucket ARN while object actions target `/*`.
5. **Shape of a hardened backend with the per-run key supplied at init:**

```hcl
terraform {
  backend "s3" {
    bucket       = "example-state-bucket"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

```bash
terraform init -backend-config="key=prod/network/terraform.tfstate"
terraform init -backend-config=backend-prod.hcl
```

## 1.4 Locks
1. **A lock is a safety signal, not an inconvenience** (terrashark). It means another operation holds the state, or
   crashed holding it.
2. **Before `force-unlock`, verify the lock holder, the CI run, the process and the timestamp**, and never while an
   apply may still be running. The sources' stale cases are a crashed process, a network interruption or a
   terminated CI job, each verified (terrashark; terraform-skill).
3. **Never `force-unlock` from automation.** A lock that blocks a pipeline should make it fail, not be broken by it
   (terraform-skill).
4. **Do not bypass a lock by deleting lock files by hand** (terraform-skill lists it as an anti-pattern); find out
   why it exists.
5. **`-lock-timeout` defaults to `0s`**: on contention the command fails at once. Set a duration such as `5m` for
   backends that other runs contend for (terraform-skill).
6. **Serialize applies for shared foundation, backend, identity and network roots** (terrashark). The pipeline side
   of this, concurrency groups that wait instead of cancelling, is in `terraform-ci-delivery-pitfalls` §2.3.
