---
name: internal-communication
description: Use when writing to colleagues about technical work — announcing a decision, flagging a risk, asking for something blocking you, handing work over, disagreeing in a review thread. Written so the reader can act without a meeting.
---

# internal-communication

Business layer (`business/README.md`), communication. The failure here is cheap per message and expensive
in aggregate: a decision nobody knew about, a risk mentioned once verbally, a thread that became an
argument. All four are writing problems.

`skills/handoff` covers agent-to-agent continuity. This is human-to-human.

## When
When announcing a technical decision beyond your own scope, flagging a risk or a delay, asking for
something you're blocked on, handing work to someone, or replying in a thread that's heating up.

## Steps

### 1. Lead with what the reader has to do
1. **First line: what this is and what it asks of them** — decision to know about, action needed, a
   question. A reader who has to reach paragraph three to find out whether it concerns them will stop
   reading at paragraph two.
2. **One message, one subject.** Two subjects means the second one gets no answer.
3. **Name the deadline** if there is one, and say what happens if it passes. "When you have time" is read
   as "never".
4. **Write for the person who wasn't in the discussion**, which by tomorrow includes you.

### 2. Announcing a decision
1. **What was decided, what it changes, from when.** In that order.
2. **Say what it rules out**, so nobody keeps working on the ruled-out path for two more days.
3. **Where it's expensive to undo, link the ADR** rather than re-explaining
   (`skills/documentation-adr`). Announcement and record are different documents.
4. **A decision announced only in a call is not announced.** Half the people who need it weren't there.

### 3. Flagging a risk or a delay
1. **Early and small beats late and complete.** A risk raised at 30% confidence can still be acted on;
   the same risk raised as a fact usually can't.
2. **Say the consequence and what you need**, not just the concern. A flag with no ask ends as
   acknowledgement and no change.
3. **Give the date as soon as you know it's moving**, not on the day it was due. Nobody minds a moved
   date as much as they mind learning about it late (`business/sales-support` §2).
4. **A concern you raised once and dropped is a concern you didn't raise.** If it still holds after the
   answer, say so; if you accept the answer, say that too so the thread closes.

### 4. Asking, and disagreeing
1. **Ask with the context and what you already tried**, so the answer is one message rather than three.
2. **Say what you'll do if you get no answer**, and by when. That converts silence into a decision
   instead of a block.
3. **In disagreement, argue about the code, never about the person.** Cite the file and the line, state
   what breaks and under which conditions — the disagreements that resolve fastest are the ones with an
   artefact in them.
4. **Concede in one line when you're wrong.** No paragraph of explanation; it reads as defending.
5. **Two rounds without progress means the thread is the wrong medium.** Move to a call, then post the
   conclusion in the thread — the people who weren't on the call still need it.
6. **Keep it short.** A long comment is read as an argument to win rather than a point to fix, and
   whatever it argues for is less likely to get done.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the ask in the first line, one subject, decisions
carrying what they rule out and from when, risks carrying a consequence and an ask, and threads that end
with a stated conclusion rather than trailing off.

## Guardrails
- **Never let a decision live only in a meeting or a DM.**
- **Never raise a risk without saying what you need** — it becomes a note that you warned, which helps
  nobody.
- **Never make a review disagreement about the person**, and never restate a point a third time; escalate
  the medium instead.
- Never post credentials, tokens or personal data into a channel or a ticket, whatever the urgency
  (`skills/auth-session-conventions` §2.4). Internal is not private.
- Where a team has its own channel conventions, they win; this is the fallback.

## Origin
Assembled from public sources: standard written-asynchronous-communication practice (state the ask first,
one subject per message, decisions recorded outside the conversation that produced them) and the
long-published guidance on separating criticism of code from criticism of the author.

Written **without internal communications expertise**. What's ours is §4 and §3.4, which come from real
review experience: short comments get acted on and long ones get debated, a point restated a third time
converts a technical disagreement into a personal one, and a concern raised once then dropped is
indistinguishable — later — from never having been raised. Deliberately excluded under rule C: anything
about a named colleague's habits. A block calibrated on one person is useful locally and indefensible
shared (`skills/distributing-blocks` §1).
