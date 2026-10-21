# runbook-writing-and-maintenance-pitfalls §2 — Ownership, testing and staleness

Source: own craft knowledge unless a point names a source; PagerDuty incident-response documentation (Apache-2.0), Azure architecture-center (CC BY 4.0) and Prometheus documentation (Apache-2.0), re-read from the source files on 2026-10-20.

## 2.1 Link between alert and page
1. **Symptom: an alert fires and the on-call searches the wiki for 15 minutes.** The alert has no link, or the link goes to a page that moved. Fix: put the link in the alert definition, as code, in the same change that creates the alert (Prometheus alerting rules carry free-form annotations meant for descriptions and runbook links, and annotation values can be templated from the alert's labels, so the link can follow the instance); make it an acceptance check for every page-level alert (`skills/production-readiness-review`).
2. **Use a stable address.** A link to a page title breaks on a rename; a link to an id or a short redirect survives. Check links as part of the review (§2.4).
3. **Keep the page and the alert in one repository or one review** where you can, so a change to the threshold forces a look at the page. Symptom: the alert threshold changed in January and the runbook still quotes the old one.
4. **Every page-level alert maps to a page; every page maps to at least one alert or operation.** Build the table once; it is the inventory (§2.5).
5. **Include the runbook link in the notification and in the dashboard panel** that shows the same signal (`skills/grafana-dashboard-pitfalls`), since the reader may arrive from either. The Prometheus alerting guide asks that alerts link to relevant consoles and make it easy to see which component is at fault, so the two links point at each other.

## 2.2 Ownership and review triggers
1. **Name an owner**: a team and an on-call alias, not a person who may leave. Symptom: nobody updates the page, and nobody is sure whether they may.
2. **Anyone on call may fix a wrong step during the incident.** The owner reviews it afterwards. PagerDuty's on-call page tells responders that if information is hard or impossible to find, they should write it down and keep improving the knowledge base; the page must make that easy (editable, no gatekeeping).
3. **Set review triggers, not only dates.** A date alone passes unnoticed. Triggers worth naming: the service's deploy or infrastructure changes, a dependency's major upgrade, an on-call handover, an alert's rule change, and any incident where the page was used. Add a calendar fallback (own knowledge: for example each quarter; choose what matches how often the system changes, not a copied figure).
4. **Show a "last executed" date and a "last reviewed" date on the page.** Two different things: reading a page and running it. A page with a review date but no execution date is not trusted yet.
5. **Handover includes the runbooks.** When a service changes hands, the new owner executes the main pages with the old owner present (§2.3). PagerDuty's on-call page adds the shift version of the same habit: the outgoing person tells the next on-call about unresolved issues and likely repeats, and a backup shift directly after the primary one lets the previous primary pass context on.
6. **The incident review closes the loop.** Every review's action list says which runbooks need updating or creating, with an owner and a date (`skills/blameless-incident-review-pitfalls` §3).

## 2.3 Testing a runbook by executing it
Azure's ransomware-resilient backup article states that restore procedures, tooling, permissions and runbooks degrade over time as the environment evolves, and that the middle of an incident is the worst moment to find the gaps. Executing is the only test that catches that.
1. **A runbook that nobody has run is a draft.** Execute it end to end, step by step, with someone who did not write it, and nobody typing from memory. Symptom of skipping: the first real run finds a missing permission, a renamed host or a command that no longer exists.
2. **Run it where it is safe.** A staging copy, a rehearsal or a game day. For a step that cannot be run safely (a destructive failover), run it as a tabletop with the commands read out and every prerequisite checked, and mark the page "not executed live" with the date.
3. **Use the page and nothing else.** Observer rule: the author may watch but not help. Every time the executor asks a question, that is an edit. Count the edits; zero edits on a first run is suspicious.
4. **Check the access, not just the steps.** The executor uses the account an on-call would have, not their admin account. Symptom: it works for the author and fails for the person on call.
5. **Time the run and write the time down** as a measurement from the date of the run, not a promise; it shows whether the page fits the recovery objective (`skills/backup-restore-drill-pitfalls`). The same Azure article says regular testing yields measured recovery time and recovery point values that the business can rely on when it sets objectives.
6. **Fix the page the same week.** Merge the edits before the exercise is forgotten, then date the page's execution line.
7. **Test the alert and the page together.** PagerDuty's guidance says an untested alert is as good as no alert. Trigger the alert in a safe way (a test event, a staged fault), see the page link arrive in the notification, and follow it (`skills/chaos-experiment`). A rule unit test (promtool test rules feeds synthetic series through the rule files and compares the alerts that fire) covers the rule's logic, not the notification, the routing or the link, so it does not replace the live trigger.
8. **Rotate the executor.** A page run only by its author keeps the author's blind spots. Next run: a newer team member, under the same rules.

## 2.4 Detecting stale steps
1. **Symptom: a command in the page fails, a hostname does not resolve, a dashboard link 404s, a label names a metric that was renamed.** Nobody noticed because the page is read only during an incident.
2. **Link-check the pages** on a schedule: every internal and external link and every dashboard or query reference. Failing links open a ticket for the owner, not a silent log line.
3. **Extract commands into scripts or a test harness where safe.** Run the read-only ones against a staging environment on a schedule; a non-zero exit is a stale step. Own knowledge: do not auto-run anything that changes state without a guard.
4. **Compare identifiers against the live system**: metric names, alert names, service and host names, flags. A small job that greps the page for identifiers and checks each exists catches renames.
5. **Tie page changes to code changes.** A pull request that renames a metric, a service or a flag lists the runbooks it touches; a reviewer checks the list (`skills/api-change-classification-pitfalls` for the same habit on contracts).
6. **Read the used pages after each incident.** The incident timeline shows which pages the responders opened and which they abandoned; an abandoned page is a candidate for a rewrite.
7. **Date-stamp environment facts** (regions, versions, instance names) so a reader sees how old the facts are. Do not hard-code what a live dashboard or inventory can show.

## 2.5 Retirement and inventory
1. **Keep an inventory**: page, owner, alert or operation it serves, last reviewed, last executed. Build it from the alert definitions so missing pages are visible.
2. **Delete a page no alert or operation reaches**, or merge it into the one that does. Symptom: three conflicting pages for one alert; the reader picks the wrong one.
3. **Leave a redirect, not an empty page**, so old alert links land somewhere useful.
4. **Retire the alert with the page.** A page for a deleted alert, or an alert for a deleted page, means one of them was forgotten (`skills/slo-design`).
5. **Count runbook use**, not quality scores. Pages never opened in an incident, and alerts that are acknowledged without opening the page, show where the real support is missing. Own knowledge: do not turn the counts into a target.
