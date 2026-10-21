# accessible-documents-pitfalls: origin and source stamps

> Provenance of `business/accessible-documents-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from general document-accessibility practice, never run on a real document
set by us. The block structures a check; it certifies nothing, and the document owner decides whether a file is
released (`business/README.md`).

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| W3C WCAG 2.2 Understanding pages 1.1.1, 1.3.1, 1.3.2, 1.4.1, 1.4.5, 2.4.2, 2.4.4, 3.1.2 and PDF techniques 1, 4, 6 | W3C Document License (terms read; no derivative texts), facts only | Structure for software, reading order, language of parts, title, alternatives and decorative artifacts, chart descriptions, images of text, table header cells, link purpose, colour (§1.1, §1.2, §1.3, §2.1 to §2.4) |
| Section508.gov PDF and Word creation pages | US government site (public domain, not stated on the pages read); facts only | HTML preferred over PDF, existence of a testing checklist and remediation guide; the pages themselves hold little detail (§3.1) |
| GOV.UK, "Publishing accessible documents" (gov.uk/guidance/publishing-accessible-documents), read raw 2026-10-20 | Open Government Licence v3.0 (footer read). Contains public sector information licensed under the Open Government Licence v3.0; facts in our own words, nothing copied | HTML first, PDF last resort, PDF/A not fully accessible, plain language, styles for headings, tables and lists, one-column layouts, table for data only, link text out of context, no text in images, scan then OCR, run a checker (§1, §2.2, §3.1, §3.2) |
| Microsoft Support pages on accessible Word, PowerPoint, Excel and PDF files and on the Accessibility Checker rules (support.microsoft.com), read raw 2026-10-20 | Microsoft site terms, no open licence; facts only, own words | Heading, list and table header features, why merged and blank cells hurt, slide titles and reading order, sheet names and cell A1, tags option on PDF export, checker severity levels (§1.1, §2.2, §2.5, §3.1, §3.3) |
| Section508.gov, "Create Accessible PDFs" and "Accessible Presentations" pages (raw, 2026-10-20); the Word and Excel authoring page addresses tried returned 404 | US government site | HTML first for PDFs, testing checklist and remediation guide exist (§3.1) |
| PDF/UA (ISO 14289) | proprietary standard | Not opened |

## Verified
Criteria and technique facts named in the table: each is a confirmation of an existing point with the criterion level
stated in the text. Contrast thresholds were deliberately not read or stated.

## Left out on purpose
Standard names, success-criterion numbers, conformance levels and numeric thresholds (contrast ratios, sizes): each
is read at the time from the standard the project is held to. Product-specific menu paths and checker names, which
change by version. Legal duties by jurisdiction. Remediation scripting. Any source with no open licence: not
opened.

## Not verified
1. **The two-pass check and impact order** are one author's practice. Searched: W3C WCAG pages, Section508.gov,
   GOV.UK and Microsoft Support pages; none gives an order of fixes. Adobe's PDF accessibility help returned access
   denied and was not read.
2. **Behaviour of export functions, checkers and screen readers** differs by product and version; Microsoft's menu
   paths were read but are not in the block, and no screen reader was run.
3. **Never run by us** on a real document.
4. Re-read before relying; add an open-licence source when one is found.

## Corrected or confirmed in the 2026-10-20 second pass
Confirmed from the pages above and now credited in the text: lists and headings by style, blank-line spacing, columns and
single-column layouts, navigation aids, plain language, merged and blank table cells, slide titles and reading order,
spreadsheet sheet names and cell A1, export with tags, HTML first, scan then OCR, checker plus human. No claim was found
wrong.

## Own guidance (not sourced)
Page furniture (§1.2.4), comments as the only home of a fact (§2.5.3), the file lock that blocks extraction (§3.1.4),
checking recognised scan text against the page and rebuilding structure after OCR (§3.2.2, §3.2.3), the five-minute
assistive-technology test (§3.3.2), the impact order of fixes (§3.3.3), and the template habit (§3.3.4).

## Related blocks
`skills/accessibility`, `business/image-alt-text-writing-pitfalls`, `skills/html-document`, `business/ux-writing`,
`skills/source-freshness`.

Independent verification 2026-10-21: 28 checked, 28 matched, 0 corrected, 0 unverified
