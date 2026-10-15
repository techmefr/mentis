# incident-comms-pitfalls §3 — Wording and checks

Most of the damage in incident messages comes from a few words and a few omissions, not from the length.

## 3.1 Say what you know, when you know it
1. **Never speculate on the cause in public.** The Guedes runbook states it as the opening rule of its
   communication page, and its checklist repeats it: do not communicate a cause before it is confirmed
   (Guedes runbook).
2. **The public summary is written from the postmortem, not before it.** PagerDuty has the external message
   written as part of the postmortem, reviewed in the postmortem meeting, and only then posted by the support
   team (Guedes runbook, PagerDuty).
3. **Write the symptom in users' terms**, not the names of services or components (Guedes runbook).
4. **State one time zone**, in every message (Guedes runbook).

## 3.2 The word "outage"
1. **Use "outage" only for a full outage.** PagerDuty's postmortem guidance says customers generally read it
   as total unavailability and assume the worst, and suggests "incident" or "service degradation" instead
   (PagerDuty).
2. **That guidance is written for the external postmortem message.** Applying it to status messages is our
   extension, because the reading by customers is the same (own guidance).

## 3.3 Templates and a check before sending
Two shapes, rewritten from the Guedes runbook's status page templates:

```
Investigating  HH:MM UTC
We are investigating reports of SYMPTOM affecting WHO. WORKAROUND, if any.
Next update by HH:MM UTC.
```

```
Resolved  HH:MM UTC
The issue affecting WHO between HH:MM and HH:MM UTC is resolved.
DATA STATEMENT. A summary follows within N days.
```

The intermediate states reuse the same skeleton: what is known, what still works, next update time.

Check before sending (our own list, assembled from §2 and §3.1 to §3.2):
1. A next-update time is present.
2. A time zone is stated.
3. The symptom is in users' terms and no cause is named.
4. The commander has approved the text.
5. The word "outage" appears only if it was one.
6. A resolution message makes a statement about data.

## 3.4 Verify
Run the sequence once as a drill: post an "investigating" message to a test channel from the template, answer
"scoping" with invented facts, let one update interval pass and check that the "still investigating" message
goes out on time and carries a next-update time. A process that was only written down was not tested (own
guidance).
