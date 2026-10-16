# data-contract-quality-rules-pitfalls §3 — SLA properties, lifecycle and roles

> Part 3 of `skills/data-contract-quality-rules-pitfalls`. Version-bound: ODCS v3.2.0. Read it when service
> levels or lifecycle fields are written. Sources: the standard's service-level, fundamentals and roles pages
> and its v3.2.0 JSON schema (Apache-2.0); points marked own guidance are ours.

## 3.1 Service-level properties
1. **Each SLA is an entry in `slaProperties`** with a required `property` and a required `value`. A `unit` is
   needed only when the property needs one; days are written d, day or days and years y, yr or years, and the
   page says units use the ISO standard.
2. **The recommended property names come from the Data QoS "periodic table"** and are case-insensitive:
   availability, throughput, errorRate, generalAvailability, endOfSupport, endOfLife, retention, frequency,
   latency, timeToDetect, timeToNotify and timeToRepair. The set is a recommendation: the page says there is no
   limit on the type of properties, and its own example uses `timeOfAvailability`, which the list omits. A
   name outside the list will not be understood by a tool that knows only the list.
3. **Prefer `latency` to freshness.** The page marks latency as preferred. State on which element it is
   measured and the unit, as the page's example does (a value in days on a named column).
4. **`timeToDetect`, `timeToNotify` and `timeToRepair`** express the response to an incident as three separate
   numbers. Fill the three, not one, so that "we are told within a day" and "we fix within a week" cannot be
   confused (own guidance).
5. **`element` says what is measured**, written as an object and element pair. Multiple elements should be
   extremely rare and are comma-separated; with a single object in the contract, the object name is not
   required.
6. **`driver` explains why the SLA exists**: regulatory, analytics or operational. A regulatory driver is a
   reason to give the SLA an owner and a check (own guidance).
7. **`scheduler` and `schedule` work as for quality rules** (part 2 of this block). An SLA nothing measures
   is a statement; say what measures it.
8. **Version 3.2.0 added authoritative definitions and custom properties to each SLA property.** Use the first
   to link the formal agreement or the measurement method. The older `slaDefaultElement` is deprecated since
   3.1.0 and its removal is announced for 4.0.0; use `element` on each entry instead.

## 3.2 Contract header and lifecycle
1. **Required header fields**: `apiVersion` (default v3.2.0 in the documentation), `kind` (the value
   `DataContract`), `id` and `version`. `id` is meant to avoid dataset-name collisions, for example a UUID;
   `version` is the version of the contract, not of the standard.
2. **Bump `version` when the contract changes meaning**, and keep `apiVersion` for the standard's version
   (own guidance, from the two definitions).
3. **`status` has example values, not a closed list**: proposed, draft, active, deprecated and retired. The
   page lists them as examples, and the v3.2.0 schema lists them as examples of a free string; the
   documentation does not mark `status` required, while an earlier 3.1.0 schema file in the same repository
   does. Decide the allowed values and the transitions in the team's own rules, and set `status` in every
   contract.
4. **A deprecated or retired contract still has consumers.** Moving status is a signal to them, not a
   mechanism; pair it with the deprecation path in `deprecation-migration` (own guidance).
5. **Deprecated header field**: `dataProduct` is deprecated since 3.1.0. Do not use it in a new contract.
6. **`description` holds purpose, limitations and usage.** The limitations field is for technical,
   compliance and legal limits on the data's use; write them for the consumer who has not met the producer.
7. **Move older contracts deliberately.** The fields renamed or deprecated across versions (the quality `rule`
   field, `scheduleCronExpression`, `slaDefaultElement`, `dataProduct`) are the first things to search for
   (own guidance).

## 3.3 Roles
1. **`roles` lists the roles that give access to the dataset.** Each entry has a required `role` (the name of
   the IAM role), an optional `access` (the kind of access) and optional first-level and second-level
   approvers.
2. **Approvers are free text**, strings holding names; the page's example puts a placeholder in one of them.
   A name in the file is not a workflow: say where the approval actually happens (own guidance).
3. **Give each role an `id`** when something refers to it, for the same reason as quality rules (part 2).
