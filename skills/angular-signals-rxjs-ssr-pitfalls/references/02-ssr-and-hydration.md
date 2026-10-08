# angular-signals-rxjs-ssr-pitfalls §2 — SSR and hydration

Server rendering gives a different runtime (no `window`, no `document` of your own, a render that must finish
before it is serialised) and hydration adds a contract: the DOM the browser receives must be the DOM the client
code expects. Each rule says what you see when it is broken.

## 2.1 Render mode per route
1. **Pick the mode route by route.** Server routes configure `RenderMode.Server` (rendered per request),
   `RenderMode.Client` (rendered in the browser, the default behaviour of an Angular app) or
   `RenderMode.Prerender` (static HTML at build time).
2. **Prerender only what is the same for every user.** Prerendering needs all the data at build time, so a
   prerendered page cannot carry data for the user loading it. A per-user or authenticated page is `Server` or
   `Client`.
3. **Prerendered code cannot lean on browser APIs.** It also limits the libraries you can use to ones that
   do not assume a browser.
4. **`getPrerenderParams` runs at build time.** It must not rely on browser or server APIs for its data, and
   `inject` is only valid synchronously inside it, never after an `await`. A large parameter set means many
   HTML files and slower deployments.
5. **Prerendered redirects are soft redirects.** They are written as a meta refresh tag in the generated HTML,
   not as an HTTP status.

## 2.2 Hydration setup
1. **Hydration is for server-rendered apps only.** Without it, the browser destroys and re-renders the DOM,
   which shows as a flicker and can hurt layout shift and largest contentful paint.
2. **`provideClientHydration()` must also be in the server bootstrap providers.** Adding it only to the browser
   bootstrap leaves the server unaware; with a generated project the root config usually covers both, a custom
   setup does not.
3. **Confirm it in dev mode.** The browser console prints hydration statistics; the framework's dev tools can
   overlay which parts hydrated and highlight the component behind a mismatch error.
4. **Event replay keeps early clicks.** Between the first paint and hydration the page looks interactive but has
   no listeners. Event replay records native events in that window and replays them afterwards. It is enabled
   along with incremental hydration; if you opt out of incremental hydration, add `withEventReplay()` yourself.
5. **Server and client must produce the same DOM.** That includes the whitespace and comment nodes the
   framework emits. The server HTML must not be altered between the server and the client.

## 2.3 What breaks hydration
1. **Direct DOM manipulation.** Native DOM calls, `innerHTML` or `outerHTML` writes, `appendChild`, moving or
   detaching nodes: the framework does not know about them and finds a different tree. Refactor to framework
   APIs.
2. **Invalid HTML structure.** A `table` without a `tbody`, a `div` inside a `p`, an `a` inside an `a`. Browsers
   repair these differently from the server output. Always write the `tbody`.
3. **`preserveWhitespaces: true`.** It is not a fully supported configuration with hydration. If it is set at
   all, set it consistently for the server and browser builds.
4. **Third-party scripts and libraries that rewrite the DOM** (ad tags, analytics, chart libraries). Defer the
   script until after hydration with `afterNextRender`; for a component that renders through such a library,
   `ngSkipHydration` is the workaround.
5. **i18n blocks are skipped by default.** The component re-renders from scratch; add `withI18nSupport()` to
   hydrate them.
6. **`ngSkipHydration` is a last resort.** It works only on a component host node (elsewhere it throws), makes
   that component and its children behave as if hydration were off, and on the root component disables
   hydration for the whole app. A component that breaks hydration is a bug to fix, not to annotate.
7. **Slow stability delays hydration.** Hydration and post-hydration cleanup wait for the app to report stable.
   Open timeouts, intervals, unresolved promises and pending microtasks delay it, and after 10 seconds the app
   reports NG0506. `provideStabilityDebugging()` logs the pending tasks; it is a temporary debugging aid, not
   something to ship.

## 2.4 Browser-only code and consistent rendering
1. **Do not touch `window`, `document`, `navigator` or `location` during server render.** Run browser-only
   work in `afterNextRender` or `afterEveryRender`, which are skipped on the server.
2. **Read the document through the `DOCUMENT` token,** not the global.
3. **Prefer platform-specific providers over `isPlatformBrowser` / `isPlatformServer` checks.**
4. **Never branch the rendered content on the platform in a template** (an `@if` on `isPlatformBrowser`). The
   server and the client then render different content, which causes mismatches and layout shift. Render the
   same content on both and do the browser-specific setup in `afterNextRender`.

## 2.5 HTTP transfer cache
1. **The server's HTTP responses are serialised into the page and reused once.** The browser's `HttpClient` finds
   them in the cache during the initial render instead of repeating the request, and stops using the cache
   once the app is stable.
2. **Some requests are never cached,** so they are fetched twice, once per side: requests carrying
   `Authorization`, `Proxy-Authorization` or `Cookie` headers, requests sent with credentials, requests or
   responses with `Cache-Control` of `no-store`, `no-cache` or `private`, and responses with `Set-Cookie`. Only
   `GET` and `HEAD` are cached by default. A doubled authenticated request is expected, not a bug in the cache.
3. **Different server and browser origins need a map.** Provide `HTTP_TRANSFER_CACHE_ORIGIN_MAP` so the two
   URLs are recognised as the same request.
4. **Tune it in `provideClientHydration`.** `withHttpTransferCacheOptions` filters or adds headers,
   `withNoHttpTransferCache` turns it off, and a request can opt out with `transferCache: false`.

## Verification
- Load the page with JavaScript throttled and click before hydration; the click must still take effect (§2).
- Read the browser console on load: no mismatch error, and the network panel shows one request per call that
  the cache is allowed to serve (§2).
- View the page source: prerendered pages contain no per-user data (§2).
