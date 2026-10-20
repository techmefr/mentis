# outbound-sales-and-crm-hygiene-pitfalls §4 — Consent and opt-out as method

Method only, re-read before relying, not legal advice. Rules on unsolicited messages differ by country, by
channel and by whether the recipient is a person or a company; the point here is the discipline that lets legal
answer, not the answer.

## 4.1 Source lineage
1. **Every contact carries where it came from and when**: a form, an event list, a purchased list, a public
   profile, a referral. Symptom: nobody can say why a person was contacted when they ask. Check: pick ten
   contacts and trace each to a source in one step. Fix: add the source field and refuse imports without it.
2. **Keep the source with the record through merges** (§2.2).
3. **A bought or scraped list is a question for legal before the first send**, not after the first complaint.

## 4.2 One suppression list
1. **Keep a single suppression list** of people who asked to stop, bounced hard or complained, keyed on every
   identifier you hold (email, profile address, phone).
2. **Apply it before every list load and every send**, in every tool. Check: add a test address, load a list
   containing it, confirm it is dropped before sending.
3. **An opt-out reaches every channel**, unless legal has written otherwise for a specific, narrower request.
4. **Keep the suppressed entry, not just the flag.** Deleting a person to honour an opt-out removes the memory
   that stops the next import from adding them back. How long the entry is kept is a question for legal.

## 4.3 Honouring a request
1. **A request is honoured at the moment it arrives**, then checked: the record is flagged, queued sends are
   cancelled, other tools are updated. Symptom: the person is mailed after asking because an export was already
   scheduled.
2. **Every message states who sent it and gives a working way to stop**, in the form legal approves for that
   audience. Whether a postal address, a particular wording or a one-click header is required is a question for
   legal; the header mechanics are `business/email-deliverability-and-sender-requirements-pitfalls`.
3. **Do not ask for a reason or require a login to opt out.** Friction here becomes a complaint.

## 4.4 What to bring to legal
1. **A short list**: the audiences (country, person or company), the channels, the source of each list, the
   message text, how an opt-out is processed, how long suppressed entries are kept.
2. **Legal decides.** This block only makes sure the facts are on the table; the personal-data basis and
   retention are `business/data-protection`.
