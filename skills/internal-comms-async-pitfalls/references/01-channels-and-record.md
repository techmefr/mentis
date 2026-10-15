# internal-comms-async-pitfalls §1 — Channels and the durable record

Every channel keeps information for a different length of time and shows it to a different set of people.
Choosing a channel is choosing who can find the message six months later.

## 1.1 What each channel is for
1. **Chat** is for quick questions, real-time and tactical coordination, pointing people at something
   posted elsewhere, and time-sensitive matters. It is ephemeral, has no guarantee of delivery across time
   zones, and is hard to discover, so it is **not the place to decide anything** and not a source of truth
   (GitHub's guide).
2. **A work tracker with a link per item** is where work is planned, tracked and discussed. GitHub's guide
   gives every task, idea and decision its own URL, so a question can be answered by a link. In this
   block "tracker" means whichever system does that for you.
3. **Anything impactful decided in chat or a meeting is written down afterwards** in a durable, searchable
   place (GitHub's guide). If you decide in chat or live, capture the outcome after the fact.
4. **A document in a shared drive** suits ideation, drafting and early feedback with a small group, but it
   is a poor canonical record: discovery is poor, state is unclear, and permissions are closed by default
   (GitHub's guide). Once the idea is mature, move the content to the canonical place.
5. **Retire the draft.** GitHub's guide says to replace the old document's content with a link to the
   canonical source and a note on its status, to avoid confusion, put the owner, status and sharing scope at
   the top, share with the organisation (comment access) unless sensitive, and prefer a shared drive to an
   individual's account for longevity.
6. **Email** is for personnel discussions, one-to-one feedback and external communication, and for matters
   that would be inappropriate in a company-visible tracker or channel. GitHub's reasons: no opt-in or
   opt-out, no linking, and the history sits in one inbox and leaves with the person.
7. **A recording** replaces a live meeting for one-way messages (readouts, demos, announcements needing no
   interaction); GitHub's guide adds a transcript for large meetings (§4.3).
8. **A live meeting** is a point of escalation, chosen by complexity, not the default way to start work
   (§4.1).

## 1.2 Keeping chat useful
1. **Escalate stalled threads.** GitHub's guide uses chat as the escalation when an issue or review has gone
   back and forth for days, and a call when several rounds still give no consensus; the decision is then
   recorded durably (§1.1).
2. **Treat chat as transient** and hold each other to writing important things down more durably (GitHub).
3. **Prefer public channels to direct messages**, unless the topic requires privacy. GitHub gives the
   reasons: more knowledge sharing, a better and faster answer, others share the question. Clef's handbook
   (CC0) says the same: public conversations are searchable by the whole team, so anyone can later see how a
   course of action was decided; when in doubt post publicly.
4. **Use the most specific channel**, threads and reactions to keep the signal high; give a channel a clear
   purpose and audience, keep noisy bots out of human channels, and archive a channel once it has served its
   purpose (GitHub).
5. **Persistent workarounds leave chat.** A fix for a temporary problem is fine in chat; if the issue
   persists, document the workaround in a durable place (GitHub).
