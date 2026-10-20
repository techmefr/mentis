---
name: helpdesk-ticketing-app-build-pitfalls
description: "Use when a helpdesk, ticketing or customer-support application is designed or built: ticket, message, requester and organisation model, one thread per ticket across email and web, inbound email parsing and loop prevention, merge and split, status lifecycle as a state machine, assignment and queues, SLA clocks with business hours and pauses, internal notes versus public replies, attachments, macros and automation rules, satisfaction surveys, roles and customer visibility, search, retention, what to split first and what gets regretted at v2. Method only; no response-time target and no retention period is stated."
---

# helpdesk-ticketing-app-build-pitfalls

A defensive block for building the application that receives requests and tracks them to an answer. Ticketing
tools fail in familiar ways: a reply creates a new ticket instead of joining the thread, an auto-reply talks to
another auto-reply forever, an internal note is emailed to the customer, an SLA clock keeps running while the
ticket waits on the customer, a merge loses a message, and a status is a free-text field nobody trusts. The
content is mostly craft knowledge; some points are checked against an open-source helpdesk schema and two mail standards (see `references/origin.md`). Designing the support
process and its queue (labels, capacity, first-response promise) is in `skills/support-queue-design-pitfalls`;
one escalated customer is in `skills/customer-escalation-pitfalls`; the help article a repeated question deserves
is in `skills/troubleshooting-kb-article-pitfalls`; the list screen is in `skills/data-table-ui-pitfalls` and
`skills/filters-search-and-saved-views-pitfalls`; the SLA dashboard is in `skills/dashboard-ui-pitfalls`; roles and
hidden fields are in `skills/field-and-row-permission-ui-api-pitfalls`; email sending is in
`skills/laravel-mail-via-notifications`; status handling is in `skills/laravel-recognise-state-machine-or-pipeline`.

## When
- A tool receives requests by email or a web form and tracks them as tickets.
- An SLA, an assignment rule, a merge or an automation rule is added.
- Customers see ticket history in a portal.
- A shared inbox is being replaced by a real tracker.

## Steps

**Read the part you need before the schema or the inbound email path is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ticket and message model, inbound email threading and loops, merge and split, status machine, SLA clocks, notes versus replies, attachments | a schema or the intake path is designed | [`01-tickets-threads-and-slas.md`](./references/01-tickets-threads-and-slas.md) |
| 2 | Assignment, macros and automation, surveys, roles and visibility, search, retention, what to split first, v2 regrets, framework pointers | permissions, rules or the first release are planned | [`02-roles-automation-and-v2.md`](./references/02-roles-automation-and-v2.md) |

## Output / checkpoint
Before building: the entities (requester, organisation, ticket, message, attachment, event), the status list with
the allowed transitions and which statuses pause the SLA, the threading key and the loop-prevention rule, the
internal-versus-public flag on every message and every outbound path, the SLA definition owned by the business,
the merge rule, the visibility matrix per role, and the retention policy owned by the data protection owner.
Evidence is a test that a reply to a notification joins its ticket, that two auto-responders never loop, that an
internal note never reaches an outbound email, that a paused status stops the clock, and that a merge keeps every
message. Nothing here was run by us.

## Guardrails
- This block states no response-time target, no business-hours calendar and no retention period; the business and
  the data protection owner set them and write them with a date.
- Never create a ticket from an email that carries a ticket key without first trying to attach it; match by
  header reference, then by key in the subject, then create (§1, point 2).
- Never answer an automated message; detect and drop it (§1, point 3).
- Never let a status be free text or a transition skip the machine; keep an allowed-transition table (§1, point 5).
- Never run an SLA clock on wall time alone; define calendar, pauses and the stop event (§1, point 6).
- Never send a note by a path that can reach the requester; the flag is checked at send time (§1, point 7).
- Never merge by deleting; move messages, keep the source ticket as a redirect (§1, point 4).
- Never expose another organisation's tickets to a requester; scope every read by requester or organisation
  (§2, point 4).

## Origin
Written from craft knowledge of building ticketing and helpdesk applications, then checked on 2026-10-20 against the
Chatwoot database schema (MIT) and two IETF mail standards, credited in the origin file; no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
