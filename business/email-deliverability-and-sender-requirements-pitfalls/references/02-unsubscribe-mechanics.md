# email-deliverability-and-sender-requirements-pitfalls §2 — Unsubscribe mechanics

An unsubscribe that works in a test and fails in a mailbox is a deliverability problem and a trust problem at
once. The header rules below come from RFC 8058 as returned by a fetch digest that quoted sections 1, 3.1, 3.2,
4 and 6 on 2026-10-20; `re-read before relying` against the RFC text. What the law requires of an
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
3. **A GET to the same address shows a page**, because a person or a scanner may fetch it that way. Whether
   a scanner's fetch of a header address is a concern is addressed by the RFC's background (section 1: anti-spam
   software often fetches URLs found in headers) and by the receiver's consent rule below; the RFC digest did
   not say that POST avoids scanner fetches, so treat any claim that it does as a hypothesis.
4. **The receiver must not POST without user consent** (section 3.2); how consent is obtained is not defined.
   So the sender cannot assume a POST means the user acted in a given way.
5. **Check it from outside.** Post to the address the way a receiver would, without cookies, and read the
   status and the absence of a redirect. A test from the sending tool's own screen proves nothing about the
   mailbox.

## 2.3 What the two providers add
1. **Google** (read on its sender guidelines page): marketing and subscribed mail from the 5,000-a-day group
   supports one-click and carries a clearly visible link in the body. Offering other options (a list review, an
   automatic removal after bounces) is allowed but must not replace one-click.
2. **Yahoo** (read on its sender requirements page): a functioning header supporting one-click for marketing
   and subscribed mail; the RFC 8058 method is highly recommended and a mailto method is acceptable; a visible
   body link that may lead to a preference page; unsubscribes processed within two days; no login required.
3. **Google's page does not state a processing time.** Do not quote Yahoo's two days as Google's.
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
