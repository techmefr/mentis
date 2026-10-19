# § 3 — Resource identity: repeats, refactors, imports, removals, destroys

> Section 3 of `skills/terraform-conventions`. Read it when `count` or `for_each` is added or changed, when a
> resource is renamed, moved into a module, imported or removed, or when anything is destroyed. A resource's
> address is its identity: change the address and the tool sees a deletion and a creation, which for a
> database or a volume is data loss. Every rule here is about not changing identity by accident.

1. **Repeat by key, not by position.** `count` addresses instances by index, so removing an item from the
   middle of a list shifts every later index and plans a destroy and recreate for each. `for_each` over a map or
   a set of strings addresses instances by key, which stays put when others come and go. Use `count` for the
   zero-or-one toggle of an optional resource and `for_each` for everything else that repeats. The set or map
   given to `for_each` must be fully known at plan time, so it cannot depend on an attribute of a resource not yet
   created; derive its keys from inputs.
2. **Treat a rename or a move as a refactor with its own step.** Changing a resource's name, putting it into a
   module, or changing a `count` into a `for_each` changes its address. Declare the move with a `moved` block (from
   Terraform 1.1) so the plan shows a move and no destroy, and check the plan shows zero destroys before applying.
   A text rename without it destroys and recreates. Keep the `moved` block until every environment has applied it.
3. **Bring existing infrastructure under management with a declarative import** (an `import` block; the
   secondary guide's feature table puts it at Terraform 1.5), which is reviewed in the plan like any change, rather than an imperative command that nobody
   reviews. Write the matching configuration, run the plan, and make it show no changes for the imported object
   before treating the import as done.
4. **Stop managing a resource without destroying it with a `removed` block** (Terraform 1.7 per the same table) set to forget
   the object while leaving it in place; the alternative is destroying the real thing. Say which you mean. The
   same applies to removing a provider: resources still in state must be handled first.
5. **A provisioner is the last resort.** The vendor says to exhaust the alternatives first, because Terraform
   cannot model what a script does, it runs only at create (or destroy), and it needs network reach to the
   resource. First use the provider's own resource for the job, then a machine image or configuration management
   tool, then the cloud's startup mechanism. A null resource with a local or remote execution step used to
   bootstrap infrastructure is a smell, and its output may leak a secret into CI logs.
6. **Use `depends_on` only for dependencies the graph cannot see.** An argument that references another
   resource already orders them; an explicit dependency on top forces extra replacements and hides the reason.
   Reach for it when the dependency is real but invisible (a policy attachment the resource needs before it can
   work).
7. **Guard what must not be destroyed.** A lifecycle argument that makes the plan fail instead of destroying a
   resource is cheap insurance on stateful resources (databases, volumes, keys). It guards only while the
   argument is present in the configuration: deleting the whole resource block removes the guard and the destroy
   goes through, which the vendor documents. So pair it with deletion protection set on the cloud resource where
   the provider offers it, and review a diff that deletes a resource block as a destroy.
8. **Read the destroy plan in full before any destroy, targeted or not.** Run the plan in destroy mode first and
   read every resource listed, not only the ones you named: a targeted destroy also removes everything that depends
   on the target, and a `for_each` fed by a local that mentions the target makes every instance a dependent.
   Targeting is for exceptional recovery, not for routine work, because it applies a partial graph. Never confirm
   automatically on a shared environment.
9. **A plan that shows replacements you did not expect is a stop sign.** Read the reason the plan gives (which
   argument forces replacement). A provider upgrade that suddenly replaces resources is a breaking change; hold
   the upgrade, read the provider's upgrade notes, and do it alone (§4.6).

**Sources:** the vendor's documentation on `for_each` (known-at-plan requirement), refactoring with `moved`
blocks (Terraform 1.1, stated on that page), import and removed blocks (the text read states no version
floor), `depends_on` (a last resort), the lifecycle page (`prevent_destroy` and its limit), provisioners
(exhaust alternatives first), the plan command's destroy mode and `-target` warning, read 2026-10-02; the open terraform-skill guide (Apache-2.0) for
the count-versus-key identity reasoning and the destroy-cascade case through locals. Version-bound: `moved` 1.1,
`import` 1.5 and `removed` 1.7 from the secondary guide only; confirm on the runtime in use. The
`depends_on` clause of point 6 follows the vendor's "last resort" wording; the added example is ours.
