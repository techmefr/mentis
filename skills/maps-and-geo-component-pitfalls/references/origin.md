# maps-and-geo-component-pitfalls: origin and source stamps

> Provenance of `skills/maps-and-geo-component-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No map component was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| RFC 7946, The GeoJSON Format (rfc-editor.org/rfc/rfc7946), read 2026-10-20 | IETF RFC, facts only, own words | coordinate order, WGS 84, antimeridian cutting, precision, crossing bbox (§1.1.1, §1.1.2, §1.1.4, §1.1.6, §1.1.11) |
| OpenStreetMap Foundation, Tile Usage Policy (operations.osmfoundation.org/policies/tiles/), read 2026-10-20 | page states no licence; facts only, own words | conditional use, attribution, no bulk or prefetch, caching, User-Agent and Referer (§1.3.1 to §1.3.3, §1.3.11, §1.3.12) |
| W3C Geolocation specification (w3.org/TR/geolocation/), read 2026-10-20, first 100000 of 128646 characters | W3C document licence, facts only | permission, secure context, minimisation, error codes, accuracy hint (§1.6.2, §1.6.4, §1.6.10) |
| W3C WCAG 2.2 Understanding SC 4.1.3, read 2026-10-20 | W3C document licence, facts only | results count as status message (§2.3.7) |
| Leaflet, `LICENSE` (BSD 2-Clause, Copyright Volodymyr Agafonkin and CloudMade) and API reference page (leafletjs.com/reference.html), read 2026-10-20 | BSD-2-Clause (`LICENSE` read) | Default coordinate system and projection, popup strings rendered as HTML (§1.1.2, §2.2.5) |
| W3C WCAG 2.2 Understanding SC 1.4.1, read 2026-10-20 | W3C document licence, facts only | Colour not the only means (§2.1.10) |

Not opened: the MapLibre and OpenLayers repositories and their licences (licence unverified, not opened), the OpenStreetMap wiki (share-alike licence), any commercial map or geocoding provider terms. No permissive source found for clustering, geocoding quotas, or the non-map accessibility alternative, searched: only the pages above.

## Own craft, not from a source
Coordinate order and datum, range validation, clustering and viewport loading, the tile-terms and attribution checklist, geocoding and autocomplete limits, routing caveats, location consent method, states and interaction, the non-map accessibility alternative, performance, security, test list and framework pointers.

## Removed
Specific provider names, prices, quotas and terms; library-specific code; routing engine design; fleet-tracking and surveillance-style uses; anything presented as legal advice.

## Verified on 2026-10-20
Coordinate order, datum, antimeridian, precision, one public tile server's policy, geolocation permission and error model, status messages. One correction (§1.3.1: conditional, not flatly forbidden). Four points added (§1.1.11, §1.3.11, §1.3.12, §1.6.10) plus test §2.6.13.

## Verified on the second pass, 2026-10-20
3 verified (default projection of one library, popup HTML rendering, colour as sole means), 0 corrected, 0 deleted. Projection facts for other libraries, clustering, geocoding quotas and provider terms were not checked.

## Not verified
1. **Everything not cited above is own knowledge**: clustering, geocoding and autocomplete limits, routing, states, performance and the non-map alternative were not checked.
2. **Provider terms** other than the OSMF tile policy (storage of geocode results, commercial tile terms, attribution wording) vary and change; re-read your provider's current terms before relying. The OSMF page may change; it was read once on the date above.
3. **Location privacy and consent points** are method only, not legal advice; the rules depend on jurisdiction, purpose and platform.
4. **Accessibility points**, including library keyboard behaviour, are recalled public practice and were not run.
5. **Framework pointers** name features from memory; no version was checked.
6. **No number** (cluster thresholds, debounce delay, quota) is stated; none was measured.
