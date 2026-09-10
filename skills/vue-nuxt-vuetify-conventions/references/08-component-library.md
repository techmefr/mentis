# vue-nuxt-vuetify-conventions §8 — The component library

> Section 8 of `skills/vue-nuxt-vuetify-conventions`. Read it when a UI element is built, or custom CSS is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. **Toolkit first**: if the chosen UI library ships a component, composable, directive or utility class
   for the need, use it rather than pulling another package or hand-rolling a `<div>`. Mixing a second UI
   library splits both the visual language and the mental model.
2. **Go to the most specific component available** — a data table for a sortable/filterable list of rows,
   a dialog for a one-off confirmation, a chip for a status — rather than assembling one from primitives.
   The specific component already carries the keyboard behaviour, the ARIA wiring and the states you
   would otherwise rebuild by hand and half-finish.
3. **Spacing, visibility and state utilities come from the toolkit's own classes** (`ma-*`, `pa-*`,
   `d-*`, cursor and opacity helpers) rather than a custom scoped `<style>`. A scoped style for a simple
   padding/margin/background is a review signal: it means the author did not know the helper existed, so
   the next person will write a second one that differs by two pixels.
4. **Check a prop really exists in the project's version of the toolkit before passing it.** A prop that
   silently does nothing — a `:show-select="false"` on a wrapped data table is the recurring shape —
   survives review because nothing errors, and the behaviour it was supposed to suppress stays on screen.
   Read the docs for the **installed** version, not the latest: props and slots get renamed across
   majors, and the newest documentation is the most convincing wrong answer available.
5. **Inside an item slot of a data table, autocomplete or select, the object exposed is often the
   library's internal wrapper**: read the data through its raw payload (`item.raw`), not through `item`
   directly. The wrapper's own fields resolve to `undefined` rather than failing, so the cell renders
   empty and the diff looks fine.
6. **A carve-out from rule 1 is legitimate** — many projects route notifications to a dedicated toast
   library rather than the toolkit's snackbar, and date handling to a dedicated date lib. Read the
   project's decision instead of assuming either way, and follow it rather than reopening it in a feature
   branch.
7. **Extend a generated or vendored component through a wrapper, never by editing the generated file in
   place.** The next regeneration silently reverts the edit, and the regression appears in a commit that
   touched nothing related.
8. **Don't wrap a toolkit component just in case.** A passthrough wrapper adds a layer that has to
   forward everything and will not, so consumers lose a prop or a slot and cannot see why. Wrap when
   there is a real house default to encode — a standard density, a standard error slot — not to reserve
   the option.
9. **A wrapper forwards attributes and slots explicitly.** Anything not forwarded is silently
   unavailable: the consumer passes a prop, nothing happens, and the wrapper is the last place they will
   look. Forward `v-bind="$attrs"` and the slots the component actually has, and say in the wrapper which
   ones are deliberately not exposed.
10. **Colours come from the theme, not from a hex in a component.** A hardcoded colour is invisible to
    the light/dark switch and to any future palette change, so it is the one element that stays wrong
    after the theme is updated — and it will be found by a user, not by a build.
11. **Don't reach into the library's internals with deep selectors.** A `:deep()` targeting a generated
    class name couples your styling to a private implementation detail: those names are not API, they
    change on a minor upgrade, and the breakage is a silently unstyled element rather than an error. If
    the component offers no seam for what you need, that is the thing to say out loud.
12. **The component's accessibility is only kept if you don't defeat it** (§7). Replacing the toolkit's
    control with a plain `div` inside one of its slots, removing the focus style to match a mockup, or
    suppressing the label because the design has none — each of these hands back the part of the
    component that was doing the work.
13. **A data table's server-side mode is a different contract from its client-side mode.**
    Half-configuring it — server-side items with client-side sorting or filtering — produces a table that
    orders and narrows the page in hand and looks entirely correct until the second page (§12.12).
14. **One icon set, resolved through the toolkit's icon configuration.** Three ad-hoc import styles
    across a codebase means three ways an icon can be missing, and it is also the usual reason a whole
    icon library ends up in the bundle (§12.7).
15. **`density` is the toolkit's own answer to "make this more compact"**, not a smaller font size hand-set
    per component. It is a documented scale (`default`/`comfortable`/`compact`) applied consistently across
    inputs, lists and tables, so a form built at `compact` density reads as one deliberate register instead
    of a collection of components each shrunk by a different amount because someone eyeballed the padding.
16. **A data table's dynamic header/item slots (`header.<key>`, `item.<key>`) target one column**, and
    reaching for `hide-default-header`/`hide-default-footer` to hand-roll the whole chrome is the sign the
    project needed a different, more specific component (§8.2) rather than a fight with this one. Rebuilding
    the header from scratch also rebuilds — or drops — the sort affordance the default header already
    wired in.
17. **Read the item payload the slot actually received before assuming it matches the row you passed in.**
    A table, autocomplete or select slot can carry derived fields the toolkit computed for its own display
    logic alongside the raw record; treating the slot payload as if it were exactly the array element
    handed to `items` is the same wrapper-object trap as §8.5, one layer further into the component's own
    slot API rather than at the top-level `item`.
18. **A checkbox rendered inside a table or list slot uses the toolkit's own selection primitive**, not a
    freestanding input wired to local state by hand. The toolkit's version is already synchronised with the
    table's `v-model` for selected rows; a hand-wired one drifts the moment the table's own selection state
    changes for a reason the slot didn't cause — a filter, a page change, a `select-all`.
19. **A component library upgrade is read against that version's own migration notes before the props and
    slots are touched**, not discovered prop-by-prop when something silently stops working. A prop renamed
    or a slot payload reshaped between majors is exactly the failure mode of §8.4 (a prop that does nothing)
    happening to the whole team at once on the day of the bump, rather than to one author reading stale
    docs.
20. **A custom theme is declared once, at the toolkit's own configuration point, and consumed by name
    everywhere else** (a semantic colour, a spacing token) rather than re-declared per component. The
    project that skips this ends up with the dark-mode flash of §12.6 for a different reason: two components
    each holding their own idea of what "primary" means, updated on two different days.
