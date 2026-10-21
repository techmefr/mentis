# email-deliverability-and-sender-requirements-pitfalls §3 — Streams, complaint rate and lists

The three subjects share a cause: reputation is attached to a domain or an address, and what one kind of mail
does to it, the other kind inherits. Platform figures were read on 2026-10-20 on the raw pages: `re-read before relying`.

## 3.1 Keep the streams apart
1. **Transactional and marketing mail are different categories.** Yahoo's page advises not sending bulk or
   marketing mail from the same IPs as user, transactional or alert mail, and separating by IP or by signing
   domain, since each carries its own reputation. Vendor guides say the same with subdomains.
2. **Do not mix content types inside one message.** Google's page says not to put promotions into receipts.
   A promotion inside a receipt makes the message marketing for the purposes of unsubscribe and reputation.
3. **One consistent From per category.** Changing the sender identity in the middle of a program confuses
   recipients and receivers alike.
4. **Which messages count as transactional in law** is a question for `business/data-protection`, not for
   this block. Apply the same test to the copy: what is the message for, and would the recipient expect it
   without having subscribed to anything.

## 3.2 A complaint rate has a source and a denominator
1. **Google** (sender guidelines page and FAQ): the spam rate is read in Postmaster Tools; the page gives 0.10
   percent as a target and says to stay below 0.30 percent and never reach it. The FAQ says the rate is
   user-reported, calculated daily, that rates above 0.10 percent already hurt inbox delivery for bulk senders,
   and that above 0.30 percent a bulk sender is ineligible for mitigation. Neither page defines the
   denominator.
2. **Yahoo** (sender requirements page): below 0.3 percent, computed on mail delivered to the inbox, and the
   page asks the sender to enrol in the complaint feedback loop and to expect its figures to differ from the
   sender's own.
3. **Every other figure is somebody's convention.** Vendor guides quote 0.05 and 0.01 percent and several
   different bounce bands that contradict each other. Quote none of them as a limit; if one is used as an
   internal alert level, say it is an internal choice.
4. **Write the source next to the figure**: Postmaster Tools, the Yahoo feed, the sending provider's
   dashboard, or the sender's own count of complaint events over mail sent.
5. **Never add or compare rates from different tools as if they were equal.** One counts complaints over
   inbox-delivered mail, another over delivered, another over sent. A drop between two tools is a change of
   denominator until shown otherwise.
6. **A rate with a small denominator is noise.** A handful of complaints on a small send moves the percentage
   far; say how many complaints and over how many messages.

## 3.3 Lists, bounces and suppression
1. **Consent-based acquisition.** No purchased, rented or scraped lists. That is a deliverability point (the
   addresses were not given to you) and a data-protection one; the second belongs to
   `business/data-protection`.
2. **Hard bounces are suppressed at once.** Soft bounces are suppressed after repeated failure; the retry
   ladder and counts in vendor guides are conventions, so take the provider's documented behaviour and write
   down what it is.
3. **A bounce or a complaint is global suppression**, across every flow and every list. An unsubscribe is
   **scoped** to the category it was given for, which is usually marketing.
4. **An import from an old provider must not re-import its bounce and complaint lists as clean.** Bring the
   suppressions across first, then the contacts.
5. **A re-engagement attempt comes before removing inactive contacts.** Define "inactive" by a human signal
   (a click, a reply, a visit, a login) and a window, never by opens (see
   `business/email-campaign-measurement-and-testing-pitfalls` §1).
6. **The tension to name, not resolve.** A suppression list exists so that a person is never mailed again,
   which means keeping the address. Retention rules say not to keep data longer than needed. One vendor guide
   says "never delete" and another vendor guide ties some retention to a country's law. Both are positions;
   the owner of data protection decides what is kept, in what form (a hashed address is one option to ask
   about), and for how long. Take the question to `business/data-protection`.
7. **Never read a consent or retention rule off a vendor guide.** The vendor guides carry penalty figures and
   consent summaries that conflict with each other and with the regulators' pages.

## 3.4 Failure patterns
- **One rate, no source.**
- **Blended sending domain**, so that a marketing complaint hurts password-reset mail.
- **Promotion in a receipt.**
- **Bounce list left behind in the migration.**
- **Dormancy defined by opens, then mail stops to people who read it.**
