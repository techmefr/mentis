# devops-conventions: origin and source stamps

> Provenance of `skills/devops-conventions`. Read it when tracing a rule to its source or checking freshness
> (`skills/source-freshness`), never to apply a rule.

Sourced from the 12-factor app (config through environment variables, logs as event streams), DORA
metrics (Accelerate: Forsgren/Humble/Kim: deployment frequency, lead time, MTTR, change failure rate)
and established GitOps/IaC practice. Mechanisms rewritten, no copied text. Market research, no
internal production feedback at this stage.

§2 point 4 (protected shared resources) added 2026-08-11, generalised from the org catalogue's
hard-interdiction skill on protected shared databases — a real rule naming one specific SQL Server
host as never-rename-never-drop. The specific host, the specific business tools it feeds (Sage, a CRM)
and the specific escalation mailbox are left out per rule C; what's kept is the shape that made the
source skill work as a hard rule rather than a wish — forbid by effect not by exact syntax, name the
blast radius explicitly because it's invisible from the SQL statement itself, and require the
escalation to go to the resource's actual owner instead of accepting a user's confirmation as consent.

**Extended 2026-10-02: §5, §6, §7.** The block covered the pipeline and the monitoring but had nothing on
the platform half of transport security, on schema changes, or on running a service under an
orchestrator, which are the three places a delivery goes wrong that a CI file cannot show.

- **§5** is written from the HSTS, TLS 1.3, ACME and CAA RFCs and the OWASP transport-layer cheat sheets.
  It holds no lifetime, version or suite value: those are named by the current specification and a
  maintained server profile, so the section does not go stale. The application-side headers are in
  `security-hardening` §6.
- **§6** rewrites the migration checklist idea of the MIT-licensed `affaan-m/ECC` database-migrations skill
  (read 2026-10-02): compatible changes, concurrent indexes, batched backfills, reversibility, testing on
  a copy. Adapted to MySQL first (state the online algorithm and lock so the statement fails instead of
  choosing a blocking copy), with the PostgreSQL equivalents, and reorganised around the fact that two
  versions of the code run against one schema during a deploy. The tool-specific workflows of that
  source (ORMs, migration runners) are left to the stack blocks.
- **§7** rewrites the Kubernetes pattern ideas of the same repository (probes, requests and limits,
  RBAC, secrets, rollback), reordered by what fails in practice and checked against the Kubernetes
  documentation and the Pod Security Standards. It carries no manifest templates, since a copied
  template ages faster than the reasons behind it.

Not taken: vendor-specific CI and cloud platform guidance (infra reality, rule C), and any numeric default
recited from memory.
