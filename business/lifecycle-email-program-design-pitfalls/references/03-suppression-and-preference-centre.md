# lifecycle-email-program-design-pitfalls §3 — Suppression, classification and the preference page

Suppression is the mechanism that makes "never mail this person again" true. In a program built flow by flow it
is usually true only inside the flow that recorded it. The mechanics of the unsubscribe headers, bounce handling
and sender requirements are `business/email-deliverability-and-sender-requirements-pitfalls`; this section is the
design decision that sits above them.

## 3.1 Suppression and unsubscribe belong to the account
1. **A person who unsubscribes from marketing is suppressed from every marketing flow, newsletter and campaign
   of the account, not only from the one that carried the link.** A per-flow unsubscribe means the same person
   keeps receiving mail from the other flows, which the person experiences as the unsubscribe not working.
2. **A hard bounce and a spam complaint suppress the address everywhere, for every type of message.** They say
   something about the address and the recipient, not about one flow.
3. **Entry checks the suppression record, and so does each send.** A person suppressed after entering a flow is
   removed at the next message, not after the sequence ends (§1.4).
4. **An import must not undo suppression.** Moving to a new provider or loading a purchased-in-good-faith
   partner list does not bring back addresses that had unsubscribed, bounced or complained; carry the old
   suppression records over first.
5. **Keeping a suppression record and keeping personal data no longer than needed pull in opposite
   directions.** The record exists so a person is never mailed again; a data-protection rule asks that data
   not outlive its purpose. How long the record may live is a question for the person who owns data
   protection (`business/data-protection`), not a default of this block and not "never delete".

## 3.2 Classify each message by what it is for
1. **A message is transactional or marketing by its purpose, decided per message.** A receipt, a password reset
   or a notice that the account changed is for the person's own transaction. An offer, a feature promotion or
   a "come back" is marketing. Being triggered by an event does not make it transactional: abandoned-cart and
   win-back mail are triggered and are marketing.
2. **A message that mixes the two is a marketing message.** A promotion inside a receipt changes what the
   message is, and what a person who opted out of marketing may be sent.
3. **An unsubscribe from marketing leaves transactional mail alone, and the reverse is false.** Nothing that
   stops a person receiving their own receipts is offered as a way to stop promotions.
4. **Which messages count as transactional in law is not decided here.** It is a question for the owner of
   data protection and, where it applies, a regulator's published guidance (`business/data-protection`).

## 3.3 The preference page is an addition, never the only way out
1. **A page where a person chooses topics or frequency can reduce unsubscribes**, because some people want
   less, not none. It is worth building.
2. **It does not replace the one-click unsubscribe path.** Published sender requirements from large mailbox
   providers ask for a one-click mechanism and a visible link, and say a preference page does not stand in for
   them (`re-read before relying`, the current requirement pages of the providers you send to).
3. **Name the failure: the preference page as the only exit.** "Manage your preferences" as the one link in the
   footer, a login before the page opens, several screens before the person can leave. The person who wants to
   stop should be able to stop in one step; the person who wants less is offered the page next to it.
4. **The preference page writes into the same suppression record as everything else (§3.1).** A "pause" or a
   topic switch that lives in a separate table the senders do not read is a preference that does not work.
5. **A preference is respected by every program in the inventory (§2.3)**, including the ones added after the
   page was built.
