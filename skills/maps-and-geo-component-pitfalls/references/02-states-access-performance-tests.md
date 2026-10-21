# maps-and-geo-component-pitfalls §2 — States, accessibility, performance and tests

Source: own craft knowledge, with one point checked on 2026-10-20 and, on a third pass the same day, WCAG 2.2 Understanding SC 2.5.1 and SC 2.1.2 (facts only, see origin.md). Unmarked points have no source.

## 2.1 States and interaction
1. **Render separately**: loading (tiles and data), loaded, empty (no places match), filtered empty (places exist, filters hide them), error with retry, offline, and location denied. Never show an empty map as "no results" when the request failed (`data-table-ui-pitfalls` §2.1, `onboarding-and-empty-state-pitfalls` §2.1).
2. **Filtered empty keeps the map and the filters**, says what is filtered and offers to clear or widen, and may zoom out to the nearest results when that is honest ("Nearest result is 40 km away").
3. **Symptom: the map jumps while the user is reading or dragging.** Cause: data refresh recentres or fits bounds on every update. Fit bounds on first load and on an explicit search, not on each refresh; never move the view under the user's hands.
4. **Scroll and gesture conflicts**: a full-width map captures page scroll, trapping the user. Offer two-finger or modifier-key panning on the page, or a clear "Interact" state, and keep an easy way past the map (`responsive-layout`). A multipoint gesture is not enough on its own: WCAG 2.2 SC 2.5.1 asks that anything done with a pinch, spread or other multipoint or path-based gesture also work with a single pointer, and gives plus and minus buttons for map zoom as the example; keyboard support alone does not satisfy it.
5. **Selection is one state shared by map, list and detail**: selecting a pin highlights its row and opens the detail; selecting a row pans to its pin. Two components with separate selection drift.
6. **Keep map state in the URL** (centre, zoom, filters, selected id) so back, reload and sharing work, with sensible rounding of the numbers; do not put a private position in a shareable link.
7. **Popups are short, focus-managed and dismissible**; a popup that hides the pin it describes, or cannot close on touch, is a defect. Prefer a side or bottom panel for rich content.
8. **Touch targets**: markers, clusters and map controls are large enough to hit on a phone, and not so densely packed that a tap picks the neighbour (`webperf`, `01-responsive-touch-interface`).
9. **Controls**: zoom, locate-me and layer toggles are real buttons with names; keep them out of the way of attribution.
10. **Do not rely on colour alone** for categories on pins (WCAG 2.2 SC 1.4.1, level A): add shape, label or icon (`accessibility`, `03-contrast-perception`).
11. **Remember the user's view and layer choice** per device where useful, as a convenience that can be reset (`settings-and-preferences-page-pitfalls`).

## 2.2 Content and data on the map
1. **Show what the pin means**: a legend or label for types, a clear selected style, and a distinct style for the user's own position.
2. **Cluster and label at readable sizes**: avoid label collisions with collision handling or by showing labels only at higher zoom.
3. **Opening hours, availability and prices shown on the map are time-bound**: show their freshness or compute them at request time, in the place's zone (§1.1).
4. **Do not expose private places**: a map of customers, staff or incident locations shows only what each viewer is permitted, enforced on the server per row and by precision (`field-and-row-permission-ui-api-pitfalls`).
5. **Sanitise popup content** from user-provided fields before putting it in HTML (`csp-and-sanitiser-pitfalls`). The Leaflet reference warns that a string given to a popup or tooltip is rendered as HTML, and says to sanitise untrusted input or pass an element whose text is set safely.

## 2.3 Accessibility: the non-map alternative
1. **A map canvas is mostly invisible to assistive technology and hard by keyboard.** Treat it as a supplementary view. Every task the map supports (find a place, see its details, get directions, choose a location) must have a path that does not need the map: a results list, a table, a text address field, a "get directions" link (`accessibility`).
2. **Make the list the primary structure** for screen-reader and keyboard users: sortable by distance where location is known, with each item's name, address, distance and a link to details, and the same filters as the map (`data-table-ui-pitfalls`).
3. **Keep the list and the map in sync, but independent**: operating the list never requires the map, and the map is not the only place a selection can be made.
4. **Offer a "list view" toggle visibly**, reachable before the map in tab order for users who need it, not hidden behind the map controls.
5. **Map controls are keyboard-operable** (and WCAG 2.1.2 asks that focus can leave the map with the keyboard alone; if the way out is not Tab, an arrow key or a standard exit such as Escape, say how to leave in text beside or inside it): pan, zoom and recentre by keys where the library supports it, visible focus, and a way to leave the map with Tab and Escape without a trap; check the library's own claims by testing, not by reading its page (`01-semantics-keyboard`).
6. **Give the map region an accessible name and a short description** of what it shows, and mark decorative tile layers as such; individual pins that matter are reachable or covered by the list.
7. **Announce meaningful changes politely**: "12 places found", "Showing results near Lyon", in one live region created at load, without moving focus (WCAG 2.2 SC 4.1.3 lists a results count as a status message; `in-app-notifications-pitfalls` §2.3).
8. **Pin popups and detail panels return focus** to the control that opened them on close, and are closable by Escape.
9. **Directions and locations also exist as text**: the written address, a copy button, and a link that opens the user's preferred maps app, for people who do not use the embedded map.
10. **Zoom and reflow**: the page works at high text zoom and narrow width without the map covering the controls (`responsive-layout`); avoid motion that cannot be reduced in fly-to animations (`web-animation-pitfalls`).
11. **Do not use a map where a sentence would do**: a single known address is a line of text and a link, not a full interactive map.

