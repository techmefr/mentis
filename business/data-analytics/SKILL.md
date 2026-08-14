---
name: data-analytics
description: Use when working against a real data landscape for reporting, dashboards, KPIs or extraction, especially when it is split across several independent systems of record rather than one warehouse.
---

# data-analytics

Business layer (`business/README.md`). For the mechanics of writing SQL well, defer to whatever
stack skill applies (`skills/*-conventions`, a query tool); this block is about the shape of the
data *landscape* itself — the thing that has to be understood correctly before a query is safe to
trust.

**This is not a substitute for the company's own data engineering expertise.** It's the set of
questions and defaults that keep an AI-assisted query from being confidently wrong about a landscape
it can't see in full. Where the company has a documented schema, a data dictionary or a governance
policy, that wins outright.

## When
As soon as a task touches reporting, a dashboard, a KPI, an extraction or a consolidation across more
than one data source — before the first query is written, not after it returns a plausible-looking
number.

## Steps

### 1. Map the landscape before querying it
1. **Name every system of record involved** and how they relate: is there one authoritative database
   per business entity/tenant (common after an acquisition-heavy growth strategy, a franchise model, or
   any multi-subsidiary structure), one shared operational database (a CRM, an ERP) common to everyone,
   or both? Each shape has different failure modes — don't assume the "one big warehouse" model without
   checking.
2. **Never assume an identifier is universal** across independent instances of the same schema. When
   the same database schema is deployed once per entity/tenant (same table names, same column names,
   *different* underlying data), the same code or ID in two instances can mean two different real-world
   things. Trace which instance a value came from before joining or comparing it across instances — the
   schema being identical is exactly what makes this trap easy to fall into.
3. **Look for a central crosswalk/reference table** before hand-rolling entity matching across systems.
   A landscape with several systems of record for the same business entities usually has (or needs) one
   pivot table mapping each entity to its identifier in every system — the CRM's ID, the per-tenant
   database's name, the reporting layer's key. That table, not a fuzzy name match, is the source of
   truth for "which record in system A corresponds to which record in system B."
4. **Distinguish the systems of record from the restitution/reporting layer.** A layer built purely of
   views over other systems (no data stored locally) is a convenience, not a mandatory hop — dashboards
   and queries can usually reach the underlying systems directly when the reporting layer's shape
   doesn't fit the need. Don't treat "go through the reporting layer" as a hard rule unless the company
   says it is.

### 2. Document tables as a usage guide, not a schema dump
1. **A full column-by-column schema reference and a "which table for which need" usage guide are two
   different documents** — keep them separate. The schema reference answers "what does column X mean";
   the usage guide answers "which table, on which system, for this business question," with the table's
   role in one sentence, its handful of BI-relevant key columns (not the full column list), and its
   common joins. Most day-to-day querying only needs the second one.
2. **State the join, not just the foreign key name**, for anything non-obvious: which column on which
   side, and what real-world relationship it encodes. A join list that only names columns forces every
   reader to re-derive the relationship each time.
3. **Write down known weaknesses of the landscape once**, and don't rediscover them every conversation:
   which source has poor data quality, which consolidation is fragile and needs manual upkeep on every
   new entity, where there's no data catalogue or lineage. A landscape's weaknesses are usually already
   known to the team that lives with it — ask, then keep the list somewhere queries can reference it.
4. **Name a data-quality problem by its actual dimension** rather than a vague "the data is bad" —
   accuracy (wrong value), completeness (missing value), consistency (the same fact disagrees across
   systems), timeliness (right value, stale), uniqueness (the same entity duplicated), validity (a value
   outside its allowed domain). A source flagged simply as "unreliable" gives a query-writer nothing to
   act on; "this source is complete but frequently inconsistent with the ERP on this field" tells them
   exactly which check to add.

### 3. Consolidation across independent instances
1. **A `UNION ALL` view across N independent per-entity databases is a real technique, and a fragile
   one**: it needs manual maintenance every time a new entity is added (a new acquisition, a new
   tenant), and its performance degrades as N grows, because every query touches every instance. Treat
   it as a stopgap whose maintenance cost is visible, not as a permanent architecture, and say so when
   proposing it as the answer to "consolidate this across all entities."
2. **A real analytical need (repeated queries, growing entity count, real-time-adjacent latency
   requirements) is the signal to raise a proper consolidated/warehouse layer**, not to add yet another
   hand-maintained view. Recommending the fragile pattern as a one-off is fine; recommending it as the
   long-term answer without naming the tradeoff is not.
3. **When that proper layer gets built, model it in tiers rather than one flat pile of views/tables.**
   The shape that keeps a growing analytics codebase workable: a **staging** tier that cleans and
   renames each source table one-for-one (no joins, no business logic — every mart pulls through this
   tier, never straight from a raw source), an **intermediate** tier where joins, filters and business
   logic actually happen (organised by business domain, not by source system), and a **mart** tier of
   the final fact/dimension tables a dashboard or an analyst actually queries. A business rule
   duplicated across several marts, or a mart joining straight to a raw source table, are both signs a
   tier boundary is being skipped rather than that the modeling is "too heavy" for the need.

