# cra-scope-and-role-determination-pitfalls §2 — Which economic-operator role we hold

> Part 2 of `skills/cra-scope-and-role-determination-pitfalls`. Read it when a team ships, resells, integrates,
> forks or modifies a product. Source: Regulation (EU) 2024/2847 as published in the Official Journal,
> https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R2847, read 2026-10-19, original
> publication, not consolidated: re-read before relying. "Own guidance" marks our sentences. Not legal advice,
> escalate to counsel.

1. **Roles are per product and per flow.** Article 3(12) defines economic operator as the manufacturer, the
   authorised representative, the importer, the distributor, or another person subject to obligations in
   relation to manufacture or making available. One organisation can hold several roles across its products.
   Own guidance: build a table product by product, never a single role for the company.
2. **Manufacturer.** Article 3(13): a person who develops or manufactures products with digital elements, or has
   them designed, developed or manufactured, and markets them under its name or trademark, whether for payment,
   monetisation or free of charge. Own guidance: both halves matter: developing (or commissioning) and putting
   its own name or trademark on it. Record who developed it, who commissioned it and whose name is on it.
3. **Importer and distributor.** Article 3(16): an importer is a person established in the Union who places on
   the market a product bearing the name or trademark of a person established outside the Union. Article 3(17):
   a distributor is a person in the supply chain, other than manufacturer or importer, who makes the product
   available without affecting its properties. Own guidance: "without affecting its properties" is the line to
   test whenever we repackage, preconfigure or bundle.
4. **Becoming a manufacturer by acting.** Article 21 as read: an importer or distributor is considered a
   manufacturer, subject to Articles 13 and 14, when it places the product on the market under its own name or
   trademark or carries out a substantial modification. Article 22: a person other than manufacturer, importer or
   distributor who carries out a substantial modification and makes the product available is considered a
   manufacturer, for the affected part or for the whole product when the cybersecurity of the whole is
   affected. Own guidance: a white-label deal, a rebrand or a patched fork is a role question to settle before
   signing, not after shipping.
5. **What each role is expected to do, by heading only.** Article 13 lists manufacturer obligations (design to
   the Annex I Part I requirements, a documented cybersecurity risk assessment, due diligence on third-party
   components, vulnerability handling for the support period, technical documentation, conformity assessment,
   declaration of conformity and CE marking, a single point of contact, user information, and others).
   Article 19 sets importer checks (conformity assessment done, documentation drawn up, CE marking, declaration,
   user information, manufacturer identification). Article 20 sets distributor checks (CE marking, documents,
   due care). Each also has duties to inform the manufacturer and authorities of vulnerabilities and
   non-conformity. Own guidance: use these headings to find the owner of each duty; the duties themselves are
   re-read in the article by counsel before anyone plans work from them. The reporting clock is in
   `skills/cra-exploited-vulnerability-clock` (part 1).
6. **Authorised representative.** Article 18 allows a manufacturer to appoint one by written mandate and lists
   Article 13 paragraphs that are not part of the mandate. Own guidance: if a manufacturer outside the Union
   is in the chain, ask who holds this role and whether a mandate exists.
7. **Chain evidence.** Article 23 requires economic operators, on request, to identify to market surveillance
   authorities who supplied them and, where available, whom they supplied, and to be able to present this for
   a stated number of years. Re-read the period before citing. Own guidance: the product register keeps supplier
   and customer names per release.
8. **Stop and escalate** when the role depends on contract wording, on who holds the trademark, or on
   whether a change is "substantial". Role is a legal conclusion; this block only prepares the facts.
