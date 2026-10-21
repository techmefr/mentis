# terraform-state-and-secrets-pitfalls §3 — Backend migration

Moving state is a one-command operation and the wrong command looks like it worked. The checks below are what
separate a migration from a state that quietly went missing.

## 3.1 Pick the command
| Goal | Command | What it does |
|---|---|---|
| Move existing state to a new backend | `init -migrate-state` | Offers to copy the existing state to the new backend (terrashark; terraform-skill; OpenTofu init page: it may prompt about workspace states, and `-force-copy` skips the prompts and implies it) |
| Accept the configured backend without migrating | `init -reconfigure` | Does not migrate (the OpenTofu init page says it disregards the existing configuration and prevents migration, read 2026-10-20); terraform-skill describes the result as a new empty state, then resources are imported or recreated |

1. **Use `-migrate-state` when moving state; use `-reconfigure` only when you mean to accept the new backend
   without carrying the old state over** (terrashark).
2. **`-reconfigure` after a backend change is how state appears to be lost.** Own reasoning from the two rows
   above: against an empty state, every resource the configuration declares looks new, so a plan proposes creating
   all of it. If a plan suddenly wants to create everything after a backend edit, check which command ran.

## 3.2 Guardrails
1. **Do not combine a backend migration with unrelated resource changes** (terrashark).
2. **Freeze applies for the affected state** before migrating (terrashark).
3. **Pull and securely store a state backup first**, outside the repository, and do not commit it. Keep it until
   rollback is no longer needed (terrashark; terraform-skill).
4. **Record** the current backend type, address and key, workspace, runtime version and who is acting (terrashark).
5. **Migrate the lowest-risk environment first** (terrashark).
6. **Afterwards compare the resource addresses before and after and finish with a no-op plan** (terrashark). A
   plan that shows changes after a migration means something did not move.
7. **Keep the old backend retained and access-controlled** until a restore has been tested or the rollback window
   has passed (terrashark). terraform-skill's own window is 30 to 90 days, which is one source's figure.

## 3.3 The sequence
```bash
terraform version
terraform workspace show
terraform state pull > state-backup.json
terraform state list > state-before.txt
terraform init -migrate-state
terraform state list > state-after.txt
diff -u state-before.txt state-after.txt
terraform plan -detailed-exitcode
```
Use the same runtime (`terraform` or `tofu`) throughout. The state backup can contain secrets (§1.1), so it goes
to a protected location.

## 3.4 Moving, restoring and overwriting
1. **`state mv` works inside one state file only.** To move a resource between state files, remove it from the
   source state and import it in the destination (terraform-skill). Address renames inside one state are in
   `terraform-refactor-identity-pitfalls` §2.
2. **`state push` overwrites the remote state.** It is for disaster recovery, not routine work (terraform-skill).
3. **Restore from a versioned backend object**, push it back, then plan; reconcile any drift with
   `apply -refresh-only` (terraform-skill).
4. **A state written by a newer runtime is refused by an older one.** The fix is to restore a backup or upgrade
   the runtime, not to edit the file (terraform-skill).
5. **Have a recovery note before any destructive state operation**: the missing rollback note is listed as a model
   mistake (terraform-skill).
