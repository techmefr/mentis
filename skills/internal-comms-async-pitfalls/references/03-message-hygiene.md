# internal-comms-async-pitfalls §3 — Message hygiene

Small habits that decide whether a message can be acted on by someone who was not watching when it arrived.

## 3.1 Writing one message
1. **Put the point first.** GitHub's guide asks for a tl;dr summary at the beginning of any communication so
   the main points get across.
2. **No bare greeting.** Chat is asynchronous: send the question with its context and links in the first
   message instead of "hello" and waiting for a reply (GitHub, citing the nohello idea).
3. **A mention carries a request.** A name with no request is much less actionable than a specific call to
   action; if you only refer to a person and do not need their attention, quote the name so it does not
   notify them (GitHub; the quoting uses backticks in that tool, so check your own).
4. **Link what you reference.** If a prior item, change or line has an address, finding it is your
   obligation: you know the thing best, and one lookup by you saves the lookups of every reader (GitHub).
5. **For an urgent reply on a tracked item, put the item's link in the message and ask for the reply there**
   (GitHub).
6. **Anticipate questions on complex announcements** (a process or tooling change) with an FAQ, and say
   "we don't know yet" or "we can't answer that right now" rather than pretending the question does not
   exist (GitHub).
7. **Say what a term means.** Avoid acronyms without context (GitHub's inclusivity paragraph).

## 3.2 Response and notification norms
These are written down per team (§5.1). GitHub's figures are one company's example.
1. **Aim to answer non-urgent messages within one business day, in your working hours**, and treat direct
   messages more like email than a phone call; an unanswered non-urgent item can be escalated to the
   right channel (GitHub's example).
2. **Reserve the all-hands mentions for what is both urgent and important**, if used at all (GitHub).
3. **No expectation of being online or responsive around the clock, even for a message from a manager,
   unless on call.** Nobody is expected to catch up on every channel after leave, and nobody should assume
   everyone read every message (GitHub).
4. **Respect the recipient's hours**: consider scheduling a message to send later when it falls outside
   their working hours (GitHub).
5. **Another team's example of an agreement**: the Clef handbook (CC0) defines four presence states and the
   response each one implies, from a few minutes to an hour when active, to the next work day when away. It
   is shown to illustrate that an agreement is explicit, not as a model to copy.

## 3.3 Review comments
1. **Prefer specific line comments, with suggested edits, to sweeping reviews** (GitHub's guide on pull
   requests, reworded here for any reviewed document or change).
2. **Ask for changes only when you intend to block** the item until you approve (GitHub).
3. **Make ownership visible**: if no review is requested from the responsible team, name it, and if the
   wrong team is notified by an ownership file, updating it is part of your change (GitHub).

## 3.4 Time and dates
1. **State the time zone** whenever you give a meeting time and avoid location-specific words such as "this
   morning" or "in the spring" (GitHub).
2. **Use an unambiguous date format**: GitHub prefers ISO 8601 (year, month, day) except in long-form
   writing, and accepts anything consistent and unambiguous.
3. **Mind holidays and working hours across time zones**; look the person's zone up in their profile or
   calendar before scheduling (GitHub).

   ```
   Review call: 2026-10-20 14:00 UTC
   ```
