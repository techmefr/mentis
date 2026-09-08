# § 3 — Contrast and visual perception

> Section 3 of `skills/accessibility`. Read it when colours, sizes or a zoom-sensitive layout are being
> written or reviewed. The thresholds here come from WCAG AA; where an org design catalogue's
> accessibility skill is installed, read them from there rather than from memory.

1. Text/background contrast ≥ 4.5:1 (normal text) or 3:1 (large text ≥ 18px bold/24px): WCAG AA level,
   checked against the design system's real colours, not eyeballed. Eyeballing fails in one direction
   consistently — on the display it was designed on, in the light it was designed in — and the readers
   it fails are the ones on a phone outdoors or a cheap monitor, who are not in the room.
2. Information is never carried by colour alone (e.g. red = error): always doubled with text, an icon or
   a pattern. The reader affected is not only someone who cannot distinguish the hues: the same failure
   applies to a printed or greyscale copy of the screen, and to a chart whose legend is a row of
   coloured squares.
3. Content resizable up to 200% (browser zoom) with no loss of content or functionality: no width frozen
   in `px` that breaks under zoom. What breaks is rarely the text — it is the container: a fixed-width
   panel that starts clipping, a horizontal scroll appearing on the whole page, or an action row whose
   last button leaves the viewport, which is loss of functionality rather than of layout.
4. **A component's own text has to survive the reader's font size, not only the browser's zoom.** Both
   exist, they are different mechanisms, and a layout sized to fit its text exactly fails under the
   second while passing the first. A row that overflows, a label truncated mid-word or a fitted table
   losing a column is the visible result, and the reader who set a larger font is precisely the one who
   cannot read what remains.
5. **A non-text control needs contrast too.** A focus ring, a checkbox border, an icon carrying meaning
   and the boundary of an input are all things a reader has to find, and a low-contrast one is invisible
   in the same conditions as low-contrast text — with the difference that its absence looks like the
   control not being there.
6. **Colour is not the only cue a hover or focus state can use.** A state expressed as a small change of
   shade is one that several readers cannot see at all, and the fix — an outline, a weight change, an
   underline — is also the fix for the reader in bright sunlight.
7. **A link inside a body of text is identified by more than its colour.** Colour-only link styling is
   the most common instance of point 2 and the one most often argued for on aesthetic grounds; the
   consequence is a paragraph whose interactive words are undiscoverable, so the reader either misses
   them or hunts by hovering.
8. **Text over an image or a gradient has no single contrast ratio.** It passes over part of the
   background and fails over the rest, which is why it cannot be checked with a colour picker and why
   the reliable answer is a solid or scrim layer behind the text rather than a measurement.
9. **Honour a reduced-motion preference.** Transitions, parallax and large movement cause real symptoms
   for some readers — not a preference about taste — and the platform already exposes the setting, so
   ignoring it is a decision rather than an oversight. The reduced variant is not "no feedback": it is
   the same state change without the travel.
10. **Never disable zoom or pinch on a mobile viewport.** It is one attribute, it is copied from
    boilerplate into most projects, and its effect is to remove the only magnification a phone reader
    has. Nothing in the layout requires it, which is why it survives review — nobody notices what it
    took away.
11. **A tooled contrast pass is necessary and not sufficient.** It reads the colours it can compute and
    misses text over an image, text rendered inside a canvas, a state that only exists on interaction,
    and anything a theme changes at runtime. A dark variant in particular is a second set of colours
    that has to be measured, not a filter applied to the first.
