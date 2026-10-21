# firebase-rules-and-client-trust-pitfalls: origin and source stamps

> Provenance of `skills/firebase-rules-and-client-trust-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of client-direct backends, never run: no project, rules file,
emulator or function was created or tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Firebase documentation pages: Firestore get-started security, query rules, Realtime Database security, rules basics, API keys, custom claims, manage sessions | product documentation, no licence checked, facts only, rewritten, nothing copied, read 2026-10-20 | Locked versus test mode and the warning on allow-all (§1.1), queries all-or-nothing (§1.3), parent grant not revocable in the real-time database (§1.4), client keys not secret and the three protection layers (§2.1), claim size and refresh paths (§2.3), ID token lifetime and revocation checks (§2.3) |
| PostgreSQL-platform skill collection named in the review | MIT (licence file read earlier) | Not rewritten here: carried by `postgres-operations-and-exposed-api-pitfalls` §3 |

## Removed
- No sentence of the documentation pages is carried; the facts are restated in our words.

## Not verified
1. **Confirmed on 2026-10-20:** locked mode default and test mode wording, queries all-or-nothing, parent-path cascade in the real-time database, claim size and refresh paths, ID token lifetime, revocation behaviour, client keys not secret. **Also confirmed 2026-10-20:** server client libraries bypass the document database rules, and lookup limits per request (10, or 20 for multi-document operations). **Still unverified:** the length of the development-mode period (two more pages read, none gave it), the administrator SDK named explicitly, other products' path independence, email-existence disclosure, anonymous sign-in counting as signed in, authorized-domain behaviour.
2. **Other client-direct backends.** Only the shape of the reasoning transfers; names and defaults do not. The PostgreSQL-based case is in the related block.
3. **Own guidance, still labelled in the text:** every point not listed in item 1, and every "Checks" section.
4. **Licence.** The documentation pages carry no licence we read; they were used for facts only.
5. **No rule, command or function was executed.**

## Related blocks
`postgres-operations-and-exposed-api-pitfalls` (Supabase and generated-API rules), `serverless-edge-worker-pitfalls`,
`flutter-notifications-background` (push setup on one stack), `credential-lifecycle-pitfalls`, `security-hardening`.
