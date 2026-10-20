# lifecycle-email-program-design-pitfalls §1 — Define the program

A lifecycle flow is four decisions and a goal: a trigger that puts a person in, an audience filter beyond the
trigger, a suppression rule that keeps the wrong people out, an exit condition that takes people out, and one
concrete thing the flow is for. Copy is downstream of all five. A flow without them cannot be measured,
cannot be audited and sooner or later mails someone it should not.

## 1.1 Trigger and audience filter
1. **The trigger is an event, not a mood.** "Signed up", "started checkout and did not order", "no login for a
   period the team chose". Write the event in the words the system records it, so someone can check that it
   fires once, for the right people.
2. **The trigger is rarely the whole audience.** A filter beyond it says who qualifies: a signup, but only from
   one source; an abandoned cart, but only a first-time visitor. Write the filter next to the trigger.
3. **A trigger with no opt-in source is unsendable.** Say where the person came from and what they were told
   they would get; the flow has to match that promise, and a flow for people who signed up for content is not a
   sales sequence (`business/data-protection` for what must be evidenced about the opt-in).
4. **An inactivity trigger needs a definition of inactive.** "Lapsed" is a signal and a window. Name both. A
   signal that is only an open is weak, because an open can be a mail provider fetching an image; see
   `business/email-campaign-measurement-and-testing-pitfalls` for what an open can and cannot say.

## 1.2 One goal and one success metric
1. **One concrete outcome.** "Engage them more" is not a goal. "Activate the integration", "place a first
   order", "start a paid plan", "come back and use the product again" are.
2. **The success metric is the goal reached, read from the system of record** (orders, activations, upgrades,
   sessions), with the window written beside it. Opens and clicks are diagnostics of a message, never the
   result of a program.
3. **Add the cost side as a guardrail**: the unsubscribe and complaint figures of the same program. More goal
   reached bought with more people leaving is a result to report, not a win.

## 1.3 The never-send list
1. **Write who must never get this flow even though they meet the trigger.** The classic cases: a current
   customer receiving the new-customer welcome, a recent buyer receiving the win-back, a person in a
   cancellation or payment-recovery flow receiving a nurture, a person already in a conversation with sales.
2. **The check runs again at send time, not only at entry.** A person can meet the trigger today and reach the
   goal tomorrow, before message three. The audience is re-evaluated before each message or the exit condition
   (§1.4) covers it.
3. **A send that arrives after the person did the thing is the embarrassing failure, and it is the most
   common.** Test it on purpose (§4.1): put a test contact through the goal mid-sequence and watch.

## 1.4 Exit conditions
1. **Name every way out, and wire each one.** The goal reached; an unsubscribe (and the account-wide rule in
   §3.1); a reply to a person-signed message when someone is meant to answer it; a hard bounce; entering
   another flow that should take over.
2. **A flow with no exit condition keeps mailing people who already did the thing.** If the platform cannot
   express an exit, say so in the definition and decide whether the flow is safe to run at all.
3. **Say what happens at the end of the sequence.** A person who did not respond is either returned to the
   general audience, held for a later re-check, or no longer mailed. Decide it; do not let the last message be
   the end of the design.

## 1.5 The definition, on one page
1. **Write it as one page:** trigger and its exact event; audience filter; opt-in source; goal; success metric with its system of record and
window; never-send list; exit conditions; end-of-sequence rule; the other programs that can reach the same
people (§2.3). If the trigger or the goal cannot be written, the flow is not ready to build.
