# helpdesk-ticketing-app-build-pitfalls §2 — Roles, automation and v2

> Part 2 of `skills/helpdesk-ticketing-app-build-pitfalls`. Read it when permissions, rules or the first release
> are planned. Craft knowledge, no external source read.

1. **Assignment is explicit and observable.** Symptom: tickets nobody owns, or two agents answer one ticket. Fix:
   one assignee and an optional group per ticket, assignment as an event, round-robin or load-based routing
   that skips absent agents, and a visible "someone is replying" hint that warns without blocking. An
   unassigned ticket past a stated age shows in a view of its own. Never assign by a hidden rule that cannot be
   listed.
2. **Macros are text, automation rules are code with a log.** A macro inserts a reply and sets fields; it is
   reviewed like any template and uses placeholders that fail loudly when empty (symptom: "Hello ,"). Rules
   (on create, on update, on a timer) run in a stated order, carry a condition and an action list, write an
   event each time, cannot re-trigger themselves without a depth limit, and can be switched off without a
   deploy. Check: a rule that sets a field that another rule watches must not loop.
3. **Satisfaction surveys are sent once, after solve, to a requester.** Symptom: a survey on every reply, or a
   survey after a merged duplicate. Fix: send on solve only, one per ticket, suppressed for internal users and
   for tickets closed by rule, with a signed link and no login; store the score next to the ticket and the
   agent, read results as a distribution, and never use a single low score to discipline anyone.
4. **Roles and visibility are a matrix.** Requester (own tickets, plus the organisation's if allowed),
   collaborator, agent (own group, all groups), supervisor, admin, auditor (read only). Abilities: view
   internal notes, reply, change priority, merge, delete, export, see requester contact data, edit rules.
   Symptom: a requester sees a colleague's ticket from another company. Fix: scope every query by requester or
   organisation in one place, enforce per field for private data (see
   `skills/field-and-row-permission-ui-api-pitfalls`), name abilities as permissions (see
   `skills/laravel-permissions-not-roles`), and test each ability on every read path: list, search, export,
   API, notification, portal.
5. **Search, views and counts.** Agents live in saved views ("mine open", "unassigned", "about to breach");
   build them as filters over indexed columns (see `skills/filters-search-and-saved-views-pitfalls`), keep
   counts cheap and approximate if exact is costly, and search message bodies through an index kept in sync
   (see `skills/search-index-sync-pitfalls`). Symptom: the inbox is slow once messages pile up.
6. **Customer data, retention and deletion.** Tickets hold personal data and sometimes secrets pasted by
   customers. The retention period, anonymisation on request and the audit log of who read what are decided by
   the data protection owner, not here. Fix: a deletion path that anonymises requester fields and message
   bodies while keeping counts, a redaction tool for a pasted password, and no raw mail source kept past what
   the policy needs. Not legal advice.
7. **Integrations: email in, webhooks out, chat and phone second.** Inbound email through a provider webhook
   with a signature check and an idempotency key (see `skills/laravel-idempotent-jobs`); outbound through
   notifications (see `skills/laravel-mail-via-notifications`) with the sender domain authenticated; webhooks
   signed, retried with backoff and shown in a delivery log. Chat or phone channels become messages on the same
   model, not parallel ones.
8. **What to split first.** Order: requester, ticket and message model with the status machine; inbound email
   with threading and loop guard; reply and note composer with visibility enforced; assignment and views;
   roles and the portal scope; SLA clocks; macros and rules; surveys; merge and split; reports. Ship the
   threading, loop and note-leak tests before any automation, because rules multiply every mistake.
9. **What is regretted at v2.** The thread stored as one blob; no per-message visibility; threading by subject
   only; free-text status; SLA computed on wall time; merge by deletion; automation with no event log or no
   loop guard; requester and organisation conflated; no raw source kept for parsing bugs; hard delete of
   tickets; one inbox address per customer hard-coded. Each is cheap in the first migration and costly after
   tickets exist.
10. **Laravel and Nuxt pointers, short.** In Laravel: a messages table with a visibility column enforced in the
    mail layer, a state machine for status with a transition table, a queued inbound parser keyed by message
    id, scheduled SLA scans (see `skills/laravel-scheduling`), a global tenant scope (see
    `skills/laravel-tenant-context-by-default`) and policies per ability. In Nuxt: render user HTML only after
    server-side sanitising, show the composer mode unmistakably, treat counts as stale, and never decide
    visibility in the client.
