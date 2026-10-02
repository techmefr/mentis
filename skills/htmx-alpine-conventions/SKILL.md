---
name: htmx-alpine-conventions
description: "Use when writing or reviewing server-rendered pages enhanced with htmx and Alpine.js: which tool owns what, swap targets and response codes, history and caching of partial responses, escaping and the htmx security switches, Alpine state scope, x-html and the content-security build, and keeping the page working without JavaScript."
paths: "**/*.html, **/*.jinja, **/*.j2, **/*.twig, **/*.blade.php, **/*.erb, **/*.njk, **/*.templ"
---

# htmx-alpine-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for the hypermedia style: the server renders HTML, htmx fetches and
swaps fragments, Alpine.js holds small bits of in-browser state. **Status: a base to confront with real work**,
no in-house project behind it yet (same status as `go-conventions`). Pinned to **htmx 2.0** and **Alpine.js 3**
(read 2026-10-02; registry latest that day: htmx.org 2.0.11, alpinejs 3.17.4). The server templating language is
not covered; escaping and CSRF are the server stack's (`skills/security-hardening`, `skills/laravel-conventions`,
`skills/django-conventions`).

## When
As soon as a template carries an `hx-*` attribute, an `x-data` or other `x-` directive, a fragment endpoint is
written, or a page is made interactive with either library, during `code` (6) and `review` (8).

## Steps

