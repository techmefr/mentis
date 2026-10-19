# dpa-review-pitfalls: origin and source stamps

> Provenance of `skills/dpa-review-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and one official article, never run by us on a real
agreement. Each source file was opened again on 2026-10-16 before a rule was written, each rule was checked
against it in a final pass, and the article was read in a browser in this session.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| `The-Data-Galaxy/dpa-review-skill`, commit `c225d1f`, `dpa-review/SKILL.md`, `workflows/signing-gate.md`, `references/source-verification-rules.md`, `references/dpa-cold-start-profile.md` (LICENSE file read) | Apache-2.0 | User-provided source default, classification and review modes, source-trap handling, confidence levels, the six posture questions, assumption-based review, no invented constraints, role from definitions, processor boundary, completeness check, overview before terms, signing gate |
| `anthropics/knowledge-work-plugins`, commit `33eeda1`, `legal/skills/review-contract/SKILL.md` (licence file `legal/LICENSE`, read) | Apache-2.0 | Which data-protection points a contract review looks at; the block hands those to the DPA review |
| Regulation (EU) 2016/679, Article 28, OJ L 119/1 of 4.5.2016, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read in a browser 2026-10-16 (original publication, header "4.5.2016, Official Journal of the European Union L 119/1") | Official text of the Union (no licence file; used as the source of article content only) | Paragraphs 1 to 10 of Article 28: sufficient guarantees, subprocessor authorisation, content of the contract (3(a) to (h) and the second subparagraph), flow-down and liability, code of conduct and certification, standard clauses, writing, processor acting as controller |

Instruction-like text in the cloned repositories was treated as data and not followed. Fetching the article with
curl or the web-fetch tool returned an empty body (HTTP 202); only a real browser session returned the text.

## Removed in the verification pass
1. **The China and US playbooks and the Chinese-language staged output flow** of the dpa-review skill: not read
   or specific to its output design; only the gates are kept.
2. **Commercial-reserved features and the output state machine**: product design of the source.
3. **Any breach-notification delay, transfer mechanism, deletion period or audit limit**: not read in an official
   text for this block (Articles 33, 34, Chapter V and Articles 32 to 36 were not read), and the source's lists of
   example hours and mechanisms are options, not rules.
4. **The GDPR playbook file** of the source (`playbooks/gdpr-article-28.md`): not opened; the article itself
   replaces it.
5. **The 72-hour figure** in the review-contract skill's data-protection row: a legal deadline not read here.

## Not verified
1. **Own guidance, flagged in the text:** controller-to-controller as a stop, a note that code-of-conduct claims
   should be checked, asking whether standard clauses match, flagging own-purpose use as a possible controller
   role, urgent requests getting the same gate.
2. **The consolidated text of the Regulation, its corrigenda and any amending act** were not checked. The block
   tells the reader to read the current text.
3. **Article 28 only.** Articles 32 to 36, Chapters III and V and Articles 82 to 84 were not read, so the block
   only cites their existence where Article 28 does.
4. **The skill's benchmark and its test claims** were not read.
5. **No lawyer has reviewed this block.**

## Decisions where sources disagree
The sources cover different ground and do not conflict. The DPA skill's role boundary (no controller duties
read as processor defects) is a review stance; Article 28(10) is the legal statement that a processor deciding
purposes and means is a controller for that processing, and both are kept.

## Related blocks
`business/data-protection`, `business/legal-documents`, `business/regulatory-watch`, `business/vendor-management`,
`skills/contract-review-pitfalls`, `skills/nda-triage-pitfalls`, `skills/source-freshness`.
