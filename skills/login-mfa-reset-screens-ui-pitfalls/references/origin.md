# login-mfa-reset-screens-ui-pitfalls: origin and source stamps

> Provenance of `skills/login-mfa-reset-screens-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No screen was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate for code and second-factor sections, concrete timing-leak cause, network-response check for sign-up, distinct reset and sign-up error messages, token-in-address check for emailed links, 401 handler and return-path checks, custom keypad section.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| HTML autocomplete tokens and input modes (public specification), OWASP authentication and forgot-password guidance | WHATWG terms; OWASP cheat sheets are CC BY-SA, not creditable here | Recalled facts only (token names, the neutral-message idea); the pages were not opened for this pass |

No MIT, Apache-2.0 or CC BY source was read for this block. The existing mentis blocks it links (`auth-session-conventions`, `security-hardening`, `webauthn-passkey-pitfalls`, `oauth-oidc-client-pitfalls`) are cross-referenced, not copied.

## Own craft, not from a source
Message equality across known and unknown accounts, sign-up and two-step cases, field and token rules, paste and show-password rules, code entry and resend design, recovery code handling, reset screens, rate-limit wording, session expiry and re-authentication, redirect rules, multi-tab behaviour, tests, framework pointers.

## Removed
Server-side token, hashing, lockout-key and mail-delivery rules (linked blocks own them); provider-specific sign-in steps; legal consent wording.

## Not verified
1. **Autocomplete tokens and input modes** were recalled, not re-read, and browsers differ in how managers use them. Re-read before relying.
2. **Cross-references to sections of `security-hardening`** (§1, §3, §6, §7, §9) were checked against the section titles only, not re-read line by line.
3. **Framework pointers** (Laravel kits, Fortify throttling, Nuxt, Next, passkey libraries) name features from memory; no version was checked.
4. **Timing equality** between known and unknown accounts depends on the server and was not measured.
