# webperf-measurement-and-budget-pitfalls §2 — Collecting vitals with the web-vitals library

Real-user monitoring looks like a few lines of code and fails in the lifecycle: values that arrive twice,
that never arrive, or that arrive as something the backend adds up wrongly.

## 2.1 Use the library, and know its lifecycle
1. **Use `web-vitals` and not hand-written observers.** The Web Quality Skills RUM guide says the library follows
   the metric lifecycle and browser edge cases that Google's tools use; the `web-vitals` README says it is built
   to match how Chrome measures and reports to the Chrome UX Report and PageSpeed Insights.
2. **A callback may never fire.** INP is not reported when the user never interacts with the page; CLS, FCP and
   LCP are not reported for a page that loaded in the background (README). Own reasoning: a dashboard that expects one row
   per page view and metric will be short, and that is not a bug.
3. **A callback may fire more than once.** CLS and INP should be reported whenever the page's visibility state
   becomes hidden, and every metric is reported again after a restore from the back-forward cache (README).
   A restore creates a new metric object with a new `id`, because it counts as a separate page visit.
4. **Call each `onX` once per page load.** Each call creates a `PerformanceObserver` and registers listeners
   for the life of the page; the README warns that calling them repeatedly can increase memory. In a single-page
   app, register at startup, not per route.
5. **`reportAllChanges` is for debugging.** It reports when the metric changes, not on every input to it, and
   the README says it is not needed or recommended for production measurement. The RUM guide agrees that it makes
   noisy telemetry.
6. **The attribution build only when the fields will be read.** `web-vitals/attribution` is about 1.5 kB larger
   (brotli) than the standard build and adds diagnostic fields such as the element most associated with the
   metric; the README says to use it only if you use those features. The RUM guide adds that the extra fields
   should be reviewed and sent only as explicit, low-cardinality values.
7. **The library may be loaded late.** It uses `buffered` observers, so entries from before it loaded are
   still seen, and the README says it should be deferred until after the code that affects users.

## 2.2 Sending the values
1. **Send `delta` together with `id` when the backend adds values up.** Some analytics providers allow a value to
   be overwritten by a later one with the same `id`; others do not, and then the total is the sum of the deltas
   with that `id`. On the first call `value` and `delta` are equal.
2. **Use `navigator.sendBeacon()`**, which is widely available and works while the page unloads (README). The
   RUM guide's sample falls back to `fetch` with `keepalive: true` when the beacon call returns false.
3. **Batch by queue, flush when hidden.** The README's batching example keeps a queue of reported metrics
   and flushes it when `visibilityState` becomes `hidden`; it cannot wait for all three to be ready, since not
   every metric is reported on every page. It recommends `visibilitychange` over `beforeunload` and `unload`.

## 2.3 Soft navigations, iframes and browser support
1. **Soft navigations are opt-in and change the first load.** With `reportSoftNavs: true`, a soft navigation is
   a user interaction, a URL change and a paint, and the README says this is supported in Chromium from version
   151. The metrics for the initial URL are finalised when the first soft navigation happens, which locks in CLS and
   INP. TTFB is reported as 0, and INP and CLS restart for each soft navigation. To measure both ways,
   register two callbacks. This is `web-vitals` 6.2.3 behaviour.
2. **Use `navigationURL` and `navigationType`.** Metrics may be reported after the page has moved on, so the URL
   the metric belongs to is on the metric, and `soft-navigation` separates those loads from full ones.
3. **Observers cannot see into iframes**, not even same-origin ones, so a page with iframes will differ from the
   Chrome UX Report, and `onCLS()` then measures the document's own layout shift (README).
4. **Browser support differs by metric.** In 6.2.3 `onCLS()` is Chromium only and the soft-navigation Core
   Web Vitals need Chromium 151 or later; the others run in Chromium, Firefox and Safari. Own reasoning: expect
   no CLS rows from browsers outside that list.

## 2.4 What the payload carries
1. **Send what lets a regression be attributed and nothing that identifies a person.** The RUM guide's list: the
   metric name, value, rating, id, navigation type, a path and a release identifier. Do not include query
   strings, user-entered text or DOM fragments. Group by the route template and not the concrete URL, so the
   buckets stay few.
2. **Record a release or experiment identifier**, so a regression can be tied to a change, and **record the
   sampling rate**; cohorts collected under different rates must not be compared as equal.
3. **Retain form factor and navigation type**, with coarse connection context, when the privacy model allows it
   (the same guide).
4. **Consent and regional privacy requirements go through the site's existing policy.** The guide says to reuse
   an existing analytics pipeline where possible, and to propose and agree a new endpoint, vendor, cookie or
   consent behaviour before adding it. Whether a vitals beacon needs consent is a legal question and is not answered here.
