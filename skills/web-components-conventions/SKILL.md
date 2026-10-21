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
   supports them: the decorators page recommends the experimental form for production today, with `experimentalDecorators`
   and `useDefineForClassFields: false` (required from target ES2022), and says the standard form needs `accessor`
   fields and, on Babel, the `2023-05` decorator version.
4. **The default change test is strict inequality.** Mutating an object or array in place triggers nothing: assign a
   new value, or call `requestUpdate()`. A custom `hasChanged` is for a real equality need.

### 2. Update cycle
1. **`render()` is pure**: properties in, template out; no state change, no side effect, no read of anything else. The
   lifecycle page says a property change in `render()` does not schedule another update and that Lit runs it on the
   server; the purity rule itself is the block's own.
2. **Derived values are computed in `willUpdate()`**; changing a property up to and including `render()` does not
   schedule a new update. Changing one in `updated()` does, so a write there needs a stated reason.
3. **DOM measurement and imperative work go in `updated()` or `firstUpdated()`**; reach shadow nodes through the
   render root or a query decorator, not through document-wide selectors.
4. **Updates are asynchronous and batched**: several property writes give one render. Await `updateComplete` before
   reading the DOM or dispatching an event that depends on the new render.

### 3. Events and listeners
1. **Dispatch events in response to user interaction or an asynchronous change, not because the owner set a
   property.** Name events in lowercase (own convention: the events page uses lowercase, hyphenated names without making it a rule);
   an event leaves a shadow root only with `composed: true`, and reaches every ancestor only when `bubbles: true` is
   set too, so set them deliberately.
2. **Listeners on `window`, `document` or other outside targets are added in `connectedCallback` and removed in
   `disconnectedCallback`.** Listeners declared in the element's own template (`@click`) are added when it renders; that they need no removal is the
   block's own reading, as the events page does not say it.

### 4. Shadow DOM and styles
1. **Children reach a named slot only with a matching `slot` attribute**; fallback content shows only when nothing is
   assigned.
2. **Style the host with `:host`** so the defaults stay overridable from outside; expose theming through custom
   properties rather than by piercing the shadow root.
3. **`unsafeCSS`, `unsafeHTML` and `unsafeSVG` take trusted input only.** Query-string and user-supplied values are
   never passed to them: the directives page names cross-site scripting, CSS injection and data exfiltration (it uses
   `innerHTML`), and the styles page shows injected CSS loading an image from a third party. The same page says only
   template-literal strings are parsed as HTML; "ordinary expressions are escaped" is an inference from that, not a
   statement.

### 5. Templates and lists
1. **A child expression renders primitives, templates, nodes and arrays; `''`, `null`, `undefined` and `nothing`
   render nothing.** An attribute that must be absent when a value is missing uses `nothing`, otherwise the attribute is
   rendered with an empty string (the expressions page says `null` and `undefined` in an attribute give an empty
   string, not a removal), so `src` goes out empty and the browser requests the page itself; `ifDefined(value)` is
   shorthand for `value ?? nothing`. A boolean in a child position renders as the text `true` or `false`.
2. **Plain `map` is enough for lists**; use `repeat` with a key when updating a DOM node costs more than moving it, or
   when nodes hold state no expression controls (a checkbox's checked state): on a reorder `map` reassigns values in
   place, so the labels move and the checked state stays behind (lists page). The key must be unique per item.

### 6. Server rendering
1. **Only part of the lifecycle runs on the server**: the constructor, `hasChanged`, `willUpdate` and `render` do;
   `connectedCallback`, `disconnectedCallback`, `attributeChangedCallback`, `shouldUpdate`, `update`, `firstUpdated` and
   `updated` do not (SSR authoring page; the lifecycle page agrees for `willUpdate`, `updated` and `firstUpdated`). Browser
   APIs belong in client-only callbacks such as `updated()`, never in the constructor, `willUpdate()` or `render()`.
   The same page says these restrictions may change while Lit SSR is in Lit Labs.
2. **A module with browser-API side effects at import breaks a server import**: move the effect into a client-only
   callback or condition it.
3. **Do not bundle `lit` into a published package.** The publishing page gives the reason: a bundled copy can put
   several versions of Lit into one application, which npm cannot deduplicate, and pre-optimising blocks the
   application's own optimisation; the SSR page also warns against inlining it and suggests conditional exports with a
   `"node"` entry. Leave `lit` a normal dependency (own wording: mark it external in the build).

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

**Re-verified 2026-10-20 (🟡, nothing run).** Licence read on 2026-10-20: the `lit/lit` repository is **BSD-3-Clause**
("The Lit Project Contributors"), which is outside the permitted licences of `CONVENTIONS.md`; so on this pass the
lit.dev pages were read as official product documentation, for facts only, with nothing copied, and the repository was
not opened for text. Pages read (lit 3.3.3 is the latest release): reactive properties, lifecycle, events, shadow DOM,
styles, template expressions, lists, built-in directives, decorators, SSR authoring, publishing. **Confirmed:** 1.1 to
1.4, 2.2 to 2.4, 3.2 (window and document listeners), 4.1 to 4.2, 5.1 (what renders nothing). **Corrected:** the
`src="undefined"` symptom (an empty string), the list of lifecycle callbacks that run on the server, the `repeat`
criterion, and the unsafe directives (now three). **Marked as the block's own:** `render()` purity, lowercase event
names, no removal for template listeners, escaping by default. **Still unverified:** the directive set beyond those
named, reactive controllers, context, tasks, localisation, the raw custom-elements specification, and the SSR toolchain
(still Lit Labs).
