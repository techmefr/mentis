# login-mfa-reset-screens-ui-pitfalls: origin and source stamps

> Provenance of `skills/login-mfa-reset-screens-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No screen was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate for code and second-factor sections, concrete timing-leak cause, network-response check for sign-up, distinct reset and sign-up error messages, token-in-address check for emailed links, 401 handler and return-path checks, custom keypad section.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| HTML Standard, autofill field names (https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill) | CC BY 4.0 for the text, confirmed in the repository LICENSE file on 2026-10-20 (code snippets BSD-3-Clause) | Tokens username, current-password, new-password, one-time-code, email; last-token rule; optional webauthn token. Read through a summarising fetcher, first 100000 characters |
| HTML Standard, the inputmode attribute (https://html.spec.whatwg.org/multipage/interaction.html) | same CC BY 4.0 | Keywords including numeric and email. Read through a summarising fetcher |
| GOV.UK Design System, password input, passwords pattern, confirm a phone number pattern (https://design-system.service.gov.uk/) | content licence not verified (the repository licence URL tried returned 404); read for facts only, rewritten in our words, credited as a source of guidance | Show password, paste, maxlength, spellcheck, clearing the password on failure, one-time-code with numeric input mode, spaces and dashes, distinct code errors, reset notification, attempt numbers as examples. Read 2026-10-20 through a summarising fetcher |
| W3C WCAG 2.2 Understanding SC 3.3.8 Accessible Authentication (Minimum) and SC 2.2.1 Timing Adjustable (https://www.w3.org/WAI/WCAG22/Understanding/) | W3C document licence, facts only, own words | paste and password-manager rule, timeout warning and extension rule. Read 2026-10-20 through a summarising fetcher |

Credit: WHATWG, HTML Standard, https://html.spec.whatwg.org/ (CC BY 4.0); GOV.UK Design System, https://design-system.service.gov.uk/.

OWASP cheat sheets (CC BY-SA) were not opened. No permissive source found for session expiry, re-authentication, redirect, multi-tab and custom keypad points, searched: GOV.UK Design System (the re-authentication page returned 404), HTML Standard, W3C authoring practices were not searched for these. The existing mentis blocks it links (`auth-session-conventions`, `security-hardening`, `webauthn-passkey-pitfalls`, `oauth-oidc-client-pitfalls`) are cross-referenced, not copied.

## Own craft, not from a source
Everything not credited in the table: message equality across known and unknown accounts, sign-up and two-step cases, field and token rules, paste and show-password rules, code entry and resend design, recovery code handling, reset screens, rate-limit wording, session expiry and re-authentication, redirect rules, multi-tab behaviour, tests, framework pointers.

## Removed
Server-side token, hashing, lockout-key and mail-delivery rules (linked blocks own them); provider-specific sign-in steps; legal consent wording.

## Not verified
1. **Verified 2026-10-20**: autocomplete tokens and the webauthn token, inputmode keywords, GOV.UK password, code and reset facts. **Corrected**: §1.2.3 (clear the password after a failed sign-in). **Added**: show-password state mismatch, type switch on submit, no maximum length, spellcheck and capitalisation, sign-in resend must not reveal the contact, distinct digit-count errors, reset notification, example attempt numbers. Deleted: none. **Second pass 2026-10-20 verified**: §1.4.1 paste rule against WCAG 3.3.8, §3.1.4 warning rule against WCAG 2.2.1; corrected: none. **Still unverified**: how each browser and manager uses the tokens, the rest of §1, §2.3, §3 (session, redirects, multi-tab, keypad) and all tests.
2. **Cross-references to sections of `security-hardening`** (§1, §3, §6, §7, §9) were checked against the section titles only, not re-read line by line.
3. **Framework pointers** (Laravel kits, Fortify throttling, Nuxt, Next, passkey libraries) name features from memory; no version was checked.
4. **Timing equality** between known and unknown accounts depends on the server and was not measured.
