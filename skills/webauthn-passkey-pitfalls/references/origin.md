# webauthn-passkey-pitfalls: origin and source stamps

> Provenance of `skills/webauthn-passkey-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a protocol page and library source, never run by us: no relying
party was built, no authenticator was used and no verification was executed. The Copenhagen page and the authentication
verifier were read in full on 2026-10-16; the registration verifier up to line 260 and the option generators
and helpers in the parts that set defaults and sizes. Each rule was checked against the lines it rests on in a
final pass, and each repository's licence file was read again. Option names, defaults and behaviours are the ones the files state at
the commits shown and are version-bound.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Copenhagen (`pilcrowonpaper/copenhagen`, commit `fb7eb3a`): `pages/webauthn.md` | MIT (LICENSE file, copyright 2024 pilcrow) | Challenge definition and minimum size, passkey versus security-key settings, attestation `none` and the format check, authenticator-data layout and flags, relying party ID versus origin, signature counter advice, second-factor credential ownership, what is signed |
| SimpleWebAuthn (`MasterKale/SimpleWebAuthn`, commit `787ca82`): `packages/server/src/registration/generateRegistrationOptions.ts`, `registration/verifyRegistrationResponse.ts`, `authentication/generateAuthenticationOptions.ts`, `authentication/verifyAuthenticationResponse.ts`, `helpers/generateChallenge.ts`, `helpers/generateUserID.ts`, `helpers/matchExpectedRPID.ts` | MIT (LICENSE.md file, copyright 2020 Matthew Miller) | Option defaults, challenge and user ID sizes, order of checks, user verification handling, counter rule, cross-origin handling, what a verify call returns and throws |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **The Copenhagen Go sample's relying party hash check.** It is inverted at the commit read (an error when the
   hashes are equal), so nothing is taken from the sample's code and point 1.10 warns about it.
2. **The Copenhagen sample's unconditional user verification check.** The prose says to check the flag only when
   you required verification; the sample checks it always. Not used as a rule.
3. **Attestation formats beyond `none`** (packed, TPM, Android, Apple, FIDO U2F and their root certificates).
   The registration file of the library was read to line 260 only and the per-format verifiers were not opened.
4. **The review's "signature counter matters only for non-passkey authenticators" as an absolute.** The page
   says passkeys can ignore it and the library enforces it when either value is above zero; point 2.6 states
   both.
5. **Library helpers not read**: attestation verifiers, metadata service, the browser package, extension
   decoding, backup-flag parsing, COSE helpers.

## Not verified
1. **Own guidance, flagged in the text:** challenge expiry about the browser timeout and per-ceremony storage
   (points 1.1, 1.2), no personal data in the user ID (point 1.4), expected values from configuration and not
   from the request (point 1.9), the wrong-relying-party-ID test (point 1.10), hand-parsing needs length
   checks (point 1.11), the ownership query (point 2.2), failing closed on user verification (point 2.3),
   wrapping the verify call and reading the flag (point 2.4), ordering of counter and session (point 2.5),
   what to log (point 2.8).
2. **Nothing was executed.** Every statement of what the library throws or returns is read from its source.
3. **The WebAuthn specification itself** and the library's website documentation were not opened; the
   specification quotes inside the library's comments are cited as such.
4. **Browser behaviour** (Safari's gesture rule, the top origin field) is the sources' statement, dated by them.

## Decisions where sources disagree
User verification on a second-factor assertion: the library's option comment says discouraged, the Copenhagen
sample says required. Both are shown (point 2.3) and the choice is left to the flow, with options and
verification required to agree.

## Related blocks
`skills/credential-lifecycle-pitfalls`, `skills/jwt-verification`, `skills/oauth-oidc-client-pitfalls`,
`skills/security-hardening`.

## Verification pass 2026-10-20
Read for facts only, restated in our words, no text copied: W3C Web Authentication Level 3 (w3.org/TR/webauthn-3, read in chunks up to character 500000 of 503413; facts only). The page reader paraphrased the text, so section numbers are as it reported them.
- Confirmed and credited: user handle at most 64 bytes with no personally identifying information (section 5.4.3, section 14.6.1; point 1.4), assertion credential ownership, allowed-list and user-handle checks (section 7.2 steps 5 and 6; point 2.2, the single-query lookup stays ours), signature counter semantics, zero counters and risk-based response (section 6.1.1; point 2.6), registration checks of challenge equality, expected origin, RP ID hash, UP and UV flags (section 7.1 steps 8 to 16).
- Still unverified: challenge size and freshness (section 13.4.3 not reached; the library's 16-byte note remains the source), timeout recommendations (section 15.1 not reached), expiry and per-ceremony storage (points 1.1, 1.2), config-sourced expected values (1.9), the rest of the section 7.2 steps (7 onward were cut off).

Independent verification 2026-10-21: 8 checked, 4 matched, 4 corrected, 0 unverified
