---
name: web-components-lifecycle-pitfalls
description: "Use when writing or reviewing a native custom element (a class extending HTMLElement): what the constructor may and may not touch, where the shadow root is attached, why attributeChangedCallback and connectedCallback must not walk children, listener teardown in disconnectedCallback, observedAttributes, guarding customElements.define against a second registration, defining after the class, valid tag names, customized built-in elements, closed shadow roots, classes added to the host itself, and methods prefixed with on."
---

# web-components-lifecycle-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the native custom-element mistakes that work when the element is
created from script and break when the parser or an upgrade creates it. The sections share one premise: **a
custom element can be constructed before it has attributes, children or a parent, and its callbacks can run in
an order you did not write**. Each rule says what you see when it is missed.

Applies to elements written directly against the platform; a library that wraps the class (such as a template
library) hides parts of this, so check what the wrapper already does before adding a guard.

Standalone block, written because the broader web-components conventions block exists only on an unmerged
branch. It is meant to be merged into the same-named framework block when that lands (see
[`references/origin.md`](./references/origin.md)). Until then it cites only blocks present on the main branch.

## When
- Writing or reviewing a class that extends `HTMLElement`.
- An element works when created with `createElement` and breaks when written in HTML, or the other way round.
- A page throws when a script is loaded twice, or a component library and an app both register a tag.
- An element reads its children or attributes at the wrong time and sees nothing.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Constructor and lifecycle callbacks: what to touch, in which callback, teardown | a callback reads attributes or children, or a listener is added | [`01-constructor-and-callbacks.md`](./references/01-constructor-and-callbacks.md) |
| 2 | Registration and public surface: define guards, names, built-ins, shadow mode, host classes, `on` methods | an element is registered, named or given a public API | [`02-registration-and-surface.md`](./references/02-registration-and-surface.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the element was created three ways (parsed from HTML that
already contains it, created with `createElement` then given attributes and appended, and defined after the
markup was already in the page) and behaved the same each time (§1), the script was loaded twice and nothing
threw (§2), the element was removed and re-added and its listeners were neither doubled nor left behind (§1).
An element only tried with `createElement` is not verified.

## Guardrails
- Never read or write attributes or children of the host in the constructor (§1).
- Never traverse children in `attributeChangedCallback` or `connectedCallback` and treat the result as final (§1).
- Never call `customElements.define` without checking the name is free (§2).
- Never extend a built-in element class to customise it if Safari is a target (§2).
- Never name a method `on<something>` unless it is the event-handler property (§2).
- Accessibility of the element (roles, focus, labels) belongs to `accessibility`.

## Origin
Rewritten from the WHATWG HTML standard's custom-elements chapter, the MDN custom-elements guide and the
eslint-plugin-wc rule documentation (MIT), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
