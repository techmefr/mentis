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
3. `Expanded`/`Flexible` inside a flex, `ConstrainedBox` where a bound is genuinely needed.
4. Adapt to the available window size (a layout builder, a size query, width breakpoints) rather than
   assuming a phone: tablets, desktop windows and foldables all arrive as "the same app".
5. Lay out around system UI explicitly: safe areas for notches, status bar and home indicator, and know the
   difference between the padding a system inset reserves and the inset the keyboard adds.
6. Touch targets meet the platform's minimum size. An icon wrapped in a bare gesture detector is usually
   too small and has no ripple feedback; prefer a real button widget (or the kit's).
