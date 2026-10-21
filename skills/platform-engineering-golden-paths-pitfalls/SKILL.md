---
name: platform-engineering-golden-paths-pitfalls
description: "Use when a team builds or runs an internal platform for other engineering teams: treating the platform as a product with users, choosing the first capabilities and partner teams, offering a golden path (template plus documentation plus defaults) that stays optional, running a service catalogue with ownership data that does not rot, scaffolding templates that open reviewed changes, measuring adoption and impact, and the adoption plateau where interest fades."
---

# platform-engineering-golden-paths-pitfalls

A defensive block for people who provide shared tooling (deploy paths, environments, templates, a portal) to
other teams inside one organisation. Premise: **an internal platform is a product whose users can walk away, so
the failures are product failures (nobody asked, nobody adopted, nobody maintained the data), not technical
ones**. Tool mechanics are elsewhere: `skills/helm-chart-pitfalls`, `skills/terraform-conventions`,
`skills/devops-conventions`, `skills/ci-workflow-hardening`, `skills/docker-compose-file-pitfalls`; measuring
delivery performance and incidents is `skills/slo-design` and `skills/blameless-incident-review-pitfalls`;
runbooks are `skills/runbook-writing-and-maintenance-pitfalls`; load of a shared service is
`skills/load-and-capacity-testing-pitfalls`.

## When
- A platform or enablement team is formed, or asked to "build the portal".
- A template, a paved road or a service catalogue is designed, or one exists and teams route around it.
- Adoption stalls, leadership asks what the platform delivered, or the catalogue is full of outdated entries.
- Choosing what the platform should provide first, and what to buy or reuse.

## Steps

**Read only the section the task meets.** §1 comes first for a new platform; §3 for a stalled one.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The platform as a product: users, thinnest layer, first capabilities, optional use, support, staffing | a platform is started, scoped or defended | [`01-platform-as-product.md`](./references/01-platform-as-product.md) |
| 2 | Golden paths, catalogue and templates: what a path contains, ownership data, ingestion, scaffolding, upkeep | a template, a catalogue or a portal is designed or rots | [`02-golden-paths-and-catalogue.md`](./references/02-golden-paths-and-catalogue.md) |
| 3 | Adoption, measurement and maturity: milestones, the plateau, metrics, levels per aspect | adoption stalls, a report is due, or a roadmap is planned | [`03-adoption-measurement-maturity.md`](./references/03-adoption-measurement-maturity.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed platform plan owes: the named user teams and what each was asked (§1), the
first capabilities with the evidence they are wanted (§1), for each golden path what it includes, who owns it and
how a team leaves it (§2), the catalogue's source, owner field and staleness rule (§2), and three or four
metrics with a baseline (§3).

## Guardrails
- Interview the teams that will use the platform before choosing what to build. Never start from the tool you
  want to run (§1).
- Provide the thinnest layer over services you can buy or reuse, and keep every capability optional. Never
  force a team onto the platform by decree (§1).
- Ship a path with its documentation, defaults and an owner. Never publish a template with no one assigned to
  keep it current (§2).
- Source catalogue data from the repositories and fail loudly on missing owners. Never maintain a second
  hand-edited list (§2).
- Set a baseline before launch and report the metric that moved with the one that did not. Never report only
  counts of registrations or page views (§3).
- This block restates a CNCF platform white paper, a platform maturity model and a developer portal project's
  documentation at idea level, plus marked own guidance; nothing was run (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten at idea level from the CNCF App Delivery group's platforms white paper and platform maturity model
(Apache-2.0) and the Backstage documentation (Apache-2.0), read 2026-10-20, with own guidance marked in the
references. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
