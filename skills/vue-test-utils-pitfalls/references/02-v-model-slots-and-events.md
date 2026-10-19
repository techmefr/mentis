# vue-test-utils-pitfalls §2 — `v-model`, slots and events

> Part 2 of `skills/vue-test-utils-pitfalls`. Read it when the contract under test is a model value, a slot or
> an emitted event. Sourced from the Vue Test Utils guide pages on `v-model`, slots and event handling (commit
> `f472a50`), read 2026-10-16. Sentences marked "own guidance" are ours.

## 2.1 Testing `v-model`
1. **A `v-model` is a prop plus an update event, and a mounted component has no parent to connect them.**
   Mounting with only `modelValue` and then typing changes nothing in the props: the component emits
   `update:modelValue` and nobody writes the new value back.
2. **Give the mount the handler that does the parent's job:**

```ts
const wrapper = mount(Editor, {
  props: {
    modelValue: 'initial',
    'onUpdate:modelValue': (value: string) => wrapper.setProps({ modelValue: value }),
  },
})
await wrapper.find('input').setValue('typed')
expect(wrapper.props('modelValue')).toBe('typed')
```

3. **The page adds an `await nextTick()` before `setProps`** in its handler for the case where the model value
   is updated inside `setup`. Own guidance: if the assertion is flaky with a synchronous handler, try that form
   first.
4. **A second model is a second pair.** For a component with `v-model:currency` as well as the default model,
   pass `currency` and `'onUpdate:currency'` in the same way and assert both props after setting each input.
5. **Own guidance:** also assert the emitted event itself (`wrapper.emitted('update:modelValue')`) when the
   parent contract matters; the prop round trip alone cannot tell "emitted once" from "emitted twice".

## 2.2 Slots
1. **Use the `slots` mounting option.** The default slot is `default`; named slots use their name. The content
   may be a string of text or HTML, a render function, an object with a template, or an imported SFC, and an
   array gives several nodes in one slot.
2. **Assert where it landed, not only that it exists.** A check that `html()` contains the text passes if the
   text is rendered anywhere; the page's more specific version checks that the content is inside the `<main>`
   element.
3. **Scoped slots are supported.** When the slot content is a string template, wrap it in
   `<template #scoped="scope">` to name the scope variable. If you do not, the slot's scope is available as
   an object called `params`.
4. **Own guidance:** change the slot content in one test run and see the assertion fail; a slot test that
   does not depend on the content passed proves only that the component renders.

## 2.3 Emitted events
1. **`wrapper.emitted()` returns an object keyed by event name** and `wrapper.emitted('name')` returns an
   array with one entry per emission; each entry is itself the array of arguments. After two clicks that emit
   a count, the second entry compares with `[2]`, not `2`.
2. **Assert the count and the payload.** The page checks the length of the array and each payload with
   `toEqual`, including an object payload that carries a derived flag (`isEven`).
3. **Trigger the event the way the user would** (`trigger('click')` on the button), and await it (part 1.1).
4. **First check that the event name is present.** The page does it with `toHaveProperty` on `emitted()` before
   it indexes into the array. Own guidance: do the same so a missing event fails with a clear message and not
   as an error on an undefined value.

## 2.4 Verify
Delete the update handler and see the model test fail; change one slot's content and see its test fail;
emit the event twice and see the count assertion fail.
