# kotlin-android-conventions — origin and source stamps

> Provenance of `skills/kotlin-android-conventions`. Read it when a rule has to be traced back to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Sources read on **2026-10-02**; rules are rewritten from the mechanism.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| Kotlin language documentation repository (coding conventions in full; null-safety and exceptions pages read by their key sections) | commit `fccdcbb` of 2026-10-02 | Apache-2.0 | §1, §2 | rewritten with this credit |
| Reference Android app by the platform vendor (agent guide and architecture write-up) | commit `a49ed25` of 2026-09-22 | Apache-2.0 | §3 | rewritten with this credit |

**Added 2026-10-02 (§4, §5):** the coroutines library documentation (Apache-2.0, commit `bd2e9a1` of
2026-09-16: basics and structured concurrency, cancellation, exception handling, flow, shared mutable state
chapters), the platform vendor's coroutine best-practices page (read from the web that day, its content is
licensed for reuse with credit) and the static-analysis tool's introduction page (configuration and
baselines). Dispatcher internals, channel and select chapters, the state-versus-event guidance of a community
skill (not read) and the tool's individual rule catalogue are not covered.

**Not read, so nothing attributed to them:** the platform vendor's Kotlin style page and architecture guide
pages, Compose guidance, and the mobile security verification standard (share-alike
licence, idea only).

**Volatile content to re-check:** the sample app's module list and test tooling.
