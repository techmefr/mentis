# authorization-models-and-entitlements-pitfalls §3 — Entitlements and plan gating

Sources: the caching page of the OpenFGA repository at 22c4d5d, which uses a sample "entitlements" store (a person is a member of an organisation, the organisation subscribes to a plan, a feature is associated with plans, and the person can access the feature if the path exists) as its worked example, read 2026-10-20. The rest is own guidance, from craft knowledge of paid products.

## 3.1 Two questions, two stores
1. **Permission: may this person do this?** **Entitlement: has this customer bought the thing?** Symptom of mixing them: a plan name appears as a role, or an admin of a customer on the free plan can switch on a paid feature. Fix: check both, in that order of cheapness, and refuse on either (own guidance).
2. **Entitlement belongs to the customer (account, organisation), not to the person** unless the product sells seats. Symptom: a colleague has the feature, another does not, on the same account. Fix: store the plan on the account and derive the person's access from membership, which is the path the sample store walks. The OpenFGA entitlements tutorial goes further and forbids writing a direct person-to-feature grant at all, so access can only be implied through organisation, plan and feature, because otherwise the application must keep direct grants in step on every membership or plan change (tutorial read 2026-10-20).
3. **Tiers that include everything below them need one rule, not three lists.** The tutorial's requirement is that each higher plan includes all features of the lower ones, and it validates the model with a scenario table of every organisation against every feature. Symptom of three hand-kept lists: a feature added to the lowest plan is missing on the higher ones. Check: a test that adds a feature to the lowest plan and asserts every higher plan gains it (the test is own guidance). The tutorial does not say how the inclusion is encoded; read it before copying a shape.
4. **The permission side must not become the feature flag** (`skills/laravel-permissions-not-roles` states the same rule for Laravel). A feature flag is a product rollout switch (`skills/feature-flag-lifecycle`); an entitlement is a commercial fact; a permission is a security fact.

## 3.2 What an entitlement is made of
1. **A feature, the plans that include it, and optionally a limit** (seats, projects, calls per period). Symptom of a boolean-only design: the free tier is "off" and cannot be "on up to three". Fix: model limits as a value with a unit and a period, checked against current use (own guidance).
2. **Resolve the plan to features in one function** and call it everywhere. Symptom: a feature list in the pricing page, another in the API and a third in the billing job. Fix: one source (a table or a model), generated or tested against the pricing page copy (own guidance).
3. **Overrides per customer need an owner and an end date** (a sales deal, an incident credit). Symptom: overrides nobody can explain two years later. Fix: reason, author, expiry, and a report of active overrides (own guidance).
4. **Usage-based limits need a metering path with its own correctness rules** (counting, idempotency, late events); the subscription lifecycle and billing side is outside this block.

## 3.3 Changes of plan
1. **Decide what each downgrade does to existing data before it happens.** Options per feature: keep readable and block creation; keep everything and block new use; archive after a grace period; remove after confirmation (own guidance). Symptom of no decision: the downgrade job deletes data or silently locks the account.
2. **An upgrade takes effect when the payment state says so, and the cache must follow.** Symptom: a customer paid and still sees the lock for the cache lifetime. Fix: invalidate the account's entitlement cache on the plan-change event, and show a "refreshing" state instead of a refusal for a short moment (own guidance; the staleness window is the caching topic in 2.5 of the decision-point file).
3. **A past-due account is a state between plans,** with its own rule (grace, read-only) written in the same table as the plans (own guidance).

## 3.4 Saying no
1. **Return the reason, not a bare refusal.** "Not included in your plan" and "you may not do this" call for different next steps, and the first one is an upgrade prompt. Return a machine-readable code and let the interface choose the wording (own guidance).
2. **Do not reveal paid-only data in the refusal.** The reason code names the feature, not the record (own guidance, same leak rule as `skills/field-and-row-permission-ui-api-pitfalls` §2).
3. **Gate on the server,** and let the interface read the same answer to hide or lock a control (`skills/field-and-row-permission-ui-api-pitfalls` §1).

## 3.5 Checks (own guidance)
1. A table: feature, plans, limit, behaviour on downgrade, cache invalidation event, test. One test per row with the customer on each side of the line.
