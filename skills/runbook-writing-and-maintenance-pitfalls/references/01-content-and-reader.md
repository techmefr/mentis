# runbook-writing-and-maintenance-pitfalls §1 — The page and its reader

Source: own craft knowledge unless a point names a source; PagerDuty incident-response documentation (Apache-2.0), Azure architecture-center (CC BY 4.0), Prometheus documentation (Apache-2.0) and the Google Cloud Architecture Framework (CC BY 4.0), all re-read from the source files on 2026-10-20.

## 1.1 The three-in-the-morning reader
1. **Design for a tired stranger.** Symptom: the author finds the page clear and the first user on call gets stuck on the second line. The reader is woken, on a phone or a laptop in a poor place, may be a person from another team, and has no context. Test: hand the page to someone who has never touched the service and watch where they stop.
2. **Open with four things, in this order.** What the alert means in plain words, how bad it is and who is hurt, the first safe action that limits damage (often "stop the bleeding" before "find the cause"), and when to stop and escalate. Everything else is below that block. Fix for an existing page: move the long explanation to a linked background page.
3. **One page for one trigger.** Symptom: a long page for a whole subsystem with a table of contents; the reader searches while the incident runs. Split by symptom, not by component, and name pages after the alert text so a search from the pager finds them.
4. **Short steps, one action each.** Numbered, imperative, one command or click each. Symptom of the opposite: a paragraph with three actions and the reader skips the second one. Put commands in code blocks, ready to paste, with the placeholders in an obvious form and listed at the top.
5. **No assumed state.** Say where to run the command, as whom, with which access, and how to get that access when you do not have it. Symptom: step 1 is "log in to the bastion" and the reader does not have a login. Own knowledge: the access path is the most common blocker; list it in the first block.
6. **Plain words, no private jargon**, and spell out every acronym once. The reader may be a new hire or a different team.

## 1.2 Steps that can be followed
1. **Every step has an expected result.** "Run X; you should see Y." When the result differs, the next line says what to do: a branch, an escalation, or "stop". Symptom: the reader sees something unexpected and has nothing to compare to, so they guess.
2. **Name decision points and the data that decides them.** "If the queue depth is above N and falling, wait; otherwise go to step 6". A decision that needs judgement names who makes it. Quote thresholds from the same source as the alert, so the page and the alert cannot disagree (§2.1).
3. **Check before you change.** Read-only steps (confirm the symptom, the scope, the last deploy) come before any step that modifies. Symptom: the first action is a restart that destroys the evidence.
4. **Tell the reader what not to do** where a common wrong move exists: do not delete the volume, do not restart both replicas at once.
5. **Link, do not copy, anything that changes elsewhere**: dashboards, the on-call schedule, the escalation policy, a vendor's status page. A copied value is a stale value. Show where the live one is.
6. **Time and cost of each slow or expensive step**, and the wait signal ("takes about 10 minutes; progress shows in this view"). Symptom: the reader aborts a healthy long operation after two minutes.

## 1.3 What a runbook for an alert needs
PagerDuty's alerting principles page says an alert needs enough context to act on, and that an alert with neither steps nor a runbook link is not useful. Applying that:
1. **The alert carries the link.** The alert's body or its service configuration points to the page. PagerDuty's crisis documentation describes attaching runbook links to the service itself; whatever your tool, the link travels with the page, not in someone's memory.
2. **The page restates the alert's condition**, in words and with the query or rule name, so the reader can tell whether the alert is still accurate. Link to the rule's source (`skills/prometheus-rules-and-promql-pitfalls`).
3. **The page says what "resolved" looks like**: the metric back to normal, the symptom gone for users, and whether the alert resolves by itself. PagerDuty's alert-testing guidance names the same three checks for alerts: threshold, no-data condition and automatic resolution; the runbook should say which of them applies.
4. **The page covers the "no data" case** when the alert can fire because a signal stopped, since that is a different problem from a bad value.
5. **A page-level alert without a first safe action is a candidate for a ticket-level alert**, not for a longer runbook (`skills/slo-design`). Both sources behind this: PagerDuty defines an alert as something that needs a human to act, says anything that wakes a person at night must be immediately actionable, and gives a four-level scheme (immediate, business hours, low priority, notification only); the Prometheus alerting guide says to avoid pages where there is nothing to do.
6. **Say why the page waits before it fires.** An alert rule can hold a condition for a set time before it fires (the pending state), so the page should state that delay and what the reader may already be missing; and a rule can keep an alert firing for a set time after the condition clears, which the Prometheus rule documentation names as the way to avoid flapping and false resolutions caused by missing data. The page's "resolved" line (point 3) should match whichever the rule uses.

## 1.4 Danger, rollback and escalation
1. **Mark every destructive, irreversible, customer-visible or costly step** with a clear label before it, and say how to undo it or that it cannot be undone. Symptom: a step that drops a cache table is step 4 of 9 with no warning.
2. **Give a rollback or abort for every change.** If none exists, say so and say who must approve it first.
3. **Name the escalation path in the first block**: who, in what order, how to reach them, and after how long without progress. PagerDuty's on-call page recommends a short, stated escalation timeout and a backup person behind the primary; link to the live schedule instead of copying names.
4. **Say when to declare an incident** and hand over to the incident process (`skills/incident-comms-pitfalls` for the customer side, `business/incident-communication` for the arc). A runbook that silently keeps the reader in "fix mode" delays that call.
5. **Record what was done.** One line telling the reader where to note the actions and times, since the review will need them (`skills/blameless-incident-review-pitfalls`).

## 1.5 Recovery and rarely run procedures
1. **Rarely run means the page is the only memory.** Azure's guidance on backups says to define the recovery process in a team runbook and to practise it, and its ransomware-recovery article says runbooks, templates and approval flows make recovery repeatable whoever is available. Include the approvals, the people to wake and the access they need.
2. **Keep a copy where the failure cannot reach it.** A runbook stored only on the system that is down cannot be read. Check by opening it from a laptop with no access to the failed environment (`skills/backup-restore-drill-pitfalls`).
3. **Prefer a script that does the step over a page that describes it**, once the step is stable. The page then says when to run it, what it changes and how to check the result. A script is also testable on a schedule (§2.4). Own knowledge: do not automate a step nobody understands yet.
4. **A runbook for incident response lists, per stage, the steps, the tools and resources, and the contacts, and is reviewed regularly** (Google Cloud Architecture Framework, operational excellence, managing incidents: communication, triage, investigation and resolution are the stages it names).
