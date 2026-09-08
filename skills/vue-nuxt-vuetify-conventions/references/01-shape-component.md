# vue-nuxt-vuetify-conventions §1 — The shape of a component

> Section 1 of `skills/vue-nuxt-vuetify-conventions`. Read it when a `.vue` file is created or restructured. The other sections and the guardrails stay in `SKILL.md`.

1. `<script setup lang="ts">`, always. Never the Options API, never untyped JS, never a `<script>`
   without `setup`.
2. **Block order fixed across the codebase** (`<template>` → `<script setup>` → `<style scoped>`) so a
   reviewer reads every file the same way. `<style>` always scoped; global styles live in a project-level
   stylesheet.
3. **One component per file.** A child component declared inside another file's script is invisible to
   search and impossible to test on its own.
4. **Never ship an empty `<script setup>` or an empty `<style>` block**: an empty block reads as logic
   deleted halfway, and says nothing about the component's intent. Omit it.
5. **A component renders, a composable thinks.** Logic — every `ref`, watcher, handler body, fetch and
   lifecycle hook — belongs in a composable, not inline in `<script setup>`. This is the most-broken rule
   of the set, so treat extraction as the default reflex rather than something to justify.
6. **Past a soft size limit** (the project's, ~150–200 lines of template), split rather than scroll. The
   limit is not aesthetic: past it nobody reads the whole file before editing it, so two people add the
   same thing in two places.
7. **Use the shorthand when the prop name matches the variable being passed.**
8. **Props, emits and model typed at the boundary.** Which form — the generic macro or the
   runtime/validator form — is a project decision, applied consistently; what is never acceptable is an
   untyped prop (§3.7, §3.8).
9. **Never destructure a reactive `props` object directly** (`const { foo } = props` breaks reactivity):
   the value is copied at that instant and never updates again. Read `props.foo`, or go through
   `toRefs(props)` / a `computed`. Nothing errors — the component simply keeps rendering the first value
   it ever saw, which reads as a caching bug somewhere else entirely.
10. **`defineProps`/`defineEmits`/`defineExpose`/`withDefaults` are compiler macros, never imported.**
    They exist only inside `<script setup>`, injected by the compiler; importing one of them from `vue`
    is a request for a runtime export that doesn't exist and either errors or silently defeats the
    macro's compile-time behaviour, depending on the toolchain.
11. **`shallowRef` for non-primitive state** (objects, arrays, heavy DOM refs) unless the nested
    reactivity is genuinely consumed. Deep reactivity on a large payload costs a proxy per nested object,
    and it is paid on every read, for a change detection nothing in the component is watching for.
12. **A composable returns `ref`s/`computed`s, never raw values.** A parameter that may be a value or a
    ref is read with `toValue()`, never `unref()` alone (no getter support) — the difference shows up the
    first time a caller passes a getter, and it shows up as a value that never refreshes.
13. **The template holds the shape, not the reasoning.** A multi-condition ternary or a chained
    expression in the markup cannot be read at a glance, tested, or reused by the sibling element that
    needs the same answer. Name it in a `computed`: the name is the documentation, and the reviewer can
    disagree with the name rather than re-deriving the logic.
14. **A child never mutates a prop.** The parent owns that value, so writing to it breaks the one-way
    contract the whole data flow depends on and makes the source of a wrong value unfindable. Emit, or
    take a `v-model`, and let the owner decide.
15. **`v-model` on a component is a declared pair, not a hand-rolled convention.** Use the model macro
    rather than inventing a `value` prop and an `input` emit: the homemade version diverges from every
    other component in the codebase, and the caller has to read the child to know which name it chose.
16. **When a component grows a prop per variant, the variation belongs to the caller.** Past a handful of
    props — or a boolean per state, which multiplies the combinations the component claims to support —
    it is describing several components, and the honest refactor is slots for what the caller should
    supply and a separate component for the case that is genuinely different.
17. **Don't `defineExpose` out of habit.** Exposing internals makes them API, so the next refactor inside
    the component is a breaking change for a parent you did not know existed — and it does not survive a
    client-only wrapper anyway (§12.5). Expose deliberately, or emit a ready payload.
