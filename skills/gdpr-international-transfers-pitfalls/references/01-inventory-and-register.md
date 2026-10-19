# gdpr-international-transfers-pitfalls §1 — Inventory and register

> Part 1 of `skills/gdpr-international-transfers-pitfalls`. Read it when a flow is added, a register built or a
> vendor reviewed. Source: Regulation (EU) 2016/679 Article 44 and Article 49(6), as published in the Official
> Journal (OJ L 119, 4.5.2016), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read
> 2026-10-19. Original publication, not a consolidated version: read the current text before relying on it.
> Sentences marked "own guidance" are ours.

1. **The general principle covers more than storage.** Article 44 says a transfer of personal data that is
   undergoing processing, or intended for processing after the transfer, to a third country or an international
   organisation takes place only if the conditions of the chapter are met by controller and processor, including
   for onward transfers from the third country to another third country or organisation. Own guidance: the
   inventory starts from where the data can be read, not only from where the database sits. Whether remote access
   or support access is a transfer is a question for the DPO; the register records the fact so the question can
   be asked.
2. **Inventory every flow, including the dull ones.** Own guidance, a checklist of places data leaks out of the
   picture: error and log shippers, analytics and session replay, email and messaging providers, support desk and
   chat tools, backups and disaster-recovery regions, CDN and edge functions, AI and model providers, payment
   providers, HR and payroll tools, group-wide dashboards, contractors' laptops, shared drives, and test or
   staging data copied from production.
3. **One register row per flow.** Own guidance, the fields: the data categories (from the field list in
   `business/data-protection` part 1); the people concerned; the sending entity; the recipient entity and its
   legal location; the location of the processing and of every storage region; the locations from which staff or
   sub-processors can access it; the onward recipients; the purpose; the mechanism claimed (part 2); the evidence
   seen with its date; the owner; the next review date. A row with an empty "location of access" is incomplete,
   not "none".
4. **Onward flows are inventoried too.** Article 44 names onward transfers from the third country. Own guidance:
   for every vendor, ask for the sub-processor list and the countries of each, file it with its date, and
   subscribe to change notices. A sub-processor change is a register event with a review, not a mail to archive
   (the contract mechanism is in `skills/dpa-review-pitfalls` part 3).
5. **Ask the vendor the real location questions.** Own guidance: where is the data stored, where is it processed,
   who can access it from where (support, engineering, security), does the vendor have a parent or affiliates
   elsewhere, which sub-processors are in the chain. A vendor answer is filed as a document, with its author and
   date.
6. **The register feeds the record of processing.** Article 49(6) says that, for the case of the compelling-legitimate-
   interests derogation, the controller or processor documents the assessment and the suitable safeguards in the
   records referred to in Article 30. Own guidance: the register of flows and the processing record are one
   source or are linked by identifier, never two copies that drift (`business/data-protection` reference 05).
7. **A new flow is a design-time question.** Own guidance: the checklist "does a new recipient or a new region
   appear" sits in the design and the vendor-onboarding steps, so the row exists before the data moves. A flow
   discovered after launch is recorded as such and escalated (part 3, point 7), not quietly added.
8. **Dummy data for tests.** Own guidance: staging and test fixtures use dummy data, which removes a whole class
   of flows from the register; where production data reaches a test tool, the flow is registered like any other.
