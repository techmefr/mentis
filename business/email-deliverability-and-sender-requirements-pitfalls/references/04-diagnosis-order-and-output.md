# email-deliverability-and-sender-requirements-pitfalls §4 — Diagnosis order and output

"My emails go to spam" is a symptom with several causes. Diagnose in a fixed order, on evidence, one change at
a time. This is method, not a verdict: an audit of someone's real domain is theirs to commission and act on.

## 4.1 Volume discipline
1. **Ramp gradually, avoid bursts, send consistently.** Vendor guides give daily volume tables for a warm-up
   (they start at 50 to 100 a day and differ widely after that). The tables are the vendors' own and are not
   copied; the direction of travel is the shared part.
2. **On a rate-limit response, stop.** Google's page for the 4.7.28 response says to pause at least ten
   minutes, work out the cause (assume DKIM, SPF and IP volume all apply when the response does not name one),
   then resume from a single connection and add connections one at a time. `re-read before relying`.
3. **Do not change provider in the week before a large send.** A convention of vendor guides; the reason is that
   two changes at once cannot be told apart.

## 4.2 The order
1. **What changed.** DNS, provider, template, list source, volume, sending domain, the date of the first
   report. A deliverability problem with no change behind it is rarer than one with a change nobody wrote down.
2. **Authentication results in the headers of a real delivered message** (§1.1), per sender. Not the DNS
   record alone.
3. **The unsubscribe headers and the endpoint** (§2), because a missing or broken one is a receiver-side
   requirement for bulk senders.
4. **The reputation tools of the major mailbox providers**, with each figure's source and denominator (§3.2).
   A provider you have no tool for is unknown, not fine.
5. **List quality.** Where the addresses came from, bounce and complaint handling, imports (§3.3).
6. **Content last.** Content is the cheapest thing to blame and the last thing to test.
7. **One change at a time**, each written down with the date, so the next report can say what moved.
8. **A seed-inbox test is a sample, not a verdict.** Placement in a few test mailboxes says nothing certain
   about the population, and a scoring site's cut-off number is its own convention.
9. **Never conclude a deliverability problem from a low open rate.** Opens are a fetch, and for readers behind a
   privacy relay they are a fetch whether or not the message was read (see
   `business/email-campaign-measurement-and-testing-pitfalls` §1). A vendor rule that "an open rate under N
   percent proves a deliverability problem" is not taken.

## 4.3 The output shape
1. **Sender inventory**: every system that sends as the domain, who owns it, which category it sends.
2. **Authentication status** per domain and per sender: SPF, DKIM, alignment, DMARC policy and report address,
   each pass, fail or unknown, with the message it was read on.
3. **Unsubscribe check result**: headers, DKIM coverage, endpoint behaviour, visible link, suppression
   timing.
4. **Complaint and bounce figures**, each with source and denominator, and the counts behind each.
5. **Unknown items**, listed. Unknown never counts as pass.
6. **The one next change**, with what would show it worked, and who decides.

## 4.4 What not to do
1. **Do not send test phishing messages or test campaigns from the production domain.** Google's page says it
   can harm the domain's reputation and may get it listed on blocklists. Use a domain you can afford to lose.
2. **Do not take a vendor's product line for a requirement.** Paid list cleaning, dedicated addresses and bot
   filters are products, not steps in this order.
3. **Do not attempt cold-outbound tactics** (rotating domains, warm-up networks that fake engagement). They
   are deliverability evasion and out of scope here.
4. **Do not touch DNS, the provider's settings or a live send** on the strength of this block. It drafts the
   change; the owner of the domain applies it.

## 4.5 Failure patterns
- **Content rewritten while authentication was failing.**
- **Several changes in one day.**
- **A good seed result read as proof.**
- **A missing mailbox-provider tool treated as a clean bill.**
