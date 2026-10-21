# email-deliverability-and-sender-requirements-pitfalls §2 — Unsubscribe mechanics

An unsubscribe that works in a test and fails in a mailbox is a deliverability problem and a trust problem at
once. The header rules below come from the raw text of RFC 8058, read on 2026-10-20 (sections 1, 3.1, 3.2, 4 and 6);
`re-read before relying` in case a later RFC updates it. What the law requires of an
unsubscribe is not here: `business/data-protection` and the person who owns that function.

## 2.1 The headers
1. **Two headers, no more.** One List-Unsubscribe header that carries one HTTPS address (it may also carry
   other address types, such as a mailto), and one List-Unsubscribe-Post header whose only content is the
   one-click value.
2. **The message needs a valid DKIM signature that covers both headers.** Section 3.1 says so, and section 4
   adds that both headers go in the signature's signed-header list. The RFC says a receiver should not offer
   one-click for a message that does not meet this. A provider that adds the headers after signing, or a
   signature that omits them, loses one-click in the mailbox without any visible error on your side.
3. **The address carries an opaque, per-recipient token** that the endpoint verifies (sections 3.1 and 6), so
   that a forged request cannot unsubscribe someone else. A predictable address made from the email alone is
   the defect to look for.

## 2.2 The endpoint
1. **It receives a POST that carries no cookies, no authorization and no other context** (section 3.1). So the
   endpoint cannot depend on a logged-in session or on a cookie. The recipient and the list come from the
   token.
2. **It does not answer that POST with a redirect** (section 3.1: the sender must not return an HTTPS
   redirect). A common failure is an endpoint behind a web server rule or a shortening layer that redirects.
3. **A GET to the same address shows a page**, because a person or a scanner may fetch it that way. The RFC's
   section 1 says anti-spam software often fetches every resource in the message headers automatically and a
   sender cannot tell that from a person; that is why a header address that unsubscribes on a plain GET removes
   people by accident, and why the older pattern was a landing page with a confirmation step. The one-click
   POST is the mechanism that replaces the confirmation step: do not unsubscribe on a GET.
4. **The receiver must not POST without user consent** (section 3.2); how consent is obtained is not defined.
   So the sender cannot assume a POST means the user acted in a given way.
5. **Check it from outside.** Post to the address the way a receiver would, without cookies, and read the
   status and the absence of a redirect. A test from the sending tool's own screen proves nothing about the
   mailbox.

## 2.3 What the two providers add
1. **Google** (sender guidelines page, raw): marketing and subscribed mail from the 5,000-a-day group
   supports one-click and carries a clearly visible link in the body, and the page shows the two headers and
   the POST the sender receives. Offering other options (a list review, an automatic removal after bounces) is
   allowed but must not replace one-click.
2. **Yahoo** (read on its sender requirements page): a functioning header supporting one-click for marketing
   and subscribed mail; the RFC 8058 method is highly recommended and a mailto method is acceptable; a visible
   body link that may lead to a preference page; unsubscribes processed within two days; no login required.
3. **Both name a time.** Yahoo asks for processing within two days. Google's FAQ recommends fulfilling
   requests within 48 hours and lists "unsubscribe requests not honoured within 48 hours" among the problems
   it reports; the guidelines page itself states no time. Treat 48 hours as the outer limit and aim well inside it.
4. **A preference page is a good addition and never the only exit.** The failure to name is a body link that
   leads only to a preference page while the header does nothing.

## 2.4 What an unsubscribe changes
1. **Scope.** An unsubscribe from marketing mail stops marketing mail. It does not stop transactional mail
   about the account (§3.3 for the classification).
2. **Speed.** Honour it well inside the strictest published time you have read (Yahoo's two days is a
   provider's, and the law's time limits are the data-protection owner's to state). A queue of already
   scheduled sends is the usual leak: check that the suppression is read at send time, not when the audience
   was built.
3. **Test it end to end**: send to a seed address, click the visible link, post to the header address, send
   again, and confirm nothing arrives.

## 2.5 Failure patterns
- **Header present, DKIM not covering it.**
- **Redirect in the one-click path.**
- **Token-less address.**
- **Login wall in front of the unsubscribe.**
- **Suppression read when the audience was built, not when the message goes out.**
- **Preference page as the only exit.**
