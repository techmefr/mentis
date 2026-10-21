# host-config-ansible-nix-pitfalls: origin and source stamps

> Provenance of `skills/host-config-ansible-nix-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the claims checked against the Ansible, NixOS and Nix documentation on 2026-10-20. Never dogfooded; no playbook or Nix configuration was run while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Ansible documentation pages: playbook variables, handlers, error handling, check and diff mode, strategies, YAML syntax, FAQ | official product documentation, licence not verified, facts only, rewritten, nothing copied, read 2026-10-20 | Precedence layers (§1.2.1), YAML quoting (§1.2.5), no-log and vault (§1.3.1-2), check and diff limits (§1.4.1), handler timing and failure (§1.5.1), batches and failure thresholds (§1.5.3) |
| NixOS manual (first part) and Nix manual flake reference | official product documentation, licence not verified, facts only, rewritten, nothing copied, read 2026-10-20 | Lock contents (§2.1.1), tracked files (§2.1.5), switch, test and boot (§2.4.1), boot-menu generations (§2.4.2), allow-unfree scope (§2.5.1) |
| NixOS/nixpkgs: `COPYING` (read 2026-10-20), `nixos/doc/manual/administration/rollback.section.md`, `nixos/modules/misc/version.nix` (option description), `doc/using/configuration.chapter.md` | MIT, Copyright Eelco Dolstra and the Nixpkgs/NixOS contributors, 2003-2026 | Rollback methods and the generations caveat, state-version meaning, unfree and insecure package settings and scope |
| Nix reference manual pages (flake reference, secrets, garbage collection command), nixos.org manual (changing the configuration) | official product documentation, licence not verified, facts only, rewritten, read 2026-10-20 | Lock file contents, tracked files, store readable by all, switch versus test versus boot |
| ansible-lint rule pages (`no_changed_when`, `name`) and index page | official documentation of the linter; its `LICENSE` returned 404 at the path tried, so no licence was verified; facts only | Changed-when and task-name rules |
| The Terraform-only repository named in the review | file-level copyleft | Not opened |

## Removed
- Module names, option names, command spellings, version numbers and example code: not carried, on purpose.
- Container and Kubernetes host setup, configuration tools other than Ansible and Nix, and cloud provisioning: other blocks.

## Not verified
1. **Checked:** variable precedence, handler timing and failure, check and diff mode, batches and failure thresholds, no-log and vault advice, YAML quoting, flake lock and tracked files, switch versus test versus boot, boot-menu generations, allow-unfree scope. **Also checked 2026-10-20:** octal file modes (quote them), shell module guards, world-readable store (Nix manual secrets page), garbage collection and generations, state-version option, force-handlers and unreachable hosts, max-fail threshold example, ignore-errors limits, quote filter in shell tasks, YAML booleans and versions, unfree scope. **Corrections:** the Ansible diff page does not mention the no-log option; the role-variables file can still be overridden by role parameters and extra variables. **Unverified:** impure evaluation, module and option design, linter as a CI gate (the linter's index does not cover CI), host-key advice (the FAQ does not address it), secrets in the process list (the FAQ does not say), reaching the host safely, update-channel support dates. Re-read before relying.
2. **Secret-management tools** for Nix and Ansible are described by category only; none was evaluated.
3. **Two tools in one block:** the sections are independent; a reader using only one can ignore the other.

## Related blocks
`terraform-conventions`, `devops-conventions`, `backup-restore-drill-pitfalls`, `secret-leak-response-pitfalls`, `source-freshness`.
