# terraform-hcl-authoring-pitfalls §3 — Lifecycle and delivery

The `lifecycle` block changes what Terraform does when a resource must be destroyed, replaced or has drifted. Each
setting is a trade: a guard that can be removed by editing the same file, an order of replacement that needs unique
names, a silence about changes made elsewhere.

## 3.1 `prevent_destroy`
1. **Put `prevent_destroy = true` on what cannot be recreated cheaply**: a production database, the bucket that holds
   state, an encryption key (Terramate). With it set, `terraform destroy` fails with an error that names the
   resource and the setting.
2. **The guard lives in the configuration it protects.** The source's way to destroy anyway is to remove the
   argument from the configuration first, so anything that deletes the resource block, or the argument, removes the
   guard together with the resource. Treat it as protection against an accidental destroy, not as access control
   (Terramate; the reading is ours).
3. **The state bucket is the exception to "put it in the same configuration".** Terramate shows `prevent_destroy` on
   a state bucket; `terraform-state-and-secrets-pitfalls` says never to manage the backend bucket from the root that
   uses it as its active backend. Both hold: protect the bucket with `prevent_destroy` in its own bootstrap root
   (`terraform-state-and-secrets-pitfalls` §1.2).
4. **Preconditions and postconditions state what must hold.** A `precondition` on a resource's inputs and a
   `postcondition` on its result, each with an `error_message`, make the plan or the apply stop with a readable
   reason instead of creating something wrong (Terramate).

## 3.2 `create_before_destroy`
1. **The default replacement is destroy then create.** For a resource that is in use, such as an instance behind a
   balancer when its image changes, that is downtime; with `create_before_destroy = true` the new one is created,
   references are updated, and the old one is destroyed (Terramate).
2. **The source applies it to security groups, IAM roles and launch templates, which are referenced by other
   resources, and gives each a `name_prefix` instead of a fixed `name`** (Terramate). Our reading is that a fixed
   name could not exist twice during the overlap, so replacement would collide; the source does not state the
   reason, and the provider behaviour was not checked (our own guidance).

```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = var.image_id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}
```

## 3.3 `ignore_changes` and `replace_triggered_by`
1. **Ignore only attributes that something else legitimately changes.** The source's cases: tags written by a backup
   or cost tool (the source lists individual tag keys), an autoscaling group's desired capacity, a function's
   code or hash when it is deployed separately, a cluster's version when upgraded outside Terraform
   (Terramate).
2. **`ignore_changes = all` means Terraform only tracks the resource.** The source reserves it for a resource
   managed externally; on a resource Terraform is expected to manage it silences every future drift (Terramate;
   the second half is our reading).
3. **Do not hide a secret behind `ignore_changes`.** The source's database example ignores a password that is
   written into the configuration; a password in configuration is a secret in state and in plan output, and it
   follows `terraform-state-and-secrets-pitfalls` §2, not an ignore rule (our own guidance).
4. **`replace_triggered_by` forces a replacement when a dependency changes**, for example when a hash of the user
   data file changes or a module's output changes (Terramate). No source read states a version floor for it, so
   check the runtime's documentation before using it; the floors the sources do state are in
   `terraform-refactor-identity-pitfalls` §3. Terramate's example uses `null_resource` as the trigger and Babenko
   names `terraform_data` for runtime 1.4 and later (§3.4).

## 3.4 Provisioners and baked images
1. **Do not deploy software to a host with `remote-exec`.** The source's problems: configuration drift between
   instances, rollbacks that need complex state handling, issues that are hard to reproduce. Bake an image (or a
   container image) and replace the instance; the launch template then has no provisioners, and an autoscaling
   group replaces instances with a rolling `instance_refresh` (Terramate).
2. **Choose by goal** (Babenko):

| Goal | Use |
|---|---|
| Instance bootstrap | `user_data` with cloud-init rendered by `templatefile()` |
| Orchestration that re-runs when an input changes (runtime 1.4 and later) | `terraform_data` with `triggers_replace` (a list; `null_resource` uses a `triggers` map) |
| Ongoing operating-system configuration | outside Terraform: Ansible, SSM Run Command or State Manager |
| Last-resort one-shot | `terraform_data` with a provisioner on runtime 1.4 and later, `null_resource` before that |

3. **Know what a provisioner costs.** Babenko lists: non-idempotent (re-runs duplicate side effects), create-only
   (updates do not re-run and `when = destroy` is fragile), `remote-exec` needs SSH or WinRM from the runner to the
   target, no drift detection, and script output leaks to CI logs where `sensitive` does not redact it (Babenko).
4. **Decision where the sources disagree.** Terramate's container example builds and pushes the image from
   Terraform with `null_resource` and `local-exec`; Babenko's costs (no drift detection, output in CI logs) apply
   to exactly that. Build and push the image in the pipeline outside Terraform, and let the configuration take an
   image reference as an input (our own decision from the two sources).
5. **A stateful resource stays mutable, with guards instead of replacement.** The source keeps a database in place
   with `prevent_destroy`, deploys changes from a snapshot where it needs an "immutable-like" update, and leaves the
   password management outside Terraform (Terramate; see §3.3 for the password).

## 3.5 Image references
1. **Reference an image by a specific version, not `:latest`.** The source's sample states it in a comment on the
   container image of a task definition; the version comes from an input such as `var.app_version` (Terramate).
2. **A moving tag makes two applies of the same configuration deploy different things**, and gives the plan nothing
   to show when the tag moves (our own guidance; the source states the instruction, not this reason).
