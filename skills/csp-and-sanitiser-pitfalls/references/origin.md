# csp-and-sanitiser-pitfalls: origin and source stamps

> Provenance of `skills/csp-and-sanitiser-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No server was started, no header was sent and no
sanitiser was executed. Each file below was re-read in full on 2026-10-16 before a rule was taken from it, each
rule was checked against it in a final pass, and each repository's LICENSE file was read again. Defaults,
option names and version numbers are those of the commits shown and are meant to be re-read, not copied.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Helmet (`helmetjs/helmet`, commit `876101e`, package version 8.3.0), `README.md` | MIT (LICENSE file, copyright 2012-2026 Evan Hahn, Adam Baldwin) | Default CSP directives, merge and `null` semantics, nonce pattern, report-only option, "very little validation", `dangerouslyDisableDefaultSrc`, `frame-ancestors` vs `X-Frame-Options`, `X-XSS-Protection: 0`, HSTS defaults and development caveat, `upgrade-insecure-requests` in Safari, default isolation headers, `Referrer-Policy`, `X-Powered-By` |
| DOMPurify (`cure53/DOMPurify`, commit `cde9599`, README describes release 3.4.16), `README.md` | LICENSE file is Apache-2.0; a `LICENSE-MPL` file is also present and the README badge reads "MPL-2.0 OR Apache-2.0". We rely on the Apache-2.0 terms only | Sanitise-last, `removed`, server-side jsdom and happy-dom statements, profiles vs allow-list, risky toggles, `isSupported`, Trusted Types behaviour, non-re-entrancy, `setConfig`, hook behaviour, node input and shadow-root notes, security mailing list |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **"HSTS preload is hard to undo".** The Helmet README says only that preload expresses intent to add the
   policy to browsers and links the MDN page for details. The irreversibility claim is not in the file and was
   dropped; §1.10 says the consequences were not read.
2. **"Per-request random nonce" as a Helmet requirement.** The README shows the pattern in an example and does
   not state it as a rule; §1.4 keeps the example and labels the "fresh every response" reasoning as ours.
3. **"A missing `style-src` falls back to `default-src`".** Standard CSP behaviour, but not stated in the README;
   not used.
4. **The DOMPurify wiki pages** (Security Goals and Threat Model, Attack Classes and Bypass History, the default
   allow-list page) are linked by the README and were not read; nothing was taken from them.
5. **The mutation-XSS and DOM-clobbering explanations.** The README names them and points to the wiki; no rule
   here depends on them.

## Not verified
1. **Own guidance, flagged in the text or the guardrails:** no `'unsafe-inline'` on `script-src` as a fix
   (§1.3), the template must carry the same nonce (§1.4), using report-only to see breakage and wiring a report
   endpoint ourselves (§1.5), `frame-ancestors` for an allow-list (§1.8), checking subdomains before
   `includeSubDomains` or preload (§1.10), the CORP embedding remark (§1.12), the `Referrer-Policy` reasoning
   (§1.13), pinning jsdom (§2.3), rendering as text when `isSupported` is false (§2.8), the assertion test per
   call site (§2.12), and treating DOMPurify and jsdom updates as security fixes (§2.15).
2. **Header values and option names** are as stated at the commits above. The default directive list changes
   between Helmet releases; the CSP, HSTS, framing and referrer semantics themselves come from browsers and were
   not tested.
3. **The MDN pages** the Helmet README links (CSP, HSTS preload, Referrer-Policy, CORP values) were not read.
4. **Trusted Types, jsdom and happy-dom behaviour** were taken from the DOMPurify README and not reproduced.
5. **CSP Evaluator** was not run.

## Decisions where sources disagree
None found. The two READMEs do not overlap except on Trusted Types and CSP, and there they agree.

## Related blocks
`skills/security-hardening`, `skills/regex-validation-pitfalls`, `skills/credential-lifecycle-pitfalls`,
`skills/package-manager-supply-chain-pitfalls`.
