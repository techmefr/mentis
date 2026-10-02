# § 4 — Modules, composition, version constraints, the lock file

> Section 4 of `skills/terraform-conventions`. Read it when a module is written or called, or a version is
> bumped. A module is a contract with whoever calls it, and a version constraint is the contract with whoever
> publishes what you call; both fail quietly until a plan surprises someone.

1. **Write a module when it names a concept, not to avoid typing.** The vendor's guidance is moderation: a
   good module raises the level of abstraction by describing a new idea in the architecture (a network, a
   service with its database) built from provider resources. A module that only wraps one resource and passes
   every argument through adds an indirection without an abstraction, and over-use makes the whole
   configuration harder to read and to move around in state.
2. **Keep the module tree flat and compose.** Deeply nested modules are hard to reuse in other combinations.
   A common layering is the resource module (a small group of tightly connected resources), the infrastructure
   module (several of them for one purpose in one region or account), and the composition (the complete
   configuration, which wires modules together and is the only level that sets environment values). Keep the
   lowest level plain, and pass what varies as variables.
3. **A standard module layout:** the files of §1, a readme, a `versions` file pinning the minimum runtime and
   provider versions it supports, an `examples` directory with a minimal and a complete use (which double as
   test fixtures), and a `tests` directory (§5.5).
4. **Every input and output is a typed, described contract.** A variable has an explicit type, a description, and
   a default only when one is reasonable; use the `optional` attribute form with typed defaults (Terraform 1.3)
   in place of an untyped map; mark secrets sensitive (§5.2); validate what the type cannot express. Make a
   variable non-nullable when a null should not silently replace the default. An output has a description and
   exposes a stable subset, not a whole provider object, so a provider upgrade that changes the object's shape is
   not a breaking change for callers.
5. **A reusable module constrains only the minimum versions** of the runtime and providers (a lower bound), so
   its callers keep the freedom to upgrade; **a root configuration constrains both ends** of each provider with
   the pessimistic operator, which allows only the last component to move. That is the vendor's stated split.
6. **Pin modules you do not own to an exact version in production,** and allow a range only when the
   publisher follows semantic versioning with a disciplined release process. An unpinned remote module is a
   change you did not review arriving at the next init. Upgrade modules, providers and the runtime in a pull
   request of their own, never mixed with a functional change, so the plan diff has one cause.
7. **Commit the dependency lock file.** It records the exact provider versions and checksums chosen at init, so
   every machine and every pipeline run uses the same providers. An init that changes it prints a message: review
   the diff and commit it as a deliberate change. An upgrade is an explicit act (the upgrade option of init), not
   a side effect.
8. **Don't read provider values you can pass.** Reaching into a data source or a remote state from inside a
   reusable module makes it dependent on an environment it should not know about; take the value as an input and
   let the composition supply it (§2.5).
9. **Release a module like software:** tag semantic versions, keep a changelog, run the module's tests and its
   examples before publishing, and treat a change to an input name, an output name or a resource address inside
   it as a breaking change (§3.2).

**Sources:** the vendor's documentation on creating modules (when to write one, flat tree and composition), version
constraints (the operators, the best-practice split between reusable modules and root modules, module version
pinning), the dependency lock file, and the style guide; and the community terraform-best-practices and
terraform-skill guides (Apache-2.0) for the resource/infrastructure/composition vocabulary and the stable-output
point, read 2026-10-02. Version-bound: `optional` with defaults needs Terraform 1.3 (secondary guide). Points 8
and 9 are reasoning of ours.
