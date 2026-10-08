# solid-ownership-pitfalls §2 — Stores, server rendering, DOM attributes

Rules where data from outside meets Solid's reactive graph, or where Solid's attribute handling differs from
what the markup suggests.

## 2.1 Stores
1. **Use `reconcile` when replacing store data with server data.** Assigning the new array or object makes
   every subscriber update. `reconcile` diffs the new data against the old and updates only what changed.
   Use it for responses, polling and socket messages.
2. **A function stored as a value needs a wrapper.** `setStore("callback", fn)` treats `fn` as an updater and
   calls it, so the function is not stored. Write `setStore("callback", () => fn)`. When the function's identity
   is the main state rather than one field in a bigger store, a signal or a plain object is the better home.
3. **Take a plain snapshot before handing store data to something that clones it.** IndexedDB's structured clone
   rejects reactive proxies, and a shallow spread of the outer object is not enough when a nested array or object
   is still a proxy. Convert the whole payload to plain data, copy nested structures deliberately, and test
   the write and read in a real browser. `unwrap` gives a snapshot without the reactive wrapper.

## 2.2 Server rendering
1. **Reactive state created at module scope is shared across requests.** On the server, one user's signal or
   store is then visible in another user's response. Create it inside a component or a provider, or in a
   function that returns it.
2. **Module-level state is fine when it is client-only and intended.** Wrap it in `createRoot`, which documents
   the intent and gives the state an owner.
3. **Browser globals do not exist in server functions.** A server function runs only on the server, so reading
   `window`, `document` or `localStorage` throws; pass the client state in as an argument instead.

## 2.3 Enumerated attributes
1. **Booleans do not mean the same on enumerated attributes.** Solid removes an attribute whose value is
   `false` and writes an empty string for `true`. For `draggable`, `spellcheck`, `contenteditable` and
   `translate` the absent attribute is the inherited or default state, not "off".
2. **ARIA state attributes are tristate.** `aria-checked`, `aria-expanded`, `aria-hidden`, `aria-pressed` and
   `aria-selected` default to "undefined" when absent, which assistive technology treats differently from an
   explicit false. `aria-expanded={isOpen()}` therefore removes the attribute while closed. Pass the string
   token: `aria-expanded={open() ? "true" : "false"}`, `draggable="false"`, `translate="no"`.
3. **Attributes that default to false are safe.** `contenteditable={true}` writes the empty string, which is
   the true state, and `aria-disabled` can be omitted for false.
4. **This holds in 1.x** as well as in the 2.0 candidate; the behaviour of the attribute handling is the same.
   More on accessible semantics is in `accessibility`.

## 2.4 innerHTML and custom elements
1. **`innerHTML` is an injection point.** Any unsanitised value rendered through it can run script, including
   data that came from your own server. Use JSX or text content; if markup is unavoidable, sanitise it first
   (see `security-hardening`).
2. **Use `prop:` for properties of custom elements.** Normal JSX attributes are written as HTML attributes, so
   arrays and objects become strings. `prop:` writes a DOM property and is client-only; it produces no
   server-render output.
3. **Listen with `on:` for custom events** on custom elements, as in `on:wc-change={handler}`, where the event
   name keeps its own spelling.

## Verification
- Request a server-rendered page twice, with different users, and confirm no state from the first appears
  (§2).
- Inspect the rendered DOM for each ARIA state: the attribute must be present with the string value (§2).
- Feed the store from a response twice with identical data and confirm subscribers did not re-run (§2).
