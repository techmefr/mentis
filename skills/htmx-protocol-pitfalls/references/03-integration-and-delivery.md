# htmx-protocol-pitfalls §3 — Integration and delivery

Applies to htmx 2.0.x. htmx initialises what is in the DOM when it swaps; anything that creates content or
reads it later has to cooperate. Delivery adds three more places where fragments and pages get confused: caches,
history and other origins.

## 3.1 Widgets and content created by other code
1. **Initialise third-party widgets with `htmx.onLoad`,** which receives the newly loaded content, and select
   inside that content only. A one-time `DOMContentLoaded` initialiser misses every swapped-in element.
2. **Call `htmx.process(element)` after any code inserts HTML that carries htmx attributes.** Content set with
   `innerHTML` after a `fetch`, or content that appears from a template, is not wired until it is processed.
3. **Templates need it too.** A framework that renders from a `template` element (Alpine's `x-if` is the
   documented case) puts nothing in the DOM until it is shown; call `htmx.process` on the revealed element, for
   example from a watcher on the flag that reveals it.
4. **Clean third-party mutations before a history snapshot.** A widget that rewrites the DOM (a rich select) is
   saved into the history cache in its rewritten state and then re-initialised on restore. Undo it in a handler
   for the `htmx:beforeHistorySave` event, by calling the widget's destroy method.

## 3.2 History
1. **Pushing a URL promises a full page at that URL.** On a history cache miss, htmx requests the URL again with
   the `HX-History-Restore-Request` header and expects the whole page back, because users also open the URL
   directly or paste it.
2. **Set `htmx.config.historyRestoreAsHxRequest` to `false`** (the default is `true`). Otherwise that full-page
   request also carries `HX-Request: true`, and a server that returns a fragment whenever it sees that header
   answers the restore with a fragment.
3. **`htmx.config.refreshOnHistoryMiss`** turns a cache miss into a hard browser refresh instead.

## 3.3 Caching
1. **Same URL, two bodies: send `Vary: HX-Request`.** A server that returns the full page without the header and
   a fragment with it must say so, or a cache keyed on the URL serves the fragment as a page (or the reverse).
2. **Different bodies need different validators.** If you use `ETag`, generate a different one for each variant.
3. **No `Vary`? Use the cache-buster.** `htmx.config.getCacheBusterParam = true` adds a parameter to the GET
   requests htmx makes, so htmx and non-htmx responses stop sharing a cache slot.
4. **`Last-Modified` works as usual** and has the same variant problem.

## 3.4 Cross-origin and delivery
1. **Expose the htmx response headers across origins.** The browser hides response headers on a cross-origin
   request unless the server lists them in `Access-Control-Expose-Headers`; request headers htmx sends must be
   allowed with `Access-Control-Allow-Headers`. Without both, `HX-Redirect` and `HX-Trigger` never reach the page.
2. **Pin the script.** The documentation's own install snippets name an exact version and carry an `integrity`
   hash with `crossorigin`; use that form, so an upstream change cannot alter the page. An unpinned URL is the
   same supply-chain exposure as any floating script.
3. **Default error responses are not swapped.** 4xx and 5xx responses are treated as errors and ignored,
   204 is not swapped, and other 2xx and 3xx are. A validation framework that answers 422 needs a `responseHandling` entry (or
   the response-targets extension) for the body to appear.

## Verification
- Swap in content that contains a widget and confirm it is initialised (§3).
- Open a pushed URL in a fresh tab and confirm a full page; press back after navigating and confirm the same
  after a cache miss (§3).
- Request the same URL with and without `HX-Request` through the real cache or CDN and confirm each gets its
  own body (§3).
