# cra-scope-and-role-determination-pitfalls §4 — What to inventory, record and escalate

> Part 4 of `skills/cra-scope-and-role-determination-pitfalls`. Read it when the determination is turned into
> a register. Source: Regulation (EU) 2024/2847 as published in the Official Journal,
> https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R2847, read 2026-10-19, original
> publication, not consolidated: re-read before relying. "Own guidance" marks our sentences. Not legal advice,
> escalate to counsel.

1. **One register row per product release line.** Own guidance, fields: product name, what it is (software,
   hardware, with remote processing), interfaces and connections, markets where supplied, since when, commercial
   activity around it, name or trademark it carries, who developed it, supplier and customer chain (Article 23
   makes this retrievable on request), intended-purpose documents, exclusions considered, role per flow, class
   candidate, counsel's answer with date and name.
2. **Components and the SBOM.** Article 3(6) defines component as software or hardware intended for integration
   into an electronic information system; Article 3(39) defines a software bill of materials as a formal record
   of details and supply chain relationships of components in the software elements. Article 13(24) lets the
   Commission specify its format and elements by implementing act; Article 13(25) lets authorities request
   SBOMs in a dependency assessment. Own guidance: produce an SBOM per release in a standard machine-readable
   form and keep it with the register; the format to adopt later was not checked.
3. **Support period is a decision to write down.** Article 3(20) defines it; Article 13(8) says manufacturers
   determine it from the expected use time and user expectations, and the information taken into account goes in
   the technical documentation. Article 13(19) requires the end date, with at least month and year, to be stated
   at purchase. Minimum lengths in the text are re-read by counsel before use. Own guidance: record the decision,
   the reasons, its owner and the date, and compare with the support periods of integrated third-party
   components, which the article lists as a factor.
4. **Record the manufacturer-side evidence early.** Article 13(7) says relevant cybersecurity aspects,
   including vulnerabilities learned of, are documented systematically and proportionately. Article 13(4)
   puts the risk assessment in the technical documentation. Own guidance: start the risk assessment file and the
   decision log at determination time, not at conformity time.
5. **Triggers to re-run the determination.** New product, new market, new commercial offer on an open-source
   project, rebrand or white-label contract, substantial modification, a new important dependency, an
   amendment to the Regulation or a new implementing act (`business/regulatory-watch` §5 for retrieving the
   current text, `skills/source-freshness` §1 for stamping what was read).
6. **Licences are a separate axis.** Open-source licence duties come from licence terms, not from this
   Regulation; see `business/licence-compliance` §5 for dependency verdicts.
7. **Escalate with a package.** Send counsel: the register row, the definitions and exclusion sentences read with
   the read date, the unresolved questions, and the launch or contract date at risk. Dates and deadlines come
   from counsel reading Article 71 and amendments; this block states none (see
   `skills/cra-exploited-vulnerability-clock` part 1 for the reporting clock as read).
8. **Output ends with** "Not legal advice, escalate to counsel."
