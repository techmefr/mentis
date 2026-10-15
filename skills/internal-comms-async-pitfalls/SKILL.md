---
name: internal-comms-async-pitfalls
description: "Use when a team's internal communication norms are written or applied: which channel carries what (chat, tracker, shared docs, email, meetings), writing decisions down, seeking input before deciding, announcing in writing before a live meeting, message and thread hygiene (tl;dr first, no bare greeting, mentions with a request, links), response-time and notification agreements, agendas and pre-reads, unambiguous time and dates, documentation ownership and maintenance, and what a leader makes explicit (team agreements, one-to-one agenda, which meetings are optional)."
---

# internal-comms-async-pitfalls

Not a step of the pipeline: a craft block for how a team talks to itself. The five sections share one
premise: **the writer pays a little once so that many readers, some of whom arrive later, pay nothing**. A
decision lost in chat, an announcement made first in a meeting and a mention with no request all push that
cost onto the readers. For the record format of an architectural decision see `documentation-adr`; for
passing work between sessions see `handoff`.

## When
- Writing or reviewing a team's communication guide, onboarding page or working agreement.
- A decision was made in chat or a meeting and nobody can find it afterwards.
- Meetings carry announcements or status, threads wander across topics, or pings arrive with no request.
- Choosing a channel for a message, or setting response times, agendas, or which meetings are optional.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Channels and the durable record: chat, tracker, shared docs, email, recordings | a message or decision needs a channel | [`01-channels-and-record.md`](./references/01-channels-and-record.md) |
| 2 | Decisions in writing: input before deciding, "I intend to", long threads | a decision is being proposed, made or summarised | [`02-decisions-in-writing.md`](./references/02-decisions-in-writing.md) |
| 3 | Message hygiene: tl;dr, greetings, mentions, links, response norms, review comments, time | a message, thread or comment is being written | [`03-message-hygiene.md`](./references/03-message-hygiene.md) |
| 4 | Meetings: agenda, pre-read, announcements, ending, memorialising | a meeting is called or run | [`04-meetings.md`](./references/04-meetings.md) |
| 5 | Team agreements, document upkeep, what leaders make explicit | a norm set is written or a document or channel is aging | [`05-agreements-docs-leaders.md`](./references/05-agreements-docs-leaders.md) |

## Output / checkpoint
Test the result as a new joiner would: pick one past decision and find it, with its reason, from a link in
under a minute without asking anyone; pick one meeting invite and check it has a goal, an agenda and a
pre-read; pick one message in a busy channel and check the point is in the first line. A norm that was only
written down, with no such check, is not verified. Nothing here was run with a team.

## Guardrails
- Never make chat or a live meeting the only record of a decision; write it down in a durable, searchable
  place afterwards (§1.1, §2.1).
- Never ask for feedback on a decision already made; seek it before, and word it "I intend to" (§2.1).
- Never announce something first in a live meeting; write it before (§4.1).
- Never send a bare greeting or a mention with no request (§3.1).
- Never use email as the team's record; keep it for sensitive and external matters (§1.1).
- Never write a time without a time zone or a vague "this morning" (§3.4).
- Never keep a document whose upkeep costs more than it returns; delete or simplify it (§5.2).
- Response times, no-meeting days and working-hour windows in this block are one company's choices, shown
  as examples (§3.2, §5.1); the source guide is tied to one company's tools, so this block names tool
  categories, not products.

## Origin
Rewritten and condensed from "How GitHub Engineering communicates" by GitHub (CC-BY-4.0,
https://github.com/github/how-engineering-communicates), with its tool-specific parts generalised; the
generalised derivative by amatlack, "Rethinking async communications" (CC-BY-4.0), is credited as related
and was only read at its README; and the Clef handbook (CC0), all read 2026-10-15. Changes were made: the
text is reworded and shortened, and none of it is GitHub's or the authors' endorsement of this block. 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
