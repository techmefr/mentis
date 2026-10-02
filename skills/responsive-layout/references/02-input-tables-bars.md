# Steps 13 to 19 — Viewport units, input capability, tables, stacked bars, line length

> Steps 13 to 19 of `skills/responsive-layout`. Read them when a layout uses viewport-width units or
> full-bleed sections, when hover or pointer behaviour changes, when a wide table or a stack of fixed
> bars has to survive a phone, or when prose or clickable text sits in a narrow column. They continue the
> numbering of steps 1 to 12.

13. **`100vw` is wider than the page.** Where scrollbars take layout space (classic scrollbars), the
    viewport-width unit includes the scrollbar, so an element sized `100vw` is wider than the room it
    sits in and produces a horizontal scroll that appears only on those engines and only when the page
    scrolls. Size to the container (`100%`, `inline-size: 100%`, or grid and flex sizing). A full-bleed
    band inside a centred column is built with a layout that lets the band span the grid (a three-track
    grid whose middle track holds the content, or a wrapper that is itself full width), never by
    sizing a child to `100vw` and compensating with negative margins, and never with `overflow-x: hidden`
    on an ancestor (step 6).
14. **Ask what the input can do, not what the device is.** The `hover`, `pointer`, `any-hover` and
    `any-pointer` media features describe capabilities, and the primary pointer is not the only pointer: a
    laptop with a touch screen reports a fine pointer with hover as primary and a coarse one as
    available. Gate hover-only decoration on `(hover: hover)`; give controls the larger target when a
    coarse pointer is available (the size floor comes from the standard,
    `skills/accessibility` §1.8, and the design system's tokens); never remove a capability because a
    feature query said touch, and never sniff a user agent (`skills/accessibility` §7.11). A hover reveal
    always has a keyboard and touch path (`skills/accessibility` §1.12).
15. **A wide table chooses one of three honest behaviours on a small screen.** (a) Scroll inside its own
    container: the container is keyboard-focusable and named so it can be scrolled without a pointer, the
    header row or first column stays visible where it helps, and the page itself does not scroll
    sideways. (b) Re-flow each row into a labelled stack: every value shows its column name, and because
    changing `display` on table parts can drop table semantics in some engines, the roles are restored or
    the markup is a list from the start (`skills/accessibility` §6). (c) Show the columns that decide, and
    offer the rest through a reachable detail view; the hidden columns are still in the DOM only when they
    are still reachable. Two-dimensional scrolling of data tables is a recognised exception to the reflow
    criterion (WCAG 1.4.10); that exception covers the table, not the page around it.
16. **Fixed and sticky layers add up.** A sticky header, a sticky sub-navigation, a promotional strip, a
    cookie notice and a bottom bar are each defensible alone and together can leave a phone in landscape
    with a slit of content. Total the height of every layer that can be on screen at once at the smallest
    height you support, keep it a minority of the viewport (the limit is a design token, not a number
    here), allow one sticky layer by default, and collapse or release the others on scroll. A second sticky
    layer's `top` is derived from the first layer's height through a custom property, not a copied
    number, and `scroll-padding-top` or `scroll-margin-top` keeps anchors and focused elements from
    landing under them (`skills/accessibility` §1.6).
17. **A control's label stays on one line, or the whole box is the target.** A button, tab or navigation
    label that wraps to two lines in a narrow column has a ragged hit area, and the second line is often
    missed. Shorten the label, give the control a block-level box with padding so the box is the target,
    or let the control grow in a deliberate wrapped layout; do not truncate a label that carries the
    meaning (step 12).
18. **Prose has a measure.** Set the maximum line length of running text in a unit tied to the font
    (`max-inline-size` in `ch`) from the type tokens, so a wide window does not stretch a paragraph into
    lines too long to track; a short measure on a phone is already handled by the viewport. Columns of
    figures use tabular numerals so digits align.
19. **Check the short, wide viewport too.** A phone in landscape is wide and very short: vertical
    centring, `min-height` of the viewport, stacked bars (step 16) and modals sized to the full height
    fail there first. Orientation is never locked to avoid it (`skills/accessibility` §7.10).

## Mechanical checks

```
grep -rnE '(width|min-width|inline-size)\s*:\s*100vw' src
grep -rnE 'user-scalable|maximum-scale' src public
grep -rnE '@media[^{]*(hover|pointer)' src
grep -rn 'position:\s*\(sticky\|fixed\)' src
grep -rnE 'max-(inline-)?size|max-width:\s*[0-9.]+ch' src
```

- In a headless browser, load each key page at the narrowest supported width and at a short landscape
  size, then assert that the document's scroll width does not exceed its client width and that no
  element's right edge passes the viewport.
- Sum the heights of the `position: sticky` and `position: fixed` elements visible at that size and
  compare with the project's limit.
- Each `<table>` is checked against step 15: scroll container with a name, stacked layout, or reduced
  columns.
