# host-config-ansible-nix-pitfalls §2 — Nix and NixOS

Source: own craft knowledge, with the points marked "NixOS manual" or "Nix manual" checked on 2026-10-20 against the official pages, read for facts only and rewritten in our words; their licence was not verified. Command, option and flake behaviour is to be re-read in the documentation of the version in use.

## 2.1 Pinning and reproducibility
1. **Pin every input and commit the lock file.** A flake lock records exact revisions; an unlocked or regularly overwritten lock gives a different system tomorrow from the same code. (Nix manual, flake reference page re-read 2026-10-20: inputs are usually unlocked in the flake file, the lock file is JSON whose entries carry the locked details, including a content hash, beside the original specification, and one subcommand adds missing entries while another refreshes the file.)
2. **Update inputs as a deliberate change** (one input at a time where possible) with a build and a diff of what changed, not as a side effect of another edit.
3. **Do not mix many package-set revisions casually.** Each extra revision enlarges the closure and the update burden; pull a single package from another revision only with a reason noted next to it.
4. **Symptom: "works on my machine" despite Nix.** Cause: impure access (reading an environment variable, a path outside the repository, the network) during evaluation or build. Fix: remove the impurity, or pass the value as an explicit input.
5. **A flake only sees files tracked by version control.** A new file that is not added is invisible to the build and produces "file not found" errors; add it before building. (Nix manual, same page: for a local git reference, only files tracked by git are visible; uncommitted changes mark the reference dirty and print a warning.)

## 2.2 Writing modules
1. **Express settings as module options with types and defaults** instead of editing large attribute sets by hand; the type check catches a mistake at evaluation, not at boot.
2. **Split a host into small modules by concern** (users, networking, one service each) and compose them per host; a single huge file is the Nix version of a god class.
3. **Prefer the module for a service over hand-written unit files,** and read its options before overriding; the module already handles users, state directories and hardening.
4. **Keep host-specific values (names, addresses, disk layout) in one place per host,** and keep shared modules free of them.
5. **Keep expressions readable:** avoid deep nesting and clever recursion; the next person reads it during an incident.

## 2.3 Secrets and the store
1. **Everything in the Nix store is world-readable.** A secret placed in an expression, a config file built by Nix, or a command line ends up readable by every local user and in every copy of the closure. Nix manual, secrets page (re-read 2026-10-20): every user on the system can read the store, which weakens isolation between services, and secrets can also reach external binary caches; the page advises reading secrets from the filesystem at run time under access control.
2. **Use a secrets mechanism that decrypts at activation time to a path with restrictive permissions,** and reference the path, not the value, in the configuration. The encrypted file may live in the repository; the key must not. The same manual page names this scheme (encrypted in the store, decrypted with proper permissions at activation) as one of the two options, the other being files placed by hand.
3. **Rotate a secret that was ever put in the store,** because garbage collection does not guarantee removal from copies and caches (the manual's secrets page confirms the cache risk; the garbage-collection part is our reading).
4. **Keep binary caches and signing keys under the same care:** a leaked signing key lets someone serve you code your hosts will trust.

## 2.4 Rollouts and rollbacks
1. **Build first, then switch.** Build the new system and inspect what changes before activating it; activate with the "test" form (not made the boot default) on the first try, so a reboot returns to the known good state. (NixOS manual: the switch form builds, makes the result the boot default and applies it; the test form applies it without making it the boot default; the boot form only sets the default for the next reboot.)
2. **Every activation creates a generation you can return to,** but only while the old generation is kept. Check that garbage-collection settings keep enough old generations to roll back to, and that the boot menu lists them. (NixOS manual, rollback section and the reference page of the collection command, re-read 2026-10-20: the boot menu lists earlier configurations, a rollback switch returns a running system to the previous one, and rollback works only for generations that still exist; the collection command removes unreferenced store paths, its delete-old option keeps only the current generation of each profile and so removes the ability to roll back, and an age-based option keeps the generations that were active at the cut-off.)
3. **A change to networking, the firewall or SSH can lock you out.** Keep a console or out-of-band access, and use the remote-deploy tool's rollback-on-failure option where it exists.
4. **Deploy to one host first,** then a group, as with any fleet; a shared module change reaches every host that imports it.
5. **State is not managed by Nix.** Databases, user data and service state live outside the declarative config; back them up (`backup-restore-drill-pitfalls`) and note the state-version option: the option's own description says it records the first release installed so that data from older releases (databases, for instance) stays compatible, that changing it does not upgrade anything, and that most users should never change it after installation.
6. **Disk fills up with old closures.** Schedule garbage collection and store optimisation, but keep the rollback window; a full disk during a build ends the run mid way.

## 2.5 Unfree software, versions and learning curve
1. **Declare unfree or insecure packages explicitly,** and record why; a global allow-all hides which unfree software the host runs. (Nixpkgs manual, configuration chapter, re-read 2026-10-20: the system configuration's package settings do not affect the user-level package commands, which read their own configuration file; unfree packages can be allowed one by one by a list or a predicate function, insecure ones by name and version, and an environment variable allows all unfree packages for a single invocation.)
2. **Check how long a release channel is supported** and plan upgrades before it ends; a pinned old revision stops receiving security fixes.
3. **Introduce Nix gradually** on one host or a development shell first; a team that cannot read the expressions cannot recover a broken host.

## Checks
- Inputs pinned and lock committed; new files tracked (§2.1).
- Modules typed, small and host values isolated (§2.2).
- No secret in the store; secrets decrypted at activation (§2.3).
- Build inspected, tested activation, rollback generation kept, out-of-band access available (§2.4).
- Unfree packages named; channel support date known (§2.5).
