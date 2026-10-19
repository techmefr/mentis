# blameless-incident-review-pitfalls §3 — Action items

A review that ends in a long list nobody owns teaches the team to stop reading reviews.

## 3.1 What earns an action
1. **Actions that reduce the chance of recurrence, and actions that improve the response** (PagerDuty lists
   both). There may be a trade-off, and that is fine: PagerDuty says the return is sometimes not worth the
   effort.
2. **Do not flood the tracker.** PagerDuty: be careful about creating too many tickets, and create only the
   ones that absolutely should be dealt with (its example is items at its top two priority levels, one
   company's scale).
3. **Prefer understanding to reflex controls.** Adhorn: learning means understanding the conditions that
   enabled the problem, and a new control after every incident ends in controls over controls.
4. **Address several contributing factors, not only the immediate technical fix** (adhorn). Adhorn groups
   actions as technical, process, organisational and learning investments (practice, simulation, knowledge
   sharing). Use the grouping as a prompt for what was left out, not as a quota.

## 3.2 Shape of one action
1. **Give each action these fields** (adhorn's list):

   ```
   Title:
   Owner:
   Due date:
   Priority:
   Contributing factor addressed:
   Success criteria:
   Backlog link:
   ```

2. **An action with no owner, no date, or no factor it addresses is a wish**, not an action. The adhorn
   checklist asks that every item have an owner and a realistic timeline, and that items address
   contributing factors rather than only symptoms.
3. **Label the tickets** with severity and date tags (PagerDuty), so patterns can be found later.
4. **Collect TODOs from the chat history** of the incident before writing the list (PagerDuty), and if a
   direction has to be chosen first, note the topic for discussion rather than opening a ticket.

## 3.3 Follow-through and sharing
1. **Track the actions to completion and check they worked.** Adhorn: follow through, track the items, and
   make sure the lessons influence later decisions; also decide when to check that actions are completed
   and effective.
2. **Decide who owns the follow-through.** PagerDuty's owner is responsible only for creating the tickets,
   not for following them to resolution. Own guidance, not sourced: a review process has to name who
   chases the tickets, or nobody does.
3. **Share the result.** PagerDuty sends an internal message to the relevant people with the key learnings
   and a link to the review; adhorn says to share analyses widely across teams.
4. **Feed other practices.** Adhorn asks what the incident suggests for load tests, readiness reviews and
   rehearsals of a response, and which runbooks or documents need updating.
