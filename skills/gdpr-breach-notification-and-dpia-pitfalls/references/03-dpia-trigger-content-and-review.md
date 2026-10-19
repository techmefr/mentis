# gdpr-breach-notification-and-dpia-pitfalls §3 — DPIA trigger, content and review

> Part 3 of `skills/gdpr-breach-notification-and-dpia-pitfalls`. Read it when a new or changed processing is
> planned, or an assessment is written or audited. Source: Regulation (EU) 2016/679 Article 35 and Article 36(1)
> to (3), as published in the Official Journal (OJ L 119, 4.5.2016),
> https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read 2026-10-19. Original
> publication, not a consolidated version: read the current text before relying on it. Sentences marked "own
> guidance" are ours.

1. **The assessment comes before the processing.** Article 35(1) says that where a type of processing, in
   particular using new technologies and given its nature, scope, context and purposes, is likely to result in a
   high risk to the rights and freedoms of natural persons, the controller carries out, prior to the processing,
   an assessment of the impact on the protection of personal data. A single assessment may cover a set of similar
   operations with similar high risks. Own guidance: the check sits in the design step, not in release week.
2. **Run a recorded trigger check on every new processing.** Own guidance: a short form answered at design time,
   with the date, the answers and the name of the person who decided. "Not needed" is a decision with an author,
   not an absence of paper. The engineer supplies the facts; the DPO or counsel decides.
3. **The text names three cases where it is required.** Article 35(3): a systematic and extensive evaluation of
   personal aspects based on automated processing, including profiling, on which decisions with legal or similarly
   significant effects are based; processing on a large scale of special categories of data (Article 9(1)) or of
   data on criminal convictions and offences (Article 10); and systematic monitoring of a publicly accessible area
   on a large scale. The word "in particular" means the list is not exhaustive. Own guidance: the form asks each of
   the three questions and also asks the open one ("new technology, new use, new population, high risk
   anyway?"). What counts as "large scale" or "similarly significant" is not decided here.
4. **Authority lists exist and are not in this block.** Article 35(4) and (5) say the supervisory authority
   establishes and publishes a list of processing kinds that require an assessment, and may publish a list of
   kinds that do not. Own guidance: the DPO names the competent authority and its current lists; the trigger form
   cites the list consulted and its date. For a French project, `business/data-protection` points to the
   authority's published material in its reference 01. The lists themselves were not read for this block.
5. **The content has four minimum items.** Article 35(7): a systematic description of the envisaged processing
   operations and purposes, including the legitimate interest pursued where applicable; an assessment of necessity
   and proportionality in relation to the purposes; an assessment of the risks to the rights and freedoms of
   the people concerned; and the measures envisaged to address the risks, including safeguards, security measures
   and mechanisms to protect data and demonstrate compliance. Own guidance: the document has one heading per
   item, and the field list of `business/data-protection` part 1 (and its reference 05) feeds the description.
6. **Ask the DPO, and write down the advice.** Article 35(2) says the controller seeks the advice of the data
   protection officer, where designated, when carrying out the assessment. Own guidance: the advice is requested
   in writing with the draft attached, and the answer and its date are stored with the assessment, including a
   disagreement and the reason the team went another way.
7. **People's views, where appropriate.** Article 35(9) says that where appropriate the controller seeks the
   views of the people concerned or their representatives on the intended processing, without prejudice to
   commercial or public interests or the security of operations. Own guidance: the form records whether the step
   was considered, what was done (user research, a representative body) or why not.
8. **Codes of conduct count.** Article 35(8) says compliance with approved codes of conduct is taken into due
   account when assessing impact. Whether a code applies is a question for the DPO.
9. **A high residual risk leads to the authority.** Article 36(1) says the controller consults the supervisory
   authority prior to the processing where the assessment indicates a high risk in the absence of measures taken
   by the controller to mitigate it. Own guidance: the assessment ends with a line stating the risk as it stands
   with the measures in place, and a high result is an escalation to the DPO before any launch date is promised.
10. **The consultation file is the assessment and more.** Article 36(3) lists what the controller provides: where
    applicable the responsibilities of controller, joint controllers and processors; the purposes and means; the
    measures and safeguards; the DPO's contact details; the assessment itself; and anything else the authority
    requests. Article 36(2) gives the authority a period of up to eight weeks from receipt to provide written
    advice, extendable by six weeks, with a notice of the extension and reasons within one month, and says those
    periods may be suspended while requested information is outstanding. Own guidance: plan the schedule from the
    text as read, treat the periods as a dependency of the release, and never start the processing meanwhile
    on the engineer's own reading. Whether a prior consultation is needed is not decided here.
11. **The assessment is reviewed, not filed.** Article 35(11) says that where necessary the controller reviews
    whether processing follows the assessment, at least when the risk represented by the operations changes.
    Own guidance: the assessment names its review triggers (new data category, new recipient, new country, new
    purpose, a breach, a change of vendor), and the change process checks them; this is a recorded line in the
    plan of any change touching the processing.
12. **An exception exists for some legal-basis cases.** Article 35(10) disapplies paragraphs 1 to 7 in a narrow
    case tied to a legal basis in Union or Member State law and a general impact assessment made when that law
    was adopted, unless Member States deem an assessment necessary. Whether it applies to a given processing is a
    question for counsel; the engineer never relies on it alone.
