---
name: maps-and-geo-component-pitfalls
description: "Use when an interactive map or geo component is designed, written or reviewed in a web or mobile application, whatever the map library: marker clustering and large point sets, tile providers and their attribution and usage terms as a checklist, geocoding and autocomplete limits, caching and consent, device location permission and privacy, coordinate and bounds mistakes, a non-map accessibility alternative, performance and the tests that catch them. Method only; not legal advice."
---

# maps-and-geo-component-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the map every store locator, delivery view and field-service screen
grows. The premise: **a map is a view over places plus a pile of third-party terms, and every defect comes from one
of the two**: ten thousand markers that freeze the tab, a tile layer used outside its terms, a geocoding call per
keystroke that burns a quota, a location prompt on page load that gets denied for good, coordinates swapped so every
pin lands in the sea, a map that a keyboard or screen-reader user cannot use at all. List and table states follow
`data-table-ui-pitfalls`; search and filter behaviour is in `filters-search-and-saved-views-pitfalls`; address forms
are in `international-input-pitfalls`; accessibility in general is in `accessibility`; mobile permission prompts are
in `flutter-conventions`; performance measurement is `webperf`.

## When
- A map, store locator, address autocomplete, route or area view, or a "use my location" control is built or changed.
- A user reports "it is slow with many points", "pins are in the wrong place", "the map is blank", "I cannot reach it by keyboard".
- A provider, key, quota or terms change, or a new data layer, is introduced.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Data model and coordinates, clustering, tiles and attribution as a checklist, geocoding limits and caching, consent and location privacy | the data, the layers, the provider calls or the location features are written | [`01-data-clustering-providers-privacy.md`](./references/01-data-clustering-providers-privacy.md) |
| 2 | States, interaction, accessibility alternative, performance, tests, framework pointers | the component UI, its accessibility or its tests are written | [`02-states-access-performance-tests.md`](./references/02-states-access-performance-tests.md) |

## Output / checkpoint
A change is done when: coordinates have one stored order and datum; large sets are clustered or served by viewport
instead of drawn whole; the tile source's attribution and usage terms were read and met for this use; geocoding is
debounced, cached where the terms allow and limited; location is requested only on a user action, with a declared
purpose, and works when denied; the same information is reachable without the map; and the tests in §2.6 exist. No
checkpoint is written: a craft block, 🟡, nothing here was run against a provider.

## Guardrails
- Fix one coordinate order and datum across storage, API and library (§1.1). Never let latitude and longitude swap between layers.
- Cluster or load by viewport beyond a few hundred points (§1.2). Never add every marker to the map at once.
- Read the tile and geocoding provider's terms for this exact use, and show the required attribution (§1.3, §1.4). Never point at a free public tile server for production traffic or bulk use without its permission.
- Ask for device location only on a user action, and keep the feature working without it (§1.6). Never prompt on load or store a precise position without need.
- Give every map task a non-map path: a list, a table, a text address (§2.3). Never make the map the only way to do something.
- Facts about a provider or library are for the date stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with points checked on 2026-10-20 against RFC 7946 (GeoJSON), the OpenStreetMap Foundation tile usage policy and the W3C Geolocation specification (facts only, credited). Every other point stays unsourced. Details in
[`references/origin.md`](./references/origin.md).
