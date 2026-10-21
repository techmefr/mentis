# accessible-documents-pitfalls §2 — Images, tables, forms and colour

> Part 2 of `business/accessible-documents-pitfalls`. Read it when a document holds images, tables, forms, a deck
> or a spreadsheet.

## 2.1 Text alternatives
1. **Give an informative image a short alternative that says what it is for.** Symptom: "image001" or "picture"
   is announced. How to word one: `business/image-alt-text-writing-pitfalls`. Check: for each image, ask what a
   reader who cannot see it would miss.
2. **Mark a decorative image as decorative** (a flourish, a repeated logo), so it is skipped instead of announced.
   In a tagged PDF that means making it an artifact; a non-empty alternative on a decorative image is a listed failure
   (WCAG 1.1.1, PDF technique 4). Alternative text in a PDF lives on the figure tag (PDF technique 1).
3. **For a chart, give the finding and the data.** A short alternative states the conclusion; the numbers go in a
   table or in the text next to it. WCAG 1.1.1 says a short alternative often cannot carry a chart and pairs it with a
   long description and the data in a table. Never leave data only in a picture.
4. **Never put text in an image.** WCAG 1.4.5 (level AA) asks for real text where the technology can do it, with
   exceptions for customisable images and essential presentation such as logotypes; text inside charts or screenshots is not covered. Symptom: a scanned paragraph or a banner that cannot be searched, resized or
   read aloud. Fix: live text, styled; if the picture is unavoidable, the alternative carries the whole text.
5. **Group or anchor an image with its caption** so they are read together.

## 2.2 Tables
1. **Use a table for tabular data and mark the header row.** In a PDF the structure is table, rows, then header or data
   cells, and a Word table's header-row option must be set before conversion (PDF technique 6). Symptom: a screen reader user hears cells with no
   column name. Check: the header-row option is set, and a header cell is a real header, not bold text.
2. **Keep tables simple.** No merged or split cells where avoidable, no blank cells used as spacing, one header
   row. A complex table is split into several simple ones. Microsoft's Word, PowerPoint and Excel pages give the
   reason: a screen reader finds its place by counting cells, so a merged, split or nested cell makes it lose the
   count, and blank cells can suggest the table has ended. GOV.UK says the same: tables for data only, no
   splitting or merging.
3. **Never use a table for layout.** It is read cell by cell in a sequence the reader did not choose.
4. **Do not let a table break across a page without repeating its header** where the format supports it.

## 2.3 Links and forms
1. **A link's text says its destination.** WCAG 2.4.4 (level A) is looser: the purpose may come from the link text plus
   its context (the same sentence, paragraph, list item or table cell), with context before the link easier for
   screen reader users. Keep the stricter rule for documents, since a link list is read out of context. Symptom: "click here", "read more" or a raw long address repeated in a
   list of links. Fix: "Annual report 2025 (PDF)", and say when a link opens a file or leaves the site.
2. **Every form field has a label tied to it**, and the tab order follows the visual order. In a PDF form, check
   the field names, the tooltip text, and that required fields are stated in words, not only by colour.
3. **Give an error message beside the field and in text.** Identifying required or error fields by colour alone is a
   listed failure of WCAG 1.4.1 (level A); the required state also has to be exposed as text (1.3.1).

## 2.4 Colour and contrast
1. **Never carry meaning by colour alone.** Symptom: a status column of red and green dots read as identical by a
   colour-blind reader. Fix: add a word or a symbol. WCAG 1.4.1 says an added non-colour cue (text, shape, icon,
   pattern) is needed, and that links must be visible as links without colour.
2. **Check text contrast against its background**, including text over images and pale grey footnotes. The
   thresholds come from the accessibility standard you are held to; read them at the time, do not recite one
   from memory (`skills/accessibility` §3, `bin/contrast_check.py`).
3. **Make text resizable and size it for reading.** A document that is read on a phone must still reflow or zoom
   without clipping; fixed-page layouts do this worst.

## 2.5 Slides and spreadsheets
1. **Use the slide layouts, not text boxes drawn on a blank slide.** Layouts give each slide a title and a
   reading order; a deck of untitled slides cannot be navigated. Microsoft's PowerPoint page says a screen
   reader reads objects in the order they were added, which can differ from how they appear, and that built-in
   layouts and its accessibility checker help.
2. **One title per slide, and unique.** A repeated "Overview" title is a navigation list of identical entries.
   Microsoft's page asks for a unique, descriptive title on every slide, even a hidden one, because people skim
   the list of titles to move around.
3. **Spreadsheets: name sheets, mark the header row, avoid merged cells, blank spacer rows and columns, and
   comments as the only place a fact lives.** Microsoft's Excel page confirms sheet names (screen readers read
   them, defaults like Sheet1 tell nothing), no blank sheets, text in cell A1 because reading starts there,
   header information, simple tables without merged cells, and descriptive table and range names. Comments as
   the only home of a fact: not found in the sources, own guidance. Put a short note on the first sheet saying what each sheet
   contains.
4. **Animation and auto-advance** are an access problem for some readers; keep the content complete in a static
   form.
