# react-nextjs-conventions §8 — The component library

> Section 8 of `skills/react-nextjs-conventions`. Read it when a UI element is built, or custom CSS is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. A copy-and-own component set (shadcn-style) is generated once and then **owned by the project**: it isn't
   a versioned dependency updated from outside.
2. Extend a generated component through a wrapper composing it, never by editing the generated file in
   place: a regeneration or another consumer inherits the deviation otherwise.
3. One merge point for utility classes (a `cn()`-style `clsx` + `tailwind-merge` helper): never a hand-built
   class string, never two sources of conditional classes on one component.
4. Folder split held: generated primitives in their own folder untouched, business wrappers above them,
   helpers and shared hooks in their own places. No business component living flat among the primitives.
