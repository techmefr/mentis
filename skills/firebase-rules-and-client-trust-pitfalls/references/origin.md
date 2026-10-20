# firebase-rules-and-client-trust-pitfalls: origin and source stamps

> Provenance of `skills/firebase-rules-and-client-trust-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of client-direct backends, never run: no project, rules file,
emulator or function was created or tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| none | not applicable | Own guidance only. The review file named a PostgreSQL-platform skill collection (MIT licence file read); its security rules are already carried by `postgres-operations-and-exposed-api-pitfalls` §3 and were not rewritten here. No Firebase documentation was opened (licence not verified) |

## Removed
- Nothing was copied or paraphrased from a source; there is nothing to remove.

## Not verified
1. **Everything platform-specific.** Behaviours such as the development-mode expiry, parent-path cascade in the real-time database, rules-as-not-filters, lookup limits, claim size, token lifetime and administrator bypass are from our knowledge of the platform and were not checked against its current documentation. Re-read before relying on any.
2. **Other client-direct backends.** Only the shape of the reasoning transfers; names and defaults do not. The PostgreSQL-based case is in the related block.
3. **Own guidance, labelled in the text:** every point; there is no sourced point in this block.
4. **Publication.** A later pass may credit official documentation once its licence file is read.
5. **No rule, command or function was executed.**

## Related blocks
`postgres-operations-and-exposed-api-pitfalls` (Supabase and generated-API rules), `serverless-edge-worker-pitfalls`,
`flutter-notifications-background` (push setup on one stack), `credential-lifecycle-pitfalls`, `security-hardening`.
