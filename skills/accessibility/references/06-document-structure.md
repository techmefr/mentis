# § 6 — Document structure and embedded content

> Section 6 of `skills/accessibility`. Read it when a diff adds a table, a list, a definition list, an
> embedded frame or object, an image that carries text or sits next to its own caption, or generates
> identifiers. Each native structure has a minimal contract; the contract is what assistive technology and
> a stylesheet-less reader rely on. Names and landmarks are §1 and §2, form wiring is §4.

## Tables

1. **A table is for data with two axes; layout belongs to CSS.** A table used to position content is read
   cell by cell as if it were data. If a legacy layout table cannot be removed, strip its semantics
   (`role="presentation"`) and keep it free of header cells and captions.
2. **A data table names itself and its headers.** A `caption` gives the table its name (the nearest
   native way; the old `summary` attribute is obsolete). Every header cell is a `th`, and `scope`
   (`col`, `row`, `colgroup`, `rowgroup`) states which cells it heads. A `th` with no data cells under or
   beside it is a mistake, and a first column of labels written as `td` is the usual way tables lose
   their row headers.
3. **Irregular tables use `headers`, and only then.** A table with merged cells where `scope` cannot say
   which headers apply gives each header an `id` and each data cell a `headers` list of those ids. The
   ids must exist in the same table (HTML Living Standard, tabular data). When a table needs this much,
   first try to split it into simple tables.
4. **Two tables on a page do not share a name.** Identical captions or labels make the page's tables
   indistinguishable in a table list; the name says which table.
5. **A sortable or interactive header exposes its state.** The sort direction is `aria-sort` on the
   header, the control inside it is a button (§1.1), and the change is announced (§2.3). Small-screen
   presentation of a wide table is `skills/responsive-layout`.

## Lists and definition lists

6. **A list is marked up as a list.** A group of peer items is `ul` or `ol`; a sequence whose order
   matters is `ol`. The direct children of `ul` and `ol` are only `li` (plus script-supporting elements);
   a `div` between them is invalid and breaks the count a reader hears. Do not use lists to indent.
7. **A definition list holds term and description groups.** `dl` contains `dt` and `dd`, optionally grouped
   in a `div` per pair, and a `dt` or `dd` outside a `dl` is invalid. It suits metadata (label and
   value), glossaries and key-value summaries, and it replaces a two-column table that has no real
   headers.
8. **Styling can strip list semantics.** Some engine and reader combinations stop announcing a list when
   its markers are removed with CSS; after restyling a navigation or a tag list, check in a screen
   reader and restore the role explicitly if it is lost (the one case where a redundant `role` is right,
   §2.1).

## Identifiers

9. **An `id` is unique in its document.** Duplicates break label association (`for`), in-page links, and
   every ARIA reference (`aria-labelledby`, `aria-describedby`, `aria-controls`, `aria-owns`), where the
   browser silently picks the first match. The recurring source is a component rendered many times with a
   hard-coded `id`; generate one per instance. A reference whose target does not exist is the same defect
   (§8.4). A reference cannot cross a shadow-root boundary.

## Frames, objects and image inputs

10. **Every embedded document has a name.** An `iframe` or `frame` carries a `title` that says what it
    contains; an `object` carries a text alternative or fallback content; an `input type="image"`
    carries `alt` describing the action, not the picture; an `area` of an image map carries `alt`.
    Third-party embeds are the usual offender (§2.2 for the name rule; `skills/webperf` §4.5 for their
    cost).
11. **Meaningful and decorative images are told apart, and neither is described twice.** A decorative image
    has `alt=""` (or is CSS). An informative one has an alternative that states its purpose, without
    "image of". An image inside a link or button next to the same words gets `alt=""` so the name is not
    read twice (`skills/seo` §2.4 for the indexing view).
12. **Text is text.** Information in the pixels of an image cannot be resized, recoloured, translated,
    searched or read aloud; use real text, with the image purely decorative. Logos are the standing
    exception, and so is an image where the exact rendering is the content (WCAG 1.4.5, Images of Text).
    The same rule serves translation: a localised string baked into an image is a string the i18n
    pipeline never reaches. An image with a gesture, a symbol or a convention that means something
    different elsewhere is chosen or varied per locale rather than reused everywhere.
13. **A caption belongs to its figure.** `figure` with `figcaption` ties an image, chart or code sample to
    its legend; the caption supplements the alternative text and does not replace it.

## Things not done without a reason

14. **No `meta http-equiv="refresh"` redirect or reload.** A timed refresh moves or replaces the page
    under a reader, which fails WCAG 2.2.1 (Timing Adjustable) unless the visitor can control it;
    redirect with an HTTP status (`skills/seo` §5).
15. **No `accesskey`.** The shortcuts collide with those of browsers and assistive technology, and their
    modifier differs per platform; offer a visible control and, where warranted, a documented,
    remappable shortcut (WCAG 2.1.4).
16. **`autofocus` only where moving focus is the point.** On a page load it skips the page's start, a
    reader's context and the skip link (§1.10); acceptable in an opened dialog or on a page whose sole
    purpose is one field.
17. **No empty headings, links or buttons.** An element with no text and no accessible name is announced
    as nothing, and `href="#"` or a `javascript:` URL is a button disguised as a link (§1.1). Template
    conditionals that remove the text but keep the tag are the usual cause.
18. **One visible label per control.** Several `label` elements for one input are announced inconsistently;
    combine them into one or move the extra text into a description (§4.1).
19. **The content still reads without its stylesheet.** The source order is a sensible reading and tab
    order; disabling styles and reading top to bottom is a legitimate test. Visual reordering with CSS
    (`order`, reversed flex or grid placement, absolute positioning) changes what the eye sees and
    nothing about what the keyboard does, so focus order and reading order follow the DOM, and any
    reordering that disagrees with it is fixed in the markup (WCAG 1.3.2, 2.4.3, and the CSS Flexbox
    note on reordering).

## Mechanical checks

Hints for a person to read: an empty result proves nothing (`skills/security-hardening` §5.9).

```
grep -rnP '<(iframe|frame)\b(?![^>]*\btitle=)' src
grep -rnP '<img\b(?![^>]*\balt=)' src
grep -rnP '<input[^>]*type="image"(?![^>]*\balt=)' src
grep -rnE 'http-equiv=.refresh|\baccesskey=|\bautofocus\b' src
grep -rnP '<h[1-6][^>]*>\s*</h[1-6]>|<a\b[^>]*>\s*</a>|href="(#|javascript:[^"]*)?"' src
grep -rLE '<th[ >]' $(grep -rl '<table' src)
grep -rL '<caption' $(grep -rl '<table' src)
```

- Duplicate identifiers: extract every `id="..."` from each rendered page, sort, and print repeats; also
  extract the targets of `for`, `aria-labelledby`, `aria-describedby`, `aria-controls` and `aria-owns` and
  confirm each exists in that page (about thirty lines of script).
- List and definition-list structure, table headers, frame titles and duplicate ids are covered by an
  accessibility engine run over the rendered HTML (axe-core has rules for each); the output is read, not
  trusted as a verdict (§2.12).
- A stylesheet-less pass: load the page with styles disabled and read it top to bottom.
