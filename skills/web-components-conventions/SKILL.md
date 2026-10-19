---
name: web-components-conventions
description: "Use when writing or reviewing custom elements with Lit 3: public reactive properties versus internal state, the update cycle and where side effects belong, events and listeners with cleanup, shadow DOM slots and styles, pure render methods, template escaping, and what breaks under server rendering."
paths: "**/*.ts, **/*.js"
---

# web-components-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for custom elements written with Lit. **Status: a base to confront with real
work**, no in-house project behind it yet (same status as `go-conventions`). Pinned to Lit 3 (documentation read
2026-10-02; registry latest that day: lit 3.3.3). The raw custom-elements specification beyond what Lit exposes, and
the design-system packaging around components, are not covered.

## When
As soon as a file defining a custom element, a Lit template or a reactive property is written or modified, during
`code` (6) and `review` (8).

## Steps

### 1. Properties and state
1. **A public reactive property is an input; internal reactive state is declared as state.** Inputs may be set from
   markup or by the owner; state is private to the element and never an attribute.
2. **The `type` option of a property drives attribute conversion, not type checking.** Typing is the compiler's job.
3. **Class fields can overwrite the reactive accessor.** With plain JavaScript fields, or TypeScript compiling to
   define semantics, a declared field shadows the property: initialise in the constructor, use `declare` or the
   `accessor` keyword, or turn off define semantics in the compiler options. Decorators need a compiler that
   supports them.
4. **The default change test is strict inequality.** Mutating an object or array in place triggers nothing: assign a
   new value, or call `requestUpdate()`. A custom `hasChanged` is for a real equality need.

### 2. Update cycle
1. **`render()` is pure**: properties in, template out; no state change, no side effect, no read of anything else.
2. **Derived values are computed in `willUpdate()`**; changing a property up to and including `render()` does not
   schedule a new update. Changing one in `updated()` does, so a write there needs a stated reason.
3. **DOM measurement and imperative work go in `updated()` or `firstUpdated()`**; reach shadow nodes through the
   render root or a query decorator, not through document-wide selectors.
4. **Updates are asynchronous and batched**: several property writes give one render. Await `updateComplete` before
   reading the DOM or dispatching an event that depends on the new render.

### 3. Events and listeners
1. **Dispatch events in response to user interaction or an asynchronous change, not because the owner set a
   property.** Event names are lowercase; make an event cross shadow boundaries only deliberately.
2. **Listeners on `window`, `document` or other outside targets are added in `connectedCallback` and removed in
   `disconnectedCallback`.** Listeners on the element's own template need no removal.

### 4. Shadow DOM and styles
1. **Children reach a named slot only with a matching `slot` attribute**; fallback content shows only when nothing is
   assigned.
2. **Style the host with `:host`** so the defaults stay overridable from outside; expose theming through custom
   properties rather than by piercing the shadow root.
3. **`unsafeCSS` and `unsafeHTML` take trusted input only.** Query-string and user-supplied values are never passed
   to them (cross-site scripting); ordinary expressions are escaped.

### 5. Templates and lists
1. **A child expression renders primitives, templates, nodes and arrays; `''`, `null`, `undefined` and `nothing`
   render nothing.** An attribute that must be absent when a value is missing uses `nothing`, otherwise an invalid
   request (`src="undefined"`) is sent.
2. **Plain `map` is enough for lists**; use `repeat` with a key only for large lists that reorder or change by
   single entries.

### 6. Server rendering
1. **Only part of the lifecycle runs on the server**; `connectedCallback`, `disconnectedCallback` and `shouldUpdate`
   do not. Browser APIs belong in client-only callbacks such as `updated()`, never in the constructor or `render()`.
2. **A module with browser-API side effects at import breaks a server import**: move the effect into a client-only
   callback or condition it.
3. **Do not bundle `lit` into a published package**; mark it external so the Node and browser builds each resolve
   the right export.

## Output / checkpoint
Elements whose inputs, state, events and slots are listed, with no side effect in `render()`. No dedicated
checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add <package>`
(`CONVENTIONS.md`). Never untrusted input into `unsafeHTML` or `unsafeCSS`. Never a side effect in `render()`. A
rule with an API name is the pinned major's; read `package.json` before applying it to another.

## Mechanical checks

```
grep -rnE "unsafeHTML|unsafeCSS|unsafeSVG" src
grep -rnE "addEventListener\((['\"])(resize|scroll|keydown|keyup|message)" src
grep -rnE "removeEventListener" src
grep -rnE "document\.(querySelector|getElementById)" src
grep -rnE "@property\(\{ *type: *(Object|Array)" src
grep -rnE "(window|document|navigator|localStorage)\." src
```

- An outside `addEventListener` with no `removeEventListener` in the same file is rule 3.2.
- `document.querySelector` inside an element is rule 2.3.

## Origin
Rewritten from the official Lit documentation (the `lit/lit` repository, `packages/lit-dev-content`, v3 docs;
the repository code is BSD-3-Clause), read from a shallow clone on 2026-10-02: components (properties, lifecycle,
events, shadow DOM, styles, rendering), template expressions and lists, and the server-rendering authoring page.
Mechanisms are the library's; wording and grouping are ours; no text copied. **Facts that move, with their pin
(Lit 3):** decorator and accessor syntax, the lifecycle method set run on the server. **Not read, a stated gap:**
directives other than those named, reactive controllers, context, tasks, localization, testing, the server-rendering
toolchain, and the raw custom-elements specification. Refresh with `skills/source-freshness` on the next major.
Written 2026-10-02, never run on real work.
