---
name: email-deliverability-and-sender-requirements-pitfalls
description: "Use when mail from a product or a brand goes to spam or is rejected, when email is being set up for a new domain or provider, when a marketing send needs its unsubscribe mechanics checked, or when someone quotes a complaint or bounce rate: sender authentication and alignment, DMARC rollout order, one-click unsubscribe headers, transactional against marketing streams, complaint rate with its source and denominator, list hygiene and suppression, and the order in which to diagnose, with unknown never counted as pass."
---

# email-deliverability-and-sender-requirements-pitfalls

Business layer (`business/README.md`), marketing. Mail that does not arrive is usually blamed on the copy,
while the cause is in authentication, in the unsubscribe mechanics or in the list. This block is the order
in which to look, and the points where the public sources and the vendors' guides go wrong. It is for the
person who owns the sending domain: a marketer, a founder, the one who set up the provider.

It states method, and platform facts only where a primary page was read on 2026-10-20 (marked `re-read before
relying`: the pages change, and the fetch returned a digest, not the raw page). Microsoft's
requirement is stated from its own announcement (read in full 2026-10-20), including the point that the post
disagrees with itself on junk versus reject. It carries no benchmark, no warm-up schedule, no bounce
band and no week count, because the sources contradict each other on them. It is not legal advice: what a
message needs in law, how long consent evidence or a suppression list may be kept, and what applies to
business-to-business mail go to `business/data-protection` and the person who owns that function. How to
send the mail from code is `skills/laravel-mail-via-notifications`; what a campaign metric can say is
`business/email-campaign-measurement-and-testing-pitfalls`.

Cold outbound infrastructure (mailbox farms, warm-up networks, domain rotation) is out of scope.

## When
- Mail lands in spam, is delayed or is bounced, or a rate-limit response appears.
- Email is set up for a new domain, provider or product, or a provider is migrated.
- A marketing send is about to go out and its unsubscribe path has not been checked.
- Someone quotes a complaint or bounce rate, or asks to tighten a DMARC policy.

## Steps

**Read only the section the task meets.** §4 for any "goes to spam" report; the rest on demand.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Authentication as three questions, alignment, DMARC monitor-first and what the current spec says about `pct` | a record is set, changed or blamed | [`01-authentication-and-dmarc.md`](./references/01-authentication-and-dmarc.md) |
| 2 | One-click unsubscribe as RFC 8058 defines it, the visible link, processing time, what never replaces one-click | a marketing send or its endpoint is built or checked | [`02-unsubscribe-mechanics.md`](./references/02-unsubscribe-mechanics.md) |
| 3 | Streams, complaint rate with source and denominator, list hygiene and suppression | a rate is quoted, lists are imported, or categories are mixed | [`03-streams-complaints-and-lists.md`](./references/03-streams-complaints-and-lists.md) |
| 4 | Volume discipline, the diagnosis order, the output shape, what not to do | mail goes to spam, or an audit of the sending set-up is asked for | [`04-diagnosis-order-and-output.md`](./references/04-diagnosis-order-and-output.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a sender inventory (every system that sends as the
domain), authentication status per domain and per sender, the unsubscribe check result, complaint and bounce
figures each with its source and denominator, a list of unknown items, and the one next change. The owner of
the domain reads it and decides; the block changes no DNS record and sends no mail.

## Guardrails
- Read authentication from the headers of a real delivered message, per sender. State that unknown is not
  pass. Never report "authentication is fine" from a record that exists but was not checked on a received
  message (§1.1, §4).
- Inventory every system that sends as the domain before tightening a policy. Never move to a stricter DMARC
  policy with an unlisted sender (§1.3).
- Re-read the current DMARC specification and the receiver's page before teaching percentage steps. Never
  carry a `pct` schedule or a week count from a vendor guide (§1.4).
- Check one-click unsubscribe against the RFC's own conditions, not against "the header exists". Never answer
  the one-click POST with a redirect, and never let a preference page or an automatic removal after bounces
  stand in for it (§2).
- Give every rate its source and denominator, and keep rates from different tools apart. Never sum or compare
  a provider-tool rate with the sender's own feed as if they were equal (§3.2).
- Treat a bounce or complaint as global suppression and an unsubscribe as scoped. Take the retention of a
  suppression list to the data-protection owner. Never decide "never delete" or "delete after N days" here
  (§3.3).
- Change one thing at a time and diagnose in the fixed order. Never conclude a deliverability problem from a
  low open rate (§4.2).
- Test phishing or campaign tests belong on a domain you can lose, not the production domain (§4.4).
- This block is a method written from vendor guides and a handful of primary pages read through a digest, and
  never run by us on a real domain. Source status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the deliverability and unsubscribe notes of several MIT-licensed email skill
repositories, checked against the Google and Yahoo sender pages, RFC 8058 and RFC 9989, read 2026-10-20.
🟡: never run by us, written without email-operations expertise. Details in
[`references/origin.md`](./references/origin.md).
