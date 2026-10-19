# dora-ict-risk-and-incident-pitfalls §2 — Incident management and reporting

> Part 2 of `skills/dora-ict-risk-and-incident-pitfalls`. Read it when an incident process is built, tested or
> an incident is under way. Source: Regulation (EU) 2022/2554, Articles 3, 17, 18, 19, 20 and 23, as published
> in the Official Journal (OJ L 333, 27.12.2022), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2554 ,
> read 2026-10-19. Original publication, not a consolidated version. Sentences marked "own guidance" are ours.
> Not legal advice, escalate to counsel or the compliance function.

1. **An incident is defined broadly.** Article 3 defines an ICT-related incident as an unplanned event or linked
   series that compromises network and information system security and harms the availability, authenticity,
   integrity or confidentiality of data or of services; a "major" one is an incident with a high adverse impact
   on systems supporting critical or important functions. Own guidance: the record must separate "incident" from
   "major incident" as two fields, the second set by a named person.
2. **Record every incident and significant cyber threat, with root cause.** Article 17(2) requires recording all
   ICT-related incidents and significant cyber threats, and procedures that identify, document and address
   root causes. Own guidance: the record is the source for later reports, so capture timestamps of detection,
   of awareness and of each status change at the time they happen.
3. **The process has seven working parts.** Article 17(3): early warning indicators; procedures to identify,
   track, log, categorise and classify; assigned roles per incident type; communication and escalation plans,
   including client notification and customer complaints; reporting at least major incidents to senior
   management and to the management body; response procedures. Own guidance: test one route per part with a
   dummy incident.
4. **Classification uses six criteria.** Article 18(1): clients or counterparts affected, number or amount of
   transactions, and reputational impact; duration and downtime; geographical spread, particularly more than
   two Member States; data losses; criticality of affected services; economic impact, absolute and relative.
   Significant cyber threats are classified on criticality of services at risk, clients targeted and
   geographical spread (Article 18(2)). Own guidance: make each criterion a field the on-call person can fill,
   with "unknown yet" allowed and dated.
5. **The thresholds are not in the article.** Article 18(3) delegates the materiality thresholds for "major"
   and for "significant" threat to technical standards that were not read for this block. Own guidance: never
   write a number into a runbook from memory; link the current standard and let the compliance function approve
   the threshold table.
6. **Reporting goes to the relevant competent authority in stages.** Article 19(1) and (4): major incidents are
   reported to the relevant authority through an initial notification, an intermediate report when the status
   changes significantly or on request, and a final report once root cause analysis is complete and actual
   figures replace estimates. The time limits are laid down under Article 20 and were not read. Own guidance:
   the process stores which stage was sent, when and by whom, and the due time of the next stage comes from the
   current text, never from a template in someone's head.
7. **Use the prescribed templates; say so if you cannot.** Article 19(1) requires the reports to be produced
   with the templates under Article 20 and, if a technical impossibility prevents using the template for the
   initial notification, the authority is told by other means. Own guidance: keep an out-of-band contact route
   written and tested.
8. **Clients are informed without undue delay.** Article 19(3): when a major incident affects clients' financial
   interests, they are informed as soon as the entity is aware, with the mitigation measures taken; for a
   significant cyber threat, potentially affected clients are told of protection measures they may take. Own
   guidance: client messaging is a prepared template owned by the entity's communication person (Article 14).
9. **Reporting may be outsourced, responsibility may not.** Article 19(5) allows outsourcing the reporting to a
   third-party provider; the entity "remains fully responsible". Own guidance: a supplier that files on behalf of
   a client needs the contract to say who decides "major" and who signs the report.
10. **Payment-related incidents follow the same chapter.** Article 23 applies the chapter to operational or
    security payment-related incidents for credit, payment, account information and e-money institutions. Own
    guidance: if the entity is one of those, ask counsel how the payment-related incident rules interact with the
    process before merging queues.
11. **Notifying other bodies is a separate question.** Article 19(1) lets Member States require copies to other
    authorities or CSIRTs, and Article 19(2) makes notification of significant cyber threats voluntary. Own
    guidance: list the national additions as questions for counsel; for overlap with the network and information
    security directive, see the sibling block on that directive if it exists, and cite it only by its number.
12. **A supplier's duty is contractual first.** The incident reporting duty of Article 19 is the financial
    entity's. Own guidance: a supplier records detection-to-notice times for its clients, because the client's
    contract may require assistance and notice (part 3, point 8), and sends only the facts it can confirm.
13. **Learn from the incident.** After a major incident disrupting core activities, Article 13(2) requires a
    review of causes and improvements; Article 6(5) requires re-reviewing the framework after major incidents.
    Own guidance: the closure of the final report opens the review ticket automatically.
