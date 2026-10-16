---
name: webauthn-passkey-pitfalls
description: "Use when a server registers and verifies WebAuthn credentials, as passkeys or as a security-key second factor, by hand or with a library such as SimpleWebAuthn: registration options and challenge handling, attestation, the origin and relying party ID checks, user presence and user verification flags, whose credential an assertion may use in a second-factor step, the signature counter, and a verify call that returns false instead of throwing."
---

# webauthn-passkey-pitfalls

A defensive block for the server side of WebAuthn. The browser and the authenticator do the cryptography; what
goes wrong on the server is a challenge that can be replayed, an origin or relying party check that is
inverted or skipped, a credential that is accepted for the wrong user and a result that was never read. The two
sources are a short protocol walk-through and the verification code of an open-source library, read at the
commits stamped in `references/origin.md`. Passwords, reset flows and the order in which a second factor is
asked are in `skills/credential-lifecycle-pitfalls`; signed tokens issued after a successful sign-in are in
`skills/jwt-verification`. Nothing here replaces the WebAuthn specification or a review of the sign-in design.

## When
- A diff adds passkey sign-in, a security key as a second factor, or credential management for either.
- A server parses an attestation object, authenticator data or client data by hand.
- A library's verify call is wired in and its options (expected origin, relying party ID, user verification)
  are being chosen.
- A second-factor step accepts an assertion and looks the credential up by its ID.

## Steps

**Read the part for the ceremony you are writing.** Registration first when both exist.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Options and registration: challenge, user ID, attestation, passkey and token settings, algorithms, registration checks, what to store | a credential is being created | [`01-options-and-registration.md`](./references/01-options-and-registration.md) |
| 2 | Assertion and second factor: checks, credential ownership, user verification, signature and result, counter, cross-origin | a sign-in or a second-factor step verifies an assertion | [`02-assertion-and-second-factor.md`](./references/02-assertion-and-second-factor.md) |

## Output / checkpoint
For each ceremony in the diff: where the challenge is stored and when it is deleted, the exact expected origin
list and relying party ID, the user verification setting on the options and on the verification, how the stored
credential is selected (by credential ID and user), and what the code does when the verify call throws or
returns false. Evidence is four replays against a local relying party: a used challenge sent again, a response
from another origin, another user's credential ID in a second-factor step, and a signature with one byte
changed. Each must be refused.

## Guardrails
- Never accept a challenge that is not stored on the server, never accept it twice, and never take it from the
  request that carries the response (point 1.1, point 1.2).
- Never take the expected origin or relying party ID from the incoming request (point 1.9).
- Never copy a hash comparison from a sample without testing that a wrong relying party ID is rejected (point 1.10).
- Never accept a credential in a second-factor step that does not belong to the authenticated user (point 2.2).
- Never treat "the verify call did not throw" as success; read the result flag (point 2.4).
- Never update the stored counter or create a session before the verification succeeded (point 2.5).
- Do not paste a real credential ID, public key or attestation into a prompt, a fixture or a log.

## Origin
Rewritten from the Copenhagen WebAuthn page (MIT) and the verification and option-generation source of
SimpleWebAuthn (MIT), read 2026-10-16. The full provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
