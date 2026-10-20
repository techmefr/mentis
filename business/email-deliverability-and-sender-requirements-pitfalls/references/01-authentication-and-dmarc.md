# email-deliverability-and-sender-requirements-pitfalls §1 — Authentication and DMARC

"Authentication is set up" hides three different questions. Most wrong diagnoses answer one and assume the
other two. Platform figures here were read on 2026-10-20 through a fetch tool that returns a digest, not the
raw page: `re-read before relying`.

## 1.1 Three questions, asked separately
1. **Does SPF or DKIM pass for this message?** Read it in the headers of a real delivered message, per
   sender, not from the DNS record alone. A record can exist and the message still fail.
2. **Does the domain that passed match the visible From domain?** That match is alignment. SPF and DKIM can
   both pass for the provider's own domain and still not count for yours.
3. **Which policy and which reports does the domain owner publish?** The policy tells receivers what the
   owner wants done with failures; the report address is how the owner finds out who sends as the domain.
4. **A message passes DMARC when at least one of SPF or DKIM passes with alignment.** RFC 9989 section
   5.3.5 says a message passes when one or more authenticated identifiers align with the author domain; the
   two identifiers are the SPF-checked envelope domain and the signing domain of a valid DKIM signature. Both
   are not needed. Alignment is relaxed (same organisational domain) or strict (identical domains).
5. **Unknown is not pass.** If you could not open a delivered message's headers, the authentication status of
   that sender is unknown, and the report says so.

## 1.2 What the two mailbox providers ask
Both pages carry enforcement dates and wording that change; read them again before quoting.
1. **All senders**: Google asks SPF or DKIM, valid forward and reverse DNS for the sending domain or IP, TLS,
   RFC 5322 message format, and no impersonation of Gmail From headers. Yahoo asks SPF or DKIM at minimum.
2. **Bulk senders**: both ask SPF and DKIM and a published DMARC record, and both accept a policy of `none`.
   Google says a stricter policy is not required for that group; Yahoo says it requires only `p=none` and
   strongly recommends a report address.
3. **What "bulk" means is not defined on either page.** Google's page says 5,000 messages a day for the
   group but does not say how the count is made or whether the status lasts; Yahoo's page gives no volume
   definition at all. A source that states "permanent bulk status" or a date from which rejection is
   permanent was not confirmed on either primary page; do not repeat it.
4. **Key size**: Google gives 1024 bits as the minimum and 2048 as the recommendation where the DNS provider
   supports it. Yahoo's page, as read, recommends at least 1024.
5. **Microsoft**: nothing is stated here. Its page was not read, and third-party summaries disagree on
   whether non-compliant mail is junked or rejected. If the audience is on Microsoft mailboxes, the owner
   reads Microsoft's own post and the block waits for it.

## 1.3 DMARC rollout starts by listing who sends
1. **Publish a policy that takes no action, with a report address, first.** The point of that stage is not
   safety for its own sake: it is to discover every system that sends as the domain.
2. **The usual finds** (from vendor guides, as examples): a marketing tool signing with its own domain, a help
   desk, a forgotten notification service, a transactional sender, an internal tool.
3. **Fix alignment per sender**, then and only then consider a stricter policy. A sender that passes but does
   not align will be treated as a failure once the policy tightens.
4. **Keep the inventory.** A new sender added later is the commonest cause of mail that "worked last month".
5. **Never tighten with an unlisted sender.** If the reports show a source nobody can name, that is a finding
   to investigate (a real service, or someone spoofing the domain), not a reason to wait or to proceed.

## 1.4 The `pct` tag and spec drift
1. **RFC 7489 is marked obsolete.** The page, as read, says RFC 9989 obsoletes it (and RFC 9091); RFC 9989 is
   a Proposed Standard on the Standards Track.
2. **RFC 9989's appendix "Removal of the pct Tag"** (read through a digest of the page text) says operational experience showed the tag was usually not applied accurately unless it was 0 or
   100, and that the inaccuracies varied between implementations. It lists `pct` as historic and introduces
   a `t` testing tag with values `y` and `n`, described as working like `pct` 0 and 100. With `t=y` a
   receiver is asked to apply one policy level lower than the published one. The appendix gives no guidance
   for a receiver that still meets a `pct` tag.
3. **The same RFC says** a general-purpose domain should not publish `p=reject`; the sentence sits in the
   summary of changes, so read the section on domain owner actions before citing it.
4. **So the rule here**: vendor guides teach staged percentage steps (10, 50, 100) over a number of weeks. The
   weeks are not from any specification and the percentage mechanism is marked historic in the current one.
   Re-read the current specification and the receiver's own documentation before teaching percentage steps,
   and carry no week count.
5. **Do not state what a given receiver does today with `pct`.** It was not read.
6. **Other details** that vendor guides give (one SPF record per domain, the ten-lookup limit of SPF, hard
   fail against soft fail, DKIM selector naming) were not read on a primary page by us. Treat them as
   conventions to verify against RFC 7208 and RFC 6376 before relying on them.

## 1.5 Failure patterns
- **Records read, messages not read.** The DNS looked right; the delivered message failed alignment.
- **The provider's domain signs, yours does not.** Pass without alignment, until the policy tightens.
- **Monitoring forever.** A policy of none is acceptable to Google and Yahoo for bulk senders and
  leaves spoofing of the domain unaddressed; whether and when to tighten is the domain owner's call, made with
  the sender inventory in hand.
- **Moving to enforcement with the inventory unfinished.**
- **Forwarded mail.** SPF often fails once a forwarder resends; DKIM can survive, so a sender relying on SPF
  alone for alignment is fragile (vendor guide, not verified here).