## 2.4 Performance
1. **Load the map library and styles only where needed**, as a lazy import after the first render, and only when the map area is near or in view (`webperf`, `vite-bundler-conventions`).
2. **Reserve the map's height** to avoid layout shift, and show a static placeholder or image while it loads (`cwv-diagnosis-pitfalls`).
3. **Limit what is drawn**: clustering or viewport queries (§1.2), simplified geometries (§1.1), canvas or vector rendering for big point sets, and few simultaneous layers.
4. **Debounce map-driven requests** on move end, cancel superseded ones, and cache by tile or bounds key within terms.
5. **Do not rebuild the map on each state change**: create the instance once, update layers and markers by diff, and destroy on unmount; leaked instances, listeners and workers are the usual memory growth in single-page apps (`web-components-lifecycle-pitfalls` for the lifecycle habit).
6. **Mind mobile cost**: lower pixel ratio or simpler styles on weak devices, battery cost of continuous location, and data cost of tiles on cellular.
7. **Measure with a real device and a realistic data size**, including the worst-case cluster at the highest zoom (`webperf-measurement-and-budget-pitfalls`).
8. **Static maps for static needs**: an email, a print sheet or a contact page can use a static image where the provider's terms allow it, instead of an interactive map.

## 2.5 Security and robustness
1. **Treat coordinates and addresses from users as untrusted input**: validate ranges and length, escape on output, and never build a provider query by concatenating raw text (`regex-validation-pitfalls`).
2. **Server-side checks decide access to place data**, not the map's filter on the client.
3. **Handle provider errors and quota exhaustion** with a user-facing fallback and an alert for you, not a silent grey map (`spend-guard-fail-closed`).
4. **Pin the library version** and re-read its changelog on upgrades; map libraries change defaults for gestures, projections and attribution controls (`package-manager-supply-chain-pitfalls`).

## 2.6 Tests
1. **Coordinate order**: round-trip a place with clearly different latitude and longitude through the form, API, database and library; assert it renders at the right spot.
2. **Range validation**: a geocode failure never stores (0, 0); out-of-range values are rejected.
3. **Clustering**: with a large synthetic set, assert the number of rendered features stays bounded, cluster counts equal the list count for the same filters, and a click zooms or opens the list.
4. **Viewport fetch**: pan quickly, assert superseded requests are cancelled and the final result matches the final bounds.
5. **Selection sync**: select by map and by list, assert one selected id everywhere and that the URL reflects it.
6. **Geocoding limits**: type quickly, assert debounced calls with a minimum length and the session token where applicable; assert a failure leaves the typed address usable.
7. **Attribution**: assert the required attribution text is present and visible at small widths and in dark mode.
8. **Location permission**: stub granted, denied and unavailable; assert no prompt on load, a working typed-address path when denied, and the denied-state message.
9. **Privacy**: assert positions are rounded or absent in logs and analytics events, and that a shared URL carries no private position.
10. **Accessibility**: assert the list alternative reaches every task, names on controls and the region, a polite announcement of result counts, focus return from popups and a keyboard-only pass that can leave the map; run an automated check (`playwright-e2e-pitfalls`, `testing-library-query-pitfalls`).
11. **Provider failure**: block tile and geocode requests, assert the list and the form still work with a visible message.
12. **Date line and edge cases**: bounds crossing the antimeridian (east value lower than west, §1.1.11) and a single-point result fit the view without error.
13. **Tile policy**: assert a production build sends an identifying User-Agent and a Referer, does not prefetch tiles for areas out of view, and keeps attribution visible (§1.3.2, §1.3.11).

## 2.7 Framework pointers (reference only)
1. **Web map libraries** (open-source engines for raster or vector tiles) differ in coordinate order, projection defaults, clustering support and keyboard behaviour; read the current documentation of the one you use before relying on any behaviour named here, and check its licence and the licence of its tile and data sources.
2. **React or Nuxt**: wrap the map in one client-only component with a stable instance created on mount and destroyed on unmount, pass data and selection as props, emit selection and bounds events, and render nothing on the server (`react-nextjs-conventions`, `nuxt-no-hydration-nondeterminism`, `data-fetching-state-conventions`).
3. **Laravel**: spatial columns and indexes depend on the database; store degrees in two typed columns or a native geography type, compute distance in the database, and keep provider keys server-side (`laravel-conventions`, `postgres-operations-and-exposed-api-pitfalls`, `mysql-pitfalls`).
4. **Vuetify or similar kits** provide list, dialog and button components for the alternative view; verify their focus and names against §2.3 (`vue-nuxt-vuetify-conventions`).
5. **Mobile**: native map widgets and location plugins have their own permission flows and background rules; see `flutter-conventions` and `android-security-hardening`.
