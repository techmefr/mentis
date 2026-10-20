# accessible-documents-pitfalls §1 — Structure and reading order

> Part 1 of `business/accessible-documents-pitfalls`. Read it when a document is written or a template is set.

Assistive software cannot see layout. It reads the structure the file declares: what is a heading, what is a
list, what comes next. A file with no declared structure is read as one long, flat run of text.

## 1.1 Declare the structure
1. **Use heading styles, not formatting.** WCAG 2.2 criterion 1.3.1 (level A) asks that structure shown by
   presentation also be available to software, and names real headings instead of large bold text, real lists, header
   cells in tables and associated form labels; whitespace used to fake columns is a listed failure. Symptom: a screen reader user cannot jump between sections, and the
   outline view of the file is empty. Check: open the outline or navigation pane of the editor; every visible
   heading should be in it. Fix: apply the heading style, and change its look in the style, not by hand.
2. **Keep heading levels in order and use one top level.** Symptom: a level skipped for its size, or three
   top-level headings for visual weight. Fix: levels follow the outline of the content, size is a style choice.
3. **Make lists with the list feature.** A typed dash or number is read as characters, and a list of many items
   loses the count a reader would have heard. Fix: real bulleted or numbered lists, nested with the indent level.
4. **Use styles for emphasis, quotes and captions**, so a change of look is made once and the meaning stays.
5. **Do not use blank lines, spaces or tabs to position things.** Symptom: a reflowed or zoomed page breaks, and
   each empty paragraph is announced. Fix: paragraph spacing and real indents, a table only for data.

## 1.2 Reading order
1. **The order the file lists content is the order it is read.** WCAG 1.3.2 (level A) asks for a software-determinable
   reading order where the order changes the meaning; it is satisfied when the visual and the programmatic order differ
   only where meaning does not depend on it, and a layout table that does not make sense when read in sequence is a listed failure. Symptom: text boxes, columns and floating
   images read in the order they were added, not in the order of the page. Check: use the editor's reading-order
   or selection pane, or tab through the exported file. Fix: reorder the objects, or put content in the main flow.
2. **Prefer the main flow to floating boxes.** Text in a box, a pull-quote or a sidebar is the usual reading-order
   failure; place it inline in the story or mark it as supplementary and put it after its section.
3. **Columns made with the columns feature are read in sequence; columns faked with a table or tabs are not.**
4. **Page furniture** (running header, footer, page number) should not be read on every page; mark it as
   decoration or keep it in the header and footer areas.

## 1.3 Identify the document
1. **Set the document language**, and mark a passage in another language so it is not read with the wrong
   voice. WCAG 3.1.2 (level AA) asks for the language of each passage to be determinable, with exceptions for proper
   names, technical terms and words absorbed into the surrounding language; for PDF it names the language entry. Symptom: a foreign phrase pronounced as nonsense. Fix: language setting per passage in the style.
2. **Give the file a real title** in its properties, and show it in the window title. WCAG 2.4.2 (level A) asks for a
   descriptive title and names the PDF title entry as a way to meet it. The default (a file name or
   "Untitled") is announced and tells nothing.
3. **Provide a way to navigate a long document**: headings, a table of contents built from them, bookmarks in an
   exported PDF, and internal links that work.
4. **Spell out an abbreviation at first use** and avoid relying on position ("the table on the right") or shape
   or colour alone to point at something.
5. **Write in plain language and short paragraphs.** Wording is `business/ux-writing`; here it matters because a
   dense page is also the one read slowest by a screen reader and a person with a cognitive disability.
