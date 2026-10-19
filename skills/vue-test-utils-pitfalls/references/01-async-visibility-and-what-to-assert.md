# vue-test-utils-pitfalls §1 — Async, visibility and what to assert

> Part 1 of `skills/vue-test-utils-pitfalls`. Read it when an assertion races the render, a hidden element is
> counted as present, or a test reaches into the component. Sourced from the Vue Test Utils guide pages on
> asynchronous behaviour, conditional rendering, writing components that are easy to test, and the component
> instance (commit `f472a50`), read 2026-10-16. Sentences marked "own guidance" are ours.

## 1.1 The DOM updates on the next tick
1. **A change to reactive data is reflected in the DOM later.** Vue updates asynchronously and a test runner
   runs synchronously, so `wrapper.find('button').trigger('click')` followed at once by an assertion on the
   text fails: the data changed, the DOM did not yet.
2. **Await the call that causes the update.** `trigger` and `setValue` return the next-tick promise, so
   `await wrapper.find('button').trigger('click')` is the fix; `await nextTick()` from Vue is the general
   form. The same holds for `setProps`.
3. **Own guidance:** make the `await` a habit on every `trigger`, `setValue` and `setProps`, even when a
   particular test passes without it, because a later change to the component can turn the race into a flake.

## 1.2 Promises Vue does not know about
1. **`nextTick` does not wait for your own promises.** If a component calls an HTTP client in a hook, the mocked
   promise is invisible to Vue and the assertion can run before it resolves.
2. **Use `flushPromises` from VTU**, which resolves all outstanding promises, then assert:

```ts
vi.spyOn(client, 'get').mockResolvedValue({ data: 'some mocked data' })
const wrapper = mount(ReportCard)
await flushPromises()
expect(wrapper.text()).toContain('some mocked data')
```

3. **Own guidance:** if the assertion still races after `flushPromises`, the code has a timer or a chain of
   awaits across modules; wait for the visible outcome (the text or the element appearing) rather than adding
   a second flush.

## 1.3 A component with an async `setup`
1. **It must be mounted inside `Suspense`.** The page's way is a small wrapper component that renders
   `<Suspense><Async /></Suspense>`, then `await flushPromises()`.
2. **The wrapper you get back belongs to the wrapper component.** Its own `vm` is empty. To reach the async
   component, use `wrapper.findComponent(Async)`.

## 1.4 Hidden is not absent
1. **`exists()` says whether an element is in the DOM.** An element under `v-show` stays in the DOM and
   `find().exists()` stays true.
2. **`isVisible()` checks visibility** for `display: none`, `visibility: hidden` and `opacity: 0` on the
   element or an ancestor, a collapsed `<details>`, and the `hidden` attribute.
3. **`isVisible()` needs the wrapper attached to the document.** Mount with `attachTo: document.body`. The
   page warns that without it CSS-driven visibility, such as `v-show`, may not be detected, especially under
   happy-dom.
4. **Own guidance:** when you attach to the document, remove the wrapper (`wrapper.unmount()`) at the end of
   the test so the next test does not find the old markup.
5. **`get()` is for what must be there** (it throws if missing); `find()` with `exists()` is for what may be
   absent.

## 1.5 What to assert
1. **Think in inputs and outputs.** Inputs are interactions, props and data streams (API calls,
   subscriptions). Outputs are rendered DOM, emitted events and side effects such as an API call. The page says
   everything else is an implementation detail: internal methods, intermediate states, even data.
2. **A test should not break on a refactor that keeps behaviour.** The page's example: a test that sets `data`
   with `setData` and selects by a CSS class breaks when either changes although the component still works,
   which it calls a false positive. The rewrite clicks the button and checks the visible text.
3. **`vm` is the escape hatch, not the default.** The page allows it in rare cases and says to assert against
   the DOM in general. `getComponent(Child).props()` is acceptable to check what a parent passes, and the page
   adds that asserting the rendered content is more thorough, because it checks that the prop was passed and
   rendered.
4. **A CSS selector in `findComponent` returns a looser wrapper type.** Pass the component type as the generic
   to get a `VueWrapper`.
5. **Make components easy to test.** The page suggests extracting API calls and complex methods into their own
   modules, so they can be tested alone or mocked.

## 1.6 Verify
Remove an `await` from one test and see it fail; break the component's text and see the test fail; read the
test and ask whether it would still pass after renaming a data property or a class.
