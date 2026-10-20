# accessible-documents-pitfalls §2 — Images, tables, forms and colour

> Part 2 of `business/accessible-documents-pitfalls`. Read it when a document holds images, tables, forms, a deck
> or a spreadsheet.

## 2.1 Text alternatives
1. **Give an informative image a short alternative that says what it is for.** Symptom: "image001" or "picture"
   is announced. How to word one: `business/image-alt-text-writing-pitfalls`. Check: for each image, ask what a
   reader who cannot see it would miss.
2. **Mark a decorative image as decorative** (a flourish, a repeated logo), so it is skipped instead of announced.
3. **For a chart, give the finding and the data.** A short alternative states the conclusion; the numbers go in a
   table or in the text next to it. Never leave data only in a picture.
4. **Never put text in an image.** Symptom: a scanned paragraph or a banner that cannot be searched, resized or
   read aloud. Fix: live text, styled; if the picture is unavoidable, the alternative carries the whole text.
5. **Group or anchor an image with its caption** so they are read together.

## 2.2 Tables
1. **Use a table for tabular data and mark the header row.** Symptom: a screen reader user hears cells with no
   column name. Check: the header-row option is set, and a header cell is a real header, not bold text.
2. **Keep tables simple.** No merged or split cells where avoidable, no blank cells used as spacing, one header
   row. A complex table is split into several simple ones.
3. **Never use a table for layout.** It is read cell by cell in a sequence the reader did not choose.
4. **Do not let a table break across a page without repeating its header** where the format supports it.

## 2.3 Links and forms
1. **A link's text says its destination.** Symptom: "click here", "read more" or a raw long address repeated in a
   list of links. Fix: "Annual report 2025 (PDF)", and say when a link opens a file or leaves the site.
2. **Every form field has a label tied to it**, and the tab order follows the visual order. In a PDF form, check
   the field names, the tooltip text, and that required fields are stated in words, not only by colour.
3. **Give an error message beside the field and in text.** Own guidance: a field outlined in red and nothing else
   is invisible to many readers.

## 2.4 Colour and contrast
1. **Never carry meaning by colour alone.** Symptom: a status column of red and green dots read as identical by a
   colour-blind reader. Fix: add a word or a symbol.
2. **Check text contrast against its background**, including text over images and pale grey footnotes. The
   thresholds come from the accessibility standard you are held to; read them at the time, do not recite one
   from memory (`skills/accessibility` §3, `bin/contrast_check.py`).
3. **Make text resizable and size it for reading.** A document that is read on a phone must still reflow or zoom
   without clipping; fixed-page layouts do this worst.

## 2.5 Slides and spreadsheets
1. **Use the slide layouts, not text boxes drawn on a blank slide.** Layouts give each slide a title and a
   reading order; a deck of untitled slides cannot be navigated.
2. **One title per slide, and unique.** A repeated "Overview" title is a navigation list of identical entries.
3. **Spreadsheets: name sheets, mark the header row, avoid merged cells, blank spacer rows and columns, and
   comments as the only place a fact lives.** Put a short note on the first sheet saying what each sheet
   contains.
4. **Animation and auto-advance** are an access problem for some readers; keep the content complete in a static
   form.
