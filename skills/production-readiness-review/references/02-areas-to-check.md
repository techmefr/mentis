# production-readiness-review §2 — Areas to check

> Part 2 of `skills/production-readiness-review`. Read it when the checklist is filled in or reviewed.
> Sources, read 2026-10-20: mercari/production-readiness-checklist, pre-production checklist, listing its areas
> (maintainability, observability, reliability, security, accessibility of information, data storage) and
> their individual checks (MIT); Azure Architecture Center, "Continuous validation..." (CC BY 4.0), for the
> load and failure validation point. Sentences marked "own guidance" are ours. Per-area detail lives in the
> related blocks; the source's thresholds and tool names are not used.

1. **Delivery and change.** The source covers automated build and deploy, rollback, gradual deploy, tests in CI
   and configuration overridable from the environment. Check: a release can be built from a clean checkout; a
   rollback has been performed once, not only described; the deploy does not raise the error rate while it runs;
   an image or artifact is pinned rather than floating (`skills/ship`, `skills/devops-conventions`,
   `skills/feature-flag-lifecycle` §2).
2. **Observability.** The source lists tracing, dashboards, actionable alerts, separation of warnings from
   critical pages, an on-call rotation, playbooks, structured logs with a request identifier and error
   tracking. Check: someone can find one failed request end to end; every alert has an action and an owner;
   critical alerts reach a person who is on call and can acknowledge them
   (`skills/observability-instrumentation` §3 and §4, `skills/slo-design` §3).
3. **Reliability.** The source lists scaling, resource requests and limits, capacity planning, zero-downtime
   deploys, graceful shutdown and degradation, disruption budgets, health probes, timeouts and sensible retries.
   Check: the capacity statement exists with its conditions; timeouts are set on every network call; behaviour
   with a dependency down is known from a test, not hope (`skills/load-and-capacity-testing-pitfalls` §3,
   `skills/chaos-experiment`, `skills/kubernetes-availability-config-pitfalls`).
4. **Validation under load and fault.** The Azure guide treats continuous validation in a production-like
   environment as the way to find faults that only appear under real traffic, and puts load and fault injection
   in the delivery cycle. Own guidance: at the higher levels, require one load run and one fault run with
   written outcomes before launch.
5. **Security.** The source requires a security design review at the upper levels, non-root containers,
   sensitive configuration kept in secret storage and no sensitive data in logs. Check: a threat model exists
   and its findings are closed or accepted; secrets are not in the repository or the image; dependencies are
   current and the supply chain is covered (`skills/threat-modeling-lite`, `skills/security-hardening`,
   `skills/package-manager-supply-chain-pitfalls`, `skills/telemetry-sensitive-data-pitfalls`).
6. **Data.** The source asks that data be recoverable from backup with a defined and tested procedure, that
   point-in-time recovery work at the top level, that operators have minimal privileges with auditable access
   and that databases keep to their maintenance and replication guidance. Check: a restore drill has been run
   against the objectives; who can read or change production data is listed (`skills/backup-restore-drill-pitfalls`,
   `business/data-protection`).
7. **Information about the service.** The source asks for a current design document, a description, owner
   contacts, links to the repository and user documentation and a dashboard that shows the objectives. Own
   guidance: this is what lets a stranger take over at night; keep the minimum, and keep it true
   (`skills/documentation-craft-pitfalls` §3).
8. **Ownership and on-call.** Own guidance: a named team owns the service, has a schedule that covers the hours
   promised, can be escalated, and has access to the production tools it needs. A service with no one on call is
   not at a level that promises availability.
9. **Runbooks for the alerts you created.** Own guidance: every page maps to a runbook with a first safe action
   and a rollback; at least one alert is exercised in a rehearsal before launch.
10. **Dependencies and limits.** Own guidance: list upstream and downstream services, their owners, rate limits,
    quotas, certificate and credential expiries, and what happens when each is unavailable or slow. A hidden
    quota is a launch-day outage.
11. **Customer-facing readiness.** Own guidance: for a public launch, add a status communication path, a support
    route and a statement of what is supported (`skills/incident-comms-pitfalls`, `skills/customer-escalation-pitfalls`).
12. **Cost and shutdown.** Own guidance: an estimate of running cost under expected load, a budget alert, and the
    way to turn the service off or hold it in a safe state if something goes wrong
    (`skills/spend-guard-fail-closed`).
13. **Compliance obligations.** Own guidance: where the service handles personal data, regulated data or an
    audit trail, ask the owner of those obligations whether anything must be in place before launch; this block
    does not answer it and does not give legal advice.
14. **Language and platform specifics.** The source's cloud and tool items (a given monitoring product, a given
    orchestrator's settings) are one organisation's choices. Substitute your own platform's equivalents and keep
    the intent of each item.
