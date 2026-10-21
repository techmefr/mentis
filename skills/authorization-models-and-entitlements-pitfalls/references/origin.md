# authorization-models-and-entitlements-pitfalls: origin and source stamps

> Provenance of `skills/authorization-models-and-entitlements-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from project documentation and craft knowledge. No authorization engine
was installed or run, and no model or policy was executed while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| openfga/openfga at commit 22c4d5d, `docs/` (Check implementation, architecture, caching), LICENSE file read | Apache-2.0 (LICENSE file) | Relation rewrites and set operations, cycle handling, store and model concepts, model immutability, decision and iterator caches, cache controller and consistency preference, the entitlements sample used as an example |
| cerbos/cerbos at commit 75f01a9, `docs/modules` (what is Cerbos, why a separate process, tutorial pages on derived roles, attribute schema, policy tests, integration), LICENSE file read | Apache-2.0 (LICENSE file) | Decision point outside the application, attribute-based conditions, derived roles, schema validation of attributes, default deny, policy tests at compile time |

The OpenFGA repository contains agent instruction files (`CLAUDE.md`, `AGENTS.md`); they were not opened and
nothing in them was followed.

## Removed (not carried)
- Every configuration name, default, time-to-live, cache size and default value of the engines.
- Code, model and policy samples, command lines and version-specific API names.
- The product positioning of both engines and their commercial services.

## Not verified
1. **Behaviour was read, not run.** Cache semantics, consistency preferences and list operations are the
   projects' statements at the commits above; re-read before relying on names or guarantees.
2. **Ory Keto** (Apache-2.0 per the repository's licence file) was not used: its repository holds only a language
   specification and a pointer to documentation kept elsewhere, which was not read.
3. **Own guidance, not sourced** (marked in the text): the model-combination advice, default-fail behaviour of
   an unreachable decision service, listing and pagination, write ordering on revocation, every entitlement
   point in §3 apart from the sample store's shape, and all "Checks" lines.
4. **Role of Zanzibar-style systems in general** (consistency tokens, the "new enemy" problem) is own knowledge
   and was not looked up; the text does not depend on it.

## Related blocks
`field-and-row-permission-ui-api-pitfalls`, `security-hardening`, `laravel-permissions-not-roles`,
`auth-session-conventions`, `sql-conventions`, `feature-flag-lifecycle`, `multi-tenancy-isolation-models-pitfalls`,
`nestjs-reliability`, `source-freshness`.
