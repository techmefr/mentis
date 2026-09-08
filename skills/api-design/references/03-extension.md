# § 3 — Extension rather than breakage: the "One-Version Rule"

> Section 3 of `skills/api-design`. Read it when an existing contract has to change, and before
> reaching for a new version number.

1. Extend the existing contract with **optional fields** rather than forking a new version for a
   minor change. A second version is not one change, it is two implementations, two sets of tests, two
   places every future fix has to land, and a migration nobody schedules — so the version that was
   cheaper to create than a compatible change is more expensive than it for as long as it exists.
2. A genuinely incompatible change (removing a field, changing a type) goes through
   `deprecation-migration` (Expand/Contract or explicit versioning), never through a silent
   modification of the existing contract.
3. Pagination, sorting, filtering: consistent conventions across the whole API, not reinvented
   endpoint by endpoint. Each reinvention costs every consumer a special case, and the special cases
   are what make a client's shared request layer impossible — which is where the cost lands rather than
   on us.
4. **Additive is only additive if the consumer tolerates the unknown.** A new field is compatible with
   a client that ignores what it does not recognise and breaking for one that validates the payload
   strictly. That expectation belongs in the contract from the start (§1.6), because after the first
   consumer it is no longer ours to set.
5. **Widening a type is not compatible.** Making a field nullable, or letting it hold a new kind of
   value, changes what every existing consumer's parser must accept — and they were written against
   the narrower promise, so the failure is on their side and arrives at whatever moment our data first
   contains the new shape.
6. **Renaming is removal plus addition.** There is no rename that is compatible, and treating it as
   cosmetic is how a "tidy-up" ships as a breaking change: the old name goes through the deprecation
   path while both are served, and the removal happens when the old one has no traffic left.
7. **A version is a promise to maintain the old one.** Introducing one means committing to its
   sunset date, its ownership and the work of keeping both correct; a version created with no plan to
   remove it becomes permanent by default, and the second and third arrive the same way.
8. **A change to what a field *means* is breaking even when the type is unchanged.** Redefining a
   count to include a case it excluded, or a status to cover a new situation, is invisible in the
   schema and changes every consumer's numbers or branches. It goes through the same path as a
   structural change, because a silent one cannot even be detected by the consumer.
9. **Compatibility is verified against the previous contract, not remembered.** The check is
   mechanical — compare the schema you are shipping with the one in production — and the checkpoint's
   "no existing field removed or retyped" is only meaningful if something actually compared them. Done
   from memory, it passes on the change that broke it.
10. **Extension has a limit, and reaching it is a finding.** A contract that has accumulated optional
    fields until nobody can tell which combination is valid has become harder to use than a second
    version would have been; the honest response is a new shape through the deprecation path, not
    another optional field. Say it when you reach it rather than after it.
11. **Deprecation is announced where the consumer will see it**, and being announced is what makes a
    later removal legitimate. A field marked deprecated only in a document nobody re-reads is a field
    still in full use on the day it is removed — which is the outage the whole section exists to
    prevent (`business/release-communication`).