### 4. Data-handling invariants
These hold regardless of which system is being queried:

1. **Never modify source data to answer a reporting question.** Reporting is read-only by construction;
   if a fix looks like it requires writing to a system of record, that's a different task with a
   different owner.
2. **Never assume a missing value** — a null, an absent row, an unpopulated field. State that it's
   missing and what that means for the result, rather than substituting a default that makes the number
   look complete.
3. **Every result must be traceable to its source**: which system, which table, which logic produced
   it. A number nobody can explain a week later is a liability, not an insight — this is what makes the
   usage-guide documentation (§2) worth maintaining in the first place.

### 5. KPI and dashboard discipline
1. **Every KPI gets a written definition before it goes on a dashboard**: the exact formula (numerator,
   denominator, filters), the table(s)/logic it's computed from, an owner, a target or acceptable range,
   and how often it refreshes. A number on a dashboard with none of that is a number nobody can defend
   when it's questioned.
2. **Run the decision test on a proposed metric**: what specific action changes based on this number
   moving? If the honest answer is "nothing, it's just interesting," it's a vanity metric — raw page
   views, follower counts, total signups with no context. It doesn't belong on a decision-making
   dashboard; a rate, a ratio, or a trend usually carries the same information in an actionable form
   (page views → conversion rate by source; signups → activation rate).
3. **One metric, one definition, one place it's computed** — the single-source-of-truth rule. The same
   name ("revenue", "active customer") computed two different ways in two dashboards is worse than an
   admittedly-imperfect metric everyone agrees on: it produces a real argument about whose number is
   right when both are technically defensible from their own definition.
4. **A dashboard that shows more than can be read at a glance defeats its own purpose.** Cognitive-load
   research on this is consistent: people track a handful of things at once reliably, not thirty. A
   handful of well-defined KPIs beats a wall of tiles; anything else belongs one click deeper, not on
   the first screen.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: the landscape mapped
(§1) before the first query, a usage-guide-shaped note on any table whose role isn't obvious, the
consolidation tradeoff named explicitly when a `UNION ALL`-shaped fix is proposed, every number
traceable to the table and logic that produced it, and — for a KPI or dashboard — a written definition
(§5.1) that survives being questioned a month later.

## Guardrails
- Never treat an identifier as portable across independent per-entity/per-tenant instances of the same
  schema without checking.
- Never present a fragile hand-maintained consolidation view as a permanent architecture without
  naming its maintenance and performance cost.
- Never put a metric on a decision-making dashboard without running the decision test (§5.2) first.
- Never let the same business term be computed two different ways in two places without flagging it —
  that's the single-source-of-truth rule (§5.3), and it's cheaper to fix before both numbers ship.
- Never guess at a company's data governance, retention or access-control policy — ask the team that
  owns the data landscape, the same way `business/data-protection` routes lawful-basis questions to a
  DPO rather than answering them.
- This block has no dedicated in-house data-engineering expertise behind it yet: a solid set of
  defaults, not proven doctrine, to be confronted with a real analytics engagement.

## Origin
§§1-4 generalised from `xefi-claude-skills` `bi/skills/contexte-xefi` and `bi/skills/main-tables` — a
real BI team's reference material for a landscape of several independent SQL Server instances (a shared
CRM, one database per business entity on an ERP instance, a referential/uniformisation instance, and a
views-only restitution instance), plus a usage guide to its main tables. The real instance names, host
names, entity counts, the ERP's actual French table/column names and the concrete crosswalk table's
real columns are left out per rule C — this block keeps the underlying mechanism: independent
same-schema instances defeat identifier portability, a central crosswalk table is the fix, a usage
guide is a different artefact from a schema dump, `UNION ALL` consolidation across many instances is a
named tradeoff not a free win, and the same read-only/no-assumed-value/traceability invariants the
source stated as absolute.

§3.3 (layered modeling) and §2.4 (data-quality dimension vocabulary) added 2026-08-11 from public
sources, no internal data-engineering expertise behind them: the staging/intermediate/mart layering is
established `dbt`-ecosystem analytics-engineering practice (a source table never queried directly from a
mart, business logic confined to the intermediate tier); the six-dimension vocabulary (accuracy,
completeness, consistency, timeliness, uniqueness, validity) is the commonly-cited core of the
DAMA-DMBOK data-quality framework. §5 (KPI/dashboard discipline) added the same day from published
dashboard-design and KPI-management practice: the decision test against vanity metrics, the
single-source-of-truth rule, and the 5-9-items cognitive-load observation behind "fewer, well-defined
KPIs beats a wall of tiles." Stamped 2026-08-11.
