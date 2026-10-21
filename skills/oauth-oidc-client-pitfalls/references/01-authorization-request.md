# oauth-oidc-client-pitfalls §1 — The authorization request

> Section 1 of `skills/oauth-oidc-client-pitfalls`. Read it when the route that redirects the browser to
> the provider is written or changed. Rules marked "own guidance" are ours and not from a source.

1. **Generate a new state for every attempt, from a cryptographically secure generator, with at least 112
   bits of entropy.** The Copenhagen Book says its purpose is to make sure the user who started the flow
   and the one redirected back are the same user. Without it, an attacker can finish a flow they started in
   your victim's browser and sign the victim in as the attacker (login CSRF). It is not strictly required by
   the specification, but the source calls it highly recommended and notes some providers require it.
2. **Keep the state server-side, per attempt.** The source's simple approach is a cookie with `HttpOnly`,
   `SameSite=Lax`, `Secure` and `Path=/`; assigning it to the current session also works. A cookie with
   those attributes is the source's choice. Own inference from its explanation of `Strict` (§3.3): the
   return from the provider is a navigation from another site, so a `Strict` cookie would not be sent.
   The state can also carry data from the login route to the callback, though the source says a cookie can
   do that instead. RFC 9700 section 2.1 agrees: invalidate the stored state after its first use at the callback, so a replayed
   callback finds nothing.
3. **Use PKCE with `S256`, with a new code verifier per attempt.** The verifier comes from a cryptographically
   secure generator with at least 112 bits of entropy (the RFC recommends 256, per the source). The
   challenge is the base64url encoding, without padding, of the SHA-256 hash of the verifier, sent as
   `code_challenge` with `code_challenge_method=S256`. Keep the verifier per attempt exactly as the state
   is kept, and send it with the code at the exchange (§2.2). The oauth2-proxy documentation lists `plain`
   and `S256` as the two methods and marks `S256` as recommended.

   ```
   response_type=code
   &client_id=<CLIENT_ID>
   &redirect_uri=<CALLBACK_ENDPOINT>
   &state=<STATE>
   &code_challenge_method=S256
   &code_challenge=<CODE_CHALLENGE>
   ```

4. **PKCE and state overlap; use both unless the provider says otherwise.** The source says PKCE can
   replace state as a CSRF protection but a provider may still require state, and recommends PKCE in
   addition to state and a client secret when the provider supports it. It also records a provider-specific
   caveat: some providers do not require a client secret when PKCE is enabled, and for those the source
   advises against using PKCE. That is a statement about specific providers, not a general rule; read the
   provider's documentation for which case applies.
5. **The authorization code grant only.** The source states that the implicit grant type is deprecated and
   should not be used.
6. **Send the redirect URI you registered, as one exact string.** RFC 9700 sections 2.1 and 4.1.3 call for exact string comparison of redirect URIs, since pattern matching has enabled real attacks. Register the full callback
   URL, send the same value in the authorization request and the token request, and register no wildcard or
   pattern. The source shows the same `redirect_uri` value in both requests. Where the callback lives on
   several hosts, register each one rather than accepting a value from the request.
7. **Request the scopes you use and no more.** RFC 9700 section 2.3 asks for tokens limited to the privileges needed. The Copenhagen source only describes the `scope`
   parameter as a space-separated list; asking for additional resources is a decision, and the less you ask
   for, the less a leaked token can do.
8. **The login route only redirects.** Per the source, the flow needs a login route (GET) that redirects to
   the provider and a callback route (GET) that handles the redirect back. Own guidance: the login route
   mutates nothing besides storing the state and the verifier, which is what keeps it safe as a GET (§3.5).
9. **Discovery trades hard-coded URLs for extra fetches.** The OpenID Connect discovery document at
   `/.well-known/openid-configuration` lists the endpoints and, per the source's example, the supported
   challenge methods. The source notes that not every provider offers one and that the drawback is the
   extra requests. RFC 9700 section 2.6 favours published server metadata over hand-copied endpoints. Own guidance: fetch it from a configured HTTPS issuer URL only, cache it, and treat the
   endpoints it returns as configuration read from the provider you chose, never from user input.
