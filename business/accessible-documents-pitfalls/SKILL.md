---
name: accessible-documents-pitfalls
description: "Use when a PDF, word-processor file, spreadsheet or slide deck is produced or reviewed for people who use a screen reader, magnification or only a keyboard: headings made by font size, a scan that is a picture of text, a table used for layout, an image with no alternative text, a link that says only 'click here', a reading order that follows the layout and not the story, a form field with no label, a file exported with the structure lost. Structure, reading order, text alternatives, tables, colour and export checks for documents."
---

# accessible-documents-pitfalls

Business layer (`business/README.md`), communication. A document is accessible when the structure a sighted reader
sees by eye is also present in the file, so software can read it aloud, reflow it or navigate it. Most failures come
from formatting that looks right and carries no structure: bold text instead of a heading, a space-aligned column
instead of a table. This block is the check to run on a document before it is sent, and on the export step. Web
pages are `skills/accessibility`; the wording of an image description is `business/image-alt-text-writing-pitfalls`;
a document built as HTML is `skills/html-document`; plain-language wording is `business/ux-writing`.

It states method only. The standard for tagged PDF (PDF/UA, an ISO standard) was not read; WCAG pages, GOV.UK's publishing guidance, Section508.gov and Microsoft Support pages were read for facts; a legal duty to publish accessible documents depends on the jurisdiction, so
this is not legal advice.

## When
- A report, contract, form, brochure, spreadsheet or deck is about to be published or sent to the public.
- A document is exported to PDF, or a scan is turned into a file.
- A template for documents is created or reviewed.
- An accessibility complaint or an audit points at a document.

## Steps

**Read only the section the task meets.** §1 when authoring or restructuring; §2 for images, tables, forms and
colour; §3 at export and before release.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Structure: real headings, lists, styles, reading order, language, title | a document is written or a template is set | [`01-structure-and-reading-order.md`](./references/01-structure-and-reading-order.md) |
| 2 | Content: text alternatives, tables, links, forms, colour and contrast, slides and spreadsheets | a document holds images, tables, forms or a deck | [`02-images-tables-forms-and-colour.md`](./references/02-images-tables-forms-and-colour.md) |
| 3 | Export and release: tagged PDF, scans and OCR, checker versus human test, remediation order | a file is exported, scanned, or about to be released | [`03-export-checks-and-release.md`](./references/03-export-checks-and-release.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a list of what was checked (structure, alternatives,
tables, links, language, contrast, a read-through with a screen reader or reading-order view), what a person
tested and what only a tool checked, and what was left unresolved. An automatic checker passing is a floor, not a
certificate; the document owner decides whether the file is released.

## Guardrails
- Build headings and lists with the document's own styles. Never fake a heading with bold or a larger font (§1).
- Set the document language and a real title. Never leave the default (§1).
- Give every informative image a text alternative and mark decorative ones as such. Never write "image of" or
  leave the file name (§2).
- Use a table for data with real header cells, and never for layout (§2).
- Make a link say where it goes. Never publish "click here" or a bare long address as the link text (§2).
- Export with tags and check the exported file, not the source. Never assume the export kept the structure (§3).
- Run the checker and a human pass. Never report a document accessible because a tool said zero errors (§3).
- Read the recognised text of a scan against the page. Never publish a scan whose recognised text nobody checked (§3).
- Method plus WCAG 2.2 facts checked against W3C pages (no text copied); status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Written from general document-accessibility practice; criteria and PDF techniques checked against W3C WCAG 2.2
pages (facts only, no text copied), GOV.UK's publishing guidance (Open Government Licence v3.0), Section508.gov and
Microsoft Support pages. 🟡: never run by us. Details
in [`references/origin.md`](./references/origin.md).
