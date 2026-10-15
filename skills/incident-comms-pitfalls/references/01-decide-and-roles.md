# incident-comms-pitfalls §1 — Decide and roles

The failure this section prevents is deciding during the incident, with the incident running, whether to
tell anyone, who may post, and how bad it is. Those are answers to have before it starts.

## 1.1 Decide in advance what gets communicated
1. **Agree criteria for public communication before an incident**, so false alarms and short-lived issues do
   not cause widespread panic. PagerDuty ties the criteria to the organisation's definition of an incident
   and to its severity levels, and lists five questions to include: which products are affected, how badly
   usage is affected, how many customers are affected, how noticeable the impact is, and whether it is
   something a customer may want contingencies for (PagerDuty).
2. **Make severity definitions specific.** PagerDuty's own table is deliberately generic and says to refer to a
   percentage of users or accounts and to make the definitions metric driven (PagerDuty).
3. **Give each severity a communication rule**, not only a response rule. The Guedes runbook's table puts an
   update cadence next to each level (every 30 minutes for the top one, hourly for the next, daily for the
   third, none for cosmetic issues) and makes the status page public for the top level. Those figures are one
   team's choice (Guedes runbook).
4. **When unsure of the severity, treat it as the higher one** and review later. Both sources say so:
   downgrading is cheap, and discovering an hour in that it was the top level is not. The commander may change
   the severity, and the change is logged with the reason (PagerDuty, Guedes runbook).
5. **Prepare templates per stage and for the special cases**: long-running incidents, small or limited
   customer impact, an incident opened and resolved at once (PagerDuty).

## 1.2 Roles: who decides, who fixes, who speaks
1. **Three responsibilities stay separate even when one person holds two.** The Guedes runbook has a commander,
   an operator and a communicator, and says that in a small team two may be one person while the
   responsibilities remain separate. PagerDuty's version: a smaller incident may let the deputy also scribe
   and act as internal liaison, because it is not intended that every role be a different person each time
   (Guedes runbook, PagerDuty).
2. **The commander does not type commands into production while commanding.** If they must, they hand over
   command first, with an explicit message stating the current state and the next step; silence is not a
   handover (Guedes runbook).
3. **One voice speaks, using the commander's facts.** The commander is the single source of truth on status;
   the communicator posts what the commander has reviewed and approved. PagerDuty's commander reminds the
   customer liaison to draft, approves the draft, and asks for it to be posted; asking the responders for
   strong objections is good practice but not mandatory (PagerDuty).
4. **Name a fallback poster.** If the customer liaison cannot post, the commander delegates somebody so the
   cadence does not stop (PagerDuty).
5. **The communicator reports back**: how many customers say they are affected, with examples the responders
   can investigate, and when each update was sent (PagerDuty, Guedes runbook).

## 1.3 Customers who need more than the status page
1. **Customers on special support or success contracts, such as a premium plan, get the impact communicated to
   them individually**, through a liaison or their account team, not only through the public channel
   (PagerDuty).
2. **Write the list of such customers before the incident.** Finding it during one is how some of them are
   missed (own guidance).

## 1.4 Security incidents
1. **Treat a suspected security incident as the top severity until shown otherwise**, and start the process
   even when unsure it is one; the commander decides afterwards whether it was (Guedes runbook, PagerDuty).
2. **Record the time of detection and page whoever owns legal and data-protection obligations**, because
   notification deadlines start at detection. The runbook names two data protection regimes and cites no
   article; which deadlines apply to you is a question for that owner, not for this block (Guedes runbook).
3. **Limit who knows the details until the scope is understood, and communicate through the designated
   person.** PagerDuty adds that the attack could be internal, so it tells responders not to discuss it with
   anyone outside the response team until forensics say otherwise (Guedes runbook, PagerDuty).
4. **The public statement waits until the facts are validated**: a timeline, what was compromised and how.
   PagerDuty then wants it out as soon as possible, preferably within a few days, because waiting makes it
   worse, and wants customers' own security teams contacted before the general notice if possible. That
   timeframe is that company's, not a rule (PagerDuty).
5. **What the statement contains**: the date in the title so it is never mistaken for a new breach, honesty
   about what data was affected including data that should not have been stored, a detailed timeline, how the
   organisation plans to prevent a repeat, and no naming of an external party unless it has already disclosed
   publicly (PagerDuty).
