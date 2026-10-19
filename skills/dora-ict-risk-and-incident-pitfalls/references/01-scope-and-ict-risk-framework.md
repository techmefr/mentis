# dora-ict-risk-and-incident-pitfalls §1 — Scope and ICT risk-management framework

> Part 1 of `skills/dora-ict-risk-and-incident-pitfalls`. Read it when scope is unclear or a framework duty is
> mapped to engineering work. Source: Regulation (EU) 2022/2554, Articles 2 to 6 and 8 to 14, as published in
> the Official Journal (OJ L 333, 27.12.2022), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2554 ,
> read 2026-10-19. That is the original publication, not a consolidated version: read the current text before
> relying on it. Sentences marked "own guidance" are ours. Not legal advice, escalate to counsel or the
> compliance function.

1. **Scope is a question for counsel, asked first.** Article 2(1) lists the entities the regulation applies to:
   credit, payment, e-money and investment firms, crypto-asset service providers, market infrastructures,
   insurers and intermediaries, fund managers, rating agencies, crowdfunding providers and others, and, as the
   last item, ICT third-party service providers. Article 2(3) removes some categories and 2(4) lets Member States
   exclude certain entities. Own guidance: write the question "is this entity in scope, under which category,
   and does any exclusion apply" and give it to counsel; never answer it from a product's marketing category.
2. **"Financial entity" has a defined meaning.** Article 2(2) uses the term for items (a) to (t) only, so the
   ICT providers of item (u) are in the regulation's scope without being "financial entities". Own guidance:
   a supplier records which of the two it is, because several duties are written for financial entities only.
3. **Proportionality changes how a duty is applied, not whether to ask.** Article 4 requires the framework
   rules to be applied in light of size, risk profile and the nature, scale and complexity of services. Article
   16 sets a simplified framework for named small categories; Articles 5 to 15 do not apply to them. Several
   duties also carve out microenterprises (a defined term in Article 3). Own guidance: mark each duty you map
   with the carve-out text, and let compliance decide which regime the entity is under.
4. **Governance sits with the management body.** Article 5 makes it define, approve, oversee and answer for
   the ICT risk framework, set roles, approve the continuity policy and the third-party policy, and receive
   reporting on third-party arrangements and major incidents; entities other than microenterprises name a role
   or a senior person to oversee third-party arrangements. Own guidance: engineers prepare the inputs for that
   reporting channel (inventory counts, incident summaries); they do not own the accountability.
5. **The framework must be documented and reviewed.** Article 6(1) and (5): a documented framework, reviewed at
   least yearly (periodically for microenterprises) and after major incidents, with a review report available
   to the authority on request. Article 6(8) lists what the resilience strategy contains, including an ICT
   reference architecture and the impact tolerance for disruptions. Own guidance: date every framework document
   and keep the review as a recorded event.
6. **Inventory is a duty with a review rhythm.** Article 8 requires identifying and documenting ICT-supported
   business functions, the information and ICT assets behind them, and their dependencies, reviewed as needed
   and at least yearly; mapping of critical assets with their configuration and interdependencies; documenting
   every process that depends on an ICT third-party provider; and updating the inventories on each major
   change (8(1), (4), (5), (6)). A risk assessment follows each major change for entities other than
   microenterprises, and legacy systems get a specific assessment (8(3), (7)). Own guidance: build the
   inventory from the deployment and procurement sources, not from memory, and store a last-verified date per
   row.
7. **Protection duties are engineering-facing.** Article 9 lists: an information security policy, network
   segmentation that can sever connections, access limited to what a function needs, strong authentication and
   key protection, documented change management where every change is recorded, tested, assessed, approved and
   verified, and documented patch and update policies. Own guidance: map each to the existing control and
   evidence (pipeline logs, access reviews) and list the gaps, without claiming conformity.
8. **Detection needs thresholds that trigger a process.** Article 10 requires mechanisms to detect anomalies and
   single points of failure promptly, multiple control layers, alert thresholds and criteria that start incident
   response with automatic alerts, regularly tested. Own guidance: the link from an alert to an incident record
   (part 2) is a seam to test.
9. **Continuity, backup and recovery have tested plans.** Article 11 requires a continuity policy, response and
   recovery plans, a business impact analysis, tests at least yearly and after substantive changes to systems
   supporting critical or important functions, crisis communication tests, and readily accessible records of
   activity before and during disruptions. Article 12 requires documented backup policy with scope and minimum
   frequency, tested restoration, restoration on systems segregated from the source, recovery time and point
   objectives set per function, and integrity checks on recovery. Own guidance: a restore test is evidence; a
   backup job's green status alone is not.
10. **Learning and communication are duties too.** Article 13 requires post-incident reviews after a major
    incident that disrupts core activities, lessons fed into the risk assessment, yearly reporting of findings
    to the management body, and awareness and resilience training for staff. Article 14 requires crisis
    communication plans and at least one person tasked with incident communication. Own guidance: schedule the
    review as a ticket opened by the incident record, not by memory.
11. **Technical standards add detail that was not read.** Articles 15 and 16(3) delegate further specification
    to technical standards by the European supervisory authorities. Own guidance: for any "how exactly" question
    (content of policies, report formats), look up the current standard and ask the compliance function.
12. **Do not outsource the responsibility.** Article 6(10) allows verification tasks to be outsourced while the
    entity "remains fully responsible". Own guidance: a supplier that offers a compliance service says what it
    covers and never sells the responsibility.
