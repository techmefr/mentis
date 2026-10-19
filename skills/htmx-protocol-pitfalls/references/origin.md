# htmx-protocol-pitfalls: origin and source stamps

> Provenance of `skills/htmx-protocol-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run against a real server by us. No request was
sent and no page was loaded while writing it.

**Merge intent.** A broader htmx and Alpine conventions block exists only on the unmerged branch of the
frontend sourcing pull request (118). This block was written standalone, with a name that cannot collide, to
hold the gaps found in a comparison against it. It is meant to be merged into the same-named framework block
when that pull request lands, section by section, and then removed.

## Version scope
**htmx 2.0.x.** The repository checkout read is the 2.0.11 release commit; its package version and the
install snippets in its documentation agree. The checkout also contains an `hx-partial` swap command and a
note that a newer generation validates forms by default; whether the former belongs to 2.0 or to a later line
could not be settled from the checkout, so neither is used in any rule. Where the
documentation and the source both state a fact (the 286 status, the response headers, the history-restore
configuration, the inheritance configuration) it was checked in both.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The htmx repository documentation: the main documentation page, the response-header pages, the attribute pages for disabled-elt, preserve and disinherit | BSD Zero-Clause, read 2026-10-08 | All of §1 to §3 |
| The htmx repository source (the single-file build): the status 286 handling, the response-header handling, the default configuration | BSD Zero-Clause, read 2026-10-08 | The `286` cancel, header names and the exact `true` check of `HX-Refresh`, the default of the history-restore option, the default response-handling table |
| One MIT htmx skill set | MIT, read 2026-10-08 (not phrased from) | Confirmed the topic list; no rule depends on it alone |

The htmx licence is the Zero-Clause BSD licence: permissive, with no attribution requirement. A second htmx
skill collection had only its index read and was used for nothing.

## Rewrite notes
Rules are re-explained principle first. The verification lists are ours.

## Not verified
1. **Nothing here was run.** All header and status behaviour is as documented and as read in the source.
2. **Header processing on 3xx** is the documentation's statement about browser behaviour; not reproduced.
3. **The `htmx-indicator` injected styles:** the source shows a default that injects CSS to hide indicators;
   its interaction with a content security policy was not checked.
4. **Request-side `HX-History-Restore-Request` and the restore flow** are as the documentation describes;
   not run.
5. **`getCacheBusterParam` and `refreshOnHistoryMiss`** are as documented; their interplay with a real CDN was
   not tested.
6. **Dropped from the review's list:** `hx-select` guidance (no behaviour beyond the attribute reference was
   read) and everything about `hx-partial`, because its version scope is unclear.
7. **Written by us, not sourced:** the verification lists and the output/checkpoint paragraph of `SKILL.md`.

## Related blocks
`security-hardening` (escaping and policy for swapped HTML), `webperf`, `accessibility` (focus after a swap),
`testing-anti-patterns`.
