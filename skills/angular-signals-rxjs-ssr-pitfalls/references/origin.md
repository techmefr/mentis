# angular-signals-rxjs-ssr-pitfalls: origin and source stamps

> Provenance of `skills/angular-signals-rxjs-ssr-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real application by us. No Angular
project was built or started while writing it.

**Merge intent.** A broader Angular conventions block exists only on the unmerged branch of the frontend
sourcing pull request (118). This block was written standalone, with a name that cannot collide, to hold the
gaps found in a comparison against it. It is meant to be merged into the same-named framework block when that
pull request lands, section by section, and then removed.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Angular repository documentation: RxJS interop, takeUntilDestroyed, SSR, hydration, zoneless, DI providers, DI troubleshooting, typed forms, signals overview, releases and update paths (repository snapshot of 2026-10-07, MIT, Google LLC) | MIT, read 2026-10-08 | §1, §2, §3 and §5 in full, the `untracked` and `asReadonly` points of §4, the token-identity rule |
| The Angular repository source: the application-initializer module's API comments | MIT, read 2026-10-08 | `APP_INITIALIZER` deprecation, `provideAppInitializer` behaviour |
| The angular-eslint rule documentation (rationale text of about 17 rules) | MIT, read 2026-10-08 | §4 in full |
| One MIT Angular skill set (RxJS interop, DI, tooling, forms skills) | MIT, read 2026-10-08 | No-`BehaviorSubject`-as-state, global destroy subject leak, `nonNullable` forms, the "never force" update point |

A second Angular skill collection was read as a counter-example only and used for nothing.

## Rewrite notes
Rules are re-explained principle first. The stability, transfer-cache and event-replay rules restate the
documentation; the verification lists are ours. The documentation snapshot is a main-branch one: it mentions
a service decorator and a zoneless default from version 21, so the version in use must be checked.

## Not verified
1. **The operator-choice guidance** (latest, ignore-while-busy, parallel, ordered) from the review list was
   dropped: no Angular or RxJS document read states it, and it was not written from memory.
2. **`ngSkipHydration` on non-host nodes** throws per the documentation; not run.
3. **`withEventReplay()` default**: the documentation says replay is enabled with incremental hydration; whether
   a given version enables incremental hydration by default was not checked.
4. **`APP_INITIALIZER` deprecation version (19)** is from the API comment, not from a release note.
5. **Nothing here was run.** Every behaviour stated, including the exact error names (NG0203, NG0506, NG0991),
   is as documented.
6. **Dropped from the review's list:** `hostDirectives`, `ViewEncapsulation.None` guidance, signal-store
   advice, i18n library choice, and the output naming rules (P3): no source read for them supports a rule.
7. **Written by us, not sourced:** the verification lists and the output/checkpoint paragraph of `SKILL.md`.

## Related blocks
`accessibility`, `webperf` (images, layout shift), `security-hardening` (untrusted HTML), `testing-anti-patterns`,
`typescript-patterns`.
