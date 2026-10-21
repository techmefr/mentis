---
name: incident-communication
description: "Use when something is broken in production and people outside the team need to be told: the first message, the updates while it runs, the one that closes it, the follow-up."
---

# incident-communication

Business layer (`business/README.md`). Two things happen during an incident: fixing it, and telling
people. They compete for the same attention, and the second one gets dropped — which is how a
twenty-minute outage becomes a trust problem.

This block covers only the telling. The diagnosing is `skills/debug`; the internal engineering analysis
afterwards — timeline, contributing factors, action items — isn't a mentis block yet.

## When
As soon as something user-visible is broken, degraded, or wrong in production — not once the cause is
known. The first message goes out before anyone understands the problem.

## Steps

### 1. Separate the roles first
1. **Someone communicates, someone else fixes.** One person doing both does neither, and the updates
   stop exactly when people most want them.
2. **Say who's coordinating**, so questions have a destination instead of interrupting whoever is
   debugging.
3. **Decide in advance which incidents get a public message**, and keep a ready first message. A public
   response guide lists the questions to settle beforehand: which products are affected, how badly, how many
   customers, how noticeable, and whether customers may want a contingency. Symptom: a short false alarm panics
   customers, or a real one goes unannounced because nobody knew whose call it was. Fix: write the criteria down
   with the severity levels and a templated first message.
4. **The writer drafts, the person leading the incident approves before it is posted.** The facts may have
   changed while the message was written. When the writer is unavailable the lead names someone to post.
   A support person who also relays what customers report to the lead is a second use of the role.

### 2. The first message: early and thin
It goes out fast and says very little, and that's correct.
1. **What's affected, from the user's side** — which feature, who notices. Not which service.
2. **That we're on it**, and when the next update comes. A named next-update time is what stops people
   asking.
3. **A workaround if one exists.** This is often the most valuable sentence in the whole incident.
4. **Never speculate on the cause.** The first theory is wrong often enough that publishing it means
   retracting it publicly later. "We're investigating" is honest and complete.
5. **Never promise a fix time** while the cause is unknown — that's a guess wearing a commitment's
   clothes (`business/sales-support` §2).

### 3. Updates while it runs
1. **Update on the schedule you announced, even with nothing new.** "Still investigating, next update
   in 30 minutes" is a real update: silence reads as nobody working. A public response guide also warns
   about the other failure: in a long incident, a stream of updates with no content tires readers, so say
   once that updates will be less frequent, name the next time, and post earlier when the impact changes.
2. **Say what changed**, including narrowing — "not the database, still looking" is progress.
3. **Correct anything you got wrong, explicitly.** Quietly editing a status page destroys the one thing
   it's for.
4. **Stay in the reader's terms.** Internal component names tell them nothing about whether they can
   work.

### 4. Closing it
1. **Say it's resolved and what confirmed that** — which behaviour you verified, not "should be fine
   now". The same guide posts the final message only when the incident lead has confirmed full recovery.
2. **Say what users should do**, if anything: retry, re-enter, ignore duplicates, check their data.
3. **Be explicit about data.** If anything was lost, duplicated or wrong while it was broken, say so
   plainly and say what happens next. Discovering it later is far worse than being told. When nothing was
   lost, say that too, in so many words.
4. **Promise the follow-up only if it will happen**, with a date.

### 5. The follow-up
1. **Describe cause and fix in the reader's terms**, not the engineering write-up.
2. **What was actually changed** so it doesn't recur. "We've added monitoring" with nothing behind it is
   the sentence people learn to distrust.
3. **No blame, and no naming individuals.** An incident that ends with a person named produces silence
   next time, which is the expensive outcome. Public incident guides add three concrete habits: do not call
   a partial degradation an "outage"; do not adjust details so the account looks better; and prefer
   contributing factors (a missing limit, stale documentation) to "human error" as the cause. Keep what
   happened apart from what will be done about it.
4. This is the outward version of the internal analysis, not a substitute for it: the internal one keeps
   the timeline and the contributing factors, the outward one keeps what a reader can act on.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a first message that names impact without
speculating on cause, updates on the announced cadence, a resolution message stating what was verified
and any data consequence, and a follow-up only where one was promised.

## Guardrails
- **Never speculate publicly about the cause.**
- **Never give a fix time you don't have.**
- **Never go silent.** A missed update is the failure mode people remember.
- **Never hide a data consequence**, and never soften it into ambiguity.
- Never publish security-incident detail without whoever owns security and legal — notification duties
  have legal deadlines and specific wording (`business/data-protection`). One public response guide holds
  the external statement until the facts and the timeline are validated and the exposed data is known, then
  asks for it soon after (within days, in its words), with detail on what was exposed and, where possible,
  advance notice to customers' own security teams. Treat that as one company's practice, not a rule.
- Never name individuals as a cause, internally or externally.
- Where the company has an incident process or comms owner, they win; this is the fallback for teams
  without one.

## Origin
Assembled from public sources: standard status-page and incident-communication practice and
blameless-postmortem culture as widely published. 🟡 never run by us; written **without internal
incident-response expertise**, and no internal escalation path or on-call arrangement is described — that
stays out under rule C. Checked on 2026-10-20 against these sources:

| Source | Licence | What it confirmed |
|---|---|---|
| PagerDuty/incident-response-docs, commit 464fc9d (464fc9d3e47e19e9d8da17cec1a41dc09624e95a), `docs/during/external_communication_guidelines.md`, `docs/training/customer_liaison.md`, `docs/before/different_roles.md`, `docs/after/effective_post_mortems.md`, `docs/during/security_incident_response.md` (the external communication part) | Apache-2.0 (LICENSE file read, copyright 2016 PagerDuty, Inc.). Credit: PagerDuty incident response documentation, Apache-2.0; ideas rewritten, no text copied | The coordinator separate from the fixer, criteria for when to communicate, a templated early first message with scope to follow, impact from the customer's side, workaround, never guess or estimate a resolution time, not too much detail, updates stating impact, recovery and next update time, avoiding content-free updates in long incidents, resolution only after confirmed recovery with data loss stated or its absence, blameless review, no "human error", no "outage" unless true, no adjusted details, security statement after validation |
| Atlassian, "Incident communication best practices" (atlassian.com/incident-management/incident-communication), read raw | Atlassian site terms, no open licence; facts only | Pre-planned channels, a dedicated status page as the source of truth, update cadence planned in advance. Its claim that silence costs more trust than the outage is a vendor assertion and is not carried as fact |

Not carried: every figure (5-minute posting, 20-minute update cadence, 2-hour long-incident threshold): the guide gives them as its
own company's choice. **Still unsourced (our guidance)**: separating communicator from fixer as the rule "most wanted" (the guide
confirms the split but not the weight), correcting a wrong statement explicitly instead of editing it quietly, promising a
follow-up only with a date, and the follow-up written in the reader's terms apart from the internal analysis. The security
detail is one company's practice. Not read: NIST SP 800-61, a regulator's breach-notification page (legal, `business/data-protection`).
Current text of the sources may have changed; check with `skills/source-freshness`.

Independent verification 2026-10-21: 18 checked, 18 matched, 0 corrected, 0 unverified
