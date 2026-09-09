---
name: nuxt-define-store-once
description: "Use when writing defineStore(): call it once at module level, never inside a setup()/composable/function body — otherwise every call recreates the store instead of reusing the shared singleton."
---

# nuxt-define-store-once

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` §2.4, so a `defineStore()` call
routes here directly instead of only through the whole Nuxt/Vue block.

## When
Writing or reviewing a Pinia (or equivalent) store definition — specifically where `defineStore()` is
called.

## Steps
1. **`defineStore()` is called once, at module level.** Never inside a `setup()`, a composable, or any
   function body that runs more than once.
2. Calling it from inside a function recreates a new store definition on every call, instead of
   reusing the shared singleton the rest of the app expects.

## Output / checkpoint
Every `defineStore()` call in the diff sits at the top level of its file, exported once — none of
them are nested inside `setup()`, a composable function, or any other function body.

## Guardrails
- A store is for state genuinely shared across **unrelated** components or pages — not a convenient
  global for state that could stay a composable or a plain `ref`
  (`skills/vue-nuxt-vuetify-conventions` §2.3). Check that before reaching for a store at all.
- Async loading/error state on the store's own fetch belongs exposed explicitly (`data`, `pending`,
  `error`), never inferred from a null check — `skills/vue-nuxt-vuetify-conventions` §2.5.

## Origin
No external source: this is `skills/vue-nuxt-vuetify-conventions` §2.4 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
