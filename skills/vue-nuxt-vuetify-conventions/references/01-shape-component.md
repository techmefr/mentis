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
18. **`defineModel` for a two-way bound prop, never a hand-rolled `modelValue` prop plus an
    `update:modelValue` emit.** The macro declares both halves in one line and stays type-safe across the
    boundary; the hand-rolled version is the same contract spelled out twice, and the two copies drift the
    first time only one side is edited. A named model (`defineModel('search')`) is how a component exposes
    more than one bound value without inventing a second convention for the second one.
19. **A `defineModel` can carry its own default and its own local `set` transform**
    (`defineModel({ default: '', set: (v) => v.trim() })`), which is where a value gets normalised on the
    way in without the parent's copy and the child's copy ever disagreeing about which one is
    authoritative. Doing the same normalisation in a `watch` on the prop is one frame late: the child
    already rendered the untrimmed value once.
20. **A generic component declares its type parameter with `generic="T"` on `<script setup>`**, not by
    casting props to `any` and hoping the caller passes the right shape. A list component typed
    `generic="T"` keeps `items: T[]` and the `item` slot's payload in the same type all the way to the
    call site — the caller gets real autocomplete on the row, and a mismatched slot usage is a compile
    error instead of a runtime `undefined`.
21. **`useTemplateRef` reads a template ref by the string name in the `ref="..."` attribute, and it is
    what makes the ref creation visible at the top of `<script setup>`** instead of buried wherever the
    template happens to declare it. A plain `ref()` meant to bind to the DOM but never referenced by name
    in the template stays `null` forever, and nothing about the component signals which of its refs are
    template refs versus internal state — `useTemplateRef` closes that ambiguity by tying the two
    together explicitly.
22. **A component with more than a couple of tightly related `ref`s benefits from being expressed through
    one composable call rather than a dozen loose declarations at the top of `<script setup>`.** The
    loose form still works, but every future feature that touches "this state" has to touch the whole
    list one by one, and nothing stops two of those refs from drifting out of sync with each other —
    which is the same shared-state risk a composable's own internal consistency check exists to prevent.
23. **`<script setup>`'s top-level bindings are all implicitly exposed to the template**, including a
    helper imported only to be called once during setup. That is convenient, not free: an import used
    purely for a side effect at the top of the script still shows up as if it were template-usable state,
    which is a small but real readability cost when scanning the script for what actually renders.
