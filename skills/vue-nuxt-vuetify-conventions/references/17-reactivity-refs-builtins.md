# vue-nuxt-vuetify-conventions §17 — Template refs, attribute fallthrough, watchers, built-ins and store traps

> Section 17 of `skills/vue-nuxt-vuetify-conventions`. Read it when a template ref is read, attributes are forwarded
> through a wrapper component, a watcher is written, a `<Transition>` or `<KeepAlive>` is used, or a store is called
> outside a component. The other sections and the guardrails stay in `SKILL.md`. **Version stamp:** Vue 3.5 (latest
> release 3.5.43 on 2026-10-02) from the framework's documentation repository read the same day; Pinia from its
> documentation (latest 4.0.3). Items tagged 3.5+ need that minor.

## Template refs
1. **A template ref is `null` until the element is mounted**, and again `null` after a `v-if` removes it. Read it
   in `onMounted` or later, never in setup or in a template expression on the first render, and write every
   use as `ref.value?.…` or behind a guard. A watcher on a template ref must account for `null`.
2. **Use `useTemplateRef('name')` (3.5+)** rather than a `ref(null)` named like the attribute: the string is
   checked against the template, and a rename in the template breaks one place visibly. Before 3.5, the variable
   name must equal the attribute value.
3. **A ref inside `v-for` is an array of elements and its order does not follow the source array.** Never
   index it with the source index; key by a data attribute or an id carried by the element.
4. **Do not put `v-if` and `v-for` on the same element**: `v-if` is evaluated first and cannot see the loop
   variable. Filter in a computed list, or wrap in a `<template v-for>`.
5. **A ref on a component gives the instance, and only what the component exposes** (refs unwrapped). Prefer a
   prop or an emitted event to reaching into a child; use the instance for focus and imperative handles that
   the child exposes on purpose.

## Attribute fallthrough
6. **Non-prop attributes and listeners fall through to the single root element**, and `class` and `style` are
   merged with the root's own. A wrapper around a native control that must apply them to the inner control sets
   `inheritAttrs: false` and binds `$attrs` to that inner element.
7. **A component with several root nodes does not inherit anything**, and Vue warns when `$attrs` is not bound
   explicitly. Bind `$attrs` to the intended node or give the component one root.

## Watchers
8. **Create a watcher synchronously in `setup`.** One created after an `await` or in a callback is not bound to
   the owner and is never stopped: keep the stop function and call it, or move the creation before the `await`.
9. **`watch` is shallow on a ref and implicitly deep on a reactive object.** Deep traversal costs in proportion to
   the object; use a getter returning exactly what matters, or a depth number (3.5+), instead of `deep: true` on a
   big structure.
10. **`watchEffect` tracks only what is read before its first `await`.** In an async effect, read the dependencies
    first or use `watch` with an explicit source, which also states the dependency.
11. **Watcher callbacks run before the component's DOM update by default.** To read the updated DOM, use
    `flush: 'post'` (or `watchPostEffect`). `flush: 'sync'` fires on every mutation, once per change, and is for
    rare cases that need it.
12. **Clean up a side effect that can be superseded** (a request, a timer): register the cleanup with
    `onWatcherCleanup` (3.5+, only during the synchronous part of the callback) or use the `onCleanup` argument,
    which has no such constraint. Use `once: true` (3.5+) for a one-shot watch.
13. **`nextTick()` waits for the next DOM update flush.** Reach for it after changing state when the next line
    reads the DOM (focus, scroll, measurement); not as a delay for hiding a missing dependency.

## Built-ins
14. **`<Transition>` takes one element or one single-root component** as content, triggered by `v-if`, `v-show`,
    a dynamic component or a changed `key`. For an element that replaces another, `mode="out-in"` runs the leave
    before the enter. Nested transitions need an explicit duration, otherwise the first `transitionend` ends the
    wait. Animate `transform` and `opacity` rather than layout properties.
15. **`<KeepAlive>` caches the switched-away component instance** instead of unmounting it. Matching by
    `include`/`exclude` uses the component name (inferred from the file name for `<script setup>` since 3.2.34);
    set `max` so it behaves as a bounded cache; resource set-up and tear-down that must follow visibility goes in
    `onActivated`/`onDeactivated`, not `onMounted`/`onUnmounted`.

## Pinia traps (also §2)
16. **A set-up store returns every state property.** An un-returned ref is not state: it is invisible to devtools,
    serialisation and hydration, and a private state property is not possible. Return only store data; a router or
    an injected value is read in the component.
17. **A store is created on its first `useXStore()` call, which needs an installed Pinia.** Calling it at module
    top level before `app.use(pinia)` fails with the "no active pinia" error. Call it inside functions that run
    after installation, or pass the instance; in server rendering always pass the request's instance so state is
    not shared across requests.
18. **Never destructure state from the store** (reactivity is lost); use `storeToRefs()` for state and getters.
    Actions can be destructured. Group several mutations in one `$patch`.

## Mechanical checks

```
grep -rnE "ref\(null\)" src --include=*.vue
grep -rnE "\.value\.[a-zA-Z]+" src --include=*.vue | grep -iE "ref|el|input|form"
grep -rnE "v-for=.* v-if=|v-if=.* v-for=" src --include=*.vue
grep -rnE "inheritAttrs" src
grep -rnE "watch(Effect)?\(" src | grep -E "await|async"
grep -rnE "deep: *true" src
grep -rnE "nextTick" src
grep -rnE "(const|let) \{[^}]+\} *= *use[A-Z][A-Za-z]*Store\(\)" src
```

- A `ref(null)` used as a template ref in 3.5+ code is a candidate for `useTemplateRef`.
- A `.value.` access on a template ref with no optional chaining or guard is rule 1.
- An `async` watcher is checked against rules 8 and 10; `deep: true` against rule 9.
