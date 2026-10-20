---
name: login-mfa-reset-screens-ui-pitfalls
description: "Use when a sign-in, sign-up, one-time-code (MFA), recovery or password-reset screen is written or reviewed in a web application, on the interface side only: error and confirmation messages that do not reveal whether an account exists, form fields that let browsers and password managers work (autocomplete tokens, paste, show password), feedback when rate limited or locked, one-time-code entry and resend, expired links and codes, session expiry and re-authentication without losing the user's work, redirects after login, and the tests that catch them. The server rules are in the existing authentication and security blocks."
---

# login-mfa-reset-screens-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the screens a user meets before they are inside. The premise: **a login
form works for the developer who knows the password.** It breaks for the user whose password manager cannot fill it,
whose code arrives after the screen timed out, who is told "no account with this email" (which also tells an
attacker), who is rate limited with no explanation, and whose session ends in the middle of a long form. This block
covers only what the user sees and does. Token, cookie, refresh and guard rules are in `auth-session-conventions`;
validation, rate-limit keys, lockout and reset-token handling on the server are in `security-hardening` (§1, §7,
§9); passkeys and second-factor assertion are in `webauthn-passkey-pitfalls`; sign-in through a provider is in
`oauth-oidc-client-pitfalls`; field and error markup is in `accessibility` §4; a long form is in
`long-and-multistep-form-pitfalls`.

## When
- A login, registration, MFA challenge, recovery or reset screen is built or reviewed.
- A user reports "my password manager does not fill it", "I never got the code", "it says too many attempts", "I lost my form when it logged me out", "the link is invalid".
- An error message names a cause that the server should keep private.

**Skip when** a part does not exist: if the product has no one-time-code or second-factor screen, skip §2.1, §2.2 (code resend) and §2.3 and write "not applicable: no code or second factor"; a sign-in by emailed link, a device pairing code or a PIN keypad is a different surface, covered by §1.1, §2.4, §2.5, §3 and §1.6, not by the code rules. Say "not applicable: reason" rather than invent a finding.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Messages without account enumeration, field attributes, password managers, paste, show password, error placement, custom keypads | a sign-in, sign-up or reset-request screen is written | [`01-messages-fields-managers.md`](./references/01-messages-fields-managers.md) |
| 2 | One-time-code entry, resend and timers, recovery codes, rate-limit and lockout feedback, expired links | a code, a challenge, a limit or a reset link is shown | [`02-codes-limits-reset.md`](./references/02-codes-limits-reset.md) |
| 3 | Session expiry and re-authentication, redirects after login, multi-tab, sign-out, tests, framework pointers | the user can be logged out, bounced or tested | [`03-session-redirects-tests.md`](./references/03-session-redirects-tests.md) |

## Output / checkpoint
A change is done when: failed sign-in, reset request and sign-up give the same visible message whether or not the
account exists (§1.1); every field carries its autocomplete token and accepts paste (§1.3, §1.4); a rate limit says
when to try again without revealing more (§2.5); a code, where the product has one, can be entered by keyboard and paste and resent safely
(§2.1, §2.3); an expired session returns the user to their place with their work kept (§3.1, §3.2); and the tests in
§3.6 exist. No checkpoint is written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Show one message for every failed sign-in and every reset request (§1.1). Never say which of email or password was wrong or whether the email is registered.
- Let the browser and the password manager do their job (§1.3, §1.4). Never block paste, split a password across fields or disable autocomplete on credentials.
- Tell a rate-limited user what they can do next, and nothing about why the server decided so (§2.5). Never show a counter that confirms a valid account.
- Keep the user's work through a session expiry (§3.2). Never throw away a long form because the cookie expired.
- Redirect only to a path inside the application after login (§3.3). Never send the user to a URL taken from a query value without checking it.
- Facts about a browser or a standard are for the date in `references/origin.md`; re-read before relying. A point without a credit to the HTML Standard or GOV.UK is still own guidance.

## Origin
Own craft knowledge. The autocomplete token and input-mode facts were checked on 2026-10-20 against the HTML Standard (CC BY 4.0), and the password, code-entry and reset points against the GOV.UK Design System pages (facts only, credited, content licence not verified, no text copied). No MIT or Apache-2.0 source was found for the screens themselves. Details in
[`references/origin.md`](./references/origin.md).
