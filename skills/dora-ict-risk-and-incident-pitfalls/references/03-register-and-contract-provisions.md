# dora-ict-risk-and-incident-pitfalls §3 — Register of information and contract provisions

> Part 3 of `skills/dora-ict-risk-and-incident-pitfalls`. Read it when a vendor is onboarded, a register is
> built or a contract is reviewed. Source: Regulation (EU) 2022/2554, Articles 3, 28, 29 and 30, as published
> in the Official Journal (OJ L 333, 27.12.2022), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2554 ,
> read 2026-10-19. Original publication, not a consolidated version. Sentences marked "own guidance" are ours.
> Not legal advice, escalate to counsel or the compliance function. For the generic vendor lifecycle see
> `business/vendor-management` §1 and §2.

1. **The entity stays fully responsible.** Article 28(1)(a): entities that use ICT services under contract
   remain fully responsible for compliance with the regulation and with financial services law. Own guidance:
   "the vendor is certified" is not an answer to an audit question; the entity needs its own evidence.
2. **Third-party risk lives inside the ICT risk framework.** Article 28(1) treats it as part of the framework
   and applies proportionality. Entities outside the simplified regime and other than microenterprises adopt and
   review a third-party risk strategy with a policy for services supporting critical or important functions
   (Article 28(2)). Own guidance: the engineering owner of a vendor knows which policy applies to it.
3. **Critical or important is a defined term.** Article 3 defines a critical or important function by the
   effect of its disruption on financial performance, soundness or continuity, or on continuing compliance with
   authorisation conditions. Own guidance: engineers describe the function and its dependencies; a named
   compliance person decides the flag and records the reason.
4. **Keep a register of information on all contractual arrangements.** Article 28(3): maintained and updated at
   entity level and at sub-consolidated and consolidated levels, covering all arrangements for ICT services from
   third-party providers, distinguishing those supporting critical or important functions from the rest. The
   authority can request the full register or sections; the entity reports at least yearly on the number of new
   arrangements, provider categories, contract types and the services and functions provided; and informs the
   authority in a timely manner of planned arrangements for critical or important functions, and when a
   function becomes critical or important. Own guidance: store one row per arrangement with the function it
   supports, the flag with date and decider, and the fields the current standard templates require.
5. **The register template was not read.** Article 28(9) delegates the standard templates to implementing
   technical standards. Own guidance: before building a register, read the current template and field list;
   never design columns from memory.
6. **Check before you sign.** Article 28(4): assess whether the arrangement supports a critical or important
   function, whether supervisory conditions for contracting are met, relevant risks including concentration
   risk, run due diligence on the prospective provider, and assess conflicts of interest. Article 28(5): only
   contract with providers that meet appropriate information security standards; for critical or important
   functions, consider the most up-to-date, highest-quality standards. Own guidance: the pre-contract checklist
   is a dated record attached to the register row.
7. **Concentration and subcontracting are weighed, not assumed.** Article 29(1): consider whether the provider
   is not easily substitutable or whether several arrangements for critical or important functions sit with the
   same or closely connected providers. Article 29(2): weigh subcontracting, third-country subcontractors,
   insolvency law and constraints on urgent recovery of data, data protection and enforcement in a third
   country, and whether long subcontracting chains impair monitoring and supervision. Own guidance: record the
   subcontractor chain you know and mark the unknown links.
8. **Contract provisions for every ICT service.** Article 30(1) requires rights and obligations set out in
   writing, in one document including service levels, available in a durable format. Article 30(2) lists the
   minimum: a description of functions and services with the conditions for subcontracting; locations of
   provision and processing, with advance notice of changes; data protection provisions; access, recovery and
   return of data on provider insolvency, resolution, discontinuation or termination; service level
   descriptions; assistance in an ICT incident at no extra cost or at a cost fixed in advance; full cooperation
   with competent and resolution authorities; termination rights and minimum notice periods; and conditions for
   the provider's participation in the entity's awareness and resilience training. Own guidance: turn this into
   a clause checklist with present, partial or missing, and quote the contract location of each.
9. **Extra provisions for critical or important functions.** Article 30(3): full service levels with precise
   quantitative and qualitative targets, notice periods and reporting duties including developments that could
   materially affect delivery, business contingency plan and security measures requirements, participation in
   the entity's threat-led penetration testing, ongoing monitoring with unrestricted access, inspection and
   audit rights for the entity or an appointed third party and the competent authority, and a mandatory
   transition period for exit. A microenterprise may agree to delegate audit rights to an independent third
   party appointed by the provider. Own guidance: a supplier reviews its standard terms against this list
   before a financial entity asks.
10. **Termination and exit are planned.** Article 28(7) lists circumstances in which arrangements must be
    terminable, among them significant breach, monitoring findings, evidenced weaknesses in the provider's ICT
    risk management, and the authority being unable to supervise. Article 28(8): exit strategies for services
    supporting critical or important functions, documented, tested and reviewed, able to move services and data
    securely to another provider or in-house without business disruption. Own guidance: engineers prepare the
    data export and the migration runbook, and test it once.
11. **Audit rights need competent auditors.** Article 28(6): pre-determine audit frequency and areas on a
    risk basis and check that auditors have the skills where services are technically complex. Own guidance: a
    supplier names a contact and an evidence pack for audits.
12. **Standard clauses are to be considered.** Article 30(4): parties consider standard contractual clauses
    developed by public authorities for specific services. Own guidance: ask counsel whether any exist for the
    service in question before negotiating from scratch.
13. **A supplier reads the same text.** Item (u) of Article 2(1) lists ICT third-party service providers in the
    regulation's scope list, and critical ones fall under an oversight framework in Chapter V section II, which
    was not read. Own guidance: a supplier asks counsel whether it counts as critical and treats the question as
    open.
