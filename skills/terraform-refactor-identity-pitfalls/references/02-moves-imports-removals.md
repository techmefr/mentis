# terraform-refactor-identity-pitfalls §2 — Moves, imports and removals

Three blocks tell Terraform that a change of address, of ownership or of management is intentional: `moved`,
`import` and `removed`. Without them the plan reads each of these as a replacement or a deletion.

## 2.1 Renames and restructures: moved
1. **Renaming a resource or a module label, moving a resource into or out of a module, and switching between
   `count` and `for_each` all change the address.** Without a `moved` block the plan shows destroy and create
   (terraform-skill; terrashark).
2. **Add the `moved` block in the same change as the edit and before the first apply**, one block per old address,
   so for a `count` to `for_each` switch one per old index (terrashark).
3. **Read the plan: it must report moves, not replacements.** Apply in a lower environment first (terrashark).
4. **Prefer reviewable `moved` blocks to `terraform state mv` in automation** (terrashark; terraform-skill).
5. **Limits of `moved`** (terraform-skill, stated 1.1+): it cannot cross a provider boundary (use `removed` plus
   `import`), it cannot cross a state file or backend key (see `terraform-state-and-secrets-pitfalls` §3.4), and a
   `moved` block left inside a module that is itself being removed silently stops working, so the resources are
   destroyed. Put the `moved` in the parent.

```hcl
moved {
  from = aws_subnet.app[0]
  to   = aws_subnet.app["a"]
}

moved {
  from = module.network_core
  to   = module.network_foundation
}
```

## 2.2 Adopting existing resources: import
1. **Prefer declarative `import` blocks to the CLI `import` command** (stated 1.5+ for both Terraform and OpenTofu
   in terrashark). They are reviewable and tracked in version control. For several resources, `for_each` works on
   an `import` block (terrashark).
2. **Confirm the remote object matches the configuration shape before importing**, import it at the right address,
   and plan: the result must show no changes. If it shows changes, align the configuration with the real object
   before applying (terrashark).
3. **Remove the `import` blocks after a successful apply**; they are one-time directives (terrashark).
4. **`plan -generate-config-out=<file>` generates configuration for imports**; review it and merge it by hand
   (terraform-skill).
5. **Unknown ownership of an imported resource is a red flag** in a migration (terrashark).

```hcl
import {
  to = aws_s3_bucket.logs
  id = "example-existing-bucket"
}

resource "aws_s3_bucket" "logs" {
  bucket = "example-existing-bucket"
}
```

## 2.3 Leaving management: removed
| Goal | Use | Tradeoff |
|---|---|---|
| Drop from management and destroy the real resource | delete the block and apply | the default path |
| Drop from management and keep the real resource | a `removed` block with `destroy = false` (Terraform 1.7+ and OpenTofu 1.7+, per terraform-skill) | declarative; the resource continues, unmanaged |
| Remove from state by hand | `terraform state rm <address>` | orphans the real resource; only when abandoning it on purpose |

1. **Keep the provider installed until every resource of that provider is destroyed or removed from state.**
   Removing the provider block first leaves the plan unable to resolve the resource type: a hard error
   (terraform-skill). The same holds for provider aliases and modules with several providers.
2. **Two phases when the resource must be destroyed**: delete the resource blocks, keep the provider, plan and
   confirm `destroy`, apply, check `state list` shows none left for that provider; then remove the provider block
   and its `required_providers` entry, run `init`, and expect an empty plan (terraform-skill).
3. **Deleting a resource block with no lifecycle transition is the model mistake the `removed` block exists for**
   (terraform-skill).

```hcl
removed {
  from = aws_s3_bucket.legacy

  lifecycle {
    destroy = false
  }
}
```
