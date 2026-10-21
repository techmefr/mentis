# data-protection §5 — The processing record kept in the repository

> Section 5 of `business/data-protection` (the numbers 3 and 4 of that file are inline in `SKILL.md`). Read it
> when the field list of step 1 should be kept as a file next to the code. Sources: Regulation (EU) 2016/679
> Article 30(1) to (5), as published in the Official Journal (OJ L 119, 4.5.2016),
> https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read 2026-10-16 (the original
> publication, not a consolidated or corrected version: read the current text before relying on it); and the
> `ethyca/fides` repository (Apache-2.0, commit `e87f3ff`, described by our review as archived): the files
> `data/dataset/manual_dataset.yml` and `demo_resources/demo_extended_taxonomy.yml`, read 2026-10-16, for the
> pattern only. Sentences marked "own guidance" are ours. Not legal advice; the legal content of the record
> belongs to the DPO.

1. **Keep the field list as a machine-readable file, versioned with the code.** The fides example files
   describe, per collection, each field with a list of data categories, and carry a taxonomy of data uses and
   of data subjects (with, per subject type, the rights listed and a flag for automated decisions or
   profiling). Own guidance: copy the pattern, not the tool or its vocabulary. A plain file in the repository
   (one entry per table or collection, one per field) is reviewed in the same pull request as the code that
   adds the field.
2. **Annotate each field with a data category, and each use with a key.** Own guidance: a diff then shows when
   a new category or a new use appears. Define your own short vocabulary with the DPO; do not adopt a vendor's
   large taxonomy as a dependency.
3. **The record a controller keeps (Article 30(1)).** Reformulated: it contains the identity and contact
   details of the controller (and joint controller, representative and DPO where applicable); the purposes of
   the processing; the categories of data subjects and of personal data; the categories of recipients,
   including those in third countries or international organisations; where applicable, transfers to a third
   country or international organisation, with the documentation of safeguards for the cases named in the
   second subparagraph of Article 49(1); where possible, the envisaged time limits for erasure by category; and
   where possible, a general description of the security measures under Article 32(1).
4. **The record a processor keeps (Article 30(2)).** Reformulated: for each controller on whose behalf it acts,
   the contact details, the categories of processing carried out, where applicable the transfers as above, and
   where possible a general description of the security measures.
5. **Form and availability (Article 30(3) and (4)).** The records are in writing, which includes electronic
   form, and the controller or processor makes the record available to the supervisory authority on request.
6. **The engineer's file feeds the record and does not replace it.** Own guidance: the repository file gives
   the factual columns (categories of data, recipients found in the code, retention job names); the legal
   fields (the purposes as a legal statement, the retention decisions, the transfer safeguards) are owned and
   written by the DPO. Link the two by a stable key per processing activity.
7. **Fail the build on a field with no category.** Own guidance: a CI check that rejects a new column or field
   with no category annotation, and a new use key not in the vocabulary, makes the update a by-product of the
   change instead of a yearly chore.
8. **Whether an exemption applies is for the DPO.** Article 30(5) states that the obligations in paragraphs 1
   and 2 do not apply to an organisation with fewer than 250 persons unless the processing is likely to
   result in a risk to the rights and freedoms of data subjects, is not occasional, or includes the special
   categories of data or data on criminal convictions and offences. Whether it covers a given organisation is
   not decided here: ask the DPO, and keep the file anyway, since it also serves the checklist of step 1.
9. **CNIL's reading of the record (read 2026-10-20, CNIL page on the register).** It repeats the contents above
   (per activity: purposes, categories of people and data, recipients including processors, transfers with
   safeguards, retention criteria, security measures where feasible) and says processors keep their own
   register. It describes the exemption for organisations under 250 people as limited to very particular
   cases and advises recording a processing in case of doubt. This confirms point 8: keep the file anyway.
10. **The fides project is reported archived** (by our earlier review; its status was not rechecked). Own guidance: treat it as a pattern to copy and do not take a dependency
   on it; its policy engine and request orchestration are not part of this pattern.
