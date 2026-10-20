# host-config-ansible-nix-pitfalls: origin and source stamps

> Provenance of `skills/host-config-ansible-nix-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the claims checked against the Ansible, NixOS and Nix documentation on 2026-10-20. Never dogfooded; no playbook or Nix configuration was run while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Ansible documentation pages: playbook variables, handlers, error handling, check and diff mode, strategies, YAML syntax, FAQ | official product documentation, licence not verified, facts only, rewritten, nothing copied, read 2026-10-20 | Precedence layers (§1.2.1), YAML quoting (§1.2.5), no-log and vault (§1.3.1-2), check and diff limits (§1.4.1), handler timing and failure (§1.5.1), batches and failure thresholds (§1.5.3) |
| NixOS manual (first part) and Nix manual flake reference | official product documentation, licence not verified, facts only, rewritten, nothing copied, read 2026-10-20 | Lock contents (§2.1.1), tracked files (§2.1.5), switch, test and boot (§2.4.1), boot-menu generations (§2.4.2), allow-unfree scope (§2.5.1) |
| The Terraform-only repository named in the review | file-level copyleft | Not opened |

## Removed
- Module names, option names, command spellings, version numbers and example code: not carried, on purpose.
- Container and Kubernetes host setup, configuration tools other than Ansible and Nix, and cloud provisioning: other blocks.

## Not verified
1. **Checked:** variable precedence, handler timing and failure, check and diff mode, batches and failure thresholds, no-log and vault advice, YAML quoting, flake lock and tracked files, switch versus test versus boot, boot-menu generations, allow-unfree scope. **Unverified:** the world-readable store, garbage collection and state-version options, impure evaluation, module and option design, idempotence advice on shell tasks, linter gate, host-key and command-line secret advice, octal modes, reaching the host safely. Re-read before relying.
2. **Secret-management tools** for Nix and Ansible are described by category only; none was evaluated.
3. **Two tools in one block:** the sections are independent; a reader using only one can ignore the other.

## Related blocks
`terraform-conventions`, `devops-conventions`, `backup-restore-drill-pitfalls`, `secret-leak-response-pitfalls`, `source-freshness`.
