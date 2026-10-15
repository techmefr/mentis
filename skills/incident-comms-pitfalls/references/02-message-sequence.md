# incident-comms-pitfalls §2 — The message sequence

A customer who hits a symptom, checks the status page or social media and finds no sign of awareness will
assume nobody knows. The sequence below is built to remove that gap: early, thin, regular, then closed
explicitly.

## 2.1 First message
1. **It says the incident is under investigation.** The goal is that nobody experiences the symptom, checks
   the status page and finds nothing (PagerDuty).
2. **It is templated end to end**, so posting it is a decision and not a writing task (PagerDuty).
3. **It may be vague on scope, and says that scope will follow** (PagerDuty).
4. **It contains**: the symptom in the users' terms, who is affected, a workaround if there is one, and the
   time of the next update (Guedes runbook).
5. **Timing differs by source and is yours to set.** PagerDuty decides and posts within 5 minutes of starting
   the incident call. The Guedes runbook posts a first message in the incident channel in the first minutes, and
   its checklist publishes the first status update in the 10 to 15 minute window. Write the target down in
   the process (PagerDuty, Guedes runbook).

## 2.2 Second message: scope
1. **Once some scope is known, post a second message** that gives the customer impact, which components or
   functions are affected and which regions. PagerDuty's example is within 5 minutes of the first message
   (PagerDuty).

## 2.3 Updates
1. **Post on the cadence for the severity even when nothing changed**, in the form "still investigating, next
   update at HH:MM" (Guedes runbook; the durrello template says the same).
2. **Each update says what changed in impact or scope, whether recovery or mitigation has started, and when
   the next update comes** (PagerDuty).
3. **Post outside the cadence when the degree of impact changes meaningfully** (PagerDuty).
4. **The figures differ, so decide and write them down.** PagerDuty: at least every 20 minutes from the
   scoping message during the first two hours. Guedes runbook: every 30 minutes for the top severity, hourly,
   then daily. durrello: every 30 minutes or on change (all three sources).
5. **Use a small fixed set of states** so readers can scan: investigating, identified, monitoring, resolved
   (Guedes runbook).

## 2.4 Long incidents
1. **Past about two hours, move to a long-incident model** where updates are less frequent, to avoid
   notification fatigue from content-free updates. When in doubt, notify at the frequency that keeps updates
   meaningful (PagerDuty).
2. **Do not decide this in the first hour.** Say in an update when a long recovery is known, and keep stating
   when the next update will come even when the cadence is reduced (PagerDuty).

## 2.5 Resolution
1. **Post it when the commander has confirmed full recovery**, and confirm it with metrics, not "it seems
   better": error rate, latency, the business metric (PagerDuty, Guedes runbook).
2. **It confirms full recovery and states plainly whether data was lost or corrupted.** If nothing lingers,
   say that too (PagerDuty).
3. **It gives the window**, from HH:MM to HH:MM in the stated time zone, and, if a summary is promised, a
   timeframe for it (Guedes runbook). Promise it only if it will happen (own guidance).
4. **A false alarm with no customer impact may have its investigation message removed**, with the commander's
   approval (PagerDuty).
5. **After resolution, the postmortem process takes over**; it is out of scope here (PagerDuty).
