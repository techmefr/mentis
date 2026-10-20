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
1. **Only the criteria in the table were read**; export behaviour, scans and OCR, spreadsheet and slide advice, and the
   two-pass check are one author's practice and may miss format-specific traps. Searched: W3C WCAG pages and
   Section508.gov; their PDF and Word pages hold few details on scans or export.
2. **Behaviour of export functions, checkers and screen readers** differs by product and version and was not
   checked against documentation.
3. **Never run by us** on a real document.
4. Re-read before relying; add an open-licence source when one is found.

## Own guidance (not sourced)
Typed or manual list and spacing rules (§1.1.3 to §1.1.5), furniture and columns (§1.2.3, §1.2.4), navigation and
plain language (§1.3), slides and spreadsheets (§2.5), export check on the exported file (§3.1), scans and OCR
checks (§3.2), and the two-pass check and impact order (§3.3).

## Related blocks
`skills/accessibility`, `business/image-alt-text-writing-pitfalls`, `skills/html-document`, `business/ux-writing`,
`skills/source-freshness`.
