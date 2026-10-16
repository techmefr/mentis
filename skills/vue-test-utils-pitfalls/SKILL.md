---
name: vue-test-utils-pitfalls
description: "Use when Vue 3 components are tested with Vue Test Utils: assertions that run before the DOM updates (await trigger and setValue, flushPromises), components with an async setup, isVisible and attachTo, testing v-model through props and the update event, named and scoped slots, emitted events, stubs and shallow mounting (async components, directives, default slots), teleported content, built-in transition stubs, server rendering with renderToString, a real or mocked router, and fake system time."
---

# vue-test-utils-pitfalls

A defensive block for component tests written with Vue Test Utils (VTU). The three parts share one premise:
**VTU mounts a real component, but several things around it are replaced, delayed or invisible to the
wrapper**: the DOM updates on the next tick, a stub replaces the child you meant to check, a teleport moves
the markup out of the wrapper, and a router is a plugin that starts asynchronously. A test that passes
without noticing one of these asserts less than it appears to. Generic assertion mistakes are in
`skills/jest-vitest-assertion-pitfalls`; queries and events with the Testing Library family are in
`skills/testing-library-query-pitfalls`; router behaviour itself is in `skills/vue-router-pitfalls`; the
choice of what to test is in `skills/testing-blocks`.

## When
- A Vue test asserts right after a click or an input and the assertion fails, or passes for the wrong reason.
- A component has an `async setup`, calls an API in a hook, or uses `v-show`, slots, `v-model`, a teleport or
  a transition.
- A test uses `shallow`, `stubs` or `mocks`, or replaces a child component or a directive.
- A component reads the router or the route, or the project renders on the server.

## Steps

**Read only the part the test meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Waiting for the DOM, other promises, async setup, visibility, what to assert | an assertion races the render, or a hidden element counts as present | [`01-async-visibility-and-what-to-assert.md`](./references/01-async-visibility-and-what-to-assert.md) |
| 2 | `v-model`, slots, emitted events | a component's contract is its model value, its slots or its events | [`02-v-model-slots-and-events.md`](./references/02-v-model-slots-and-events.md) |
| 3 | Stubs and shallow mounting, teleport, transitions, server rendering, router, fake time | a child, a directive, a portal, a transition, the router or the clock is replaced | [`03-stubs-teleport-router-and-time.md`](./references/03-stubs-teleport-router-and-time.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: an assertion that failed before an `await` was made to pass
by awaiting the call that changes the DOM (part 1.1), a test of a model value fails if the update handler is
removed (part 2.1), a slot test fails when the slot content is changed (part 2.2), a stubbed child shows up as
a stub in the printed HTML (part 3.1), and a router test builds a new router in each test (part 3.6). A test that
passes but was never made to fail proves nothing.

## Guardrails
- Never assert on the DOM after `trigger`, `setValue` or `setProps` without awaiting it (part 1.1).
- Never use `nextTick` to wait for a promise Vue does not know about; use `flushPromises` (part 1.2).
- Never call `find` and `exists` to check visibility; a `v-show` element is in the DOM (part 1.4).
- Never assert against `wrapper.vm` or a CSS class when the user-visible text or an emitted event shows the
  same fact (part 1.5).
- Never test a `v-model` component without wiring the update handler back to the prop (part 2.1).
- Never stub a child you want to assert on, and never leave `renderStubDefaultSlot` on after the test (part
  3.1).
- Never share one router instance between tests (part 3.6).
- Never mount a component before calling `vi.setSystemTime` (part 3.7).
- This block states the Vue Test Utils documentation as of the commit read on the date in
  [`references/origin.md`](./references/origin.md); the VTU version the pages describe was not checked, and
  nothing was run while writing the block.

## Origin
Rewritten from the Vue Test Utils documentation (vuejs/test-utils, MIT), read 2026-10-16. 🟡: never run by us;
open points are in [`references/origin.md`](./references/origin.md).
