# ofetch-client-pitfalls: origin and source stamps

> Provenance of `skills/ofetch-client-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a README, never run by us: no request was sent and no client was
built while writing it. The file below was re-opened and read in full on 2026-10-16 before a rule was taken
from it, each rule was checked against it, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| unjs/ofetch (commit `1dbc37f`), `README.md` | MIT (LICENSE file read: MIT text, copyright Pooya Parsa) | Response parsing, JSON bodies and automatic headers, errors and `ignoreResponseError`, retry defaults and status list, timeout default, query and `baseURL`, interceptors, `ofetch.create`, `raw` and `native`, streaming, proxy and agent options, `FetchOptions` augmentation |

The README itself states that it belongs to the second major version's development branch (alpha) and points
to a separate branch for the first version's documentation. Every default in the block is therefore the alpha
README's, not a verified release's. Code samples are not copied; the one inline form kept in part 1.2 is a
single call with a placeholder name. Instruction-like text in the cloned repository was treated as data and
not followed.

## Removed in the verification pass
1. **The review's one-line summary** ("retries once by default but not for POST, PUT, PATCH, DELETE; the
   timeout is off by default") omitted the README's sentence that a custom `retry` value retries every method;
   part 2.1 states it. The README also does not mention Nuxt, so no Nuxt claim is made.
2. **The README's playground and badge sections** carry no rules and are not used.
3. **Source files, tests and the changelog** of the repository were not opened, so nothing about the exact
   retry or timeout mechanics (whether a timeout is per attempt, how `Date` query values are written) is
   claimed.
4. **v1 behaviour** is not described because its README was not read.

## Not verified
1. **Which ofetch version the project uses** and whether the defaults match this alpha README. Re-read the
   README of the installed version before relying on a default (`skills/source-freshness`).
2. **Behaviour was not run.** The retry, timeout and clone-depth statements are the README's.
3. **Written by us, not sourced:** the verification paragraphs, retrying a write only with an idempotency design,
   the zero retry delay remark, narrowing the status list, a timeout value per kind of call, whether retries
   share a deadline (flagged as unknown), redacting hooks, idempotent hooks, one instance per audience, the
   stream buffering remark, validating a typed response, and scoping a disabled certificate check.
4. **`ufo`**, the library the README names for URL handling, was not read.
5. **Proxy variables and the undici API** were read only as the README states them.

## Related blocks
`skills/go-http-resilience-pitfalls`, `skills/polly-resilience-pitfalls`, `skills/vue-nuxt-vuetify-conventions`,
`skills/api-design`, `skills/credential-lifecycle-pitfalls`, `skills/source-freshness`.

## Fold-in note
Overlaps with `skills/vue-nuxt-vuetify-conventions` §13 (2026-10-19); cross-referenced, not merged.