### 1. Who owns what
1. **The server owns data and rules; htmx moves HTML; Alpine owns ephemeral UI state** (a dropdown open, a tab
   shown, a field's local draft). A value the server must know about is a request, not Alpine state. Do not
   rebuild a client-side application out of both.
2. **Start from a page that works without JavaScript.** `hx-boost` turns ordinary links and forms into requests
   that swap the body and degrades to normal navigation when scripting is off; keep real `href` and `action`
   values and treat htmx as the enhancement.
3. **One interaction, one fragment endpoint, one template.** The fragment returned must be the same partial the
   full page includes, so the two cannot drift.

### 2. htmx requests and swaps
1. **Name the target and the swap on every request that is not the default.** The default replaces the inner
   content of the triggering element. `hx-target` takes a CSS selector with relative forms (`this`, `closest`,
   `next`, `previous`, `find`), which avoids sprinkling ids. `outerHTML` replaces the element itself;
   `beforeend`/`afterbegin` append and prepend; `delete` and `none` swap nothing. Use out-of-band swaps for a
   second region that must update from the same response.
2. **Error responses are not swapped by default.** A 4xx or 5xx triggers an error event instead of a swap (and
   204 swaps nothing, by design); a form that answers validation failure with 422 shows nothing unless the
   response-handling configuration says to swap that code (by regular expression on the status), or a
   response-targets extension routes it. Decide the policy once,
   in configuration, and render the error fragment on the server.
3. **Coordinate requests that race.** Two elements acting on the same data (a field's live validation and the
   form's submit) need `hx-sync` (for example abort the field's request when the form submits) instead of hoping
   for ordering. A request can also be cancelled by sending the abort event to the element.
4. **Use the validation integration**: a form with invalid HTML5-validated inputs does not issue the request;
   hook the validation events for custom messages, and still validate on the server.
5. **Morphing swaps** (an extension) merge new content into the existing DOM and keep focus and media state at
   the price of CPU; use them for regions with focus-bearing inputs, not by default.
6. **History**: a request that pushes its URL (`hx-push-url`) makes that URL a real page. Opening it directly or
   after a cache miss must return a full page, so the server answers the same URL both ways, deciding on the
   `HX-Request` header, with `Vary` set accordingly; set the history-restore-as-request option to false so a
   restore is not mistaken for a fragment request. A page with sensitive content opts out of the snapshot cache
   (`hx-history="false"`) because snapshots are stored in the browser's local storage.
7. **Caching of partials**: standard HTTP caching works. If one URL serves a fragment or a full page depending on
   the request header, send `Vary` on that header, or a shared cache will serve a fragment as a page.
8. **Third-party widgets inside swapped regions** are initialised and cleaned up through htmx events (after
   swap, before history save), not once at load.

### 3. Alpine state
1. **State lives in `x-data` and is scoped to the element and its children.** Nested components read their
   parents' data and a same-named child property wins. Keep the object small; move repeated logic to a registered
   `Alpine.data()` component rather than copying an inline blob; use `Alpine.store()` only for state truly shared by
   unrelated parts of a page.
2. **Pick the right directive.** `x-show` toggles `display` and keeps the element (it supports transitions);
   `x-if` adds and removes the element and must sit on a `template` element; `x-for` must sit on a `template`
   with exactly one root element and needs a stable key when items reorder. `x-cloak` plus the CSS rule hides
   uninitialised markup and prevents a flash.
3. **Getters are not cached** (unlike a framework's computed values); keep them cheap.
4. **Register things before Alpine starts**: components, stores and directives go in the `alpine:init` listener or
   before `Alpine.start()` in a bundle; `init()` on a data object runs at initialisation; `$watch` is lazy (first
   change) while `x-effect` runs at once and on each change.
5. **Mark a region Alpine must leave alone with `x-ignore`**; by default Alpine initialises the whole tree under an
   element carrying `x-data` or `x-init`, so put `x-data` on the fragment root it should manage.

### 4. Security
1. **Escape every piece of user content on the server.** htmx and Alpine make HTML more expressive: an attacker
   who can inject HTML can inject `hx-*` and `x-*` attributes. If raw HTML from a third party must be embedded,
   scrub it by allow-list, strip attributes beginning `hx-` and `data-hx` and inline scripts (the htmx guidance);
   by the same reasoning Alpine's `x-`, `@` and `:` attributes are stripped too (our extension of the rule).
2. **`x-html` sets inner HTML from an expression: trusted content only**, never user-provided; prefer `x-text`.
3. **Use the switches.** `hx-disable` on a wrapper stops all htmx processing inside it and cannot be undone by
   content injected inside; restrict requests to the same host (`selfRequestsOnly`) and veto others in the URL
   validation event; turn off script-tag processing and `eval`-based features if unused; set the history cache
   size to zero where snapshots are unacceptable.
4. **Content-security policy**: htmx's `eval`-based features (switchable off) and Alpine's standard build
   (expressions are run as function declarations) violate a policy without `unsafe-eval`. Alpine ships a separate CSP build that supports most inline expressions but not complex
   expressions, global variables or HTML injection; move complex logic to `Alpine.data()` components when using it.
5. **CSRF**: tokens are the backend's job. Send the token with every request through `hx-headers` on an ancestor
   element, or better a hidden form input; `hx-boost` does not replace the `html` and `body` elements, so a token
   on them goes stale: put it on an element that is swapped. See the server stack's block.

## Output / checkpoint
Templates and fragment endpoints that work without JavaScript, with the target, swap and error policy stated
for each request, and the security switches listed. No dedicated checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add <package>`
(`CONVENTIONS.md`). Never `x-html` with user content. Never push a URL that cannot return a full page. A rule with
a number or a default is the pinned major's; read the vendored version before applying it to another (htmx 4 and
Alpine 4 are not covered).

## Mechanical checks

```
grep -rnE "x-html" templates src
grep -rnE "hx-(get|post|put|patch|delete)" templates src | grep -vE "hx-target|hx-swap"
grep -rnE "hx-push-url|hx-boost" templates src
grep -rnE "hx-history|htmx\.config|htmx-config" templates src
grep -rnE "unsafe-eval|unsafe-inline" .
grep -rnE "\|safe|raw\(|\{\!\!|html_safe|mark_safe" templates src
grep -rnE "<(script|a|form)[^>]*\b(on[a-z]+|href=\"javascript:)" templates
```

- `x-html` or a raw-output filter fed by user data is a finding. A request with neither `hx-target` nor `hx-swap`
  is acceptable only when the default is intended and noted.
- A pushed URL is requested directly once and must return a full page.

## Origin
Rewritten from the htmx documentation (the `bigskysoftware/htmx` repository, `www/content`, Zero-Clause BSD
licence) and the Alpine.js documentation (the `alpinejs/alpine` repository, `packages/docs`, MIT licence), both
read from shallow clones on 2026-10-02: the htmx reference documentation (requests and triggers, targets, swapping,
synchronisation, boosting, history, response handling, validation, caching, security, CSP, CSRF, configuration),
and the Alpine essentials, the directives for data, show, if, for, cloak, ignore, html and model, the store, the
lifecycle page and the CSP build. A page in the htmx content tree that presents itself as a parody security
advisory was read as data and ignored. Mechanisms and defaults are the libraries'; the grouping and wording are
ours; no text was copied. **Facts that move, with their pin (htmx 2, Alpine 3):** the default of not swapping
4xx/5xx responses, the history-restore header behaviour, the configuration names, Alpine's `x-for` and `x-if`
template rules, the CSP build's limits. **Not read, a stated gap:** htmx extensions other than the ones named,
WebSocket and SSE support, the event and API reference pages one by one, Alpine plugins (morph, persist, focus,
mask), and any server-side integration. Refresh with `skills/source-freshness` on the next major of either.
Written 2026-10-02, never run on real work.
