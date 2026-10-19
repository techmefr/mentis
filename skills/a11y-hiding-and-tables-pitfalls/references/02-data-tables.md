# a11y-hiding-and-tables-pitfalls §2 — Data tables

> Section 2 of `skills/a11y-hiding-and-tables-pitfalls`. Read it when a table of data is written or reviewed.
> Restated from the A11y Project post `src/posts/accessible-data-tables.md` (repository commit `27de226`,
> Apache-2.0 repository licence, no separate content licence stated), read 2026-10-16. The post covers simple
> tables only. Sentences marked "own guidance" are ours.

1. **A table is for tabular data, and it needs help to be read.** Sighted users scan a table; a screen reader goes
   through it line by line, so the markup has to supply the associations a sighted user makes by eye. The post
   reduces the work to two things: a caption, and marking row and column headings.
2. **Give every data table a caption.** The post says to put a caption element right after the opening table
   tag. Without it, it says, a screen reader starts reading cell values with nothing to say what the table is,
   which is frustrating; with it, the reader announces the table's name along with its size (the exact wording
   depends on the screen reader). Own guidance: the caption names the table's subject, the surrounding heading
   does not replace it.
3. **Mark header cells as headers, and say which direction.** Use `th`, not a styled `td`. On a column header put
   `scope="col"`, and on the row header, normally the first `th` in the row, put `scope="row"`. The post says a
   reader will probably work it out unaided but that the attribute makes it unambiguous.
4. **Make the headers unique and readable.** The post asks for column headers to be unique, and for the row
   header chosen for a row to be unique enough, and readable, to identify the row. Own guidance: a row header
   that is a number, an icon or a repeated word fails this; if no column is a good identifier, add one, hidden
   visually with the class in point 1.2 of the hiding part if the design cannot show it.
5. **Group header rows and body rows.** The post's example puts the header row in a head section and the data
   rows in a body section. Own guidance: it is the shape to start from when restyling or generating a table.
6. **A grid of `div` elements is not a table.** Own guidance: if the content is tabular data, use the table
   elements (the page you are replacing loses all of the above); if a component library renders the table,
   check its output for the caption and the scope attributes. This post does not cover interactive grids,
   sortable columns, spanned cells or multi-level headers, and nothing here says how to mark them up.
