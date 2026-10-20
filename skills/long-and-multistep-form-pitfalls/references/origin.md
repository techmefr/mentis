# long-and-multistep-form-pitfalls: origin and source stamps

> Provenance of `skills/long-and-multistep-form-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge; nothing was run and no form was built or tested while
writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read. No source with a LICENSE file read and verified as MIT, Apache-2.0 or CC BY was used. | n/a | n/a |
| HTTP semantics (RFC 9110), additional status codes (RFC 6585), problem details (RFC 9457): facts only, restated in our own words, recalled from memory and not re-opened | IETF standards, facts only | ETag and If-Match, 412 and 428, error body shape |

## Rewrite notes
Every other rule is own guidance from general practice in business-application forms. No text, example or
number was copied. No numeric threshold is given.

## Removed
- Debounce delays, session lengths and field-count thresholds: no verified source, so none given.
- Any claim about a particular form library's behaviour: not read.

## Not verified
1. **RFC details** (member names of problem details, exact header semantics, the idempotency-key header draft
   status) were recalled, not re-read; check them before relying.
2. **Browser behaviour** (unload confirmation text, visibility-change delivery of requests, local storage limits)
   differs by browser and version; test it.
3. **Accessibility claims** (focus management, live regions, the timing criterion) restate common practice and were not
   checked against the current standard text.
4. **Own guidance, not sourced:** all points on drafts, dirty state, step routing, conflict screens and merge rules.

## Related blocks
`accessibility`, `frontend-ux-antipattern-review-pitfalls`, `international-input-pitfalls`, `interface-design`,
`ux-writing`, `laravel-precognitive-request-scoping`, `api-design`, `laravel-post-may-run-twice`.
