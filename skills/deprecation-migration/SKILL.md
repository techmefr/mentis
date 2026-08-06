---
name: deprecation-migration
description: Use when a system, an API, a DB column or a dependency still in use has to be removed/replaced, frames the decision (advisory vs compulsory deprecation) then picks the progressive migration pattern (Strangler, Adapter, Feature Flag, Expand/Contract), rather than a brutal replacement in a single deployment.
---

# deprecation-migration

Cross-cutting step, before `plan` (4) on a migration/deprecation task specifically: distinct from
`archi` (decisions about new architecture) and from `plan` (breaking down work already framed).

## When
As soon as a task consists of removing, replacing or evolving in an incompatible way a system
already in use (API, DB column, dependency, module): never for a brand-new feature with nothing to
deprecate.

## Steps

### 1. Five questions before deciding
1. Does this system still have **unique value** that nothing else covers?
2. How many **real consumers** depend on it (an actual grep, not an estimate)?
3. Does a **replacement already exist** and is it ready (not merely planned)?
4. What is the **migration cost per consumer** (a mechanical script vs a manual rewrite)?
5. What is the **cost of keeping** the system as-is vs the cost of the migration: if keeping it
   costs less than migrating, don't migrate on principle.

### 2. Advisory vs compulsory deprecation
1. **Advisory**: the consumer chooses their own pace, a warning exists (log, docs, warning) but
   nothing breaks until they've migrated.
2. **Compulsory**: a fixed date/version where the old thing stops working: reserved for cases where
   keeping the legacy becomes a real risk (security, blocking debt), never chosen by default.

### 3. Choose the migration pattern
1. **Strangler**: the new system progressively absorbs the old one's responsibilities, route by
   route/feature by feature, the two coexist for the duration of the switch.
2. **Adapter**: a translation layer makes the old and the new speak to each other without touching
   the consumers: useful when the internal migration has to stay invisible from outside.
3. **Feature Flag**: a controlled switch, instantly reversible if a problem appears: preferred as
   soon as immediate reversibility matters more than code simplicity.
4. **Expand/Contract** (DB schema): add the new column/table → double-write (old + new) → backfill
   the history → switch reads to the new one → delete the old one, **in separate deployments**,
   never in a single deployment that does everything at once.

## Output / checkpoint
Decision documented (advisory/compulsory + pattern chosen) before `plan` (4) breaks the work into
steps: never a replacement in a single commit/deployment for a system with identified real
consumers.

## Guardrails
- Never a brutal removal of a system with active unmigrated consumers, even under a compulsory
  deprecation (a transition window always exists).
- Expand/Contract: every step is a separate, observable deployment, not one single transaction:
  otherwise the rollback becomes as risky as the problem we were avoiding.
- Don't migrate on principle if step 1.5 (cost of keeping vs cost of migrating) leans towards the
  status quo.

## Origin
Rewrite of the `deprecation-and-migration` skill from a market generalist dev skill catalogue; the
5-question checklist and the 4 patterns (Strangler/Adapter/Feature Flag/Expand-Contract) are taken
as-is, rewritten to the mentis template.
