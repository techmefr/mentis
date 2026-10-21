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

## Re-verified 2026-10-20 (🟡, nothing run)

Licence files read on 2026-10-20: `JetBrains/kotlin-web-site` (Apache-2.0), `Kotlin/kotlinx.coroutines` (Apache-2.0),
`android/nowinandroid` (Apache-2.0) and `detekt/detekt` (Apache-2.0). Pages from `docs/topics` of the Kotlin repository:
coding conventions, null safety, exceptions; from the coroutines repository: basics, composing suspending functions,
context and dispatchers, cancellation, exception handling, flow, shared mutable state; from the app: the agent guide and
the architecture learning journey. The vendor's coroutine best-practices page and the detekt introduction page were read
on the web as official documentation for facts only; the vendor's licence page says its documentation text and samples
are Apache-2.0 and other site content CC BY 2.5, and which of the two covers that page was not established, so nothing
was copied and the page is credited here.

| Source | Points confirmed |
|---|---|
| coding conventions | §1.1, §1.2, §1.4 to §1.11 (read-only by default, collection factories, expression forms, `if` against `when`, guard parentheses, nullable Boolean, loops and `..<`, strings, named arguments, aliases, lambdas, backing property), §2.1 to §2.4, §2.8 (property against function, extensions, infix, factories, library rules) |
| null safety, exceptions | §1.3, §2.5 to §2.7 (`require`, `check`, `error`, smart casts, unchecked exceptions, `use`, `Error` branch) |
| coroutines pages | §4.1, §4.4 to §4.10 (structure, cancellation, `yield`, `ensureActive`, `runInterruptible`, `NonCancellable` in `withContext`, rethrow, failure up the tree, handler on roots only, supervisor, volatile, confinement, mutex, `flowOn`, exception transparency) |
| vendor best practices | §4.2, §4.3, §4.11, §4.12 |
| agent guide and architecture page | §3.1 to §3.7 |
| detekt introduction | §5.1, §5.4 |

**Corrected or reworded:** the reasons against the global scope (now the vendor page's three), the unreachable-branch helper
(`error()`), the build-failure remark for the analyser, the agent guide's test wording. **Added:** §4.13 (cancellable
bridge). **Marked as the block's own:** the formatter-first rule (§3.8), the supervisor remark (§4.8), the analyser framing.
**Still unverified:** the detekt baseline task name and suppression identifiers (the page does not give them), the
Compose test details beyond the agent guide, build-failure settings, and the vendor's Kotlin style page (not read).

Independent verification 2026-10-21: 20 checked, 20 matched, 0 corrected, 0 unverified
