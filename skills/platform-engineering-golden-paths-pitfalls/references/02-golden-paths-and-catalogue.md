# platform-engineering-golden-paths-pitfalls §2 — Golden paths, catalogue and templates

Sources: the CNCF Platforms White Paper at tag-app-delivery commit cadc776 (the golden-path description), and the software catalog pages (descriptor format, life of an entity, well-known relations, API), the software templates introduction and the adoption pages of the Backstage documentation at commit 64ab86e, read 2026-10-20. "Own guidance" marks craft knowledge.

## 2.1 What a golden path is
1. **A golden path is a bundle: a starting template, documentation and a reusable workflow for one common job.** The white paper's example is a supply-chain workflow for building, scanning, testing, deploying and observing a web application on a cluster, delivered with a project template and documentation. Symptom of a template alone: a repository that builds on day one and nobody knows how to run, change or leave on day thirty. Check: a new engineer ships a change to production from the path without asking the platform team.
2. **One path per common job, not per technology preference** (own guidance). Symptom: eleven templates, three of which nobody maintains. Fix: count active users per path each quarter and retire the ones with none (own guidance).
3. **The path is the secure and compliant default,** so the team inherits scanning, access rules and logging by using it (§1.2).
4. **Name an owner and a version for each path,** and keep a way for existing projects to see that a newer version exists (own guidance). Symptom of copy-once templates: every project drifts from the path after a month and fixes from the platform never arrive. Fix: update by pull request where possible, or a documented upgrade guide.
5. **The path is optional** and its exit is documented (§1.3).

## 2.2 Templates that open reviewed changes
1. **A scaffolding form can create the repositories and open pull requests in the places a team would otherwise edit by hand.** Backstage's introduction describes templates asking for input variables and producing code skeletons, and the adoption pages describe a form that opens requests in several repositories (traffic, infrastructure, manifests) hiding that complexity. Symptom this fixes: bad copy and paste and a forgotten variable, the failures the adoption page names.
2. **Output goes through review like any other change,** so the template does not bypass the approval rules (own guidance). Symptom: a template with a service account that can push anywhere.
3. **Validate inputs in the template** (names, regions, sizes from a list) and show the result before creating (own guidance).
4. **Test the template itself:** generate a project in the pipeline and build it (own guidance). A template that no longer builds is found by users first.
5. **Template actions are code with naming rules of their own;** one example in the documentation is that an identifier with dashes breaks expressions that refer to it. Re-read the tool's rules for custom actions.

## 2.3 The catalogue and its data
1. **Source entries from files kept with the code,** one descriptor per service in its repository, ingested by the catalogue. The Backstage description: a standard descriptor file maintained by the owners, which the catalogue keeps itself current with. Symptom of a hand-maintained spreadsheet or portal form: the adoption page's own example, where a list of repositories and owners falls out of date with each reorganisation.
2. **Every entry needs one owner, and the owner is a team,** not a person. The ownership relation in the documentation is the single owner shown to readers, meant for display; it is explicitly not for deciding authorization in running systems (use the access system, `skills/authorization-models-and-entitlements-pitfalls`).
3. **Ingestion rules should be visible.** The documentation describes providers that feed raw entities, policies and processors that validate and enrich them, and an assembly step before an entity becomes visible. Symptom: an entry the owner registered never shows up. Fix: expose the validation errors to the owner (own guidance).
4. **Removal is eager:** when a provider reports an entity gone, the catalogue deletes it and its derived data. Symptom of a flaky source listing: entries vanish and return. Check what happens when the source is down (own guidance).
5. **Orphaned entities are a signal.** The API documents a query for entries marked as orphans (nothing provides them any more). Review them on a schedule (own guidance on the cadence).
6. **Enforce the file in CI or at creation once adoption plateaus.** The adoption pages say incremental adoption stalls, new projects are not listed, and something must change; the section on enforcement was an unfinished placeholder at the commit read (§3.1).

## 2.4 What goes in the catalogue
1. **Only what someone asks for:** owner, lifecycle, docs link, runbook, on-call, dependencies, API (own guidance).
2. **A field with no reader gets filled with rubbish.** Remove fields nobody queries (own guidance).
3. **Show it where people already work:** the adoption pages stress the portal brings information together but does not replace the tools for deep work.

## 2.5 Checks (own guidance)
1. Pick ten random services: owner correct, docs link alive, last deploy path shown. The failure rate is the number to report.
2. For each path: generated project builds, deploys to a test environment, and a stranger can follow its documentation.
