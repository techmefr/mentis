---
name: credential-lifecycle-pitfalls
description: "Use when code stores or checks a password, resets one, verifies an email address, enrols a second factor or generates a token that proves something (session id, reset link, verification code): validation, password hashing and rehashing, enumeration and throttling, single-use hashed tokens, TOTP and recovery codes, random values."
---

# credential-lifecycle-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the credential flows of an application that owns its own
accounts: the password, the reset, the email check, the second factor and the random value behind each of
them. `skills/auth-session-conventions` owns what happens after login (token lifetime, refresh, storage),
`skills/jwt-verification` owns signed tokens, and `skills/oauth-oidc-client-pitfalls` owns login through a
provider; this block owns the flows that create and recover the credential. The principles hold in any
language. Parameter values are version-bound and dated in `references/origin.md`; a project that
already has a password policy follows it where it is stricter. WebAuthn and passkeys are out of scope.

## When
A diff adds or changes sign-up, login with a password, a change-password or forgot-password route, an email
verification step, an email-change flow, TOTP or recovery-code enrolment, a one-time code sent by SMS or
mail, or any code that generates a random identifier used as a secret.

## Steps

**Read only the section the flow touches.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Passwords: validation, hashing, rehashing, throttling, error messages | a password is accepted, stored, compared or rate-limited | [`01-passwords.md`](./references/01-passwords.md) |
| 2 | Recovery and second factors: reset, email verification, email change, TOTP, recovery codes | a reset link, a verification step or an MFA enrolment is written or changed | [`02-reset-verification-mfa.md`](./references/02-reset-verification-mfa.md) |
| 3 | Tokens and random values: generation, storage, single use, bias | any value is generated or stored to prove an identity or an action | [`03-tokens-and-random.md`](./references/03-tokens-and-random.md) |

## Output / checkpoint
For each flow in the diff: the password hash and its parameters, where the parameters are stored and how a
hash is upgraded at login, the throttle applied to each guessable input and to each endpoint that sends
mail, how each token is generated, stored, expired and consumed, and which sessions the flow invalidates.
Evidence is a replay of: a wrong-password and an unknown-user attempt returning the same message, a reused
reset token refused, and an expired code refused.

## Guardrails
- Never store a password with a general-purpose hash such as MD5, SHA-1 or SHA-256 (§1.5).
- Never compare a hash or a token with `==`, and never truncate or silently edit a password (§1.1, §1.9).
- Never store a reset or verification token in clear; store its hash (§3.4).
- Never send a reset or verification link whose page can leak the token in a `Referer` header (§2.4).
- Never hard-code the hash parameters in the verification path; read them from the stored hash (§1.8).
- Hash parameters and token lifetimes change with hardware and guidance: re-read the sources named in
  `references/origin.md` rather than copying the numbers from memory.
- Do not paste a real credential, hash or token into a prompt or a test fixture.

## Origin
Rewritten from the password, password-reset, email-verification, MFA, server-side-token and
random-value pages of the Copenhagen Book (MIT) and the libsodium documentation on password hashing (ISC),
read 2026-10-15. The full provenance, parameter versions, what was removed and what is our own guidance are
in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
