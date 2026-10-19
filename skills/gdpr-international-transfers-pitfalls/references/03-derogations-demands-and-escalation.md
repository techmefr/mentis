# gdpr-international-transfers-pitfalls §3 — Derogations, foreign demands and escalation

> Part 3 of `skills/gdpr-international-transfers-pitfalls`. Read it when no mechanism is available, a derogation
> is proposed or a foreign demand arrives. Source: Regulation (EU) 2016/679 Articles 48 and 49, as published in
> the Official Journal (OJ L 119, 4.5.2016), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
> , read 2026-10-19. Original publication, not a consolidated version: read the current text before relying on
> it. Sentences marked "own guidance" are ours.

1. **Derogations apply only in the absence of the two routes.** Article 49(1) opens with the case where there is
   no adequacy decision and no appropriate safeguards, binding corporate rules included. Own guidance: the first
   question is whether route 1 or 2 (`02-mechanisms-and-proof.md`) was really excluded and by whom, not whether a
   derogation can be found.
2. **The listed derogations.** Article 49(1), first subparagraph, names seven conditions: explicit consent after
   being informed of the possible risks due to the absence of adequacy and safeguards; necessity for a contract
   with the data subject or for pre-contractual steps at their request; necessity for a contract in the interest
   of the data subject between the controller and another person; important reasons of public interest;
   establishment, exercise or defence of legal claims; protection of vital interests where the person cannot
   consent; and a transfer from a public register under conditions. Own guidance: the engineer may describe the
   facts of a flow in these words; whether a condition is met is not decided here.
3. **Each condition has limits in the text.** Paragraph 4 says the public interest is recognised in Union or
   Member State law. Paragraph 2 says a register transfer shall not cover the entirety of the data or entire
   categories in the register, and, where the register is open to persons with a legitimate interest, goes only
   at their request or to them. Paragraph 3 says the consent, contract and compelling-interest conditions do not
   apply to public authorities acting in the exercise of their public powers. Paragraph 5 says Union or Member
   State law may set limits on transfers of specific categories for important public-interest reasons.
   Own guidance: the checklist for a proposed derogation quotes the paragraph and the facts side by side.
4. **The last-resort case is narrow.** The second subparagraph of Article 49(1) says that where a transfer could
   not rest on Article 45 or 46 and no listed derogation applies, it may take place only if it is not repetitive,
   concerns only a limited number of people, is necessary for compelling legitimate interests of the controller
   not overridden by the interests and rights of the person, and the controller has assessed all the circumstances
   and provided suitable safeguards on that basis. The controller informs the supervisory authority and, besides
   the information of Articles 13 and 14, informs the person of the transfer and the interests pursued.
   Own guidance: a flow that recurs, covers a whole customer base or is run by an automated job is described as
   such and sent to the DPO; the engineer never builds a permanent feature on this case.
5. **The assessment is written down.** Article 49(6) says the controller or processor documents the assessment and
   the suitable safeguards of paragraph 1's second subparagraph in the records of Article 30. Own guidance: the
   file holds that assessment, who made it, the date and the notice to the authority and to the person, or states
   that none was sent and why.
6. **Foreign demands are a separate path.** Article 48 says a judgment of a court or tribunal, or a decision of an
   administrative authority, of a third country that requires a controller or processor to transfer or disclose
   personal data may be recognised or enforceable only if based on an international agreement, such as a mutual
   legal assistance treaty, in force between the requesting country and the Union or a Member State, without
   prejudice to other grounds for transfer under the chapter. Own guidance: the first engineer or support agent
   who receives a legal demand does not answer, does not hand over data and does not confirm that data exists;
   the demand is forwarded unchanged, the same day, to the person named in the runbook. Whether a given demand is
   enforceable here is for counsel.
7. **What the engineer sends to the DPO.** Own guidance, a one-page file per escalation: the flow and its register
   row; the data categories, number of people and their locations; the recipient entity, its location and its
   parent; the mechanism claimed and the evidence, or the statement that none exists; any foreign-law concern the
   vendor or the team knows of (stated as a fact, not a conclusion); the deadline pressure, if any; what the
   team proposes and what it will not do until answered. Questions that go in the file because the text read
   does not settle them: whether a country's law affects the chosen mechanism, whether extra measures are needed,
   whether access from abroad is a transfer, and whether a derogation is available.
8. **A flow found live without a mechanism.** Own guidance: record it, stop adding data to it where the DPO says
   so, and escalate the same day with the file in point 7; do not back-fill the row with a mechanism the file does
   not prove. The decision to suspend, keep or re-route belongs to the DPO or counsel.
9. **Review.** Own guidance: after any escalation, the register row, the vendor questionnaire and the onboarding
   checklist are updated so the next flow meets the question earlier.
