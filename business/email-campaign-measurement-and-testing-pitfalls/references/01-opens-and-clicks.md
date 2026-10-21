# email-campaign-measurement-and-testing-pitfalls §1 — Opens and clicks

Both counts feel like people. Both are, mechanically, requests for a resource. This section says what that
costs. The Apple facts were read on Apple's Mail Privacy Protection page on 2026-10-20 as raw page text;
the vendor and gateway facts on the pages named in §1.1 item 6 and §1.3 item 2. `re-read before relying`.

## 1.1 What an open is
1. **An open is a fetch of a small remote image (a tracking pixel), not a person reading.** It is recorded when
   the image is requested.
2. **Apple's page** says its privacy feature (named "Protect Mail Activity" on the current page, beside a
   separate "Hide IP Address" setting) downloads remote content in the background by default, whether or not
   the message is opened. The traffic goes through two relays: one knows the reader's IP address and not the
   content, the other knows the content and not the IP address. The reader can turn the feature off in the Mail
   settings of each device.
3. **So for readers behind it, an open can mean "the provider fetched it".** Their count is inflated. Readers
   who block images produce no open at all. The count is therefore wrong in both directions, for different
   people, and nothing in the number tells you the mix.
6. **An email vendor's own help page agrees.** Mailchimp's page on open and click rates says an open is counted
   when its tracking image is downloaded, that a client with images off registers no open, that a click is also
   counted as an open when the image did not load, and that bot activity such as Apple's feature can falsely
   inflate both opens and clicks. A vendor that sells the open rate says it is not 100 percent accurate.
4. **Not known from the pages read**: the share of your readers using that feature, which operating-system
   versions apply, and whether Google or Yahoo pre-fetch images. Apple's per-OS support pages and the other
   two providers' documentation were not read; one independent tester's claim that background download did
   not occur in his IMAP set-up was seen in a search result and is not verified. Say "unknown" for the share.
5. **Whether opens can still carry a signal** (for example a fetch that happens hours after delivery) is not
   settled by anything read here. Do not build a rule on it.

## 1.2 What not to do with opens
1. **Not for segmentation.** "Opened in the last 30 days" includes the relay's fetch and excludes the reader
   with images off.
2. **Not for sunset rules.** Removing "non-openers" removes people who read the mail.
3. **Not for subject-line winners** (§3.1), and not for an "engagement score" built on them.
4. **Not as the proof of a deliverability problem** (`business/email-deliverability-and-sender-requirements-pitfalls`
   §4.2).
5. **What to use instead**: a click that was followed by a session on the destination, a reply, a visit, a
   purchase, a login. Name which one the program is judged on, and write it where the report is.
6. **A diagnostic use is still allowed** if labelled: opens compared across two sends to the same audience as
   a rough sign that something moved, never as a statement about people.
7. **Two sources disagree and both are partly right.** One vendor guide keeps open rate as its primary result
   and sells a bot filter for it; two others say to stop optimising on opens or to turn open tracking off for
   cold mail. The first treats a fetch as a reader; the second is a stronger default.

## 1.3 What a click is
1. **A click is also a fetch**: a request to a tracking address that redirects to the destination.
2. **Something other than the person can make that request.** RFC 8058's section 1 (raw text) says anti-spam
   software often fetches resources in message headers automatically and a sender cannot tell that from a
   person. For body links: Microsoft's Safe Links page says Defender for Office 365 scans URLs in inbound mail
   during mail flow, rewrites them, and verifies them again at the time of click; and Mailchimp's page says
   bot activity can inflate click metrics. Neither page says a gateway always requests the destination, or what
   the sender's log then shows, so "scanners inflate body-link clicks" is supported but its size on your list
   is unknown; the next point is how to test it.
3. **Look for the pattern, do not assume it.** A click that arrives within seconds of delivery, on every link,
   in the recipients' list order, before any open or session, is the signature to check for in the raw click
   log. If it is present, filter those clicks or count only a click followed by a session on the destination.
   If it is absent, say that too.
4. **A vendor "bot detection" add-on is a product, not a method.** The method is the pattern check above
   and the session behind the click.
5. **Report clicks as "clicks, of which N backed by a session"** when the destination can be measured. When it
   cannot (a third-party page), say so and keep the claim modest.

## 1.4 Privacy of the measurement
Tracking pixels and tracked links place identifiers in mail. Whether and how they need consent, and what the
recipient must be told, is `business/data-protection` and `skills/event-tracking-plan-pitfalls`. This block
does not decide it.

## 1.5 Failure patterns
- **"Open rate" as the headline.**
- **Sunset by opens.**
- **A bot filter bought instead of a pattern checked.**
- **Clicks counted with no session behind them.**
- **The relay share assumed, either way.**
