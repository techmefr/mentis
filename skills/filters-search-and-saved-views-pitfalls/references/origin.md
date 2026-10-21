# filters-search-and-saved-views-pitfalls: origin and source stamps

> Provenance of `skills/filters-search-and-saved-views-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No filter bar was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TanStack/table at commit 95c4768 (Vue guides: column-filtering, global-filtering, column-faceting, pagination) | MIT, Copyright (c) 2016 Tanner Linsley (`LICENSE` read 2026-10-20) | Client against server filtering on the same dataset, auto-removal of empty values, case-sensitive and insensitive comparators, faceting as data for filter interfaces, page reset on filter change |
| HTML Standard, history API section (WHATWG), <https://html.spec.whatwg.org/multipage/nav-history-apis.html>, read 2026-10-20 | CC BY 4.0 (WHATWG; licence file read 2026-10-20 for another block), facts only | Push and replace share one routine, same-document, SecurityError on a non-rewritable URL, implementation-defined cap on state entries |
| W3C UI Events, composition events and isComposing, <https://www.w3.org/TR/uievents/>, read 2026-10-20 (first 100,000 characters) | W3C Document License; facts only, own words | Composition session shape, isComposing on key and input events |
| W3C WCAG 2.2 (Recommendation), <https://www.w3.org/TR/WCAG22/>, full page fetched 2026-10-20 | W3C Document License; facts only, own words | SC 3.3.2, 4.1.3, 1.4.1, 2.5.3 behind §2.6 points 1, 3, 4 |
| W3C WAI-ARIA 1.2, <https://www.w3.org/TR/wai-aria-1.2/>, full page fetched 2026-10-20 | W3C Document License; facts only, own words | Status role implicit polite and atomic; alert assertive (§2.6.3) |
| W3C ARIA Authoring Practices: search landmark example, modal dialog pattern, date picker dialog example, combobox pattern, read 2026-10-20 | W3C notice with permissive licence; facts only, own words | Search landmark and unique labels, focus handling of dialogs, typed date input beside a calendar, Escape clearing as optional (§2.2.7, §2.6.2, §2.6.5, §2.6.6) |
| HTML Standard, the search element and the placeholder attribute, full page fetched 2026-10-20 | CC BY 4.0 (WHATWG), facts only | Search element scope, placeholder not a label (§2.6.1, §2.6.2) |

## Own craft, not from a source
URL state rules, saved-view ownership and versioning, request races and debounce, facet count agreement, filter semantics (OR within a field, nulls, time zones), empty-result design, accessibility and test lists, framework pointers.

## Removed
Library option names and code, fuzzy matching, nested-row filtering, framework install steps.

## Not verified
1. **Library facts** are the documentation's claims at the commit; none was run. Re-read before relying.
2. **Verified 2026-10-20:** replace against push semantics and the entry cap (HTML Standard); composition session and isComposing (UI Events); label, search landmark, status role, colour, label in name, dialog focus, typed date input and Escape-clear in the accessibility points of §2.2.7 and §2.6 (sources above, none wrong, one narrowed: Escape clearing is optional in the pattern). **Still unverified:** router query handling and SQL null logic (general knowledge), debounce and facet behaviour, saved-view rules, the "placeholder often fails contrast" remark (no page read states it).
3. **Framework pointers** name features from memory; no version was checked.
4. **No debounce delay or length threshold** is stated; none was measured.

Independent verification 2026-10-21: 13 checked, 13 matched, 0 corrected, 0 unverified
