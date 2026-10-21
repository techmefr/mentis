# multi-tenancy-isolation-models-pitfalls §1 — Isolation models

All points in this file are own guidance from craft knowledge; nothing was read from a source for it.

## 1.1 The four shapes
1. **Shared tables with a tenant column (row isolation).** Cheapest to run and to migrate, weakest wall: one missing filter leaks, and one large tenant shares indexes and vacuum with everyone. Symptom of outgrowing it: a few tenants hold most rows and every query plan is dominated by them; a customer demands separate backups.
2. **One schema per tenant in a shared database.** Same tables repeated in each schema. Better separation of names and grants, easy per-tenant export, but a migration touches every schema, and catalogue size grows with the number of tenants. Symptom: slow migrations and slow tooling past a few thousand schemas (measure; the number depends on the engine).
3. **One database per tenant.** Strong wall, per-tenant backup, restore, move and encryption keys, and a natural fit for residency. Cost: connection management, migration orchestration and cross-tenant reporting. Laravel specifics are `skills/laravel-tenant-context-by-default`.
4. **One deployment per tenant (silo).** Strongest isolation and independence of versions; highest cost per tenant and a fleet to operate. Fits a few large or regulated customers.
5. **Mixed tiers are normal:** small tenants share rows or a schema, large or regulated ones get a database or a deployment. Decide the promotion path (move a tenant up a tier) before selling the premium tier.

## 1.2 How to choose
1. **Write the requirements per customer class:** number of tenants, size of the largest one against the median, data residency, contractual isolation, need for per-tenant restore, customisation of schema, tolerance for a shared outage.
2. **A table: requirement against model,** and choose the cheapest model that meets every hard requirement. A promise made in a contract is a hard requirement; a preference is not.
3. **Count the migrations cost.** Number of tenants times migration time, and what happens when one fails halfway (§3.3). A model with ten thousand units to migrate needs an orchestrator.
4. **Cross-tenant features are the hidden cost of strong walls:** global search, analytics across customers, a partner portal. Decide how they are built (a separate read model fed from each tenant) before choosing the wall (own guidance on the pattern).
5. **Do not mix models by accident.** Symptom: some tables carry a tenant column inside a database-per-tenant design, with nobody sure which one is authoritative. Fix: one rule stated in the architecture notes, checked in review.

## 1.3 Moving between models
1. **Design identifiers so a tenant can move:** globally unique keys, or keys that include the tenant, rather than sequences that restart per schema.
2. **Rehearse the move on a copy,** with the cutover steps from your migration guidance (`skills/devops-conventions` §6) and a rollback.
3. **Sell the move as a feature only after it has been done once** in production-like conditions.

## 1.4 Checks
1. The requirement table exists and each row names its model, the reason, and the promotion path.
