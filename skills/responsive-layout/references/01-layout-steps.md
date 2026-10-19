# Steps 1 to 12 — Breakpoints, fluid sizing, overflow, bars and keyboard

> Steps 1 to 12 of `skills/responsive-layout`. Read them for any layout change: where a layout breaks and what it does instead.

1. **Breakpoints sit where the content breaks, not at device names.** Narrow the viewport until the layout
   fails (text wraps badly, a column starves, a control clips), put the breakpoint there, and keep few of
   them. A list of phone and tablet widths is out of date by the next product cycle.
2. **Prefer continuous states to snaps.** Between the phone layout and the desktop layout lies a wide gap
   (a small tablet, a half-width window, a landscape phone) where neither fits. Fluid columns, wrapping
   flex rows and container-relative sizing carry the middle; a layout with only two states is broken
   exactly there. Test the gap on purpose.
3. **Make the small end a design, not a shrink.** Reduce padding and gutters, set type with a clamped
   fluid scale (`clamp(min, preferred, max)` from the type tokens), and let secondary information
   collapse. Desktop spacing on a phone is the common cause of a cramped page and of an empty one.
4. **Full-height means the dynamic viewport.** `100vh` ignores the mobile browser bars and pushes content
   under them; use `dvh` (with `svh` or `lvh` when the distinction matters) and keep a fallback for
   engines without it.
5. **Grids size themselves.** `repeat(auto-fit, minmax(<min>, 1fr))` or flex wrapping with a basis beats a
   column count switched by breakpoint. `minmax` needs a `min(100%, <min>)` guard, or one wide track forces
   a horizontal scroll on a narrow screen.
6. **Hunt horizontal overflow at the source.** Find the element wider than the viewport (a table, a
   `pre`, an image, a fixed width, a long unbroken string) and give it its own scroll container or
   `min-width: 0` on the flex or grid child. `overflow-x: hidden` on `body` is concealment: the content is
   still cut off, and sticky positioning breaks.
7. **No fixed widths on children.** A `width` in px on a card, input or modal inside fluid parents is the
   usual cause of a clipped phone layout. Use `max-width`, percentages and intrinsic sizing.
8. **Navigation collapses on purpose.** Decide what the bar becomes when it cannot fit (menu, overflow,
   bottom bar) and keep it keyboard-operable (`skills/accessibility` §1). Do not rely on hover to reveal it.
9. **A fixed bar reserves its height.** A fixed header or footer takes content out of flow: pad the main
   region by the bar's height (a token or a custom property, not a copy of the number) and respect the
   safe-area insets (`env(safe-area-inset-*)`) on devices with notches and home indicators.
10. **The on-screen keyboard covers fields.** A form pinned to the bottom, or a modal sized to the full
    viewport, hides the focused input. Scroll the focused field into view, size modals with `dvh`, and test
    with the real keyboard rather than a narrowed desktop window.
11. **Verify by sweeping.** Drag the viewport width continuously from the narrowest to the widest and
    watch for breaks; two checks at two widths pass layouts that fail in between. Check at 200% zoom and
    with a larger default font (`skills/accessibility` §3).
12. **Text grows.** Translations and user font settings expand strings; a label sized to fit its English
    text will overflow in another language. Let containers grow, wrap or truncate with a reachable full
    value (`business/ux-writing` §5.10).
