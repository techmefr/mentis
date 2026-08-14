# vue-nuxt-vuetify-conventions §8 — The component library

> Section 8 of `skills/vue-nuxt-vuetify-conventions`. Read it when a UI element is built, or custom CSS is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. **Toolkit first**: if the chosen UI library ships a component, composable, directive or utility class for
   the need, use it rather than pulling another package or hand-rolling a `<div>`. Mixing a second UI library
   splits both the visual language and the mental model.
2. Go to the most specific component available (a data table for a sortable/filterable list of rows, a
   dialog for a one-off confirmation, a chip for a status) rather than assembling one from primitives.
3. Spacing, visibility and state utilities come from the toolkit's own classes (`ma-*`, `pa-*`, `d-*`,
   cursor and opacity helpers) rather than a custom scoped `<style>`. A scoped style for a simple
   padding/margin/background is a review signal.
4. Check a prop really exists in the project's version of the toolkit before passing it. A prop that
   silently does nothing (a `:show-select="false"` on a wrapped data table) is the recurring shape of this
   mistake, and it survives review because nothing errors.
5. Inside an item slot of a data table / autocomplete / select, the object exposed is often the library's
   internal wrapper: read the data through its raw payload (`item.raw`), not through `item` directly.
6. A carve-out from rule 1 is legitimate — many projects route notifications to a dedicated toast library
   rather than the toolkit's snackbar, and date handling to a dedicated date lib. Read the project's
   decision instead of assuming either way.
7. Extend a generated/vendored component through a wrapper, never by editing the generated file in place.
