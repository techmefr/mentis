# react-nextjs-conventions §8 — The component library

> Section 8 of `skills/react-nextjs-conventions`. Read it when a UI element is built, or custom CSS is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. A copy-and-own component set (shadcn-style) is generated once and then **owned by the project**: it isn't
   a versioned dependency updated from outside. That cuts both ways and both halves matter. Nothing upstream
   can break the build, which is the point; but no upstream fix arrives either, so an accessibility defect
   or a browser regression in a primitive is now yours to find and yours to repair. Treating the folder as
   vendor code you are merely storing is the mistake — it is application code that happened to arrive
   pre-written.
2. Extend a generated component through a wrapper composing it, never by editing the generated file in
   place: a regeneration or another consumer inherits the deviation otherwise. The failure is quiet in both
   directions — a regeneration reverts your change without mentioning it, and until then every other screen
   in the application silently got a behaviour that was only ever wanted on one.
3. **When a primitive genuinely has to change, the change is recorded where the next person will look.** A
   real upstream defect, or a project-wide decision that belongs in the primitive rather than in fifteen
   wrappers, is a legitimate edit — but a regeneration will revert it in silence, so the reason lives in a
   comment at the edit and in the block's own notes. An undocumented divergence is indistinguishable from
   generated code, which is exactly why it disappears.
4. **A wrapper forwards what it does not handle.** Spreading the remaining props and forwarding the ref is
   not boilerplate: a wrapper that accepts only the four props today's screen needs is a narrower component
   than the one it wraps, so the next consumer who wants `aria-describedby`, a test attribute or an
   `onBlur` cannot use it and copies the primitive again. One wrapper per primitive becomes three, and they
   diverge.
5. One merge point for utility classes (a `cn()`-style `clsx` + `tailwind-merge` helper): never a hand-built
   class string, never two sources of conditional classes on one component. Utility frameworks resolve
   conflicts by which class wins in the stylesheet, not by which one appears later in the attribute, so two
   sources of truth produce a result that depends on build order rather than on the code — it works
   locally and inverts in production, or works until an unrelated class is added.
6. **The caller's `className` is merged last.** A wrapper that concatenates its own classes after the ones
   it received makes overriding impossible from outside, and the consumer's next move is an `!important` or
   a hand-built copy of the component. Order the merge so the call site can win.
7. **Variants are data, not a chain of conditionals.** A variant API (a `cva`-style map) keeps adding a
   state to one entry; nested ternaries over `size` and `intent` in the class string make every new
   combination a rewrite, and they make it impossible to see which combinations exist.
8. **A boolean prop that changes the whole layout is two components.** `<Panel isCompact>` rendering a
   different structure means every future prop has to be read twice, and the two branches drift until each
   one is only correct for its own caller. Split them and share the parts that are genuinely shared.
9. **The primitive owns the accessible behaviour, and a wrapper must not strip it.** Focus management, the
   `aria` wiring between a trigger and its panel, the escape handling — those live in the generated
   component precisely so that no screen has to remember them. Reimplementing the visual part of a
   disclosure or a dialog "because the primitive was in the way" ships a control that a keyboard cannot
   reach (§10).
10. **Render polymorphically instead of duplicating.** A button that sometimes needs to be a link is the
    library's `asChild`-style escape hatch, not a second component; hand-rolling it as a `div` with an
    `onClick` loses the keyboard activation, the focus ring and the semantics in one move.
11. **No custom CSS for something the utility layer already has.** A hand-written rule for spacing, a
    cursor, an opacity or a truncation is a rule that no longer participates in the design system: it does
    not respond to the tokens, does not switch with the theme, and has to be found by grep when either
    changes.
12. **A colour, a radius or a spacing step is a token, never a literal.** A hex value hard-coded once is
    hard-coded fifty times within a quarter, and then the dark-mode or rebrand pass consists of finding all
    fifty. The token is also the only version that a designer can read.
13. **Two of the same primitive is a defect, not a preference.** A second spinner, a second modal, a second
    date input will diverge — different focus behaviour, different loading semantics — and the divergence
    surfaces as a bug report about inconsistency that nobody can reproduce on the other one.
14. **No business knowledge inside a primitive.** A `Table` that knows about invoices cannot be reused and
    cannot be regenerated, and the business rule it absorbed is now in the last place anyone would look for
    it. The primitive takes data and callbacks; the meaning stays in the wrapper above it.
15. Folder split held: generated primitives in their own folder untouched, business wrappers above them,
    helpers and shared hooks in their own places. No business component living flat among the primitives —
    the split is what makes "can this file be regenerated?" answerable by its path instead of by reading it.
