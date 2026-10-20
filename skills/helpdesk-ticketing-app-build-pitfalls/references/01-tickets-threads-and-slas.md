# helpdesk-ticketing-app-build-pitfalls §1 — Tickets, threads and SLAs

> Part 1 of `skills/helpdesk-ticketing-app-build-pitfalls`. Read it when a schema or the intake path is designed.
> Mostly craft knowledge; points 1, 2, 3, 6 and 7 carry facts from an open-source helpdesk schema (MIT) and two IETF mail standards, read 2026-10-20 and restated in our words (`references/origin.md`, sources 1 to 3). Everything not marked as sourced is our own guidance. No response target is stated.

1. **Model: requester, organisation, ticket, message, event.** A requester is a person (often several addresses),
   an organisation groups requesters, a ticket is the unit of work, a message is one inbound or outbound item,
   an event is an append-only record of a change (status, assignee, priority, merge, rule fired). Symptom of
   storing the thread as one text blob: no per-message author, no per-message visibility, no search by sender.
   Fix: messages as rows with direction (inbound, outbound, note), author, channel, raw source kept, and
   visibility fixed at creation; ticket fields change only through events, so "who did that" has an answer. The reference helpdesk schema stores each message as a row with a type, a private flag, a polymorphic sender and a source id, and gives each conversation a per-account display number beside its internal id (source 1); the event-only change rule is our own guidance.
2. **Threading needs a key, tried in order.** Symptom: every customer reply opens a new ticket, or a reply to
   an old closed ticket lands in the wrong one. Fix: match the incoming message by the reply-reference headers
   against stored message ids first, then by a ticket key in the subject, then by a signed token in the reply
   address, and only then create a ticket. Store the message id of every outbound mail so replies match. A
   reply to a closed ticket follows a stated rule (reopen within a window, otherwise a new linked ticket). The mail standard defines the reply headers that make the first step possible: a reply carries the parent's message id in its in-reply-to field and the chain of ancestors in its references field (source 3). The reference schema makes the closed-ticket rule a per-inbox switch for accepting messages after resolution, and another switch that locks a contact to a single conversation (source 1). The order of the three matching steps is our own guidance.
3. **Loops and automated mail.** Symptom: an auto-reply meets a customer's out-of-office and the two bounce
   forever, or the system answers a bounce. Fix: detect automated senders (auto-submitted and precedence
   headers, empty return path, known no-reply patterns), do not create a ticket or send an acknowledgement for
   them, rate-limit acknowledgements per sender, and never send from the system to its own intake address. The standard on automatic replies confirms the core of it: an automatic reply should not be sent to a message whose Auto-Submitted field has any value other than "no", nor to one with a null return path, nor to one marked list, junk or bulk in the Precedence field; replies should go to the return path and not to Reply-To or From; an automatic reply should itself carry Auto-Submitted with the value auto-replied; and the same absence notice should not go to the same sender again within a period of several days, with seven days named as the default (source 2). Known no-reply address patterns are not in the standard and stay our own guidance.
   Check: feed an out-of-office and a delivery failure notice into intake and assert no outbound mail.
4. **Merge and split without loss.** Symptom: merging two tickets deletes one thread, or the customer replies to
   the dead ticket and it vanishes. Fix: merge moves messages and attachments to the surviving ticket in one
   transaction, writes an event on both, turns the source ticket into a closed redirect that forwards new
   replies, and keeps the union of requesters. Split copies a chosen message range to a new linked ticket.
   Merge across organisations is refused or needs an explicit permission, since it changes who can read what.
5. **Status is a state machine.** Symptom: free-text or ad hoc statuses and "closed" tickets that reopen by
   accident. Fix: a small fixed set (for example new, open, waiting on customer, waiting on third party,
   solved, closed), an allowed-transition table, a reason on a solve or a close, and a distinction between
   solved (the customer may reopen by replying) and closed (frozen, a reply creates a linked ticket). See
   `skills/laravel-recognise-state-machine-or-pipeline`. Agent-facing statuses and customer-facing wording are
   separate: the portal shows a simpler label than the internal one.
6. **SLA clocks are policies on a calendar.** Symptom: a ticket breaches overnight, or the clock runs while the
   ticket waits for the customer. Fix: a target is a pair (start event, stop event) measured on a named
   business-hours calendar with time zone and holidays; waiting-on-customer pauses it; a change of priority or
   plan recalculates from a stated point; store the due time on the ticket and recompute on events, and scan
   for warnings with a scheduled job rather than per request. Keep first reply and resolution as separate
   clocks. The reference schema agrees: an SLA policy holds a first-response, a next-response and a resolution threshold and an only-during-business-hours flag, a policy is applied per conversation in a row with a status, and each breach or hit is an event row; working hours are stored per day of week with open and close times, and the inbox has a time zone (source 1). No holiday table was found in the schema read, so holidays remain our own addition. Numbers and calendars are the business's; time-zone handling follows
   `skills/booking-and-scheduling-app-pitfalls`.
7. **Internal notes versus public replies.** Symptom: an agent's note is emailed to the customer, or an
   internal name leaks in a CC. Fix: the composer has two clearly different modes with different colours and
   a default of public only when the last action was a customer message; the visibility flag is stored, read at
   send time by the mail layer (not only by the screen), and every outbound path (email, portal, webhook,
   export, notification to followers) filters on it. Check: write a note that mentions a secret and assert it
   appears in no outbound payload. Collaborators on a ticket get notes only if they are internal users (the reference schema's participants of a conversation are users, source 1).
8. **Attachments are untrusted files.** Symptom: a malicious attachment is served inline, or a huge file blocks
   intake. Fix: store outside the web root, serve with a download disposition and a fixed content type,
   scan by the policy of the organisation, cap size and count with a clear bounce message, strip tracking
   pixels and remote images from rendered HTML mail, and sanitise HTML before display. Inline images in a mail
   are attachments with a content id, kept with their message.
9. **Time and ordering.** Store UTC with the original header time; show messages in received order, not sent
   order, because clocks lie; show each viewer their own zone. A ticket's "last activity" is derived from
   events, and an internal note counts as agent activity but not as customer activity for SLA and for
   "waiting" rules.
