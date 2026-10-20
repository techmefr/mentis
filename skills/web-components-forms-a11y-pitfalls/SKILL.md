---
name: web-components-forms-a11y-pitfalls
description: "Use when a native custom element must behave like a real control or sit inside a form, a shadow root, or a server-rendered page: form participation through ElementInternals (value, validity, reset, disabled, restore), default roles and labels, focus delegation, custom states, events that cross the shadow boundary (composed, retargeting, composedPath), shadow styling hooks, and declarative shadow DOM for server rendering."
---

# web-components-forms-a11y-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the second half of custom-element work: the part where an element stops being a private widget and has to cooperate with the page around it. The premise: **a custom element is a bare box to the platform; it is not focusable, not labelled, not submitted, not reset, and its events do not mean what they meant before the shadow root was added, until you wire each of those yourself**. Each rule gives the symptom, the check and the fix.

Constructor, callbacks, registration and teardown are in `skills/web-components-lifecycle-pitfalls`; the library-level practice for Lit is in `skills/web-components-conventions`; general widget semantics are in `skills/accessibility` and `skills/nuxt-semantic-element-first`. This block does not repeat them.

## When
- A custom element wraps an input and "the form does not send it", "reset does nothing" or "it stays enabled inside a disabled fieldset".
- A custom button, checkbox or select is announced as nothing, cannot be tabbed to, or has no accessible name.
- A listener on the host sees the wrong `event.target`, or an event never leaves the shadow root.
- Page styles do not reach into the element, or the element's styles leak out or lose to the page.
- The element must render on the server, then become interactive.

**Skip when** the element only displays content and takes no input: §1 does not apply; say "not applicable: reason".

## Steps

**Read the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Form participation: `formAssociated`, `setFormValue`, validity, reset, disabled, restore, attribute against property | the element holds a value that a form must submit or validate | [`01-form-participation.md`](./references/01-form-participation.md) |
| 2 | Default semantics, labels, focus, custom states, event retargeting and `composed` | the element is interactive, or events cross the shadow edge | [`02-semantics-focus-events.md`](./references/02-semantics-focus-events.md) |
| 3 | Styling hooks across the boundary, declarative shadow DOM, hydration, testing | styles must cross the boundary, or the element is server-rendered | [`03-styling-and-server-render.md`](./references/03-styling-and-server-render.md) |

## Output / checkpoint
An element is done when: a native `<form>` with it inside submits the expected pair, resets, disables with its fieldset and reports invalid through the form's own validation (§1); with the keyboard alone and a screen reader it is reachable, named, and announces its state (§2); an outer listener receives the event with a target that names the host (§2); and, if server-rendered, the page is readable and the markup is stable before any script runs (§3). No checkpoint is written: a craft block, 🟡, nothing here was run in a browser by us.

## Guardrails
- Make the element form-associated and give the form its value through the element's internals (§1.1). Never mirror the value into a hidden light-DOM input as a workaround that duplicates validation and reset.
- Set default role, label and state through the internals, and let the page override them with attributes (§2.1). Never leave a clickable box with no role, no name and no tab stop.
- Dispatch events from the host and state `bubbles` and `composed` on purpose (§2.4). Never rely on a retargeted `event.target` to find the inner node.
- Expose styling through custom properties and named parts (§3.1). Never ask page authors to reach into a shadow root, and do not reopen a closed root to allow it.
- Treat server-rendered markup as the first paint and the class as an upgrade (§3.3). Never read layout or the DOM of children in a constructor that can run on the server.
- Facts about specifications are for the date in `references/origin.md`; re-read before relying.

## Origin
Rewritten from the WHATWG HTML and DOM standards (CC BY 4.0) read 2026-10-20, plus own craft knowledge; no text copied. Details and gaps in [`references/origin.md`](./references/origin.md).
