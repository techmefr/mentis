# react-nextjs-conventions §10 — Accessibility and bundle weight

> Section 10 of `skills/react-nextjs-conventions`. Read it when a control is rendered, or a dependency added. The other sections and the guardrails stay in `SKILL.md`.

1. An icon-only button with no visible label needs an `aria-label`. Every `<img>` needs an `alt`: the
   description if it carries meaning, `alt=""` (never omitted) if it's purely decorative — a missing `alt`
   reads out the filename to a screen reader.
2. An open modal: focus placed on it, trapped inside, returned to the trigger on close.
3. Native semantic elements over clickable `div`s; heading order without skipped levels.
4. Never block paste on an authentication field (password, one-time code).
5. Never disable viewport zoom: if the layout breaks at 200%, the layout is the problem.
6. A default import from an icon lib, or a heavy module loaded at the level of a rarely visited route,
   bloats the bundle for nothing: named import / `next/dynamic`.
