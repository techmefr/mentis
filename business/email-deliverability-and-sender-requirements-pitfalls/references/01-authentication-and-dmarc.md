# email-deliverability-and-sender-requirements-pitfalls §1 — Authentication and DMARC

"Authentication is set up" hides three different questions. Most wrong diagnoses answer one and assume the
other two. Google and Yahoo figures were read on 2026-10-20 as the raw text of their pages (Google's sender
guidelines and FAQ, Yahoo's requirements page); the RFC points were read as raw RFC text. The pages change:
`re-read before relying`.

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

## 1.2 What the mailbox providers ask
The pages carry enforcement dates and wording that change; read them again before quoting.
1. **All senders**: Google asks SPF or DKIM, valid forward and reverse DNS for the sending domain or IP, TLS,
   RFC 5322 message format, and no impersonation of Gmail From headers. Yahoo asks SPF or DKIM at minimum.
2. **Bulk senders**: both ask SPF and DKIM and a published DMARC record, and both accept a policy of `none`.
   Google says a stricter policy is not required for that group; Yahoo says it requires only `p=none` and
   strongly recommends a report address.
3. **Google defines "bulk" in its FAQ; Yahoo does not.** Google's FAQ says a bulk sender is one sending close
   to 5,000 messages or more to personal Gmail accounts within 24 hours, counted over every message from the
   same primary domain (a subdomain's mail counts toward its parent's total), and that a sender who meets this
   once is classed as bulk permanently, with no expiry, whatever it changes later. Symptom: a team splits
   volume across subdomains to stay under the line, or plans to "leave" bulk status. Fix: assume the
   requirements for the larger group apply once the domain has ever come near the line. Yahoo's page gives no
   volume definition. Treat any other threshold wording as a paraphrase until checked on the page.
4. **Key size**: Google requires a DKIM key of 1024 bits or longer to reach personal Gmail accounts and
   recommends 2048 where the DNS provider supports it. Yahoo asks for at least 1024. RFC 6376 says signers
   must use RSA keys of at least 1024 bits and verifiers must be able to check keys from 512 to 2048 bits.
5. **Microsoft (Outlook)**, from Microsoft's own announcement for high-volume senders (Microsoft Community
   Hub, Defender for Office 365 blog, published April 2025, updated 30 April 2025, read 2026-10-20 in full, re-read
   before relying): the scope is domains sending more than 5,000 messages a day, and the post does not say how
   the count is made. For that group SPF must pass for the sending domain, DKIM must pass, and DMARC must be
   published at p=none at least and align with SPF or DKIM (both preferred). It also recommends a valid From or
   Reply-To address that can receive replies, a working unsubscribe link, list hygiene and bounce handling, and
   honest headers and consent.
6. **The Microsoft post contradicts itself on the action.** Its update says non-passing mail is rejected with a
   5.7.515 "sending domain does not meet the required authentication level" response, effective 5 May 2025; the
   paragraph after it says routing to Junk begins on that date and rejection comes later, date to be announced.
   Symptom: a sender reads one paragraph and plans for the wrong outcome. Check: the live post and the bounce
   text actually returned by Outlook. Fix: do not state either outcome as current; send test mail and read the
   response. The post also says the safe-sender list is not honoured for this check, and that a third-party
   sending service still needs the records published in the sender's own domain.
7. **SPF lookup limit and forwarding (same post).** Exceeding ten DNS lookups can make SPF fail; Microsoft
   suggests reducing includes or flattening. It says forwarding can break DMARC alignment and recommends ARC for
   forwarders and lists. It sends DMARC aggregate reports to the address in the record and says it does not plan
   to send forensic reports. It advises moving none, then quarantine, then reject, gradually.

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
2. **RFC 9989's appendix A.6 "Removal of the pct Tag"** (raw text, 2026-10-20) says operational experience showed the tag was usually not applied accurately unless it was 0 or
   100, and that the inaccuracies varied between implementations. It lists `pct` as historic and introduces
   a `t` testing tag with values `y` and `n`, described as working like `pct` 0 and 100. With `t=y` a
   receiver is asked to apply one policy level lower than the published one. The appendix gives no guidance
   for a receiver that still meets a `pct` tag.
3. **The same RFC says, in its section on indirect mail flows**, that a domain hosting users who may post to
   mailing lists should not publish `p=reject`; that a domain publishing `p=reject` must not rely on SPF alone
   (relays and forwarders usually break SPF while DKIM signatures generally stay valid) and must sign with DKIM;
   and that such a domain wishing to reach reject should first read its aggregate reports under `p=none` for at
   least a month and then under `p=quarantine` for an equally long period. That duration is the RFC's own
   advice for that kind of domain, not a general schedule; do not generalise it to every sender.
4. **So the rule here**: vendor guides teach staged percentage steps (10, 50, 100) over a number of weeks. The
   weeks are not from any specification and the percentage mechanism is marked historic in the current one.
   Re-read the current specification and the receiver's own documentation before teaching percentage steps,
   and carry no week count.
5. **Do not state what a given receiver does today with `pct`.** It was not read.
6. **SPF and DKIM details, read in RFC 7208 and RFC 6376** (raw text, 2026-10-20). A domain that publishes
   more than one SPF record gets a permanent error, not a merge. Symptom: SPF fails after a second tool asked
   for "its" record. Check: count the SPF records on the domain. Fix: one record carrying every sender. RFC 7208
   section 4.6.4 limits evaluation to ten lookups caused by the include, a, mx, ptr and exists mechanisms and the
   redirect modifier (ip4, ip6 and all cost none), and an implementation must return a permanent error when it
   is exceeded; each MX record also may not lead to more than ten address lookups. Symptom: SPF breaks when a
   marketing tool is added although the record "looks right". Fix: count lookups through the nested includes,
   drop unused senders. RFC 6376 section 3.1 says selectors exist so a domain can hold several keys at once
   (per mail stream, per office, or to rotate a key without a gap); the naming is the owner's choice. Hard
   fail against soft fail was not checked; do not teach one as better.

## 1.5 Failure patterns
- **Records read, messages not read.** The DNS looked right; the delivered message failed alignment.
- **The provider's domain signs, yours does not.** Pass without alignment, until the policy tightens.
- **Monitoring forever.** A policy of none is acceptable to Google and Yahoo for bulk senders and
  leaves spoofing of the domain unaddressed; whether and when to tighten is the domain owner's call, made with
  the sender inventory in hand.
- **Moving to enforcement with the inventory unfinished.**
- **Forwarded mail.** SPF checks the connecting server, which a forwarder changes; RFC 7208's appendix on
  mediators and forwarding discusses this, and Microsoft's post says forwarding can break alignment. RFC 9989
  says SPF will most likely fail on relayed mail while DKIM signatures generally remain valid, so a sender
  relying on SPF alone for alignment is fragile.
