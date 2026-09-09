---
name: nuxt-no-props-destructure
description: "Use when reading a component's props: never const { foo } = props — it breaks reactivity silently. Read props.foo, or go through toRefs(props)/a computed."
---

# nuxt-no-props-destructure

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` §1.9, so destructuring a reactive
`props` object routes here directly instead of only through the whole Nuxt/Vue block.

## When
Writing or reviewing `<script setup>` code that reads a component's `props` — especially a
destructuring assignment (`const { foo } = props`).

## Steps
1. **Never destructure a reactive `props` object directly.** The value is copied at that instant and
   never updates again.
2. **Read `props.foo` directly**, or go through `toRefs(props)` to get a reactive ref per field, or
   through a `computed` that reads `props.foo` inside its getter.
3. Nothing errors when this is done wrong — the component simply keeps rendering the first value it
   ever saw, which reads as a caching bug somewhere else entirely, not a destructuring mistake.

## Output / checkpoint
No `const { ... } = props` in the diff — every prop read goes through `props.foo`, `toRefs(props)`,
or a `computed`.

## Guardrails
- `defineProps` return value is the object to avoid destructuring directly; a default extracted via
  `withDefaults` is still a prop and still subject to this rule.
- The neighbouring compiler-macro rule (`defineProps`/`defineEmits` never imported) lives right next
  to this one in `skills/vue-nuxt-vuetify-conventions` §1 — read it if the confusion is about macros
  rather than reactivity.

## Origin
No external source: this is `skills/vue-nuxt-vuetify-conventions` §1.9 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
