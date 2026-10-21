# firebase-rules-and-client-trust-pitfalls: origin and source stamps

> Provenance of `skills/firebase-rules-and-client-trust-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of client-direct backends, with the points listed under sources re-checked against the official documentation on 2026-10-20, never run: no project, rules file,
emulator or function was created or tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Firebase documentation pages: Firestore get-started security, rules conditions, query rules, Realtime Database security, rules basics, rules unit tests, API keys, App Check, custom claims, manage sessions, anonymous sign-in, callable functions, function retries | CC BY 4.0 for text and Apache-2.0 for code samples, as stated in the footer of the get-started and rules-basics pages (the footer was not checked on each of the other pages); credit: Firebase documentation, Google; rewritten, nothing copied, read 2026-10-20 | Locked versus test mode and the warning on allow-all (§1.1), queries all-or-nothing (§1.3), parent grant not revocable in the real-time database (§1.4), client keys not secret and the three protection layers (§2.1), claim size and refresh paths (§2.3), ID token lifetime and revocation checks (§2.3) |
| PostgreSQL-platform skill collection named in the review | MIT (licence file read earlier) | Not rewritten here: carried by `postgres-operations-and-exposed-api-pitfalls` §3 |

## Removed
- No sentence of the documentation pages is carried; the facts are restated in our words.

## Not verified
1. **Confirmed on 2026-10-20:** locked mode default and test mode wording, queries all-or-nothing, parent-path cascade in the real-time database, claim size and refresh paths, ID token lifetime, revocation behaviour, client keys not secret. **Also confirmed 2026-10-20:** server client libraries bypass the document database rules, and lookup limits per request (10, or 20 for multi-document operations). **Re-opened 2026-10-20 and confirmed:** locked mode default and test mode wording (rules basics), signed-in-only as a development option, never-in-production warning, lookup limits (10 and 20, billed even when rejected), all-or-nothing queries, `or` and `in` conditions, collection-group rules version, real-time database cascade and non-cascading validation, claim size (1000 bytes) and the three refresh paths, one-hour token lifetime, stateless tokens, revocation check cost, key identification role and default restriction to Firebase APIs, password-endpoint quota remark, attestation scope and limits, unit-test library calls, event retries and the retry windows, anonymous cleanup. **Corrected:** the test-mode expiry is unverified and the block no longer states it as fact; anonymous sign-in counting as signed in is our reading; the callable page does not demand an auth check or input validation. **Still unverified:** the length of the development-mode period (three pages read, none gave it), the administrator SDK named explicitly (the document-database page speaks of server client libraries), other products' path independence, email-existence disclosure (the page was not opened: redirect to a host whose licence was not read), authorized-domain behaviour.
2. **Other client-direct backends.** Only the shape of the reasoning transfers; names and defaults do not. The PostgreSQL-based case is in the related block.
3. **Own guidance, still labelled in the text:** every point not listed in item 1, and every "Checks" section.
4. **Licence.** Two of the pages read show a CC BY 4.0 footer; the others were assumed to carry the same site-wide notice and were used for facts only.
5. **No rule, command or function was executed.**

## Related blocks
`postgres-operations-and-exposed-api-pitfalls` (Supabase and generated-API rules), `serverless-edge-worker-pitfalls`,
`flutter-notifications-background` (push setup on one stack), `credential-lifecycle-pitfalls`, `security-hardening`.

Independent verification 2026-10-21: 24 checked, 24 matched, 0 corrected, 0 unverified
