---
name: incident-communication
description: Use when something is broken in production and people outside the team need to be told — the first message, the updates while it runs, the message that closes it, and the follow-up afterwards. Separate from fixing it; both happen at once.
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
   in 30 minutes" is a real update: silence reads as nobody working.
2. **Say what changed**, including narrowing — "not the database, still looking" is progress.
3. **Correct anything you got wrong, explicitly.** Quietly editing a status page destroys the one thing
   it's for.
4. **Stay in the reader's terms.** Internal component names tell them nothing about whether they can
   work.

### 4. Closing it
1. **Say it's resolved and what confirmed that** — which behaviour you verified, not "should be fine
   now".
2. **Say what users should do**, if anything: retry, re-enter, ignore duplicates, check their data.
3. **Be explicit about data.** If anything was lost, duplicated or wrong while it was broken, say so
   plainly and say what happens next. Discovering it later is far worse than being told.
4. **Promise the follow-up only if it will happen**, with a date.

### 5. The follow-up
1. **Describe cause and fix in the reader's terms**, not the engineering write-up.
2. **What was actually changed** so it doesn't recur. "We've added monitoring" with nothing behind it is
   the sentence people learn to distrust.
3. **No blame, and no naming individuals.** An incident that ends with a person named produces silence
   next time, which is the expensive outcome.
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
  have legal deadlines and specific wording (`business/data-protection`).
- Never name individuals as a cause, internally or externally.
- Where the company has an incident process or comms owner, they win; this is the fallback for teams
  without one.

## Origin
Assembled from public sources: standard status-page and incident-communication practice (early
acknowledgement, fixed update cadence, impact stated before cause, resolution confirmed by observed
behaviour) and blameless-postmortem culture as widely published. Written **without internal incident-
response expertise**, and no internal escalation path or on-call arrangement is described — that stays
out under rule C. The separation of the communicator from the fixer, and the framing of "still
investigating" as a real update, are the two rules we'd most want enforced.
