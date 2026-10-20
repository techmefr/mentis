---
name: host-config-ansible-nix-pitfalls
description: "Use when writing or reviewing host configuration as code with Ansible or Nix and NixOS: idempotent tasks versus shell commands, inventory and variable precedence, secrets in playbooks, check and diff runs, handlers and ordering, and on the Nix side flakes, pinned inputs, secrets outside the store, and safe rollouts and rollbacks."
---

# host-config-ansible-nix-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for configuring machines rather than provisioning cloud resources. The premise:
**a host configuration is only as good as its second run**: a playbook that works once and changes something
every run hides real changes, a variable defined in five places picks a surprising winner, a secret ends up
readable by every user of the machine, a rebuild locks you out of the host. Cloud and network provisioning are
in `terraform-conventions`; pipelines and monitoring are in `devops-conventions`.

## When
- A playbook, role, inventory or variable file is written or changed.
- A host is declared with Nix, NixOS modules or flakes.
- A configuration run changes more than expected, fails half way, or behaves differently on two hosts.
- Secrets, users or SSH access are managed by the configuration.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ansible: idempotence, modules over shell, variables and inventory, secrets, check mode, handlers, rollout | a playbook or role changes | [`01-ansible.md`](./references/01-ansible.md) |
| 2 | Nix and NixOS: flakes and pinning, secrets and the store, rollouts, rollbacks, garbage collection | a Nix expression, module or deployment changes | [`02-nix-and-nixos.md`](./references/02-nix-and-nixos.md) |

## Output / checkpoint
For a change touching this block: a second run reports no changes, no secret is stored in plain text or readable
by other users, a dry run or build was inspected before applying, the first rollout was a single non-critical
host, and the way back (previous generation or restored file) was tried.

## Guardrails
- Use a module that knows the desired state (§1.1). Never run a shell command that cannot report "unchanged".
- Keep each variable defined in one place with a documented override order (§1.2). Never scatter a setting across files.
- Keep secrets encrypted at rest and out of the world-readable store (§1.3, §2.3). Never commit one in plain text.
- Read the diff before applying (§1.4, §2.4). Never apply an unreviewed run to production.
- Roll out to one host first and test the rollback (§1.5, §2.4). Never change the access path of a host without a second way in.
- Module names, option names and defaults change between versions; re-read the documentation of the versions in use (🟡, nothing here was run).

## Origin
Written from our own craft knowledge of Ansible and Nix practice, with the points listed in the origin file checked on 2026-10-20 against the official Ansible, NixOS and Nix pages (facts only, licence not verified). No source text was taken (the one repository the
review found is Terraform-only and file-level copyleft, and was not opened). See [`references/origin.md`](./references/origin.md).
