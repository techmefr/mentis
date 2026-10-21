# webauthn-passkey-pitfalls §2 — Assertion and second factor

> Section 2 of `skills/webauthn-passkey-pitfalls`. Read it when a sign-in or a second-factor step verifies an
> assertion. Restated from the Copenhagen WebAuthn page (`pages/webauthn.md`, commit `fb7eb3a`) and from
> SimpleWebAuthn's `verifyAuthenticationResponse.ts` and `generateAuthenticationOptions.ts` (commit `787ca82`),
> both MIT, read 2026-10-16. Option names and defaults are the library's at that commit and version-bound.
> Sentences marked "own guidance" are ours.

1. **The checks mirror registration, with a different type and no credential data.** A fresh stored challenge,
   the get type (not the create type), the exact origin, the relying party ID hash, user presence, and user
   verification when required. The page says this part is nearly identical to registration; the library runs
   them in that order and then checks the signature.
2. **In a second-factor step, the credential must belong to the authenticated user.** The page bolds it: skipping
   the check lets an attacker skip the second factor entirely, because any registered credential would satisfy
   the signature check. Pass that user's credentials as the allowed list for non-discoverable keys. The specification's assertion steps (WebAuthn Level 3 section 7.2, steps 5 and 6) have the server check that the returned credential ID is in the allowed list and that a returned user handle equals the account's. Own guidance:
   the library takes whichever stored credential you hand it and has no notion of users, so the ownership check
   is yours; look the credential up by credential ID and user ID in one query and treat "not found" like a
   failed signature.
3. **User verification: the options and the verification must agree.** The library's option comment says to set
   `discouraged` when the assertion is part of a second-factor flow and otherwise `preferred` or `required`; the
   Copenhagen sample asks for `required` in both. The two sources differ, so choose per flow. The library's
   verification defaults to requiring user verification, so a flow that discouraged it must also tell the verify
   call not to require it, or every such assertion fails. Own guidance: when unsure, requiring it on the verify call
   fails closed. Presence is always required.
4. **A verify call that does not throw has not necessarily succeeded.** The library throws for a wrong type,
   challenge, origin, relying party hash, missing user presence or verification, and a counter that did not
   advance, but the signature check comes back as a boolean in the result. Own guidance: wrap the call so that
   any exception is a failed sign-in with one generic message, and proceed only when the result flag is true.
5. **Counter and session come after the result.** Own guidance: update the stored counter and start the session
   only from a result that passed. The page says the signature covers the authenticator data and the SHA-256 of
   the client data JSON, and for ECDSA the signature is DER encoded; a library does this, and a hand-written
   check must verify that exact input.
6. **The signature counter matters for some credentials only.** The page says that for hardware tokens bound to
   one device you store the counter and require it to rise, and that passkeys, which are meant to be shared across
   devices, can ignore it. The library rejects a response when the counter is not greater than the stored one,
   but only if either of the two is above zero, and returns the new counter to store. So a credential that
   always reports zero passes; do not build a policy that treats a zero counter as an error. WebAuthn Level 3 section 6.1.1 agrees: a counter that does not rise, with both values nonzero, may mean a clone, a fault or out-of-order processing; it does not say which side cloned, so the response is the relying party's risk decision, and an authenticator without a counter reports zero.
7. **Cross-origin ceremonies are rejected unless you expect them.** When the client data says the call came from
   a cross-origin frame, the library requires a configured expected top origin, and when it is not cross-origin
   it rejects a top origin that is present. Its source notes that Safari did not support the top origin field as
   of May 2026, so the check runs only when the field exists; this is version-bound, so re-read it when
   embedding the sign-in in a frame.
8. **Keep the library's returned details.** Besides the new counter, the result gives whether the user was
   verified, the device type, the backed-up state and the origin and relying party ID that matched. Own guidance:
   log the matched origin and credential ID (not the signature) on a failure to make a wrong configuration
   findable, without writing the challenge.
9. **Ordering a second factor in a larger flow is another block.** When a password reset, an email change or a
   login asks for a second factor, the order of the steps is in `skills/credential-lifecycle-pitfalls`.
