# vue-nuxt-vuetify-conventions §1 — The shape of a component

> Section 1 of `skills/vue-nuxt-vuetify-conventions`. Read it when a `.vue` file is created or restructured. The other sections and the guardrails stay in `SKILL.md`.

1. `<script setup lang="ts">`, always. Never the Options API, never untyped JS, never a `<script>` without
   `setup`.
2. Block order fixed across the codebase (`<template>` → `<script setup>` → `<style scoped>`) so a reviewer
   reads every file the same way. `<style>` always scoped; global styles live in a project-level stylesheet.
3. One component per file. A child component declared inside another file's script is invisible to search
   and impossible to test on its own.
4. Never ship an empty `<script setup>` or an empty `<style>` block: an empty block reads as logic deleted
   halfway, and says nothing about the component's intent. Omit it.
5. **A component renders, a composable thinks.** Logic — every `ref`, watcher, handler body, fetch and
   lifecycle hook — belongs in a composable, not inline in `<script setup>`. This is the most-broken rule of
   the set, so treat extraction as the default reflex rather than something to justify.
6. Past a soft size limit (the project's, ~150–200 lines of template), split rather than scroll.
7. Use the shorthand when the prop name matches the variable being passed.
8. Props/emits/model typed at the boundary. Which form — the generic macro or the runtime/validator form —
   is a project decision, applied consistently; what is never acceptable is an untyped prop.
9. Never destructure a reactive `props` object directly (`const { foo } = props` breaks reactivity). Read
   `props.foo`, or go through `toRefs(props)` / a `computed`.
10. **`defineProps`/`defineEmits`/`defineExpose`/`withDefaults` are compiler macros, never imported.** They
    exist only inside `<script setup>`, injected by the compiler; an `import { defineProps } from 'vue'`
    line is a request for a runtime export that doesn't exist and either errors or silently defeats the
    macro's compile-time behaviour, depending on the toolchain.
11. `shallowRef` for non-primitive state (objects, arrays, heavy DOM refs) unless the nested reactivity is
    genuinely consumed.
12. A composable returns `ref`s/`computed`s, never raw values. A parameter that may be a value or a ref is
    read with `toValue()`, never `unref()` alone (no getter support).
