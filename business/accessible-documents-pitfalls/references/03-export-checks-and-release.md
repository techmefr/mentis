# accessible-documents-pitfalls §3 — Export, checks and release

> Part 3 of `business/accessible-documents-pitfalls`. Read it when a file is exported, scanned or about to be
> released.

The structure made in the source file is not a promise about the exported file. Printing to a PDF, saving as an
image or converting between formats can keep it, flatten it or drop it.

## 3.1 Export
1. **Export with the option that writes tags.** Symptom: the PDF opens, looks perfect and has no structure; a
   screen reader reads it as unlabelled text or not at all. Fix: use the export function that produces a tagged
   file, not "print to PDF".
2. **Check the exported file, not the source.** Open it in a viewer that shows the tag tree or reading order,
   check headings, lists, tables and the language, and read it with a screen reader for a minute.
3. **Keep the source and the export together**, and fix in the source, then export again. Hand-editing the tags
   of the export is the last resort, and is lost at the next export.
4. **Do not lock the file in a way that blocks assistive software.** A security setting that forbids text
   extraction for accessibility stops the reader.
5. **Prefer a web page to a PDF where both are possible.** The Section508.gov PDF page says federal policy is to
   prioritise HTML and use PDF only when necessary, because PDFs are often less accessible and less mobile friendly;
   it also publishes a PDF testing checklist and a remediation guide to start from.
6. **Provide an accessible alternative where a format cannot be fixed**, such as a web page or a plain text
   version, and say where it is. A fallback does not excuse a fixable file.

## 3.2 Scans
1. **A scan is a picture.** Symptom: no text can be selected or searched, and a screen reader has nothing to
   read. Fix: recognise the text, then correct it.
2. **Read the recognised text.** Recognition errors are silent: a wrong digit in a figure, a lost column, a
   merged line. Check: compare a sample of numbers and names with the page image. Never publish a result nobody
   compared.
3. **Rebuild the structure after recognition**: headings, lists, tables, reading order. Recognised text with no
   structure is only better than a picture.
4. **Prefer the born-digital source** over a scan of its printout whenever it exists.

## 3.3 Check and release
1. **Run an automatic checker, then a human pass.** A checker finds missing tags, titles and alternatives; it
   cannot tell whether an alternative is meaningful, whether the order makes sense or whether a heading is the
   right level. Report the two separately.
2. **Test with the assistive technology your readers use**, on one realistic page: navigate by headings, read a
   table, follow a link. Own guidance: five minutes of this finds more than a long checklist.
3. **Fix in order of reader impact.** Language, title, structure and reading order first, then alternatives and
   tables, then links and colour, then finishing touches. A beautiful page with no structure helps nobody.
4. **Put accessibility into the template.** Symptom: the same errors recur in each new document. Fix: styles,
   heading levels, language, table style and contrast already correct in the template, and a short checklist
   with it.
5. **State what is not accessible, and how to get the content another way.** If a file is released with known
   gaps, say so and give a contact and a promise date, rather than staying silent. Whether a duty to publish
   accessible documents applies, and what the declaration must contain, depends on the jurisdiction; this is not
   legal advice, and the French national framework is covered in `skills/accessibility` §5.
