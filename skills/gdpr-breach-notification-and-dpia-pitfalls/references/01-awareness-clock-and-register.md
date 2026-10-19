# gdpr-breach-notification-and-dpia-pitfalls §1 — Awareness, clock and register

> Part 1 of `skills/gdpr-breach-notification-and-dpia-pitfalls`. Read it when an incident may involve personal
> data or a runbook is written. Source: Regulation (EU) 2016/679 Article 33(1), (2), (4) and (5), as published in
> the Official Journal (OJ L 119, 4.5.2016), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
> , read 2026-10-19. That is the original publication, not a consolidated or corrected version: read the current
> text before relying on it. Sentences marked "own guidance" are ours.

1. **The clock in the text starts at awareness.** Article 33(1) says the controller notifies the competent
   supervisory authority without undue delay and, where feasible, not later than 72 hours after becoming aware
   of the breach, unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons.
   Own guidance: the case therefore stores one field, the moment the organisation became aware, and computes the
   deadline from it. The figure is taken from the text each time the runbook is reviewed, not from habit.
2. **Who declares awareness is a question for the DPO.** The text uses the word without defining it in the
   article read. Own guidance: the runbook names who records the timestamp and the evidence for it (the alert, the
   message, the ticket), and the DPO decides when a doubtful signal counts. An engineer neither backdates nor
   delays the timestamp to look better.
3. **A late notice carries reasons.** The same paragraph says that a notification not made within the period is
   accompanied by reasons for the delay. Own guidance: the case has a field for the reasons, filled as events
   happen, not reconstructed afterwards.
4. **The risk threshold is the DPO's call.** Whether the breach is unlikely to result in a risk is not decided in
   this block. Own guidance: the engineer supplies facts (what data, how many records, was it readable, who could
   have seen it, is it contained) and the DPO or counsel records the decision and who took it, including a
   decision not to notify.
5. **A processor tells the controller without undue delay.** Article 33(2) says the processor notifies the
   controller without undue delay after becoming aware of a breach. Own guidance, from the receiving side: the
   address that receives processor alerts is monitored, the alert opens the same case, and the controller's own
   awareness timestamp is recorded when the message is read. From the processor side: the escalation path names
   the controller contact, and the hand-off is a recorded event. The contract wording is reviewed with
   `skills/dpa-review-pitfalls` part 3.
6. **Information may come in phases.** Article 33(4) says that where, and in so far as, the information cannot be
   provided at the same time, it may be provided in phases without undue further delay. Own guidance: the case
   tracks a list of facts still open, with an owner each, so each phase is a recorded event and nothing waits for
   a complete picture.
7. **Every breach is documented, notified or not.** Article 33(5) says the controller documents any personal data
   breach, covering the facts, its effects and the remedial action taken, in a way that lets the authority verify
   compliance with the article. Own guidance: one register entry per incident, written even when the DPO decides
   no notice is due; the entry holds the facts, the effects, the actions, the awareness timestamp, the decision
   and its author. A register that only lists notified breaches fails the text as read.
8. **Containment does not wait for the paperwork.** Own guidance: the technical response (revoke, rotate, isolate)
   runs in parallel with the case; the case records what was done and when, because those entries feed the
   remedial-action part of the register and the measures part of the notice (part 2).
9. **Drill it.** Own guidance: a dummy incident exercises the whole path (alert, case, awareness timestamp,
   processor message, DPO question, draft notice, register entry) with no real personal data, and the drill
   reports where the clock would have been lost.
