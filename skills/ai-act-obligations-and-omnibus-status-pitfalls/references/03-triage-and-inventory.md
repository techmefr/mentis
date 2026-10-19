# ai-act-obligations-and-omnibus-status-pitfalls §3 — Triage and inventory

> Part 3 of `skills/ai-act-obligations-and-omnibus-status-pitfalls`. Read it when systems are listed or classified.
> Source: Regulation (EU) 2024/1689, Articles 5(1), 6, 49, 50, 51, 53(1), 3(63) and Annex III headings, as originally
> published, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689 , read 2026-10-19; Regulation
> (EU) 2026/1744 points 7, 8 and 20 read for the changes noted. Statements are in our own words. The classes below are a
> triage for a human, not a classification. Sentences marked "own guidance" are ours.

1. **Triage in a fixed order.** Own guidance: for each system or model ask in turn whether a prohibited practice may be
   involved, whether it may be high-risk, whether a transparency duty may apply, and whether it is, or builds on, a
   general-purpose model. A system can sit in more than one class. A "maybe" goes to counsel, not to a decision.
2. **Prohibited practices (Article 5(1)).** As read, the list includes manipulative or deceptive techniques that
   materially distort behaviour; exploiting vulnerabilities from age, disability or social or economic situation;
   social scoring with defined detrimental effects; criminal-risk prediction based solely on profiling; untargeted
   scraping of facial images to build recognition databases; emotion inference in workplaces and education, with a
   medical or safety exception; biometric categorisation to infer sensitive attributes; and real-time remote
   biometric identification in public spaces for law enforcement, subject to listed exceptions. The act read adds
   points (ba) and (bb), on generating intimate or sexually explicit material of an identifiable person without consent
   and on child sexual abuse material, with paragraphs 1a and 1b qualifying when the placing on the market is caught.
   Own guidance: each wording is a legal test, not a keyword; any hit, even a partial one, stops work on that feature
   until counsel answers.
3. **High-risk by two routes (Article 6).** Route one: the system is a safety component of a product, or is itself a
   product, covered by the Union harmonisation legislation listed in Annex I, and that product needs a third-party
   conformity assessment. Route two: the system falls in an area of Annex III, whose headings read include
   biometrics, critical infrastructure, education and vocational training, employment and worker management, and
   access to essential private and public services. Own guidance: map each system to the Annex III heading it may
   touch, and keep that mapping even when the answer is "none".
4. **A derogation exists and has limits (Article 6(3) and (4)).** An Annex III system is not high-risk if it poses no
   significant risk of harm to health, safety or fundamental rights, including by not materially influencing
   decision-making, when it meets one of four conditions (narrow procedural task, improving a completed human
   activity, detecting decision patterns without replacing human assessment, or a preparatory task); it is always
   high-risk if it profiles natural persons. A provider relying on it must document the assessment before placing on
   the market. As originally published it must also register the system (Article 49(2)); the proposal wanted to
   remove that registration and its fate in the act was not checked. Own guidance: record the assessment and which
   condition is claimed; whether it holds is a question for counsel.
5. **The act adds clarifications on safety components (Article 6(1a) to (1c) as inserted).** Systems used solely for
   non-safety aspects of assistance, optimisation, efficiency, automation, convenience or quality control are not
   safety components, while a system whose failure would endanger health and safety is one. Own guidance: re-run the
   Annex I route for any system previously excluded on that ground.
6. **Transparency duties (Article 50).** As read: providers must design systems that interact directly with people so
   that people are told they deal with an AI, unless obvious; providers of systems generating synthetic audio, image,
   video or text must mark outputs in a machine-readable, detectable way; deployers of emotion recognition or biometric
   categorisation must inform the people exposed; deployers of systems producing deep fakes must disclose that the
   content is generated or manipulated, with a lighter form for evidently artistic or satirical works; and
   deployers publishing AI-generated text to inform the public on matters of public interest must disclose it,
   unless a human review or editorial control exists with editorial responsibility. Information must be given at the
   latest at the first interaction or exposure, in a clear and distinguishable way, and meet accessibility
   requirements. Own guidance: put the disclosure wording and its place in the interface in the inventory.
7. **General-purpose models (Articles 3(63), 51, 53(1)).** A model with significant generality, able to perform a wide
   range of tasks and to be integrated downstream. Systemic risk is attached to high impact capabilities, presumed above
   a computation threshold written in the article, or to a Commission decision. Providers of such models must keep
   technical documentation, supply information to downstream integrators, keep a copyright-compliance policy and
   publish a training-content summary. The threshold value and the list were not copied here. Own guidance: a team that
   fine-tunes or integrates a model records which of the two it is, and asks counsel when it may be a provider of
   the model itself.
8. **What to inventory.** Own guidance, one row per system or model: name; owner; intended purpose and the marketing
   copy that states it; role as provisionally read (see part 2); model and vendor in use and the contract; where the
   output is used; affected people; provisional class and the Annex III heading considered; transparency measure and
   where it appears; the human oversight in place; data sources; changes since launch (rebrand, retrain, new purpose);
   and the date and name of counsel's answer.
9. **What to record when something changes.** Own guidance: a change log per system, with who decided, the reason,
   the test run and the date; an incident or complaint log; and a literacy log of training offered. Keep them in
   one place and name its owner.
10. **What this part cannot settle.** The class of any real system, the reading of any exception, and the content of
    obligations beyond those quoted here were not decided. Not legal advice, escalate to counsel.
