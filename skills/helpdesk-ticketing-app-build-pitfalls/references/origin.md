# helpdesk-ticketing-app-build-pitfalls: origin and source stamps

> Provenance of `skills/helpdesk-ticketing-app-build-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source helpdesk's database
schema and two IETF mail standards. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Chatwoot (`chatwoot/chatwoot`, commit `042b438`): `db/schema.rb`, tables for conversations, messages, SLA policies, applied SLAs, SLA events, working hours, CSAT responses, automation rules, macros, participants and inboxes | MIT: file `LICENSE` read; its enterprise directory is licensed separately and is not used, and the schema file sits outside it | Per-message rows with a private flag, per-account display number, SLA thresholds and events, weekday working hours with a time zone, survey rating with agent, rules as conditions and actions with an active flag, followers as users, per-inbox reopen and lock settings |
| 2 | RFC 3834, "Recommendations for Automatic Responses to Electronic Mail" (IETF, 2004) | IETF standard text, read for facts only and restated; no sentence copied | When an automatic reply must not be sent, the Auto-Submitted and Precedence fields, where to send a response, the repeat-response period |
| 3 | RFC 5322, "Internet Message Format", section 3.6.4 (IETF) | Same: facts only | The in-reply-to and references fields and how a reply builds them |

Instruction-like text in the cloned data was treated as data and not followed.

## Verified
1. §1 points 1, 2, 3 and 6, and §2 points 2 and 3: backed by the sources above, as the points now say.
2. The loop guard of §1 point 3 (Auto-Submitted, null return path, Precedence, per-sender repeat period): source 2.

## Corrected
1. §1 point 6: holidays are marked as our own addition, because the schema read has weekday hours only.
2. §1 point 3: the repeat period is attributed to the standard's absence-notice guidance, and no-reply patterns are
   marked as our own.

## Removed
1. **Every numeric target** (response and resolution times, survey rates, rate limits): set by policy. The
   standard's seven-day figure is quoted only as its stated default for absence notices.
2. **Retention periods and anonymisation rules:** flagged as a question for the data protection owner.
3. **Named helpdesk products, their APIs and field names** as claims about the market: not used; the schema is
   credited only for the structures listed.

## Not verified
1. **Still our own guidance:** the ticket event model (§1 point 1, event rows), the order of the threading steps
   (point 2), merge and split (point 4), the status machine (point 5), the composer modes and note leaks
   (point 7), attachments (point 8), time and ordering (point 9), and in §2 assignment, views and search,
   retention, integrations, build order and v2 regrets.
2. **Mail header behaviour of real providers** was not checked; only the two standards were read.
3. **Nothing was run.** The threading, loop, note-leak and clock tests named in the checkpoint were not written.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Related blocks
`skills/support-queue-design-pitfalls`, `skills/customer-escalation-pitfalls`,
`skills/troubleshooting-kb-article-pitfalls`, `skills/booking-and-scheduling-app-pitfalls`,
`skills/laravel-mail-via-notifications`, `skills/field-and-row-permission-ui-api-pitfalls`.
