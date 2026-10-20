# host-config-ansible-nix-pitfalls §1 — Ansible

Source: own craft knowledge; module and keyword behaviour is to be re-read in the documentation of the version in use.

## 1.1 Idempotence
1. **A task states a desired state and reports a change only when it made one.** Prefer the module for the job (package, file, template, service, user, line-in-file) over a shell or command task.
2. **Symptom: the second run still shows changes, or a run is never "green".** Cause: a shell or command task with no way to detect "already done". Fix: add a creation or existence guard, or a real changed-when condition, or replace it with a module.
3. **Use a template or a copy for whole files and a line edit only for a single line you do not own.** Repeated line edits drift into a file nobody can read; one template under version control is the single source.
4. **Declare the end state, not the steps.** "Package present" survives a re-run; "run the installer" does not.
5. **Check:** run the playbook twice on a clean test host. The second run must report zero changes; any change is a defect to explain.

## 1.2 Variables and inventory
1. **Variable precedence has many layers and the winner is rarely the one you expect.** Keep a setting in one place by default (role defaults), override it in one documented layer (group or host variables), and do not use the highest-priority layers casually.
2. **Prefix role variables with the role name** so two roles do not share a name and overwrite each other.
3. **Keep environments as separate inventories with their own group variables,** not one inventory with conditions; a production host must not be reachable from a staging run by a typo.
4. **Facts are collected from the host and can be stale or missing** when fact gathering is off. Do not branch on a fact you did not gather in this run.
5. **Quote values that must stay strings;** the YAML parser turns an unquoted `no`, `on`, `1.10` or a leading zero into other types, a classic source of a wrong file mode or version.

## 1.3 Secrets and access
1. **Encrypt secret variables with the tool's vault feature or an external secret store** and keep the vault password out of the repository. A plain-text secret in a variable file is a leaked secret once the repository is shared.
2. **Stop secrets reaching logs.** Mark tasks that handle them with the no-log option, since task output and verbose runs print arguments.
3. **Write secret files with restrictive owner and mode in the same task that creates them,** so there is no window where they are world-readable.
4. **Use a dedicated connection user with the least privilege escalation it needs,** and keys, not passwords. Pin or verify host keys instead of disabling host-key checking.
5. **Do not put a secret in a command line:** other users on the host see it in the process list. Pass it through a file with a restrictive mode or an environment of the task.

## 1.4 Check mode, diff and testing
1. **Run in check mode with diff and read the output before the real run.** Check mode is a prediction: tasks that depend on earlier changes, or shell tasks, may be skipped or wrong in it.
2. **Test roles on a throwaway host or container** and make that test part of the review; a role tested only on the author's machine meets the real host first in production.
3. **Lint the playbooks in CI** and treat the linter's rule on shell tasks and unnamed tasks as a gate.
4. **Name every task** in plain words; the run output is the log you read at night, and an unnamed task is unreadable there.

## 1.5 Handlers, ordering and rollout
1. **A handler runs once at the end, after the tasks that notified it, only if they changed something.** A failure before the end means the handler never ran and the service keeps the old configuration; force handlers or restart explicitly when the order matters.
2. **A restart that breaks the service ends the run on that host.** Validate the new configuration file with the service's own check command before replacing the old one.
3. **Roll out in batches with a failure threshold** so a bad change stops after one host, not the whole fleet.
4. **Never change the way you reach the host (SSH settings, firewall, network interface) in the same run without a safeguard.** Keep a second path or schedule a revert.
5. **Keep tasks free of assumptions about the first run.** A host that was partly configured by hand must converge to the same state; tasks that fail on existing state are not idempotent.

## Checks
- Modules over shell; a second run reports no changes (§1.1).
- Variables in one layer each; environments separate (§1.2).
- Secrets encrypted, kept out of logs and command lines (§1.3).
- A diff run was read; roles tested on a throwaway host (§1.4).
- Config validated before restart; batched rollout; access path protected (§1.5).
