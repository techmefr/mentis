# flutter-conventions §3 — Layout

> Section 3 of `skills/flutter-conventions`. Read it when a screen is laid out, or an overflow shows up. The other sections and the guardrails stay in `SKILL.md`.

1. Unbounded-constraint errors are **constraint** problems, not styling problems: read what the parent passes
   down before adding a fixed size. A hardcoded height that makes the error go away is the bug moving to
   another device.
2. **The messages map to specific causes**, which is what makes them fast to fix rather than mysterious: a
   *scrollable given unbounded height* means it sits inside another unconstrained scrollable or an
   unconstrained column — give it a bounded slot (`Expanded`) rather than a fixed height; an *input that
   cannot have unbounded width* is the same shape horizontally; *flex overflowed* means a child asked for more
   than the parent allotted — make the child flexible or let it wrap; *incorrect use of a parent-data widget*
   means a positioning widget isn't a direct child of the ancestor that reads it; and **a "not laid out" error
   is a cascade, so ignore it and look further up the stack for the real constraint failure**.
3. **The error prints the constraints it received.** That dump is the answer to "why is this unbounded",
   and reading it is faster than any amount of reasoning about the tree — it says exactly what the parent
   offered, so the question becomes which ancestor produced those numbers rather than what to wrap the
   child in.
4. `Expanded`/`Flexible` inside a flex, `ConstrainedBox` where a bound is genuinely needed. The distinction
   worth holding is that a flex child asking for a bound is usually asking the wrong question: the parent
   already has the space, and the child's job is to say what share of it it wants.
5. **Clipping is not fixing.** Silencing an overflow by cutting the content off leaves the content there
   and unreachable — a label truncated mid-word, a button half off the edge, a row whose last item cannot
   be tapped. The overflow was reporting a real shortage of space, and the two honest answers are to let it
   scroll or to let it wrap.
6. **An overflow is silent in release.** The debug stripes are a debug feature, so a layout that only breaks
   on a small device or a long translation ships without a word — which is why the interesting sizes belong
   in a test or at least in one deliberate look, rather than in a bug report from a user with a 4.7-inch
   phone.
7. Adapt to the available window size (a layout builder, a size query, width breakpoints) rather than
   assuming a phone: tablets, desktop windows and foldables all arrive as "the same app". So does a
   landscape rotation and a split-screen half, both of which halve one dimension of a screen that was only
   ever seen upright.
8. **The screen size is not the widget's space.** A media query answers a question about the window, so a
   widget inside a dialog, a sheet, a split view or a nested scrollable that sizes itself from it is using a
   number that does not apply to it. The local constraints come from a layout builder, and that difference
   is the cause of most "it works on the page but not in the modal" reports.
9. **A size taken from a design mock is a device assumption.** The mock was drawn at one width, and a height
   in logical pixels copied out of it is correct on that device and wrong on the next — which is point 1's
   hardcoded height arriving through a legitimate-looking door. Express the intent (a share, a minimum, an
   aspect ratio) rather than the measurement.
10. **Text height is not yours to predict.** The reader's font-scale setting can make every label
    substantially taller, so a row that fits exactly at the default overflows for a large share of users —
    including the ones who most need the app to work. Let text wrap, give it room, and check one size above
    the default.
11. **A scaled-up label must not push its control out of the row.** The interaction between point 10 and the
    touch target of point 15 is where accessible text and accessible tapping collide: the layout that
    survives both lets the row grow taller rather than squeezing the control narrower.
12. Lay out around system UI explicitly: safe areas for notches, status bar and home indicator, and know the
    difference between the padding a system inset reserves and the inset the keyboard adds.
13. **The keyboard resizes the screen.** A column that fitted before it appeared now has half the height,
    so the fix is a scrollable rather than smaller content — and the field being typed into has to be
    scrolled into view above it (§6.16), because a form the user cannot see while typing is worse than one
    that scrolls.
14. **Aspect ratio for media, not a fixed height.** An image or a video given a hard height letterboxes on
    one device and crops on another, and it is also the shape that jumps when the real dimensions arrive.
    Reserving the ratio keeps the layout still while the content loads (§4.11).
15. Touch targets meet the platform's minimum size. An icon wrapped in a bare gesture detector is usually
    too small and has no ripple feedback; prefer a real button widget (or the kit's). The feedback is not
    decoration — without it a tap that did nothing is indistinguishable from a tap that missed, so the user
    taps again, which for a submit control is the double-submit case of §6.14.
16. **Intrinsic sizing is expensive.** Asking children how large they would like to be measures the subtree
    an extra time per frame, and nested inside a list it multiplies. It is occasionally the right tool and
    never the default; where it appears in a scrolling context, the honest answer is usually a fixed extent
    or a bounded slot.
