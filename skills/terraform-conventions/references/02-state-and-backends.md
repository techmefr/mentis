# § 2 — State, backends, locking

> Section 2 of `skills/terraform-conventions`. Read it when a backend is chosen or changed, when state is
> split, moved or repaired. State is the tool's memory of what it manages; losing it, corrupting it or letting
> two runs write it at once is the failure mode that is hardest to undo.

1. **Never use local state for anything a team or production depends on.** A remote backend gives one shared
   copy, locking, versioning, encryption and an audit trail. Start with the remote backend from the first
   commit: moving later is possible but is a migration, and a state file in version control is both a leak and
   a conflict machine. The state file is never committed.
2. **State holds secrets in clear text, so protect it like a credential store.** Every value in the
   configuration that ends up as an attribute, including values marked sensitive, is written to state and to saved
   plan files; marking only hides it from the terminal. Encrypt the backend at rest, require encrypted transport,
   restrict who can read the state to the pipeline and a short list of people, log access, and keep backups
   under the same controls. This is why secret handling (§5.2) tries to keep values out of state altogether.
3. **Make the backend enforce locking.** A lock stops two runs writing at once. On the object-store backend
   for AWS the native lock file (the `use_lockfile` argument) replaces the older table-based lock, which the
   documentation now marks deprecated; the native form exists from Terraform 1.10. Other backends have their own
   locking, and some (for example local files) have none. Choose the backend for its locking model, and
   configure the permissions the lock needs (they include writing the lock object).
4. **Separate states for separate lifecycles and separate blast radii.** One monolithic state makes every plan
   slow, every apply risky and every credential powerful. Split by environment first (production and non-production
   never share a backend key or a credential), then by component with an independent lifecycle (network, data,
   compute) or an independent owner. Combine resources that change together. Workspaces alone are not isolation:
   they share a backend and its permissions, so they do not replace separate credentials per environment.
5. **Read another stack's data through a narrow interface.** Reading the whole remote state of another
   configuration couples you to its internals and needs read access to everything in it, secrets included; prefer
   published outputs from a module, a parameter store, or a data source that looks the object up. Keep the remote
   state read for true ownership boundaries between teams.
6. **When a lock is stuck, find out why before releasing it.** A crashed run leaves a lock that is correct to
   clear; a long-running apply on another machine is not. Check who holds it and whether the process is alive,
   then use the tool's force-unlock with the lock id, and never delete lock files by hand or bypass locking with
   a flag to "get unblocked". The same goes for the state itself: never edit the state file by hand; use the
   state subcommands (move, remove) or declarative blocks (§3.3 to §3.5), and take a backup first.
7. **A state operation gets a rollback note.** Before a move, a remove, an import or a backend change,
   record how to undo it and where the pre-change copy of the state is. A backend migration is rehearsed on a
   copy, and the old backend is kept until the new one has completed a clean plan.
8. **Bootstrap the backend itself with care.** The storage that holds the state cannot be created by the
   configuration whose state it holds, so it is created once by a small separate configuration or by hand, with
   versioning, encryption, access control and deletion protection on, and then left alone.
9. **Run a scheduled plan to detect drift, and alert on it; never auto-apply it.** A plan that reports changes
   nobody made means someone changed the infrastructure outside the code (`devops-conventions` §2.1). The
   detailed exit code of the plan command distinguishes no change, failure and changes, so a pipeline can alert
   on the last. Reconciliation is a human decision: either the code or the infrastructure is wrong.

**Sources:** the vendor's documentation on backends and state locking, the S3 backend (lock file, deprecation
of the table-based lock), sensitive data in state, and the plan command; and the open terraform-skill guide
(Apache-2.0) for the state-organisation, lock-handling and drift-alert practice, read 2026-10-02. Points 4
(exact split criteria), 7 and 8 are reasoning of ours, informed by those guides. Version-bound: the native lock
file needs Terraform 1.10 (the secondary guide states it; the vendor page read states only the deprecation); OpenTofu numbers its releases differently, so confirm the floor on the runtime in use.
