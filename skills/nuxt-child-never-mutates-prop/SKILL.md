---
name: nuxt-child-never-mutates-prop
description: "Use when a component writes to a value it received as a prop: never — the parent owns it. Emit, or take a v-model, and let the owner decide."
---

# nuxt-child-never-mutates-prop

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` §1.14, so a child component
writing to a prop routes here directly instead of only through the whole Nuxt/Vue block.

## When
Writing or reviewing a component that assigns to, pushes into, or otherwise mutates a value it
received through `props` — including mutating a nested object or array passed as a prop.

## Steps
1. **A child never mutates a prop.** The parent owns that value; writing to it breaks the one-way
   data-flow contract the whole component tree depends on.
2. **Emit an event, or take a `v-model`**, and let the owning parent decide whether and how the value
   changes.
3. This applies to nested mutation too — pushing into an array prop or setting a nested object
   property is still a mutation of the parent's data, even though the prop binding itself doesn't
   change.

## Output / checkpoint
No component in the diff assigns to, or mutates a nested field of, a value it received as a prop —
every change to that data is expressed as an emitted event or a `v-model` update handled by the
owner.

## Guardrails
- When the mutation "feels local" (a checkbox toggling a nested flag), that's exactly the case
  `v-model` on a component exists for — see `skills/vue-nuxt-vuetify-conventions` §1.15 for the
  declared-pair form rather than a hand-rolled convention.
- The failure mode is specifically that the source of a wrong value becomes unfindable — the bug
  surfaces far from the mutation, in whatever else reads the same prop.

## Origin
No external source: this is `skills/vue-nuxt-vuetify-conventions` §1.14 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
