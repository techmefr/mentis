# webauthn-passkey-pitfalls §1 — Options and registration

> Section 1 of `skills/webauthn-passkey-pitfalls`. Read it when a credential is being created. Restated from the
> Copenhagen WebAuthn page (`pages/webauthn.md`, commit `fb7eb3a`) and from SimpleWebAuthn's server package
> (commit `787ca82`: `generateRegistrationOptions.ts`, `verifyRegistrationResponse.ts`, and the challenge, user
> ID and relying party helpers), both MIT, read 2026-10-16. Defaults and option names are the library's at that
> commit and version-bound. Sentences marked "own guidance" are ours.

1. **The challenge is random, single-use and at least 16 bytes.** Copenhagen defines it as a randomly generated
   single-use token and recommends at least 16 bytes of entropy; the library's comment cites the specification
   saying challenges should be at least 16 bytes and then generates 32. The registration check reads the
   challenge from the response and the page says to verify it against storage and delete it from storage.
   Own guidance: keep it on the server next to the session that started the ceremony, give it an expiry about
   as long as the browser timeout (the library's default option is 60 seconds), and never accept a challenge
   that the same request supplied.
2. **A new challenge for every ceremony.** Registration and authentication each get their own. Own guidance:
   a challenge stored for registration must not satisfy a later sign-in, so store which ceremony it belongs to.
3. **Call the browser API from a user gesture.** Copenhagen notes that Safari only allows the create call when
   it was initiated by a user interaction such as a button click.
4. **`user.id` is random bytes, not your database ID.** The page says it can differ from the ID the application
   uses; the library generates 32 random bytes, notes the specification caps the field at 64 bytes, and no
   longer accepts a string. Own guidance: it is stored on the authenticator, so put no email address or other
   personal data in it.
5. **Send the user's existing credentials as the exclude list**, so the same authenticator is not registered
   twice (both sources).
6. **Attestation is `none` for most applications.** The page says you do not need to prove the authenticity of
   the authenticator and that not all authenticators support it; if you asked for `none`, check on the server
   that the statement format in the attestation object is `none`. The library's default is also `none`. Checking
   other formats (direct or enterprise attestation) is a separate piece of work and is not covered here.
7. **Passkey and second-factor settings differ.** For a passkey, require a discoverable (resident) key and
   require user verification. For a security key used as a second factor, user verification and resident keys
   can be discouraged, and the authenticator can be limited to cross-platform tokens. The library's default for
   both settings is "preferred", which leaves the outcome to the authenticator; pick one deliberately.
8. **Offer algorithms the server can verify, and check what came back.** The page recommends ES256 (identifier
   -7) as the widely supported one and mentions RS256 (-257) for a few more devices; the library's default list
   is EdDSA, ES256 and RS256 and it rejects a registered key whose algorithm was not offered. The page also says
   to validate the algorithm and the curve of the COSE key.
9. **Verify the registration in full, with expected values you hold.** The checks, in the order the library
   runs them: the response type is the create type; the challenge is the stored one; the origin is exactly
   yours (scheme, host and port); the relying party ID hash matches; user presence is set; user verification is
   set when you required it; credential data is present, including the credential ID and a public key. The
   relying party ID is the domain without protocol or port (`localhost` in development) and the authenticator
   data carries its SHA-256 hash; the origin includes protocol and port. The library accepts a list of origins
   and of relying party IDs. Own guidance: write them in configuration and never derive them from the `Host`
   header or the request URL.
10. **A sample's hash comparison can be wrong; test it.** At the commit read, the page's Go sample returns an
    error when the received relying party ID hash is equal to the expected one, which is the opposite of the
    intent and would reject the right site and accept any other. The page's own text and the library are
    correct. Own guidance: whichever code you write, include one test with a wrong relying party ID that must be
    refused and one with the right one that must pass.
11. **Authenticator data is binary with exact offsets; use a library.** The page lists them (32 bytes of hash,
    one flag byte whose bits are presence, verification and credential-data-included, a four-byte counter, then
    the credential data). Own guidance: hand-parsing needs a length check before every slice and tests with
    truncated input; a maintained parser already has them.
12. **Store the credential ID, the public key, the user it belongs to and the counter**, and the page suggests
    converting the COSE key to a more compact standard format. The library's result also carries the device
    type (single-device or multi-device) and whether the credential is backed up, and its comment says to keep
    both for later reference.
