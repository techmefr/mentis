# long-and-multistep-form-pitfalls: origin and source stamps

> Provenance of `skills/long-and-multistep-form-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge, then sourced in part on 2026-10-20; nothing was run and no form was built or tested while

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: multi-request save atomicity and retry duplication (1.3.8), flush of a pending autosave on unmount, draft kind check per save path, silent draft failure check, checkable output list, skip-when line.
writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| RFC 9457 problem details (rfc-editor.org page, read 2026-10-20) | IETF standard, facts only, own words | members, media type, extension rule, errors-with-pointer example, do-not-parse-detail |
| RFC 6585 §3 (read 2026-10-20) | IETF standard, facts only | 428 purpose, optional use |
| RFC 9110 (pages read 2026-10-20, If-Match section 13.1.1 re-read from the text version) | IETF standard, facts only | 412 meaning (section 15.5.13); If-Match strong comparison, evaluation, 412 or 2xx on failure (section 13.1.1) |
| Government design system, error-summary page (read 2026-10-20) | page text, facts only, own words; the frontend repository licence file (MIT, Crown copyright) was read 2026-10-20, the design-system repository licence file was not reachable | summary placement, focus, linking, page title prefix, message at field |
| WCAG 2.2 understanding pages for SC 2.2.1 and SC 3.3.1 (W3C, read 2026-10-20) | W3C document, facts only, own words, page credited | timing options, error text rules, native validation caveats |
| HTML Standard, autofill section (read 2026-10-20) | CC BY 4.0 (licence file read 2026-10-20), WHATWG | purpose tokens, section prefix, off |

## Rewrite notes
Every rule not credited above is own guidance from general practice in business-application forms. No text, example or
number was copied. No numeric threshold is given.

## Removed
- Debounce delays, session lengths and field-count thresholds: no verified source, so none given.
- Any claim about a particular form library's behaviour: not read.

## Not verified
1. **RFC details:** problem details and 428 were re-read; the If-Match comparison rule (RFC 9110 section 13.1.1) was re-read and verified
   2026-10-20; the idempotency-key header draft status was not; check it before relying.
2. **Browser behaviour** (unload confirmation text, visibility-change delivery of requests, local storage limits)
   differs by browser and version; test it.
3. **Accessibility claims:** the timing criterion, error text and error summary were checked; focus management on step
   change, live regions, fieldset and legend, and disabled-button advice were not.
4. **Own guidance, not sourced:** all points on drafts, dirty state, step routing, conflict screens and merge rules, and the
   browser unload confirmation (the HTML Standard slice read did not cover it).
5. **No permissive source found for drafts, dirty state, wizards or conflict screens, searched:** RFC and W3C/WHATWG pages above, the
   government design-system pages; no open-licensed wizard or draft-saving guide was opened.

## Related blocks
`accessibility`, `frontend-ux-antipattern-review-pitfalls`, `international-input-pitfalls`, `interface-design`,
`ux-writing`, `laravel-precognitive-request-scoping`, `api-design`, `laravel-post-may-run-twice`.
