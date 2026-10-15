# internal-comms-async-pitfalls §2 — Decisions in writing

A decision is only as useful as the reason attached to it, and a reason is only available if it was written
where someone can search for it. For the shape of an architectural decision record, see `documentation-adr`.

## 2.1 Input before the decision
1. **Write down the why and the how**, not only the outcome, in the most durable, searchable and
   discoverable medium available (GitHub's guide).
2. **Record context, trade-offs and consequences**, in a way that lets stakeholders take part in the
   decision (GitHub).
3. **Seek feedback before the decision, not on it.** GitHub's wording: statements should read "I intend to",
   not "I decided". Opening a pull request, issue or post is not collaboration by itself.
4. **Show what you did with the feedback**: GitHub's leaders' tips say to document how you incorporated the
   team's input, so people see it was worth contributing.
5. **A document is a joint piece of work** between the decision-makers and stakeholders: agree what the
   problem is, which constraints exist, and how and when it will be solved. Put it where it is easy to find
   (GitHub). It needs enough detail for its decision; GitHub's examples are availability, rollout, scaling
   and timelines.
6. **A meeting is not a decision by itself**, especially on technical matters; record what was decided
   afterwards (§4.3).
7. **One findable place for team decisions**, easy to search (GitHub's leaders' tips).

## 2.2 Long threads
1. **Keep the opening post current.** On a long or much-commented item, update its body for anyone arriving
   late, and from time to time add a comment that restates the current understanding of the problem and
   the proposed answer (GitHub).
2. **Pick the right starting point.** When the question is "should we even do this", or there are many ways
   to do it, GitHub starts with an open discussion post and opens a tracked item once decisions are made.
3. **One purpose per thread.** When a side topic appears, open a new item and continue there, or do it on a
   teammate's behalf if they hijack the thread; if the new item blocks the current one, say so and move on
   (GitHub).
4. **Do not do significant work that no tracked item covers**; ask for an item or open one (GitHub).

## 2.3 Optimise for the reader who arrives later
1. **Pause before sending and ask how easy it is for someone coming along behind you to understand what you
   are doing and why** (GitHub's leaders' tips). This is slightly more work for the writer and saves the
   readers' time later.
2. **Make a record of the information, not of the conversation.** Own guidance, not sourced: a thread that
   needs fifty messages to explain a decision has not been written down yet; write the summary.
