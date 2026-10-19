# oauth-oidc-client-pitfalls §2 — The callback and the identity

> Section 2 of `skills/oauth-oidc-client-pitfalls`. Read it when the callback route, the token exchange or
> the account-linking code is written or changed.

1. **Check the state first, and refuse when it is missing or different.** The source calls this critical and
   names the common mistake: checking that the returned `state` equals the stored one while forgetting to
   check that the parameter exists at all, so a callback with no state and no stored state compares equal.
   Both the returned and the stored value must be present, and they must match. A mismatch is an error, not
   a restart of the flow.
2. **Exchange the code on the server, with the verifier.** The callback route sends the single-use code to
   the provider's token endpoint in an `application/x-www-form-urlencoded` POST with `grant_type=authorization_code`,
   the client ID, the same redirect URI, the code and, when PKCE was used, the stored `code_verifier`. A
   client secret goes in the HTTP Basic `Authorization` header (client ID and secret, base64-encoded), or in
   the body for providers that accept it. The browser never holds the client secret, and the code is
   exchanged once.

   ```
   POST <TOKEN_ENDPOINT>
   Authorization: Basic <CREDENTIALS>
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code
   &client_id=<CLIENT_ID>
   &redirect_uri=<CALLBACK_ENDPOINT>
   &code=<CODE>
   &code_verifier=<CODE_VERIFIER>
   ```

3. **The code and everything it returns are credentials.** The response carries an access token and may
   carry a refresh token and an expiry. Own guidance: none of them is logged, put in a URL, or passed to
   the front end unless the front end calls the provider itself; the cookie-and-storage rules are
   `skills/auth-session-conventions` §2.
4. **An access token is not a session.** The source says it should never be used as a replacement for
   sessions. The access token proves the provider issued something to your server; it says nothing about
   the browser now talking to you. Create your own session from the verified identity (§3.1) and keep the
   provider tokens server-side, only if you need to call the provider later.
5. **Key the account on the provider's stable identifier, not on the email.** The source's example fetches
   the profile with the access token and stores the provider's user ID, which finds the registered account
   when the user returns. For OIDC the ID token always carries a unique identifier in `sub`. Own guidance:
   the key is the pair of provider and that identifier, because a `sub` is only unique within one issuer
   and an email can change hands.
6. **An email from the provider may be unverified; do not assume otherwise.** The source says the address
   provided by the provider may not be verified, and that you may need to verify it yourself or block users
   without a verified email. For account linking it adds: if you link by email, check the verified field
   the provider exposes (usually something like `is_verified`), do not assume verification unless the
   provider's documentation says so, and stop users without a verified email from completing sign-in and
   prompt them to verify first. This is the account-takeover path: an attacker registers at a provider that
   does not check addresses with the victim's email and signs into the victim's account with you.
7. **An ID token is verified, not decoded.** Check its signature, issuer and audience the way
   `skills/jwt-verification` section 1 says, and check the `nonce` if you sent one. The oauth2-proxy
   documentation names three options `insecure`: allowing an unverified email in an ID token
   (`--insecure-oidc-allow-unverified-email`, default false), skipping issuer verification
   (`--insecure-oidc-skip-issuer-verification`, default false, noted as needed for one multi-tenant
   provider) and skipping the nonce check (`--insecure-oidc-skip-nonce`, listed with a default of true).
   Read that last default: a client that skips the nonce unless told otherwise is verifying less than you
   may assume. Option names and defaults are version-bound (oauth2-proxy at the commit in
   `references/origin.md`).
8. **Where the user lands after login is a redirect target.** If the login route accepts a "return to"
   value, validate it against a list of your own paths or hosts before storing it with the state; an
   unvalidated one is an open redirect on your own domain. The Copenhagen Book points to its open-redirect
   page for this, which was not read; the output rules are `skills/security-hardening` §2.
