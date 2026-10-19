# gdpr-breach-notification-and-dpia-pitfalls §2 — Notifications and communication

> Part 2 of `skills/gdpr-breach-notification-and-dpia-pitfalls`. Read it when a notice to the authority or a
> message to the people concerned is drafted or a template is built. Source: Regulation (EU) 2016/679 Article
> 33(3) and Article 34, as published in the Official Journal (OJ L 119, 4.5.2016),
> https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read 2026-10-19. Original
> publication, not a consolidated version: read the current text before relying on it. Sentences marked "own
> guidance" are ours.

1. **The authority notice has a minimum content.** Article 33(3) says it at least describes the nature of the
   breach, including where possible the categories and approximate number of people and of records concerned;
   gives the name and contact details of the DPO or another contact point; describes the likely consequences;
   and describes the measures taken or proposed, including mitigation where appropriate. Own guidance: the
   template has one block per item, with a visible "unknown yet" marker, so a gap is declared instead of hidden.
2. **Numbers are approximate and said so.** The text asks for approximate numbers "where possible". Own guidance:
   an estimate carries its basis (the query, the log range) and is revised in a later phase (part 1, point 6)
   rather than held back.
3. **Facts come from the case, wording comes from the DPO.** Own guidance: the engineer fills the nature, the
   data categories and the measures from the case record; the consequences paragraph and the final text are
   written or approved by the DPO or counsel. No notice leaves the company without that approval.
4. **A message to the people concerned is a separate decision.** Article 34(1) says that when the breach is
   likely to result in a high risk to the rights and freedoms of natural persons, the controller communicates the
   breach to the data subject without undue delay. Whether the threshold is met is not decided here; it goes to
   the DPO with the facts (part 1, point 4). Own guidance: the case has a distinct question for it, answered and
   dated, because the threshold differs from the one for the authority.
5. **That message has its own form.** Article 34(2) says it describes the nature of the breach in clear and plain
   language and contains at least the information and measures from points (b), (c) and (d) of Article 33(3): the
   contact point, the likely consequences and the measures taken or proposed. Own guidance: write for a person
   with no technical background, say what they can do, and test the draft on someone outside the team.
6. **The conditions that remove the duty are the DPO's call.** Article 34(3) lists three cases where the
   communication is not required: protection measures applied to the affected data that make it unintelligible to
   unauthorised persons, such as encryption; subsequent measures after which the high risk is no longer likely
   to materialise; and disproportionate effort, in which case a public communication or similar measure informs
   people equally effectively. Own guidance: an engineer may state the facts behind a condition (what was
   encrypted, with which key held where, what was done after), never conclude that it applies. The conclusion and
   the author are recorded in the register.
7. **The authority may decide too.** Article 34(4) says that if the controller has not already communicated, the
   authority, having considered the likelihood of a high risk, may require it or decide that a condition of
   paragraph 3 is met. Own guidance: a "no message" decision is recorded with its reasoning so it can be shown
   to the authority.
8. **Plan the channel before the day.** Own guidance: for each population the product holds (customers,
   employees, users of a free tier), the contact route and its freshness are known in advance, and a disclosure
   page or equivalent exists that can be switched on. Use `skills/incident-comms-pitfalls` for the wording
   discipline, with the DPO's text prevailing where they differ.
9. **One version of the facts.** Own guidance: the authority notice, the people's message, the public statement
   and the status page are all written from the same case record; when a fact changes, the record changes first
   and each text is revised from it with the date.
