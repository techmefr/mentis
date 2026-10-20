# host-config-ansible-nix-pitfalls: origin and source stamps

> Provenance of `skills/host-config-ansible-nix-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge. Never dogfooded; no playbook or Nix configuration was run while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None opened. The only repository the review listed is Terraform-only under a file-level copyleft licence and was not opened | n/a | Nothing taken |

## Removed
- Module names, option names, command spellings, version numbers and example code: not carried, on purpose.
- Container and Kubernetes host setup, configuration tools other than Ansible and Nix, and cloud provisioning: other blocks.

## Not verified
1. **Every behaviour stated** (variable precedence being layered, handler timing, check-mode limits, flake lock and tracked-file behaviour, world-readable store, generation rollback and garbage collection) is general knowledge and was not checked against current documentation or run. Re-read before relying.
2. **Secret-management tools** for Nix and Ansible are described by category only; none was evaluated.
3. **Two tools in one block:** the sections are independent; a reader using only one can ignore the other.

## Related blocks
`terraform-conventions`, `devops-conventions`, `backup-restore-drill-pitfalls`, `secret-leak-response-pitfalls`, `source-freshness`.
