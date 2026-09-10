# mentis: block catalogue & sourcing backlog

> **mentis = superpowers, the in-house version, one we control.** A framework *of our own*,
> continuously enriched by **rewriting** (rule B, `CONVENTIONS.md`) the best ideas/agents from
> other repos on the market, never by depending on them. This file holds: **1)** what we have,
> **2)** what we could rewrite to complete/improve it. Living document: we extend it as we go.
> Statuses: 🟢 used on real production work / ✅ rewritten here (idea taken and reworked) / 🟡 written, not
> dogfooded yet / 🔜 to wire up / 🔎 to mine / ✕ ruled out. **🟢 is the only one that means "proven"** — ✅
> says the rewrite is done, not that anyone has run it.

## 0. Audit vs an org skill catalogue (2026-08-06)

The catalogue audited ships **211 skills** across ten plugins: laravel 45, flutter 37, react 36, nuxt
21, python 20, csharp 15, global 14, design 10, project-management 9, design-patterns 4. It is versioned and
org-wide, so **where it is installed it is the authority on the house style** — its package lists, its
internal libraries, its tracker charter, its design tokens.

**The resolution changed on 2026-08-06, deliberately** (see the two entries at the end of this section). The
first pass drew a boundary per block and deleted the mentis side of each overlap. That pass ran on two blocks
before the direction was reversed: deferring means a block **stops working when the catalogue isn't
installed**, which is rule A's soft-dependency failure — and mentis is meant to hold up on a plain repo with
nothing installed. So the rules were **mined, de-identified and rewritten generically** instead, and the
boundary now runs the other way: mentis carries the generic default, the catalogue overrides it as a house
style where present. Nothing naming an internal library, package list, product, tracker or design value
crossed over (rule C).

| Subject | Catalogue counterpart | Where it landed in mentis |
|---|---|---|
| Cross-language rules | `global` (14) | **`skills/code-baseline`** (new): no comments, no ticket refs, no AI attribution, file ceiling, no god classes/bag-names, domain exceptions, external APIs behind an owned client, parsed files as typed objects, distinct concepts as distinct types, tests owed by new behaviour, diff coverage |
| Laravel | `laravel` (45) | **`skills/laravel-conventions`** (new): thin models, events over observers, permissions not roles, no DB enums, no cascade, no queries in loops, validation, typing, naming, config, seeders, soft-delete pruning, job ordering, REST shape, test tiers. `php-patterns` stays on the language below it |
| Flutter | `flutter` (37) | **`skills/flutter-conventions`** (new): context across async gaps, disposal, decomposition, constraints, the four async states, routing, forms, state management, secure storage, permissions, tests |
| Vue/Nuxt | `nuxt` (21) | `skills/vue-nuxt-vuetify-conventions`, rewritten self-contained (13 sections) |
| React | `react` (36) | `skills/react-nextjs-conventions`, rewritten self-contained (10 sections) |
| Python | `python` (20) | `skills/python-conventions`, rewritten self-contained (8 sections) |
| C#/.NET | `csharp` (15 at mining, 37 at the 2026-09-07 bodies pass) | `skills/dotnet-conventions`, rewritten self-contained (7 sections: §7 and 10 points added 2026-09-07; sectioned into `references/` and deepened 2026-09-08, 3,167 → 6,976 words of rules, every section and point number preserved, none added; **dogfooded once 2026-09-09** on a small .NET 9 solution in the SDK container, 36 tests green, which closed five gaps the *build* found rather than a reading: CA1822 turning a stateless collaborator into a static class with no position in the block (§2.15), `ValidateOnStart` validating nothing without a registered validator and its own package (§2.16), §4.15's explicit enum numbering plus §7.8's missing fallback arm failing to compile under warnings-as-errors (§7.10), `InvariantGlobalization` turning §6.5's human-facing half from a wrong result into an exception (§6.13), and CA1707 making every underscored test name an error, i.e. the analyser scoping the guardrail implied and never stated; **widened against the current platform 2026-09-09**, two new sections — §8 resilience and throttling, §9 what only breaks at publish — plus nine points from the vendor's own current documentation, 7,490 → 9,727 words, x7.57 → **x5.83**); **widened 2026-09-09**, §9 gained three points against current public Native AOT/trimming guidance (suppressed warnings, AOT's inability to generate code at run time, reading a package's own compatibility from publish warnings rather than assuming it), 9,727 → 9,957 words, x5.83 → **x5.7**); **widened again 2026-09-09**, §8 gained two points against
current public HTTP-resilience/rate-limiting guidance (never stack more than one resilience handler
per client; outbound rate limiting needs its own token-bucket-style strategy, distinct from inbound
throttling), 9,957 → 10,104 words, x5.7 → **x5.61**); **widened again 2026-09-09**, §5 and §3 each gained points
(async-dispose ownership, guarded double-dispose, generic nullability constraints; authorization-
handler short-circuit, real-time connection re-validation), 10,104 → 10,432 words, x5.61 → **x5.44**); **widened 2026-09-10** via a background pass on the three thinnest remaining sections — §7 language idioms (`nameof` scope, list patterns, `u8` literals, `global using`, `params` collections), §1 async/cancellation (linked token sources, single-use `ValueTask`, `AsyncLocal` flow, `IProgress<T>`'s synchronization-context capture) and §4 types/visibility (the `file` access modifier, `readonly struct`, static abstract members/generic math, partial properties) — sourced from current public .NET documentation, 10,432 → 11,762 words, x5.44 → **x4.82**); **widened again 2026-09-10**, a larger background pass over five sections — §2 dependencies/logging (`HttpClientFactory` registration, decoration at the root, logging scope, a `BackgroundService` crashing the host, cross-field `IValidateOptions`), §3 authorisation (resource-based authorisation, a custom `IAuthorizationRequirement`, output caching leaking across users, minimal-API endpoint filters, a job storing identity), §6 data access/portability (`DbContext` pooling and leaked state, per-query `AsSplitQuery`, `SaveChangesInterceptor`, filtered `Include`, compiled models), §8 resilience/throttling (telemetry on retries, inbound/outbound partition keys, load-shedding vs queueing, fallback strategy, chaos/fault injection) and §9 publish-time failures (`GeneratedRegex` vs `RegexOptions.Compiled`, `RequiresUnreferencedCode`/`DynamicallyAccessedMembers`, `TrimmerRootAssembly`, AOT vs ReadyToRun, the config-binding source generator) — sourced from Microsoft Learn/ASP.NET Core/EF Core current docs, 10,880 → 14,286 words, x4.82 → **x3.97**); **widened a third time 2026-09-10**, a background pass over §1 async/cancellation (`Parallel.ForEachAsync`, `PeriodicTimer`, thread-pool starvation), §3 authorisation (`IClaimsTransformation`, on-behalf-of tokens, GraphQL/Blazor auth), §5 disposal/nullability/enumeration, §8 resilience/throttling (distributed rate limiting, `SocketsHttpHandler` pooled-connection lifetime) and §9 publish-time failures (globalization-invariant mode, Native AOT interop/ReadyToRun) — sourced from Microsoft Learn/.NET Blog, 14,286 → 17,138 words, x3.97 → **x3.31**); **widened a fourth time 2026-09-10**, a background pass over §4 types/visibility (`ref struct`/`allows ref struct`, discriminated unions via sealed records, `protected internal` vs `private protected`), §5 disposal/nullability/enumeration (`[EnumeratorCancellation]`, linked `CancellationTokenSource`, object-pool reset), §6 data access/portability (concurrency tokens, `ComplexProperty`/owned types, keyset pagination), §7 language idioms (index/range operators, primary constructors) and §9 publish-time failures (Blazor WASM partial trimming, `DynamicDependencyAttribute`) — sourced from current Microsoft Learn/.NET Blog docs, 17,138 → 19,679 words, x3.31 → **x2.88**); **widened a fifth time 2026-09-10**, a background pass over §1 async/cancellation (`System.Threading.Channels`, `SemaphoreSlim.WaitAsync`), §2 dependencies/logging (`PostConfigure`/`ValidateOnBuild`, `ActivatorUtilities`, `IHostedService`), §5 disposal/nullability/enumeration (`WeakReference<T>`, `IMemoryOwner<T>`), §7 language idioms (`StringSyntaxAttribute`, extended patterns) and §8 resilience/throttling (Polly v8 strategy ordering) — sourced from Microsoft Learn/.NET Blog/Polly docs, 19,679 → 23,360 words, x2.88 → **x2.43**); **widened a sixth time 2026-09-10**, a background pass over §3 authorisation (resource-based authorisation), §4 types/visibility (`required`/`SetsRequiredMembers`), §6 data access/portability (EF Core compiled queries), §8 resilience/throttling (Polly v8 `Retry-After`) and §9 publish-time failures (Native AOT + MVC/RDG) — sourced from Microsoft Learn/.NET Blog/Polly docs, 23,360 → 26,730 words, x2.43 → **x2.12**); **widened a seventh time 2026-09-10**, a background pass over §1 async/cancellation, §2 dependencies/logging, §3 authorisation, §5 disposal/nullability/enumeration and §9 publish-time failures — sourced from current Microsoft Learn/.NET Blog docs (.NET 9/10, C# 13, ASP.NET Core 10), 26,730 → 29,969 words, taking `csharp` below x2 for the first time, x2.12 → **x1.89**); **widened an eighth time 2026-09-10**, a background pass over §1 async/cancellation, §4 types/visibility, §6 data access/portability, §7 language idioms and §8 resilience/throttling — sourced from What's New in C# 14 and EF Core 9/10 docs, 29,969 → 33,380 words, x1.89 → **x1.70**)
|
| Design system | `design` (10) | **`business/interface-design`** (new): token discipline, container decision tree, required screen states, button hierarchy, chips by kind, icon-text coupling, reference gathering — **house values deliberately excluded**; sectioned into `references/` and deepened 2026-09-08, 2,041 → 5,938 words of rules, §0 marked read-every-time, no section added |
| Story management | `project-management` (9) | `business/product-ownership` §6–§8: story anatomy, label discipline, criticality, review axes, review output, decomposition, estimation-needs-the-code |
| Patterns | `design-patterns` (4 at audit time, 7 as of 2026-08-11) | `skills/design-patterns` §4: the concrete entry condition per pattern (strategy, state, null object, object construction, value object, pipeline, transaction boundaries), on top of the whether-to-reach-for-one decision that remains ours |

Two subjects were **not** brought over, on purpose: mockup accessibility stays with `skills/accessibility`
(which cites its standard rather than a remembered number) and mockup copy stays with
`business/ux-writing` — both already own the rendered-code side, and a design-time twin would be the second
source `maintaining-blocks` §4 exists to catch. `go-conventions` and `java-conventions` have no counterpart
and are untouched.

**Same audit, applied to the `test-casebook` family** (MIT, `techmefr/*`, ours — `test-casebook` 1.1.0 for
the frontend, `test-casebook-back-js` 1.0.0 and `test-casebook-back-php` 1.0.0 for the backends, all three
on npm as of 2026-08-11): it ships the testing
doctrine *and* its executing agents (`test-writer`, `test-reviewer`) plus a plan-before-tests `PreToolUse`
hook. Resolution: **the package is the authority where installed** — `tdd` defers to it and `dozer` hands
over to `test-writer`, keeping only the default-FAIL contract, which must hold in a repo with nothing
installed. Nothing is removed from the package: its agents are referenced throughout its own `AGENTS.md`
and per-stack guides, so cutting them to protect our roster would gut a working product. And the two hooks
are **not** duplicates — one refuses a test with no plan, the other refuses a pass with no evidence; they
chain. Detail in `references/README.md`.

**What the deletion pass found before it was reversed, worth keeping.** Reading the catalogue closely to
decide what to cut surfaced **two rules in mentis that contradicted it**, not merely duplicated it: a Vuetify
need-to-component table routing transient notifications to a snackbar the catalogue explicitly bans, and a
"macros only, never the runtime props form" rule its typing skill prescribes the opposite of. Both are gone.
That's the real argument for the audit: a second source doesn't stay a duplicate, it drifts into a
disagreement, and the block that drifts is the one nobody re-reads. Two further conflicts are now stated
rather than hidden — `type` vs `interface` and where tests live differ **between** catalogues, so the generic
blocks say "pick one and apply it uniformly" instead of picking for you.

**What the catalogue completed in mentis** (same pass): it revealed two stacks clearly worked on that our
roster ignored — Python (20 skills) and Flutter (37) — with `elrond` routing an MR on either of them **nowhere**.
Fixed by adding `samwise` and `faramir`, plus updating `elrond`, which had also gone stale on
`frodo`/`boromir`/`theoden` (it still routed only three stacks out of eight). It also revealed **three whole
subjects mentis had no block for at all**: the cross-language floor (now `code-baseline`), the Laravel
framework layer (now `laravel-conventions` — `php-patterns` had explicitly stopped at the framework boundary
and nothing picked it up), and mobile (now `flutter-conventions`). Those three are the clearest value of the
audit: not deduplication, but three gaps nobody had noticed.

**The one duplicate found inside mentis, now fixed:** the eight per-stack readers each carried ~150 lines of
identical GitLab plumbing (prefetch, batching, the two modes, existing discussions, the inline-posting payload
and its four traps). `samwise` and `faramir` pointed at `boromir` for it rather than copying it again, which was
a stopgap — an agent reading another agent's file inherits its stack bias too, so that is not a shared
mechanism. It now lives once in `references/mr-review-plumbing.md`, cited by all eight; each agent keeps only
its own default mode and file paths. The five stack readers dropped to ~40% of their previous length
(gimli 225→106, legolas 186→71, frodo 188→76, boromir 211→95, theoden 209→92) and `aragorn` kept its numbered
structure with §10 as the pointer.

**The same duplicate had grown back everywhere else in those files, and was extracted on 2026-08-14:** the
plumbing pointer had been factored out, but the role, the memory, the loop, the tools, the prohibitions, the
two modes, the fresh-context guarantee, the trace and the base comment style had drifted back into eight
near-copies — 93 to 96% similarity against `aragorn`, for 92 KB paid on every reader spawn and doubled when
`elrond` runs two in parallel. That trunk now lives once in `references/review-core.md` (9 KB), and each reader
keeps only its calibration, its scope, its default mode, its rule sources, what it looks for and its style
delta: 89 KB → 40 KB across the eight. A fix to the loop is now written once instead of eight times.

Worth stating plainly, because it was first written up as a token saving and it isn't one: a single review
now loads 4 KB of reader plus 10 KB of core, against 11.5 KB of reader before — about 2 KB *more*. The
eight are never loaded together, one reader runs at a time. This is a maintenance change, and the token
work of the same day is elsewhere: the frontmatter descriptions (41 KB → 23 KB on every session) and the
five oversized convention blocks (a task touching two sections loads 9 KB rather than 26 KB).

**The output side, same day:** shrinking what an agent reads did nothing about what it writes, and
`doc/HOW-WE-WRITE-OUR-AGENTS.md` §5 had been claiming "short output by default" as a cross-cutting
guarantee with no mechanism behind it since it was written. `references/terse-reporting.md` is that
mechanism, cited from the `TRACE` section of the seventeen report-producing agents and from
`review-core.md` §8. It governs the report, never the artefact — an MR comment, an ADR and a commit
message keep their own register — and it exempts the three things a terse register actually breaks:
negation and polarity, the verdict word, the confidence level. Evidence stays quoted in full.

No duplicate found **inside** mentis otherwise: the pairs most at risk were checked — `bug-triage` vs
`qa-exploratory-testing` (report handling vs pre-merge discovery), `security-hardening` vs `seraph`
(writing-time vs audit-time), `debug` vs `when-stuck` (a bug with a cause vs the approach itself),
`over-engineering-review` vs `simplify` (lists vs applies), `internal-communication` vs `handoff`
(human vs agent), `content-creation` vs `social-publishing` (worth publishing vs publishing it).

## 1. Block registry

### Skills: the pipeline (`WORKFLOW.md` §2)
| Block | Step / layer | Origin (idea rewritten) | Maturity |
|---|---|---|---|
| start-feature | 0 (worktree) | a market worktree-management skill, rewritten | 🟡 (rewritten 2026-08-06: it called a local orchestrator's MCP tools directly, which broke rule B and made step 0 undistributable — plain git is now the default path, the orchestrator optional. Same correction in `using-mentis`, `plan`, `brainstorm`, `finish`) |
| brainstorm | 1 | native `brainstorming` | 🟡 |
| spec | 2 | a market skill catalogue (grill-with-docs) + internal; **sectioned and deepened 2026-09-08** — the block was 140 rules words, five numbered steps and nothing else, the thinnest in the repo, and became five sections under `references/` in the same order with a router table in `SKILL.md` (140 → 3,689 words of rules, taking the `project-management` row from x4.7 to x1.29 together with `product-ownership`). Written as a procedure, it named the five deliverables and never said what makes each one *correct*: recording an answer in the words that were used rather than a paraphrase that hides the misunderstanding, "not decided" versus "not said", naming the fixture each criterion needs so `tdd` does not discover the case cannot be built, saying where a result is observable since that is what picks the test's tier, a definition stating what a term *excludes*, an exclusion that is really a dependency being labelled as one, and a deliberate *non*-decision earning an ADR because the absence is invisible in the code. The pass also settled which block owns acceptance criteria: `business/product-ownership` §4 owns what makes a business criterion valid, §3 here turns it into the technical contract and now points there instead of restating it | 🟡 |
| archi | 3 | internal graphify + a three-way dedup pass (name, shape, call site) with the negative result recorded | 🟡 (dedup mechanism written, not dogfooded yet) |
| plan | 4 | a market skill catalogue (planning-and-task-breakdown) | 🟡 |
| tdd | 5 | our own `test-casebook` + market long-running agent patterns (default-FAIL contract); the no-test-tampering sibling rule for the code step added 2026-08-11 | 🟡 |
| code | 6 | native + internal; no-test-tampering guardrail added 2026-08-11, named directly by the operator | 🟡 |
| nuxt-no-props-destructure | 6 | `vue-nuxt-vuetify-conventions` §1.9 extracted to its own trigger, 2026-09-09, narrow-trigger + pointer pilot | 🟡 |
| nuxt-child-never-mutates-prop | 6 | `vue-nuxt-vuetify-conventions` §1.14 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| nuxt-define-store-once | 6 | `vue-nuxt-vuetify-conventions` §2.4 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| nuxt-no-hydration-nondeterminism | 6 | `vue-nuxt-vuetify-conventions` §9.1–§9.2 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| nuxt-semantic-element-first | 6 | `vue-nuxt-vuetify-conventions` §7.1 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| vue-nuxt-vuetify-conventions | 6 | several market Vue/Nuxt/Vuetify skill catalogues (Vue patterns, Nuxt4, Nuxt composables, Vuetify) + a market Nuxt/Vue linter (correctness/security) + a market open source TypeScript project (a11y/bundle) + de-identified internal review feedback (recurring patterns); re-checked directly against the public vue.doctor/nuxt.doctor tools on 2026-08-10, which surfaced 2 real gaps (compiler-macro import, useAsyncData key default) now closed; §13 added and §4 deepened 2026-09-07 by a **bodies pass** over the same org catalogue (21 skills): the first pass had read descriptions only, the bodies carried four mechanisms it could not see — BEM's out-of-scheme shapes, the class/style split and its extract-to-computed threshold, opting a folder into the framework's import scan, and the typed-client layer whose real weight is the hydration-typing trap and the shared applied state between two handles on one record; **depth pass 2026-09-08** on the three thinnest sections (§10 realtime 113 → 875 words, §2 composables/stores 211 → 944, §3 typing 174 → 899), which stated rules without the failures they prevent — two of the additions are real absences rather than restatements: module-scope state shared *across SSR requests* (a cross-account leak the block never named) and a private channel "authorised" by a name the client itself composes; **second pass the same day** on §7 accessibility (172 → 899) and §6 i18n (199 → 877), both of which were true-but-terse checklists — §7 gained the placeholder-as-label, unattached-error, colour-as-sole-meaning, removed-focus-outline, hover-only-action and no-page-language failures plus the voice-control consequence of an accessible name that omits the visible text, and §6 the mistakes that are correct in the source language and wrong elsewhere (a `n > 1` ternary for plurals, concatenated sentences, a translation rendered as HTML, hand-formatted dates, German's ~30% expansion, one key reused for two meanings); **widened 2026-09-10** via a background pass on the five thinnest sections — §1 shape/component (`defineModel`, generic components, `useTemplateRef`), §8 component library (density, dynamic slots, Vuetify migration), §10 realtime/events (SSE vs WebSocket, fan-out cost, backoff), §11 reactivity/security/correctness (CSRF cookie flags, `markRaw`) and §12 recurring review patterns (prop drilling, watch vs computed) — sourced from current vuejs.org/vuetifyjs.com docs, 12,625 → 14,503 words, taking `nuxt` from x1.57 to **x1.37** | 🟡 |
| react-nextjs-conventions | 6 | a market React skill catalogue (best practices) + a market React/Node skill catalogue (redux-toolkit) + a market shadcn skill catalogue + a market React linter (correctness/security section) + a market open source TypeScript project (a11y/bundle); re-checked directly against the public React Doctor tool (react.doctor) on 2026-08-10, which surfaced 3 real gaps (prop drilling, setState-count/useTransition, missing alt) now closed; **depth pass 2026-09-08 on all ten sections** (3,002 → 10,476 words of rules), each original rule kept verbatim and given the mechanism plus what a reader sees when it breaks — the additions that were real absences rather than elaborations are a `NEXT_PUBLIC_` variable as published content, a Server Component's props being serialised into the HTML payload, a cookie-only `POST` route handler having no origin check where a Server Action does, changing the wrapper element unmounting the subtree it wraps, a cleanup running on every dependency change, browser-seeded state breaking hydration, a query key missing an input so two requests share a cache entry, and reading cookies opting a whole route tree out of static rendering | 🟡 (written, not dogfooded yet — depth is not dogfooding, and this block still has no React repo behind it) |
| over-engineering-review | 9 | a market deletion-oriented review tool (deletion angle, tags, net line score) | 🟡 |
| nestjs-node-conventions | 6 | a market NestJS skill catalogue + an advanced market TypeScript skill + a market React/Node skill catalogue (prisma/trpc/zod) | 🟡 (written, not dogfooded yet; first mentis block for the Node backend) |
| inertia-conventions | 6 (new 2026-08-11) | official Inertia.js documentation (shared data via `HandleInertiaRequests`, `useForm`, partial/lazy/deferred reloads) + current Laravel+Inertia integration practice (typed props from the same DTO/resource, Laravel Precognition); §4 (the override against `laravel-conventions`/Nuxt-Next-specific sections) is ours, written after a real conflict: a Laravel+Inertia repo reviewed against REST/lomkit and Nuxt-runtime expectations that don't hold for that architecture, and neither this repo nor the installed org catalogue (its Laravel and Nuxt plugins) covered Inertia at all before this; §4.5/§4.6 went through two revisions the same day — a project-level "is the REST package a dependency" test was too coarse for a project running **both** Inertia (pages) and the REST package (a separate real API) at once, a real reported case; the fix checks the specific controller (what it returns, where it's routed) instead; §4 point 7 added 2026-08-11 — a CdP running the fixed version still had their own Claude session say "conflict between mentis and the house rules" and deleted their whole setup over a case that was already resolved, so every stack block's override paragraph now says explicitly to apply the resolution and move on, never report it as an open conflict; **sectioned and deepened 2026-09-08** — the five sections that lived inline in `SKILL.md` moved to one file each under `references/`, a sixth was added, the router became a table of triggers, and every section took the same depth pass as the sectioned blocks (1,705 → 6,679 words of rules, taking the `laravel` row from x5.82 to x4.27). §4 kept its number and every point number inside it, because three other blocks cite it and this block's own guardrails cite §4.5/§4.6; tests moved from §5 to §6, which nothing outside the block cited. The new §5 is the visit lifecycle, on which the block had said nothing: scroll and local state reset on every visit unless preserved, the cancelled-visit rule that makes a search box correct for free, an asset version that has to be wired to the build or a browser open across a deploy keeps running the old bundle, page data living in the browser's history entry and so surviving a logout on a shared machine, prefetch issuing real requests against `GET` routes with side effects, SSR being an optional second process. The other addition worth citing is what the reader can actually read: a page's props are in the HTML and in devtools whether a component renders them or not (§2.6), which is why authorization belongs in the controller before they are computed (§1.8) and why a negative assertion is the only test that catches a leak (§6.5) | 🟡 (no in-house Inertia production experience yet; `laravel-conventions` §6 and `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`' intros now point here) |
| typescript-patterns | 6 | internal synthesis (real production experience from the operator on pure TS/JS) | 🟢 |
| php-patterns | 6 | PHP-FIG (PSR-12) + official PHP docs; re-checked directly against the PSR-12 text on 2026-08-10 — almost all of it is formatting already covered by Pint/PHP-CS-Fixer, `declare(strict_types=1)` was the one real gap (the one PSR-12 rule with runtime effect); §1.1 corrected 2026-08-11 against the real, installed org catalogue's Laravel plugin (`no-strict-types`) — Laravel deliberately omits the declaration at its framework boundary (loose scalars in from routes/requests/config, Larastan does the static enforcement instead), a real, dogfooded, currently-installed reversal of the PSR-12 default that neither this block nor `laravel-conventions` named explicitly until now; **sectioned and deepened 2026-09-08** — the three sections that lived inline in `SKILL.md` moved to one file each under `references/`, two were added, the router became a table of triggers (960 → 5,386 words of rules, finishing the `laravel` row at x3.45). §1 kept its number and §1.1 its position, since `laravel-conventions` §5.12 cites it by number as the rule it overrides. The new §4 (comparison, arrays and the standard library) and §5 (time, numbers and text) were completely absent and are pure language: `==` changing meaning for string-to-number comparison in PHP 8, `in_array` comparing loosely against what are usually allow-lists, `isset` versus `array_key_exists` on a key holding null, `+` being a union while `array_merge` renumbers, `array_filter` preserving keys so `json_encode` emits an object instead of an array depending on which element was filtered out, a by-reference `foreach` leaving a live reference the next loop overwrites with, `DateTime` mutating in place while returning itself, a date with no timezone taking the server's default, floats not holding decimals and integer overflow becoming a float in silence, byte-based string functions cutting a UTF-8 character in half so `json_encode` returns `false` and the response is empty, and the four function choices that are security decisions rather than style (`hash_equals`, `password_hash`, `random_int`, `preg_quote`); **dogfooded once 2026-09-09** on a small framework-free CLI (52 tests green, containers rather than installs), which closed four gaps that re-reading had not found: `createFromFormat` normalising an impossible day and reporting it as a warning with `error_count: 0`, so both plausible guards pass it (§5.15); a `DateInterval`'s `days` being unsigned with the direction only in `invert` (§5.16); `final` making a class undoubleable, where the fix is §3.2's interface and not deleting the keyword (§3.15); and the deep-copy fix in §3.9 being fatal on a `readonly` property up to PHP 8.2 and legal only from 8.3, measured both ways (§3.16) — plus a checkpoint that routed to `gate`/`gimli` and said nothing about framework-free PHP | 🟡 (sourced from the market, same uncertainty status as gimli (the operator is new to PHP) — one small dogfood CLI does not change that) |
| dotnet-dispose-what-you-own | 6 | `dotnet-conventions` §5.9–§5.10 extracted to its own trigger, 2026-09-09 — first non-web-framework stack in the narrow-trigger + pointer pilot | 🟡 |
| dotnet-no-swallow-exceptions | 6 | `dotnet-conventions` §5.5 (and the fire-and-forget note in §1) extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| dotnet-null-pattern-matching | 6 | `dotnet-conventions` §5.6 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| dotnet-no-ambient-static-state | 6 | `dotnet-conventions` §4.1 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| dotnet-options-lifetime-mismatch | 6 | `dotnet-conventions` §2.18 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| go-conventions | 6 | golangci-lint (errcheck/govet/staticcheck/gosimple/ineffassign/unused) + uber-go/guide; re-checked directly against the Uber Go Style Guide on 2026-08-10, filtered for what a linter doesn't catch mechanically — 3 real gaps closed (no panic in library code, comma-ok type assertion, os.Exit/log.Fatal confined to main()) | 🟡 (no internal production experience) |
| python-conventions | 6 | PEP 484/526/604/695/8 + ruff + mypy/pyright + an org catalogue (20 skills), mined and de-identified; re-checked against PEP 8/ruff on 2026-08-10, re-verified unchanged; **sectioned and deepened 2026-09-08** — the eight sections that lived inline in `SKILL.md` moved to one file each under `references/`, the router became a table of triggers, and every section took the same depth pass as the five already-sectioned blocks (1,629 → 7,697 words of rules). The real absences were in the two sections that were thin out of proportion to what can go wrong in them: §4 async (110 words) had nothing on `gather`'s failure semantics, unbounded concurrency, cancellation-as-an-exception or the fact that `async` provides no lock — only the absence of pre-emption between awaits — and §6 DI (69 words) had nothing on a dependency's lifetime being unable to exceed the lifetime of what it holds. The PEP 8 re-check note moved out of §5, where it was provenance sitting among the rules, into `references/origin.md`; **dogfooded once 2026-09-08** on a small stdlib-only project (a pipeline measuring this repo's own depth table into SQLite, 44 tests green), which found three real gaps now closed: the checkpoint required `ruff`/`mypy` while the block opened by claiming every rule holds with nothing installed, so on a project where installs are refused the checkpoint was unsatisfiable on compliant code and no fallback was stated (§8.17); §8 was phrased entirely in pytest's vocabulary so its most portable content read as inapplicable to a stdlib runner (§8.18); and §7 was mapper- and migration-tool-shaped with nothing for a database with no ORM — §7.8–§7.11 turned out fully portable and §7.18–§7.19 add the create-if-not-absent script that silently never migrates an existing database and the engine defaults a mapper would have handled. §4, §6 and the mapper half of §7 correctly stayed unread, which is the routing mechanism exercised once rather than asserted; **widened 2026-09-10** via a background pass on the five thinnest sections — §1 typing (`Protocol`/`TypedDict`/`ParamSpec`), §2 none/failures/exceptions (exception groups, `except*`), §3 naming, §5 structure/style and §6 DI/lifetimes (`contextvars`, `weakref`, `contextlib`) — sourced from PEP 484/526/604/695/612 and the stdlib docs, 9,239 → 11,224 words of `references/`, taking `python` from x1.88 to **x1.52**); **widened a second time 2026-09-10**, a background pass over the three sections not yet touched by the first pass — §4 async (`asyncio.timeout`, backpressure via `Queue`, `to_thread` vs a process, `shield`), §7 ORM/migrations (`pool_pre_ping`, autogenerate limitations, branched migration heads) and §8 toolchain/tests (fixture-scope leaks, `parametrize` combinatorics, Hypothesis) — sourced from asyncio/SQLAlchemy/Alembic/pytest/Hypothesis docs, 11,224 → 12,624 words, taking `python` from x1.52 to **x1.39**); **widened a third time 2026-09-10**, a background pass over §1 typing, §2 none/failures/exceptions, §3 naming, §4 async and §6 DI/lifetimes — sourced from PEP 698/742/728 and current asyncio/exception-group docs, 12,624 → 14,939 words, x1.39 → **x1.21** | 🟡 (no internal *production* experience, same status as go-conventions — one small dogfood project does not change that, and `samwise` keeps its question register) |
| python-no-implicit-truthiness | 6 | `python-conventions` §2.1–§2.2 extracted to its own trigger, 2026-09-09 — first non-Laravel stack in the narrow-trigger + pointer pilot | 🟡 |
| python-no-bare-except | 6 | `python-conventions` §2.8–§2.11 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| python-async-no-blocking-calls | 6 | `python-conventions` §4.4–§4.5 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| python-no-db-cascade-delete | 6 | `python-conventions` §7.1 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| python-no-magic-strings | 6 | `python-conventions` §3.7 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| code-baseline | 6 | an org cross-language rule set (14 skills), mined and de-identified; the floor every per-stack block sits on; §7 added 2026-08-11 from a 15th skill (`extend-dont-override`) added to the real catalogue after the original mining pass — narrowest-supported-mechanism-first before copying or replacing a vendor file; **depth pass 2026-09-08 on all eight sections** (4,397 → 9,129 words of rules) — the block with least room, since it was already the deepest here, so the additions are the failure modes the sections were silent on: catch scope, cleanup on the failure path and cause preservation in §3; the primitive-obsession family (two ids of one primitive type, units, money as amount-plus-currency, a boolean pair encoding one state, a nullable field carrying two meanings) in §5; timeout, retry-with-backoff, idempotency on an outbound write, testing the client at the transport layer rather than mocking the client, and the webhook receiver's own three rules in §4; §6 reframed around the debt rather than the doctrine; and five more shapes in §8, including enforced-on-the-happy-path-only and verify-by-reading-the-system's-answer | 🟡 |
| laravel-conventions | 6 | an org catalogue (45 skills), mined and de-identified; fills the framework gap `php-patterns` explicitly left open; re-checked against the company's own internal house documentation on 2026-08-11, 1 internal contradiction fixed (§1.1 said "action/service", `code-baseline` already bans the `*Service` bag-name — the source's explicit no-Service/no-Repository rule settled it) plus the explicit `boot()` prohibition added to §1.2; **bodies pass 2026-09-07** against the same catalogue, now 65 skills: 48 already covered, and the gaps closed were §11 (new — failures: throw rather than return, reporting is not handling, an HTTP-native exception rather than a render callback, no hand-rolled content negotiation), §1.4 (a concern trait owns its concept end to end, which corrected §1.1's "simple scopes"), §1.5 (recognising a state machine or a pipeline from Laravel-shaped triggers), §3.14 (pruning is deleting), §3.12 (widened to model/abstraction with the earned-by test), §4.5 (every table through its model), §5.8 (localised date accessors), §7.4 (a command runs more than once), §9.11 (a data change ships its seed data) and §10.3 (the support-window date); §10.6 landed 2026-09-07 from `laravel/boost` (github.com/laravel/boost, named directly, same rule-C carve-out as §10.5 — a real public first-party Laravel package) after the real, installed org catalogue's Laravel plugin stopped treating Boost as MCP-only: install it with `--skills`, not the MCP server alone, since the layer-package layout of §10.5 is how its own skill actually resolves; **widened 2026-09-10** via a background pass on the three thinnest sections — §2 authorisation (`Gate::before` for a super-admin bypass, Sanctum ability tokens, testing a 403 as a contract, a silently-discovered policy), §5 naming/typing/style (readonly promoted properties, predicate naming for booleans, an enum's backing-type choice, `final` by default) and §8 jobs/realtime (`ShouldBeUnique` vs `WithoutOverlapping`, presence channels, on-demand notifications, `ShouldBeEncrypted`) — sourced from current official Laravel documentation, 15,419 → 16,839 words of `references/`, taking the `laravel` row from x3.13 to **x2.99**); **widened again 2026-09-10**, a larger background pass over five more sections — §1 where-behaviour-lives (contextual binding, contract binding earned by a real second implementation, `Macroable` scope, provider grouping by domain, deferred-provider trade-off), §3 data-model/schema (custom casts, `Attribute::make`, composite index ordering, FK `onDelete` semantics, JSON column indexing), §4 queries (constrained eager loading, `morphWith`, subquery selects, `whereHas` vs join, transaction retry on deadlock), §6 HTTP surface (named rate limiters, conditional resource attributes, resource-collection pagination meta, custom validation rules, api/web middleware group defaults) §7 configuration/commands (`config:cache` as a deploy step, signature syntax, schedule timezone, task chaining, testing commands via `assertExitCode`), §10 architecture (contextual binding, deferred providers, middleware-group order, feature flags in config, Composer auto-discovery, facade resolution) and §11 failures (a queued job's `failed()`, retry idempotence, `Http::fake()` pitfalls, `ValidationException` vs a domain exception, 429/`Retry-After` as an expected failure, asserting exception content rather than only its class) — sourced from current official Laravel documentation, `laravel-conventions` reaching 16,536 words total, taking `laravel` from x2.99 to **x2.69**); **widened a third time 2026-09-10**, a background pass over §1 where-behaviour-lives, §5 naming/typing/style, §7 configuration/commands, §8 jobs/realtime and §9 tests/static-analysis (Larastan's level/extension model) — sourced from current official Laravel documentation, `laravel-conventions` reaching 20,682 words in `references/` alone, taking `laravel` from x2.69 to **x2.48**); **widened a fourth time 2026-09-10**, a background pass over §2 authorisation, §3 data-model/schema, §4 queries, §6 HTTP surface and §10 architecture — sourced from current official Laravel 12.x documentation, `laravel-conventions` reaching 22,315 words, taking `laravel` from x2.48 to **x2.25**); **widened a fifth time 2026-09-10**, a background pass over §5 naming/typing/style (PHP 8.3/8.4 typed constants, asymmetric visibility), §7 configuration/commands (Laravel Prompts, `Config::string`/`integer`/`boolean`), §8 jobs/realtime (`ShouldBroadcastNow`, `Concurrency::run()`), §9 tests/static-analysis (`Http::fake` sequences, `Mail`/`Queue`/`Event` fake assertions) and §11 failures (`Context`, `terminate()`, `dontReportDuplicates()`) — sourced from current official Laravel documentation, `laravel-conventions` reaching 24,847 words, taking `laravel` from x2.25 to **x2.1**); **widened a sixth time 2026-09-10**, a background pass over §1 where-behaviour-lives, §2 authorisation, §3 data-model/schema, §10 architecture and §11 failures — sourced from current Laravel 12/PHP 8.4 documentation, `laravel-conventions` reaching 27,572 words, taking `laravel` below x2 for the first time, x2.1 → **x1.96**); **widened a seventh time 2026-09-10**, a background pass over §4 queries, §6 HTTP surface, §7 configuration/commands, §8 jobs/realtime and §9 tests/static-analysis — sourced from current Laravel 12.x documentation (signed URLs, Sanctum abilities, cursor pagination, `Http::preventStrayRequests()`, `Bus::chain()->catch()`, Pest arch presets), `laravel-conventions` reaching 30,907 words, x1.96 → **x1.81** | 🟡 |
| laravel-no-db-enums | 6 | `laravel-conventions` §3.1–§3.3 extracted to its own trigger, 2026-09-09 — pilot for a narrow-trigger + pointer restructuring: the mechanism and the five-reason argument stay in the parent block, this file only narrows *when* the rule fires (a migration adding a fixed-set column) | 🟡 |
| laravel-no-cascade-delete | 6 | `laravel-conventions` §3.5–§3.10 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| laravel-no-observers | 6 | `laravel-conventions` §1.2 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| laravel-throw-dont-return-errors | 6 | `laravel-conventions` §11.1–§11.5 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| laravel-no-queries-in-loops | 6 | `laravel-conventions` §4.1–§4.2 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| laravel-scope-dont-check-after-fetch | 6 | `laravel-conventions` §2.4 extracted to its own trigger, 2026-09-09, second pilot batch | 🟡 |
| laravel-prefer-orfail-fetch | 6 | `laravel-conventions` §4.3 extracted to its own trigger, 2026-09-09, second pilot batch | 🟡 |
| laravel-mail-via-notifications | 6 | `laravel-conventions` §6.16 and §8.7 extracted to its own trigger, 2026-09-09, second pilot batch | 🟡 |
| laravel-no-fat-models | 6 | `laravel-conventions` §1.1 extracted to its own trigger, 2026-09-09, second pilot batch | 🟡 |
| laravel-no-magic-strings | 6 | `laravel-conventions` §5.3 extracted to its own trigger, 2026-09-09, second pilot batch | 🟡 |
| laravel-pruning-fires-delete-events | 6 | `laravel-conventions` §3.13–§3.14 extracted to its own trigger, 2026-09-09, third pilot batch | 🟡 |
| laravel-idempotent-data-commands | 6 | `laravel-conventions` §7.7–§7.9 extracted to its own trigger, 2026-09-09, third pilot batch | 🟡 |
| laravel-idempotent-seeders | 6 | `laravel-conventions` §7.12 and §9.10 extracted to its own trigger, 2026-09-09, third pilot batch | 🟡 |
| laravel-seed-new-features | 6 | `laravel-conventions` §9.11 extracted to its own trigger, 2026-09-09, third pilot batch | 🟡 |
| laravel-idempotent-jobs | 6 | `laravel-conventions` §8.2 extracted to its own trigger, 2026-09-09, third pilot batch | 🟡 |
| laravel-post-may-run-twice | 6 | `laravel-conventions` §6.15 extracted to its own trigger, 2026-09-09, fourth pilot batch | 🟡 |
| laravel-no-hand-rolled-content-negotiation | 6 | `laravel-conventions` §6.13 extracted to its own trigger, 2026-09-09, fourth pilot batch | 🟡 |
| laravel-api-breaking-changes | 6 | `laravel-conventions` §6.14 extracted to its own trigger, 2026-09-09, fourth pilot batch | 🟡 |
| laravel-precognitive-request-scoping | 6 | `laravel-conventions` §6.17 extracted to its own trigger, 2026-09-09, fourth pilot batch | 🟡 |
| laravel-support-window-date | 6 | `laravel-conventions` §10.3 extracted to its own trigger, 2026-09-09, fourth pilot batch | 🟡 |
| laravel-permissions-not-roles | 6 | `laravel-conventions` §2.1–§2.2 extracted to its own trigger, 2026-09-09, fifth pilot batch | 🟡 |
| laravel-strict-types-default | 6 | `laravel-conventions` §5.12 extracted to its own trigger, 2026-09-09, fifth pilot batch | 🟡 |
| laravel-date-via-localised-accessors | 6 | `laravel-conventions` §5.8 extracted to its own trigger, 2026-09-09, fifth pilot batch | 🟡 |
| laravel-recognise-state-machine-or-pipeline | 6 | `laravel-conventions` §1.5 extracted to its own trigger, 2026-09-09, fifth pilot batch | 🟡 |
| laravel-aggregate-in-database | 6 | `laravel-conventions` §4.5 extracted to its own trigger, 2026-09-09, fifth pilot batch | 🟡 |
| flutter-context-after-await | 6 | `flutter-conventions` §1's opening rule and §1.2 extracted to its own trigger, 2026-09-09, narrow-trigger + pointer pilot | 🟡 |
| flutter-no-controller-in-build | 6 | `flutter-conventions` §1.14 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| flutter-dispose-what-you-create | 6 | `flutter-conventions` §1.12–§1.13 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| flutter-four-async-states | 6 | `flutter-conventions` §4.1–§4.2 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| flutter-no-future-in-state | 6 | `flutter-conventions` §7.6 extracted to its own trigger, 2026-09-09, same pilot | 🟡 |
| flutter-conventions | 6 | an org catalogue (37 skills), mined and de-identified; replaced the earlier "no mobile block" position; §7 deepened 2026-08-11 against the company's own internal BLoC/Cubit documentation — the one section in this block now sourced from actual production use, not a catalogue description; **depth pass 2026-09-08 on all ten sections** (3,380 → 10,321 words of rules, x6.1 → x2.0), written from documented framework and platform behaviour since there is no production experience to draw on — the additions that were real absences are the device-level ones: a secure-storage read failing after the keystore is cleared, a session's data outliving a logout on a shared phone, the process being killed in the background, a permission revoked while backgrounded, a one-shot system prompt, an overflow being silent in release, the reader's font scale making a fitted row overflow, and a media query answering about the window rather than the widget; a stale `§1.2` citation for disposal (§1's disposal half starts at point 5) was found by doing the pass, and ten more references were realigned; **dogfooded once 2026-09-09** on a small Flutter app in the SDK container, 63 tests green and the analyser clean, which closed seven gaps — five of them surfaced by a failing test or a failed resolve rather than by reading: `on Exception` missing the half of the framework's failures that are `Error`s (§7.18), an awaited call into the holder saying nothing about whether it worked so a screen leaves on a failed save (§7.19), a status enum plus a nullable payload keeping the impossible combination representable (§7.20), a parse moved off the main isolate hanging a widget test rather than failing it (§8.18), the localisation generator being both a required generation step and an exact dependency pin (§9.16), an unconditional settle failing in under a second rather than never returning (§10.13 corrected) with `find.byType` matching the framework's own widgets (§10.17), and the composition root having nowhere to live in the two-layer split (§10.18); **widened 2026-09-10** via a background pass on the five thinnest sections — §1 the two mistakes that crash, §2 widgets/rebuilds, §4 screen states, §5 navigation and §6 lists/forms — sourced from current official flutter.dev/dart.dev documentation, 11,412 → 14,063 words, taking `flutter` from x1.82 to **x1.48**); **widened a second time 2026-09-10**, a background pass over §3 layout, §7 state-management, §8 data-storage/permissions, §9 text/motion/monitoring and §10 naming/structure/tests — sourced from flutter.dev/api.flutter.dev/riverpod.dev/dart.dev, 14,063 → 16,332 words, taking `flutter` from x1.48 to **x1.27** | 🟡 (no mobile production experience at all, `faramir`'s question register applies — neither the depth pass nor one dogfood app changes that) |
| java-conventions | 6 | Effective Java (Bloch) + SpotBugs/Error Prone + established Spring conventions; re-checked against Effective Java's item list on 2026-08-10, 2 real gaps closed (equals/hashCode contract, final-by-default) plus a Spring/JPA gap (lazy loading / N+1, mirroring python-conventions' ORM section) | 🟡 (sourced from the market, no internal production experience, same status as go-conventions) |
| seo | 6 | Google Search Central + web.dev (Core Web Vitals, structured data); re-checked item by item against the current SEO starter guide on 2026-08-10, 2 real gaps closed (hreflang, nofollow/anchor text) | 🟡 (sourced from the market, no dedicated SEO production experience in house) |
| accessibility | 6 | WCAG 2.2 (AA) + MDN + W3C ARIA APG; re-checked against the 6 success criteria genuinely new in 2.2 (not carried over from 2.1) on 2026-08-10, 5 real gaps closed (Focus Not Obscured, Dragging Movements, Target Size, Redundant Entry, Accessible Authentication Minimum), Consistent Help left out deliberately; **sectioned and deepened 2026-09-08** — the four inline sections moved to one file each under `references/` and the router became a table of triggers (1,027 → 3,896 words of rules). No section and no threshold was added: the four are the standard's own shape at component level, and every point added is a mechanism rather than a number, because a recalled threshold is the failure `skills/source-freshness` exists for. The five WCAG 2.2 points closed on 2026-08-10 kept their exact positions (§1.6–§1.8, §4.4–§4.5), since this block's own origin cites them by number. The additions are the failures the checklist stated no consequence for: headings as the *navigation* mechanism rather than typography, landmarks and a skip link, an undeclared page language selecting the wrong pronunciation rules, hover-only affordances that do not exist for a keyboard, a `role` *replacing* semantics rather than adding to them, a live region that has to exist before its content arrives, a state attribute set once at render asserting something wrong half the time, an accessible name that omits the visible label defeating voice control, `aria-hidden` over a focusable subtree producing a silent tab stop, a reader's font size being a different mechanism from browser zoom, the copied viewport attribute that disables pinch zoom, autocomplete metadata, the input type as an accessibility decision, and a disabled control announced as available while being unreachable by keyboard | 🟡 (sourced from the market, no dedicated a11y production experience in house) |
| qa-exploratory-testing | 8 (complement) | established exploratory testing literature (session-based testing) + ISTQB (boundary testing) | 🟡 (sourced from the market, no dedicated QA production experience in house) |
| devops-conventions | 6 (infra/CI) | 12-factor app + DORA metrics (Accelerate) + established GitOps/IaC practices; §2 point 4 (protected shared resources) added 2026-08-11 from the org catalogue's hard-interdiction skill on protected shared databases | 🟡 (sourced from the market, no dedicated production experience in house) |
| data-pipeline-conventions | 6 (data) | dbt conventions + DAMA-DMBOK (quality dimensions) + Kimball dimensional modelling; §1.4–§1.5 added 2026-09-07 from an org BI skill for handling supplied accounting files, read for its handling discipline rather than its format knowledge (never write back over the file someone handed you; confirm a destructive transformation before applying it) — §3.1 already held the raw-layer version at pipeline scale, the missing case was the ad-hoc one; **sectioned and deepened 2026-09-08** — the four inline sections moved to one file each under `references/` and the router became a table of triggers (749 → 3,212 words of rules), the **last single-file block counted in the depth table**. No section added; §1.4, §1.5 and §3.1 kept their numbers. None of the failures here announces itself, which is the depth: idempotence covering the *whole* run so an upsert followed by a log append or a notification is not idempotent, a partial run having to leave a state you can classify, a run keyed on the wall clock being unbackfillable, late-arriving corrections making a forward-only window stop matching the source, a quarantine with a published count rather than a silent skip, the *number* of failing rows being what makes an alert actionable, a validation with no owner getting loosened at the first inconvenient hour, duplicates being defined by a business key whose wrong choice deletes real data, a check reading the pipeline's own output passing on any consistent error, a deletion upstream being an event rather than an absence, reusing the source's key letting a renumbering rewrite your history, and incremental processing being correct only if you can say what "new" means; **dogfooded once 2026-09-08** alongside `python-conventions` on a small stdlib-only pipeline, which closed one real ambiguity: §2.4 said to quarantine the bad rows where blocking is unacceptable, and applied, that is impossible for half the checks — a duplicated key, a total disagreeing with its parts and an entity counted in two groups are properties of the *set*, so no row can be set aside; §2.4 now says the run is the quarantine unit in that case. §1.2, §1.4 and §2.7 were the three rules that carried the exercise with no translation needed | 🟡 (sourced from the market, no dedicated production experience in house) |
| auth-session-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate jwt/oauth-oidc/keycloak/auth0 agents, no equivalent here) + a documented internal incident on a token refresh flow + OWASP session management; §4 (reference login flow) extracted from our two real frontend implementations read side by side; re-checked directly against the OWASP Session Management Cheat Sheet on 2026-08-10, 3 real gaps closed (privilege-change invalidation, absolute session lifetime, Clear-Site-Data on logout) plus an explicit CSRF note | 🟢 (§4 describes code already in production on two frontends; the rest still to dogfood) |
| security-hardening | 6 | a market generalist dev skill catalogue (`security-and-hardening`) + OWASP Top 10/ASVS/escaping cheat sheets; the writing-time vs audit-time split is ours; **sectioned and deepened 2026-09-08** — the five inline sections moved to one file each under `references/` and the router became a table of triggers (1,030 → 4,144 words of rules). No section added: the five are the shape of a boundary. §3 kept its number (`business/data-protection` cites it) and §2.4 stayed the SSRF rule the 2026-08-10 OWASP check added. None of these failures is loud — a missing authorisation declaration returns the right data to whoever wrote it — so the depth is the skipped case: the boundary being the right place because it is *enumerable*, reject-don't-repair, request-binding accepting fields the interface never shows, a value from another system still being untrusted, escaping on input giving a database correct for one destination, a resolved-path check rather than a join, secrets in URLs reaching history and proxies, an outbound call spending its own credentials, authorising before the work, **default-deny**, every response *field* being subject to the endpoint's decision, a webhook's authorisation being signature verification, the lock file being the real inventory, an install step running with your credentials, and the negative test being the only proof | 🟡 (written, not dogfooded yet) |
| background-jobs-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate kafka/rabbitmq/bullmq/sidekiq/celery agents, no equivalent here) + established distributed-systems practice (at-least-once, idempotency keys, bounded retries, dead-letter) | 🟡 (written, not dogfooded yet) |
| webperf | 6 | a market generalist dev skill catalogue (`webperf`) + web.dev performance guidance + bundle-weight items from a market open source TypeScript project | 🟡 (written, not dogfooded yet) |
| domain-modeling | 3 | a recognised market skill author (`domain-modeling`) + DDD staples; states-not-flags is ours | 🟡 (written, not dogfooded yet) |
| deprecation-migration | cross-cutting | a market generalist dev skill catalogue (5 questions + 4 patterns) | 🟢 (direct rewrite, mechanism taken as-is) |
| api-design | 3 | a market generalist dev skill catalogue (Hyrum's law, One-Version Rule); **sectioned and deepened 2026-09-08** — the three inline sections moved to one file each under `references/` and the router became a table of triggers (375 → 2,392 words of rules). This was the thinnest block counted in the depth table, for the same reason `spec` was: a checklist of principles an experienced reader already agrees with and cannot apply under pressure, because the pressure comes from a change that looks compatible and is not — so the depth is a catalogue of those: **loosening is compatible and tightening is not**, widening a type breaking every parser written against the narrower promise, renaming being removal plus addition, a change to a field's *meaning* being breaking with the type unchanged, a default value being part of the contract, consumers depending on our *failures* so a changed status code turns careful retry handling into a duplicated write, an unspecified ordering being a choice made once by accident, and compatibility being verified by comparing the two schemas rather than remembered | 🟢 (direct rewrite) |
| observability-instrumentation | 6 | a market generalist dev skill catalogue (on-call questions, RED/USE, anti-cardinality); **sectioned and deepened 2026-09-08** — the four inline sections moved to one file each under `references/` and the router became a table of triggers, §1 marked read-every-time because it is what makes the other three judgeable (511 → 3,048 words of rules). No section added; §1 and §2 kept their numbers, cited from `skills/api-design` and `skills/security-hardening`. Instrumentation is written by someone who is not the person who will read it, at a moment that is not the incident, which is the gap the depth closes: cardinality being *multiplicative*, the pairs where one member is unbounded (route template vs raw path, error class vs error string), an average hiding the tail so the reader concludes the system is healthy, a counter resetting on deploy and reading as a drop, an error counter incremented only on the remembered branch reporting zero during an outage, a value interpolated into a log message defeating grouping, the correlation ID needing propagation across a queue, **duration as part of an alert's condition**, a percentage threshold paging on a single failure at a low-volume hour, and **alerting on absence** — the job that did not run | 🟢 (direct rewrite) |
| documentation-adr | 3 | a market generalist dev skill catalogue (5-6 field ADR template); "When"/Guardrails corrected 2026-08-11 against the real, installed org catalogue's cross-cutting plugin (`no-project-docs`) — an ADR is proposed, never committed as a file, unless asked, an ADR folder already exists, or the proposal is accepted; the original phrasing had this block volunteering a new doc file the moment a decision qualified; **sectioned and deepened 2026-09-08** — the four inline sections moved to one file each under `references/` and the router became a table of triggers (841 → 2,909 words of rules). No section added, and §1.2 and §4 kept their numbers, both cited from `skills/design-patterns` §5 and §4 also from `business/interface-design` §6. Every rule here is ignorable at no immediate cost — a missing field, a deleted record and an unnamed trade-off all produce a repo that works today — so the depth is the later reader: an ADR being its own file because its subject is a *moment* and a record kept in a comment gets edited until it describes the present, an indefinite status leaving half the codebase compliant with both halves citing the file, the alternatives field being the one dropped for time and the one that does the work, an unfillable field being a finding, both supersession links having to exist and the forward one being the one usually missing, an ADR contradicted by the code being a live defect that makes the whole log untrustworthy, and §4's asymmetry — the cost is readable in the code and the benefit is readable nowhere | 🟢 (direct rewrite) |
| wayfinder | cross-cutting | a recognised market skill author (parent ticket with 5 sections + typed children) | 🟢 (direct rewrite, adapted to Jira) |
| handoff | cross-cutting | a recognised market skill author (reference by path, never duplicate) | 🟢 (direct rewrite) |
| debug | support 6 | native `systematic-debugging` + a market skills repository (`root-cause-tracing`: backwards call-chain walk + stack capture; `defense-in-depth`: layered validation); the no-test-tampering rule (§3.4/Guardrails) added 2026-08-11, named directly by the operator — a coding agent editing a failing test's expectation instead of the implementation, which reports a regression as a passing suite | 🟡 (extended: our version named the goal but gave no technique to reach it) |
| when-stuck | cross-cutting | a market skills repository (`problem-solving/*`, merged; collision-zone-thinking dropped) | 🟡 (written, not dogfooded yet; first block here that isn't a convention) |
| testing-anti-patterns | 5 / review lens | a market skills repository (`testing-anti-patterns` + `condition-based-waiting`, merged: tests that report safety they don't have) | 🟡 (written, not dogfooded yet) |
| extract-conventions | setup/maintenance | graphify + recognised market skill authors | 🟡 (generates the references from the real code) |
| choose-model | cross-cutting | internal synthesis (no external source taken as-is) | 🟡 (grid written, not yet applied retroactively to all existing agents) |
| dispatch-parallel | cross-cutting | a market skill/agent framework (dispatching-parallel-agents + subagent-driven-development, merged) | 🟡 (written, partial experience via elrond→aragorn/gimli/legolas) |
| writing-skills | cross-cutting (meta) | a market skill/agent framework; step 7 (order by frequency, re-sort past ~10 points) added 2026-08-10 from the context-engineering lost-in-middle framing, distinct from the packaged `context-engineering` skill already ruled out below | 🟡 (written, applies the single template + rule B checklist) |
| writing-agents | cross-cutting (meta) | internal synthesis (formalises the 7-pillar template already in use) | 🟢 |
| testing-blocks | cross-cutting (meta) | a market skills repository (`testing-skills-with-subagents`: RED/GREEN/REFACTOR on behaviour, pressure taxonomy, record the rationalisation verbatim) | 🟡 (written; the obvious next move is to run it on itself) |
| distributing-blocks | cross-cutting | a market skills repository (`pulling-updates-from-skills-repository` + `sharing-skills`) | 🟡 (written; answers README stages 3-4, no consumer yet) |
| maintaining-blocks | cross-cutting (meta) | a market skills repository (`meta/gardening-skills-wiki`); the checks themselves are this repo's own past bugs | 🟡 (written; the first real run is the reference audit before a tagged release) |
| design-patterns | 3 / 6 | the Gang of Four catalogue as published on `refactoring.guru` (22 patterns, re-verified 2026-08-10, all 22 now carry an explicit verdict — subtracted, dismissed, entry-conditioned or escape-valve); the catalogue pages carry **no overuse caution**, which is the whole gap — recognise-don't-apply, the second-real-case threshold, the framework-already-does-it subtraction and the Repository-over-ORM verdict are ours; §4 grew 3 more entries 2026-08-11 (value object, pipeline, transaction boundaries) from the real, installed org catalogue's design-patterns plugin, which had grown from 4 to 7 skills since the original mining pass — these are real recurring shapes outside the 22-pattern GoF set, not a gap in that set; **sectioned and deepened 2026-09-08** — the five sections that lived inline in `SKILL.md` moved to one file each under `references/`, a sixth was added, the router became a table of triggers (2,347 → 6,333 words of rules, x5.19 → x1.92); **widened against the org catalogue's own stack-specific implementation files 2026-09-09** — three points in §4.7 (flush-not-commit, savepoints, model events firing inside the boundary), seven more points in §4, and a brownfield rule in §1, 6,333 → 7,369 words, x1.92 → **x1.65**. §4 kept its number and every point inside it, since `business/fintech-compliance` cites §4.5 and `laravel-conventions` cites the transaction rule at §4.7 twice; §2's bullets became numbered points, text unchanged. The new §6 (when a pattern stops earning its place) closes a structural gap rather than an oversight: the source catalogue, and every section here, was about whether to *add* a pattern, and nothing said when to take one out — hence the deletion test, the interface whose second implementation was decommissioned, the pool justified by a measurement on a runtime since upgraded, the pattern grown to fit a case that does not share its axis, the suite with a test per implementation and none for the dispatch, and the ADR line that outlives the structure and gets the pattern reimplemented from the document. Two stale references into this block were fixed in the same pass: `laravel-conventions` §4 and §8 both cited a §7 this block has never had; **widened 2026-09-10** via a background pass on §1 recognise/don't-apply, §2 framework-already-does-it, §3 where-they-earn-their-place, §5 use-the-name-correctly and §6 when-it-stops-earning — sourced from public code-smell literature (Beck/Fowler, the rule of three) and the classic GoF pattern definitions as generally documented — 7,369 → 9,393 words, taking `design-patterns` from x1.65 to **x1.3** | 🟡 |
| shell-scripting-conventions | 6 | public defensive-shell baseline (`set -euo pipefail`, quoting, `shellcheck`); §2 and §4 are this repo's own `verify-gate.sh` bugs — fail-open on a missing parser, dropped exec bit, CRLF from Windows | 🟡 (the four bugs it prevents were real, so the content is validated even though the block hasn't been run as a block) |
| bug-triage | 7 (entry) | local video-reading Claude skills (`claude-real-video`, `watch-video-skill`: scene-change frames + dedup + subtitle-or-Whisper transcript on `ffmpeg`, MIT) for the evidence step, named as optional so nothing depends on it; the queue framing is native Claude Code (`/loop`/`/schedule`, proactive loops); the rest is ours — observation vs the reporter's theory, "cannot reproduce" owing its own evidence list, severity by impact | 🟡 (fills a real pipeline hole: `debug` assumed a runnable failing case) |
| product-ownership | product | an org catalogue's 9 story-management skills, mined and de-identified (anatomy, review axes, criticality, estimation); public sources for given/when/then criteria and definition-of-ready/done; §8.2/§8.3 and §9 added 2026-09-07 — the catalogue's tenth skill (decomposition behind a hard confirmation gate, the tracker write being a consequence of an approved plan) plus two rules from a real organisational change: a story is sized to one MR, and §9 covers the configuration where the story's author builds it, naming what replaces §7's independent reader (the epic above, the fresh-context gate below) instead of pretending the separation survives; **sectioned and deepened 2026-09-08** — the nine sections that lived inline in `SKILL.md` moved to one file each under `references/` and the router became a table of triggers (2,952 → 7,616 words of rules, taking the `project-management` row from x4.7 to x1.29 together with `spec`). §6 to §8 kept their numbers, since `references/README.md` and this file both cite that range. No section was added: the nine already covered the subject, and what they lacked was the mechanism and what the reader actually sees — a request phrased as a solution smuggling in a decision nobody took, an ordering that optimises for whoever asked loudest, a refusal naming no alternative coming back unchanged next week, a criterion nobody can build a fixture for, a "done" resting on somebody's memory of the conversation, and an estimate given without the code being an estimate of the story's wording; **widened 2026-09-10** via a background pass on §3 saying-no, §4 acceptance-criteria and §5 ready-and-done (plus `skills/spec` §1 the-interview and §4 out-of-scope, same pass) — sourced from public product-ownership/agile literature (prioritisation frameworks, three amigos, MoSCoW's won't-have vs deferred, anchoring/confirmation bias in interviews), taking `project-management` from x1.26 to **x1.07** | 🟡 (ours is the priority/refusal/criteria layer and tying "done" to the two guarantees; the tracker mechanics stay out) |
| community-management | communication | a marketplace community-management skill (moderation policy templates, engagement ladder, DAU/MAU + member-to-member replies + support deflection as metrics, "what you tolerate in the first hundred members becomes the culture") + a B2B SaaS social-media-manager skill for crisis response | 🟡 (no internal CM expertise; §4 — what a CM must never answer alone — is ours and is the failure we actually expect) |
| content-creation | communication | an MIT marketing skill collection (34 skills), a LinkedIn growth set, a YouTube creator set and several repurposing skills — the repurposing insight taken, plus the observation that per-network work differs mainly in hook and length; none of them reviews or fact-checks a claim, and all start from a topic rather than from an artefact | 🟡 (no internal content expertise; §2's artefact→format table and the honest-hook line are ours) |
| social-publishing | communication | a community social-media skill suite (`social-ai-team`, 10 skills) for its pause-and-approve gate at every handoff; its per-platform writers rejected as fragmentation, the volatile facts moved to `references/social-platforms.md` | 🟡 (no internal social-media expertise; the access table is the part with a six-month expiry) |
| internal-communication | communication | standard async-writing practice + separating criticism of code from criticism of the author; §3.4 and §4 come from real review experience (short comments get acted on, a point restated three times becomes personal) | 🟡 (no internal comms expertise; anything calibrated on a named colleague deliberately excluded under rule C) |
| source-freshness | cross-cutting (meta) | Anthropic's `claude-for-legal` suite (freshness gate + `[verify]` tag), generalised from legal reference content to version-pinned framework facts; `context7` wired as the retrieval side, authoring-time only; §3.5 (closed-enumeration refresh) added 2026-08-10, generalising the technique used to re-check design-patterns/security-hardening/react-nextjs-conventions/vue-nuxt-vuetify-conventions against their named external catalogues | 🟢 (dogfooded four times before being written up here) |
| portless-ready | setup/infra | a market portless tool (wiring is ours) | 🟡 (makes a stack portless: HTTPS alias + port hygiene) |
| **gate** | 7 | market long-running agent patterns (`default-FAIL hook` + `fresh-context evaluator`); the `NEEDS_WORK` loop back to `code` is native `/goal` (goal-based loops), not a block | 🟡 (agent `galadriel` + the `hooks/` pair written and unit-tested against 6 cases; per-repo wiring still to do) |
| review | 8 | a recognised market skill author (two-axis code review) + the house agents + native | 🟡 |
| simplify | 9 | native `simplify` | 🟡 |
| ship | 10 | internal (`/SHIP`, gandalf) | 🟡 |
| finish | 11 | internal, plain git — rewritten from an orchestrator teardown step with no dependency on it | 🟡 |
| merge-worktree | 11 | a market context-engineering kit (`git-worktrees`) | 🟡 |

### Business layer (`business/`, weaker contract: no gate, no evidence, 🟡 ceiling)
| Block | Function | Origin (idea rewritten) | Maturity |
|---|---|---|---|
| data-protection | legal | GDPR text + published regulator guidance; the engineering consequences (logs/URLs, search indexes and backups surviving a deletion, exception reporters exporting data, non-prod copies) are ours | 🟡 (no internal legal expertise; shaped as "which questions reach a lawyer") |
| legal-documents | legal | Anthropic's `claude-for-legal` suite (draft-for-attorney-review posture, jurisdiction assumptions surfaced) + a survey of community legal skills that *generate* the documents — the step we refuse; the input-pack framing and "every published promise is an unticketed requirement" are ours | 🟡 (no internal legal expertise; which documents are mandatory left as a question for counsel) |
| regulatory-watch | legal | same suite (regulatory-change monitors, freshness gate, `[verify]` on unsourced claims) + a community GRC pack covering 30 frameworks with no update mechanism, which is the gap this fills; jurisdiction-first and "unverified rather than wrong" are ours | 🟡 (no internal legal expertise; produces dated questions, never a compliance verdict) |
| licence-compliance | legal | licence texts + the published permissive/weak/strong-copyleft distinctions; lock file as the real inventory, generated notices and the rule-C symmetry are ours | 🟡 (no internal legal expertise) |
| ux-writing | UI/UX | published content guidelines of the major design systems; the domain-modeling consistency link, the no-concatenation rule and the empty/no-match/failed-to-load split are ours; **sectioned and deepened 2026-09-08** — the five inline sections moved to one file each under `references/` and the router became a table of triggers (1,005 → 4,217 words of rules). No section added; §4.1 kept its number, cited from `business/release-communication` §2. Interface text has no test — a wrong string ships green and the only evidence is a behaviour — so the depth is that behaviour: a validation message naming the *rule* rather than the verdict, the message being the only thing that can say what happened to the reader's work after a failed save, "you cannot" versus "it did not work" where only one is retryable, a zero being a measurement and not an empty state, a permission-empty list as a third case where "add your first item" cannot be followed, sample content in an empty screen being reconciled against as real, the form of address propagating into every verb form, a half-translated screen failing silently because a missing key renders as its source text, a plural not being a conditional, and a hardcoded string bypassing the translation file, the review and the search at once | 🟡 (no internal UX-writing expertise, no tone-of-voice reference available) |
| product-marketing | marketing | published positioning structure (audience / alternative / outcome / boundary); claim-needs-a-source as `default = failure` applied outside code, and technical claims read by a builder, are ours | 🟡 (no internal marketing expertise, no brand or campaign reference available) |
| sales-support | sales | published discovery-before-solution practice and the estimate-versus-commitment distinction; the estimation rules mirror internal engineering practice (points, spikes, scope moves not the number) with nothing named | 🟡 (no internal sales expertise; pricing and contract terms deliberately out of scope under rule C) |
| release-communication | communication | keep-a-changelog conventions + standard deprecation-notice practice; the three-bucket ordering by required action, and "anything fitting no bucket is internal noise", are ours | 🟡 (no internal technical-writing or comms expertise) |
| incident-communication | communication | published status-page practice + blameless-postmortem culture; separating the communicator from the fixer, and "still investigating" counting as a real update, are the two rules we'd most want enforced | 🟡 (no internal incident-response expertise; escalation and on-call arrangements stay out under rule C) |
| data-analytics | BI / data (new 2026-08-11) | the org catalogue's two BI landscape skills (§1–§4: the multi-instance landscape, the cross-instance-identifier trap, the crosswalk-table fix, usage-guide-vs-schema-dump, `UNION ALL`-as-named-tradeoff — real instance/host names, entity counts and the ERP's real French table/column names left out under rule C); §3.3 layered modeling (staging/intermediate/mart) from established `dbt`-ecosystem analytics-engineering practice; §2.4 six-dimension data-quality vocabulary from DAMA-DMBOK; §5 KPI/dashboard discipline (decision test vs vanity metrics, single source of truth, glanceable KPI count) from published dashboard-design practice; **sectioned and deepened 2026-09-08** — the five inline sections moved to one file each under `references/` and the router became a table of triggers (1,804 → 4,520 words of rules). No section added, and every section and point number preserved, which matters more here than in most blocks: `agents/oracle` walks §1 to §5 by number as its report structure and §2.4/§4.3/§5.2/§5.3 are cited by point from that agent and from three business blocks. None of this block's failures raise an error — every one returns a plausible number — which is what the depth adds: a name match failing in both directions with only one visible, "which system wins when two disagree" being a governance question with an owner, two sources holding two different populations, several refresh cadences making "today's figure" a mix of ages, a permission-scoped account returning a smaller entirely valid-looking answer, the data-quality dimension choosing the check, the **grain** deciding whether a join fans out, a consolidation having to carry its source instance as a real column, an unreachable instance returning successfully with its rows missing, a number without its filters not being traceable at all, zero being the worst default because zero is a legitimate value, and any figure someone is accountable for becoming a target | 🟡 (no internal data-engineering expertise) |

| fintech-compliance | legal / finance (new 2026-08-11) | published PCI DSS/tokenisation guidance (never let card data reach a server we control if a hosted-field/token alternative exists), published KYC/AML/sanctions-screening practice (onboarding + risk-driven re-screening, OFAC/UN/EU lists), published ledger-engineering writing aimed at engineers (Modern Treasury, TigerBeetle: append-only, no silent update/delete, balance as a derived read, atomic multi-entry posting), published Stripe-style payment-integration practice (idempotency keys on both the outgoing call and the incoming webhook, signature verification before trust, dedup by event id) | 🟡 (no internal fintech/compliance expertise; routes the regulatory calls, owns the engineering invariants — same posture as `data-protection`) |
| people-ops | HR (new 2026-08-11) | published structured-interview/hiring-bias-reduction guidance (defined competencies before the posting, identical questions per round, independent scoring against a rubric, documented job-related rationale); published 30/60/90-day onboarding research (manager engagement as the strongest predictor, phased context→contribute→execute goals); published offboarding/IT-security checklists (access revocation scheduled to departure type, privileged access revoked with general access, notice-period knowledge transfer, owner-and-deadline per step); §4 (ongoing performance) added same day from published continuous-feedback/recency-bias/calibration practice | 🟡 (no internal HR expertise; jurisdiction-specific employment law explicitly routed out, same posture as `data-protection`) |
| customer-success | support / CS (new 2026-08-11) | published help-desk ticket-triage/SLA/escalation practice (priority levels with stated response/resolution targets, automatic escalation on breach, self-serve KB as volume reduction); published SaaS customer-health-score guidance (multi-signal composition, adoption/seat-utilisation as early churn signals, proactive outreach before the QBR, "gone dark" as its own signal) | 🟡 (no internal support/CS expertise; sibling to `sales-support`, which stops at the closed deal) |
| finance-ops | finance (new 2026-08-11) | published internal-controls/segregation-of-duties guidance aimed at small businesses (requester ≠ approver ≠ reviewer, compensating controls where headcount doesn't allow real separation, measured faster fraud detection with the control in place); general invoicing/receivables-aging and budget-as-tracked-commitment practice | 🟡 (no internal finance/accounting expertise; distinct from `fintech-compliance`, which is a product's ledger, not the company's own books) |
| vendor-management | procurement (new 2026-08-11) | published SaaS/third-party vendor-risk-assessment guidance (review built into procurement before signing, risk-tiered by data/access scope, documented decisions including accepted residual risk, re-review triggered by scope change/incident/ownership change, not only the calendar) | 🟡 (no internal procurement expertise; the cross-references into `licence-compliance` and `data-protection` §4 are ours — neither block names the broader vendor-selection process it assumes happens somewhere) |
| learning-development | HR (new 2026-08-11) | published L&D-ROI-measurement guidance (identify the gap before choosing training, baseline before measuring, skills-gained/time-to-proficiency/career-mobility over attendance-and-satisfaction) | 🟡 (no internal L&D expertise; sibling to `people-ops`, which owns onboarding/performance, not ongoing skill-building) |
| sustainability-esg | legal / comms (new 2026-08-11) | published ESG-reporting and greenwashing-prevention literature (materiality assessment as the starting point, the specific greenwashing patterns: unbacked quantified claims, symbolic qualitative commitments, partial quantification disclosed as complete) | 🟡 (no internal ESG expertise; applies `product-marketing`'s claim-needs-a-source posture and `data-analytics`'s traceability rule to one high-scrutiny claim category — both cross-references ours) |
| investor-relations | finance (new 2026-08-11) | published startup-fundraising/due-diligence guidance (data room built before outreach, stage-appropriate depth, sensitive material gated by default, reconciliation across deck/cap table/financials/forecast) | 🟡 (no internal fundraising/IR expertise; applies `data-analytics`'s single-source-of-truth rule and `incident-communication`'s honest-update posture to the investor relationship — both cross-references ours) |

**First business-layer agent**: `oracle` (below, in the domain-agent table) reads a KPI/dashboard/
analytics-query artefact against `data-analytics` — the business layer had 16 skills and no reader
before it, unlike every dev-pipeline skill's stack reader (gimli/aragorn/…). It still never gates
(business/README.md's weaker contract), so it sits in the agent roster rather than a business-only
table. `fintech-compliance` gets no agent of its own, matching `data-protection`'s precedent: a routing
checklist doesn't need a reader, only an artefact (a query, a dashboard) does.

### Domain agents (invoked by steps 8/10)
| Agent | Role | Maturity |
|---|---|---|
| aragorn / gimli | MR review, house style (Nuxt/Vue · PHP/Laravel) | 🟢 (real production use, every MR on the Nuxt front-end and the Laravel API — the two stacks actually worked day to day) |
| legolas | MR review, house style (React · Next.js) | 🟢 (real production use, both React and Next.js MRs run through it) |
| boromir / theoden / frodo | MR review (Go · C#/.NET · generic JS/TS backend) | ✅ (sourced from the market for Go/.NET, no real MR on those stacks yet) |
| samwise / faramir | MR review (Python · Flutter/Dart) | 🟡 (added by the catalogue-completion pass: 20 Python and 37 Flutter skills there meant those stacks are worked on and `elrond` routed them nowhere; both now read `python-conventions` / `flutter-conventions` first and treat an installed catalogue as the house override) |
| elrond | review orchestrator: detects the stack, delegates, never reviews itself | 🟢 (real production use, routes every MR to aragorn/gimli today) |
| gandalf | final MR gate (`/code-review` + `/security-review`) | 🟢 (real production use; known limit logged separately: its nested sub-agents don't surface their findings back to it, see `gandalf-nested-agents-lose-results` in memory — consolidate/call readers directly meanwhile) |
| **galadriel** (GATE, formerly "evaluator") | judge with a clean context, **no Write/Edit**, returns PASS/NEEDS_WORK with cited evidence | ✅ (written; the hook pair now exists in `hooks/`, per-repo wiring not done yet, not dogfooded yet) |
| neo | Vue3/Nuxt3 implementation (Composition API, reactivity, perf) in functional/ | ✅ (not dogfooded yet) |
| tank | SQL tuning (MySQL/SQL Server) and Elasticsearch-Scout mapping/indexing | 🟢 (dogfooded 2026-08-07 on the Laravel API and the Nuxt front-end: found a real search-index mapping/filter-type mismatch across 7 files, distinct from the case already known, and said explicitly what it couldn't confirm without a live ES container) |
| morpheus | Laravel/Eloquent implementation, end-to-end for a small or mixed-layer change (API, queues, perf) | 🟢 (dogfooded 2026-08-07 on `formation-laravel`: turned dozer's 4 red tests green without touching the test file, ran the existing suite to confirm no regression, refused to self-certify beyond that and deferred to gimli/gandalf) |
| laravel-architect / laravel-eloquent-expert / laravel-api-expert / laravel-events-expert / laravel-commands-expert / laravel-testing-expert / laravel-debugger / laravel-simplifier | the Laravel build role split into one agent per layer — design, data, HTTP, async/events, console commands, test authoring, failure diagnosis, clarity pass | ✅ (written 2026-09-09; `morpheus` stays the generalist for a small or mixed-layer change, the eight are the specialists a per-stack Claude Code agent catalogue's layered roster showed was missing here; none dogfooded yet) |
| trinity | NestJS/Node implementation (modules, DTOs, Zod/tRPC contracts, Prisma) | ✅ (not dogfooded yet; fills the builder gap opposite frodo; no NestJS project exists on disk yet to run it against) |
| dozer | writes the test suite (default-FAIL contract), tests only, never implementation — **defers to `test-casebook`'s `test-writer` where that package is installed**, and is the fallback otherwise | 🟢 (dogfooded 2026-08-07 on `formation-laravel`: wrote a genuinely red test for a real missing rate-limit, caught and fixed a Laravel test-helper quirk without touching app code, correctly told apart from the vulnerability under test, flagged unrelated suite flakiness rather than hiding it) |
| keymaker | technical SEO audit of a live page/site, never edits | ✅ (not dogfooded yet) |
| sparks | real-world performance audit of a live page/screen (Web Vitals, network waterfall, main-thread work), never edits | ✅ (written 2026-08-10, filling the one live-site audit axis the roster was missing — SEO/a11y/functional/security static+dynamic all already had one, performance only had the authoring-time `webperf` skill; not dogfooded yet) |
| link | technical a11y audit of a live page/site, never edits | ✅ (not dogfooded yet) |
| mouse | manual/exploratory testing of a flow on a running app, never edits | ✅ (not dogfooded yet) |
| seraph | dedicated static security audit (OWASP, secrets, dependencies), read-only, never active exploitation | 🟢 (dogfooded 2026-08-07 on `formation-laravel`: 4 sourced majors, findings traced into the vendor packages' own source, not pattern-matched) |
| smith | dynamic adversarial probing (auth bypass, injection, IDOR) on an explicitly authorised running target, complements seraph's static audit, never edits | ✅ (written 2026-08-10, filling a real gap: nobody in the roster attempted a live exploit, only static audit and functional exploration; not dogfooded yet) |
| architect | periodic architecture-debt audit (git hot-spots, deletion test, prioritised report) | 🟢 (dogfooded 2026-08-07 on `formation-laravel`: caught a real OSDD boundary leak and a dead access-control scope, applied the deletion test to correctly rule out two candidates) |
| palantir | open-web research (advisories, fact-checking, market practice beyond training cutoff), sourced/dated answer, never edits | 🟢 (dogfooded 2026-08-07: cross-checked a Bun-runtime-evasion claim against 4 independent sources, surfaced a real interpretation split between them instead of flattening it) |
| oracle | business-layer reader for a KPI/dashboard/analytics-query artefact against `business/data-analytics`, advisory notes only, never a gate (business/README.md's weaker contract) | ✅ (written 2026-08-11, the first business-layer agent — no internal BI expertise behind it, phrases thin-confidence findings as questions like `gimli`; not dogfooded yet) |

## 2. Sourcing backlog: ideas/agents to rewrite in order to complete/improve

Market scouting is done continuously (last pass 2026-08, including the official Anthropic skills
repo and a 137-agent per-technology catalogue). Each line = an idea to **rewrite here**,
not to install; sources are anonymised by category (Claude Code agent/skill catalogues, stack
linters, orchestration frameworks, etc. on the market).

| Source category | Idea / agent to take | Enriches | Status |
|---|---|---|---|
| **Claude Code's own documentation** (`code.claude.com/docs`, read 2026-09-07: skills, sub-agents, scheduled-tasks, agent-teams, model-config, the August weekly digests) | the platform surface itself: the full skill and agent frontmatter, effort levels as an axis distinct from the model, fork mode on by default, `isolation: worktree`, `SendMessage` resume, subagents vs teammates, the `/goal` vs `/loop` vs `Monitor` split, the seven-day `/loop` expiry and the jitter | `references/claude-code-platform.md` (new), `CONVENTIONS.md` (both templates + the enforcement rule), `choose-model`, `writing-agents`, `writing-skills`, `dispatch-parallel`, `WORKFLOW.md`, 20 agent files | ✅ (2026-09-07: the repo had been written against the platform as of ~2026-08-14 and every block asserting what is native was asserting what *was* native. The load-bearing find is ours, not the docs': 25 agents carried `name`/`description`/`model` only, so twelve prose-only *"never Write/Edit"* rules were guarantees the runtime never held — now `disallowedTools`. Stamped and expiring 2026-12-07, per `source-freshness`) |
| **`claude plugin eval`** (native, scored eval cases with an automatic no-plugin baseline arm) | the RED/GREEN comparison `testing-blocks` describes by hand, mechanised: `evals/**/case.yaml` + `graders/*.md`, runnable against a plugin or a skills directory | `testing-blocks` | 🔜 **open** — the block now names the runner and says its own protocol predates it, which is honest but not done. What is owed: this repo's pressure scenarios expressed as eval cases, so promoting a block out of 🟡 is a command anyone can re-run rather than a session somebody remembers. **Blocked, measured 2026-09-07**: `claude plugin eval init` answers *"`plugin eval` is currently in early access"* on CLI 2.1.218 here, so the cases cannot be run yet — authoring them blind would be writing a test suite nobody can execute, which is the shape `code-baseline` §8 point 6 refuses. What is done instead is the prerequisite: `.claude-plugin/plugin.json` exists, so the day the gate opens this repo resolves as a target (`mentis@skills-dir`) with the no-plugin baseline arm, rather than needing a manifest written first |
| market long-running agent patterns | `evaluator.md` (fresh-context evaluator pattern) → `galadriel` agent | gate | ✅ (agent written) |
| the current wave of credential-stealing packages, and agents told to install them by text they read | `hooks/block-installs.sh` (PreToolUse on `Bash`): refuses every install, one-shot runner and `curl \| bash`, then resolves what a `package.json` script actually runs; names pnpm as the way to install and asks where the instruction came from | every agent, `CONVENTIONS.md`, `references/review-axes.md` §2 | ✅ (72 cases, blocked and allowed both; limits documented rather than oversold — it is an interlock, not a sandbox; dogfooded 2026-09-09 against a real repo's own command list, which is where the `pnpm exec` false positive came from) |
| market long-running agent patterns | `verify-gate.sh` (PreToolUse default-FAIL hook on read evidence) | gate | ✅ (rewritten as the `hooks/` pair; ours: fail-closed only on the guarded path so a repo without a parser still works, plus a read log so "produced" and "looked at" are distinguished; tested against 6 cases; wired into a real repo 2026-09-09 and inert there, since the pair guards a contract file only the mentis pipeline produces) |
| named directly by the operator (a build agent editing a failing test's expectation instead of the implementation) | `hooks/guard-test-changes.sh`+`.py` (PreToolUse on Edit/Write): a pre-existing assertion line disappearing without `MENTIS_ALLOW_TEST_CHANGES` set is blocked | `skills/debug` §3.4, `skills/code`, `skills/tdd`, `galadriel` | ✅ (internal synthesis, no external source; 18 cases across 5 ecosystems, `bin/test_guard_test_changes.py`; dogfooded 2026-09-09 in a real NestJS repo, which found that a prettier-formatted assertion hid its expected value from a line-level comparison) |
| **Anthropic's `claude-for-legal`** (13 vertical legal plugins, official) | freshness gate on bundled reference content, `[verify]` tag for unsourced claims, jurisdiction assumptions surfaced, "every output is a draft for attorney review — the attorney, not the plugin, owns the position" | `source-freshness`, `business/legal-documents`, `business/regulatory-watch` | ✅ (mechanisms taken and generalised; its practice-profile + research-connector architecture is aimed at law firms and stays out of scope) |
| community legal skills for Claude (contract review, policy generators, a 30-framework GRC pack) | *generating* terms/NDAs/policies and scoring contracts; the GRC pack tracks versions and dates precisely | / | ✕ (they produce the legal document, which is exactly the step we refuse — a business block routes to counsel, it doesn't draft; the GRC pack also has no update mechanism, so its careful dates rot silently, which is the argument for `source-freshness`) |
| `context7` MCP server | current library/framework documentation on demand, beyond any training cutoff | `source-freshness` §3, `references/README.md` | ✅ installed (user scope, verified connected 2026-08-06); authoring-time only, never a runtime dependency of a pipeline step — rule B |
| `claude-mem` (npm, `thedotmack/claude-mem`) | session memory compression across Claude Code sessions, worker process, native auto-memory left enabled alongside it | README Quickstart §6 | ✅ installed 2026-08-10 (user scope, provider `claude`, runtime `worker`); kept alive by a plain hourly cron (`~/.claude-mem/keepalive.sh`), not a native loop — the worker is a background daemon a session-scoped `/loop` dies with and a cloud routine can't see; a Desktop scheduled task could reach it but would tie process supervision to the app being open, so cron stays the answer. Not wired into any pipeline step — rule B |
| `graphify` (personal skill) | turns a repo into a queryable knowledge graph (`graphify-out/`), community detection, honest EXTRACTED/INFERRED/AMBIGUOUS trail | README Quickstart §6 | ✅ installed (personal skill, no package); refreshed check-at-use (graph age checked on invocation, `--update` runs itself past 24h) rather than a timed loop, since `--update` needs a live agent session — authoring-time convenience only, rule B. Corrected 2026-09-07: `archi` step 1 and `extract-conventions` step 1 named it as their *first action*, which is a rule-B break the "convenience only" claim here was already denying — both now state the capability (have a map of what exists) with the tool as one way to get it. Arbitrated the same day against `claude-mem`'s `smart-explore` (tree-sitter AST search over MCP, ~2-6k tokens per query, nothing persisted) and `pathfinder` (cross-feature duplication report with citations): the index form wins for `archi` step 1 because the artefact form's staleness — a graph directory that is right the day it is built — is the cost this repo kept paying, and `pathfinder` belongs to `agents/architect`'s periodic audit rather than to a per-feature step. `graphify` stays installed and is no longer named by any step as its first action |
| Perplexity-backed MCP research servers on the market (several: Sonar search/deep-research/reasoning + citations) | broad web search → fetch the authoritative few → cross-check → cite, as an on-demand research agent | `palantir` agent | ✅ (mechanism rewritten on native `WebSearch`/`WebFetch`, no API key, no runtime MCP dependency — rule B) |
| `refactoring.guru` design-pattern catalogue | the 22 Gang of Four patterns, when each applies | design-patterns | ✅ (catalogue taken as the reference; its missing overuse caution is what our block adds) |
| community video-reading skills (`claude-real-video`, `watch-video-skill`, `claude-video-vision`) | make a video readable by an agent: scene-change frame extraction + dedup + subtitle-or-Whisper transcript, fully local on `ffmpeg`, MIT | bug-triage §1.1 | ✅ (idea taken, tool named as optional; local execution means using it breaks no rule, requiring it would) |
| community social-media skill suite (`social-ai-team`) | 10 skills: brand onboarding, content calendar, one writer per platform (X/LinkedIn/Threads/Instagram/Facebook/TikTok), publisher, performance review; pause-and-approve gates | `business/social-publishing` | ✅ (approval gate taken — it matches our doctrine; the per-platform writers rejected as fragmentation, and its required paid image-generation + scheduling services would make every consumer buy a subscription, rule B) |
| marketplace community-management skill + a B2B SaaS social-media-manager skill | platform selection, moderation policy templates, engagement ladder, community metrics, crisis response | `business/community-management` | ✅ (metrics and the first-hundred-members observation taken; neither has an "answer nothing alone" list, which is the part that prevents the real damage) |
| MIT open-source marketing skill collection (34 skills) | SEO, content writing, copy editing, repurposing, thread writing, per-network content, ads, analytics; paid API keys all optional | `business/content-creation` | ✅ (editorial mechanics reviewed and reduced to one block; **no review or fact-checking mechanism anywhere in it**, which is the layer we add) |
| LinkedIn growth skill set + YouTube creator skill set | hook reverse-engineering, re-hooking cross-platform, publishing cadence; retention scripts, thumbnail briefs, Shorts, channel audits | `business/content-creation`, `references/social-platforms.md` §format mechanics | ✅ (mechanics taken as **reported heuristics**, explicitly not platform-documented rules; per-platform skills again rejected as fragmentation) |
| social-media MCP publishing servers (a multi-platform poster; MCP connectors shipped by the mainstream scheduling vendors during 2026) | hold the partner status themselves, so posting works without our own app review | `references/social-platforms.md` | 🟡 usable by a human who chose that vendor, **never a block dependency**; and an aggregator makes the human gate matter more, not less |
| platform publishing APIs (X, LinkedIn, Meta/Instagram/Facebook/Threads, TikTok, YouTube, Pinterest, Reddit, Bluesky, Mastodon, Viadeo) | who actually gates programmatic posting and what it costs | `references/social-platforms.md` | ✅ surveyed 2026-08-06, six-month window; **Viadeo ✕** — ~4M mostly inactive accounts, repositioned to employer brand under its owner group, no usable third-party publishing API |
| community meme generator (`meme-lord`) | viral-meme generation: trend research, AI image generation, A/B testing | / | ✕ (routes image generation through a paid third-party service, so a shared block would make every consumer buy a dependency; and brand-adjacent published content is a `business/product-marketing` decision with a named owner, not an agent's) |
| community video-production skills (`clipify`, a video-production toolkit) | long video → 9:16 social clips, face tracking, burned captions; component/transition systems | / | 🔎 (real capability, wrong layer for now: it belongs to marketing/comms output, depends on heavy local pipelines, and we have no such need on a real project yet — revisit if comms asks) |
| recognised market skill author | grill-with-docs → CONTEXT.md+ADR | spec | ✅ |
| recognised market skill author | non-polluting two-axis code review | review | ✅ |
| recognised market skill author | `wayfinder` → `wayfinder` skill, `handoff` → `handoff` skill, `improve-codebase-architecture` → `architect` agent | plan / session resumption / architecture audit | ✅ |
| recognised market skill author | `domain-modeling` | domain-modeling | ✅ (the assumed overlap with documentation-adr was only in the output: that block is a recording template, nothing covered reaching the decision) |
| market generalist dev skill catalogue | `observability-and-instrumentation` → `observability-instrumentation` skill, `api-and-interface-design` → `api-design` skill, `documentation-and-adrs` → `documentation-adr` skill, `deprecation-and-migration` → `deprecation-migration` skill | code/api/docs/migration | ✅ |
| market generalist dev skill catalogue | `security-and-hardening` → `security-hardening`, `webperf` → `webperf` | new blocks | ✅ (both written; security-hardening exists because seraph and /security-review both look at code that already exists, neither is consulted while the boundary is written) |
| market generalist dev skill catalogue | `context-engineering` | / | ✕ (meta on writing prompts/CLAUDE.md, not a dev skill; the meta layer here is already `writing-skills`/`writing-agents`) |
| market generalist dev skill catalogue | `browser-testing-with-devtools` | gate (already overlaps `mouse`/`verify-flow`) | ✕ (redundant) |
| **the upstream this framework responds to** (14 skills, 0 agents) + its companion skills repo (31 skills) | full enumeration, done late: our own sourcing had never listed the contents of the project mentis takes its premise from. Numerically we're ahead (59 skills + 15 business blocks / 21 agents, as of 2026-08-06), but they cover a different axis: thinking techniques and meta, where we had nothing | see the rows below | 🟡 (mined: `meta/`, `debugging/`, `testing/` and `problem-solving/` are all treated in the rows below — six taken, three refused with a reason. 🟡 rather than ✅ because the enumeration is one pass over their repositories as of 2026-08-06, not a subscription) |
| market skills repository (companion) | `meta/testing-skills-with-subagents` → `testing-blocks` | validating our own 🟡 blocks | ✅ |
| market skills repository (companion) | `meta/pulling-updates-from-skills-repository` + `meta/sharing-skills` → `distributing-blocks` | README stages 3-4 | ✅ |
| market skills repository (companion) | `debugging/root-cause-tracing` + `debugging/defense-in-depth` → folded into `debug` | debug | ✅ (extended rather than duplicated; the layering was bounded to boundaries, the source doesn't limit it) |
| market skills repository (companion) | `debugging/verification-before-completion` | gate | ✅ (already owned: that's what step 7 + `galadriel` + the `hooks/` pair do, with cited evidence) |
| market skills repository (companion) | `testing/testing-anti-patterns` + `testing/condition-based-waiting` → `testing-anti-patterns` | tdd / review | ✅ (merged: one responsibility, tests that report safety they don't have) |
| market skills repository (companion) | `problem-solving/when-stuck` (dispatch) + `simplification-cascades` + `inversion-exercise` + `scale-game` + `meta-pattern-recognition` → one block `when-stuck` | new: thinking techniques | ✅ (merged into one block: techniques reached for rarely, six files is six files nobody opens; added a 3-occurrence threshold and the over-engineering line count, the source treats unification as straightforwardly good) |
| market skills repository (companion) | `problem-solving/collision-zone-thinking` | / | ✕ (forcing two unrelated domains together generates metaphors reliably and decisions rarely; this framework already errs toward too much material) |
| market skills repository (companion) | `collaboration/remembering-conversations` | / | ✕ (the memory system already in place covers this) |
| market skills repository (companion) | `architecture/preserving-productive-tensions` | documentation-adr §4 | ✅ (kernel kept, block refused: as a standalone skill it had nowhere to attach, so it's reduced to the one sentence that changes behaviour — an ADR naming the trade-off it deliberately holds, so `simplify` doesn't collapse it) |
| market skills repository (companion) | `research/tracing-knowledge-lineages` | / | ✕ (already owned structurally: every block carries an `Origin` and every idea a row in this file, which is the lineage the skill prescribes keeping; a block telling us to do what the template already forces would be pure ceremony) |
| market skills repository (companion) | `meta/gardening-skills-wiki` → `maintaining-blocks` | new: corpus upkeep | ✅ (generic idea rewritten; every check in it is a bug this repo actually had — the phantom `WORKFLOW.md`, `review` routing to a removed agent, ✅ claimed for deleted files, a rename rewriting market-catalogue text) |
| market skill/agent framework | `dispatching-parallel-agents` + `subagent-driven-development` → merged into `dispatch-parallel` | orchestration | ✅ |
| market skill/agent framework | `writing-plans` | plan | ✅ (owned by `plan`: atomic increments, dependency order, one task item each, and no auto-execution of the whole plan) |
| market Claude Code agent catalogues (several) | `git-advanced-workflows` (advanced worktrees) | start-feature / finish | ✕ (duplicate lead, same source ruled out below: a reference course, not an orchestrated block; worktree mechanics already covered by `start-feature`/`merge-worktree`) |
| market multi-agent orchestration framework | org-chart coordinator+agents | multi-agent dispatch | ✕ (architecture reading only, same conclusion as the row below: no forced fresh context, no evidence/verdict mechanism, so nothing to take for the GATE) |
| market live-state tool | live state from reality + socket API | a separate personal project | 🔎 **deferred** (different product, not a mentis block) |
| market replay/audit tool | post-hoc replay/audit | a separate personal project | 🔎 **deferred** (different product, not a mentis block) |
| market token compression tool | compression + per-call token measurement | a separate personal project | 🔎 **deferred** (different product; and the native equivalent may be enough) |
| market voice→vault pipeline | voice→vault pipeline | a separate personal project | 🔎 **deferred** (different product, not a mentis block) |
| market Vue skill catalogue | `skills/vue/` (script-setup-macros, core-new-apis, advanced-patterns) | vue-nuxt-vuetify-conventions | ✅ |
| market Nuxt skill catalogue | `skills/nuxt4-patterns/SKILL.md` | vue-nuxt-vuetify-conventions | ✅ |
| market Nuxt skill catalogue (another) | `skills/nuxt/references/nuxt-composables.md` (useState/useCookie/useRequestFetch discipline, limited extract) | vue-nuxt-vuetify-conventions | ✅ |
| market Vuetify skill catalogue | `.deprecated/vuetify-4/SKILL.md` + `references/patterns/` | vue-nuxt-vuetify-conventions | ✅ |
| market context-engineering kit | `plugins/git/skills/git-worktrees/SKILL.md` ("How to Merge Worktree" section) | merge-worktree | ✅ |
| market Claude Code agent catalogue | `vue-expert` (frameworks) → `neo` agent | domain agents (frontend build) | ✅ |
| market Claude Code agent catalogue (large collection) | confirmed absence of a Vue/Nuxt agent (grep across 203 agents) → confirms the gap filled by `neo` | domain agents (frontend build) | ✅ (cross-reference) |
| market Claude Code agent catalogue (another) | `sql-pro` (02-language-specialists) → `tank` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue (large collection) | `sql-pro`, `database-optimizer` → `tank` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue | `elasticsearch-expert` → `tank` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue (another) | `laravel-specialist` (02-language-specialists) → `morpheus` agent | domain agents (backend build) | ✅ |
| market Claude Code agent catalogue (large collection) | `php-pro` (web-scripting), no Laravel specialisation → confirms the gap filled by `morpheus` | domain agents (backend build) | ✅ (cross-reference) |
| market long-running agent patterns | kill-switch / steer (operator hooks) | / | ✕ (a human is present) |
| market output-compression style | output compression | / | 🟡 re-assessed: the fully telegraphic style stays ruled out (unreadable), but the principle "short output by default, to limit output-token spend" is kept as a cross-cutting guarantee (see `doc/HOW-WE-WRITE-OUR-AGENTS.md` §5) |
| market frameworks for fully agentic autonomy | 24/7 / end-to-end autonomy | / | ✕ (counter-example: no-auto-merge) |
| market Vue skill catalogue (another) | `skills/vue/` (usage of a third-party JSON→Vue rendering lib) | vue-nuxt-vuetify-conventions | ✕ (not a generic Vue convention, outside the needs of the stacks in scope) |
| market Nuxt skill catalogue (another) | `skills/nuxt-modules/` (authoring a published/npm Nuxt module) | vue-nuxt-vuetify-conventions | ✕ (out of scope: the operator writes app code, not modules) |
| market Nuxt skill catalogue (another) | `skills/nuxt/SKILL.md` (dispatcher) | vue-nuxt-vuetify-conventions | ✕ (redundant with the progressive-disclosure principle already established in using-mentis) |
| market skill catalogue (another) | `using-git-worktrees` | merge-worktree | ✕ (as-is redistribution of a skill already taken natively and in start-feature) |
| market headless Vuetify lib | headless lib (`@vuetify/v0`) | vue-nuxt-vuetify-conventions | ✕ (different from the styled Material Vuetify used on the Nuxt/Vue frontend) |
| market Vue skill repo (two variants, same content) | `vuetify-skilld` | vue-nuxt-vuetify-conventions | ✕ (folder missing from the current git tree, content not found (same finding on both forks)) |
| market skill catalogue (another) | `web-ui-vuetify` | vue-nuxt-vuetify-conventions | ✕ (file not found in the current tree; already covered by the per-stack reviewers at review time) |
| market Vuetify reference corpus | exhaustive reference corpus (450 files) | vue-nuxt-vuetify-conventions | ✕ (too large for a condensed block) |
| market skill catalogue (another) | `material-design-3-guide` | vue-nuxt-vuetify-conventions | ✕ (generic multi-framework MD3 guide, off topic) |
| market front-end handbook | `frontend-best-practices` | vue-nuxt-vuetify-conventions | ✕ (generic content already known, better covered by design:*, actually inaccessible 403) |
| market skill catalogue (another) | `frontend-design` | vue-nuxt-vuetify-conventions | ✕ (repo gone 404, already overlaps the native frontend-design skill) |
| market skill catalogue (another) | `ln-114-frontend-docs-creator` | vue-nuxt-vuetify-conventions | ✕ (file missing, depends on a proprietary pipeline that can't be transposed) |
| market memory tool for Claude Code | `mem-search` | / | ✕ (a whole subsystem, redundant with the memory system already in place) |
| market memory tool for Claude Code (same publisher) | `version-bump` (formerly claude-code-plugin-release) | / | ✕ (operations script specific to that tool, not a generalisable method) |
| third-party market graphify skill | `graphify` | / | ✕ (confirmed duplicate of the native graphify skill already installed) |
| market Claude Code agent catalogue (large collection) | mcp-developer | future Node/NestJS project (MCP) | ✕ (premature, no active MCP work; to be revisited when the porting phase is concrete) |
| market Claude Code agent catalogues (several) | api-documenter | / | ✕ (no signal of API-doc pain in the memory) |
| market Claude Code agent catalogue (large collection) | readme-generator | / | ✕ (already overlaps the manual test-casebook changelog) |
| market Claude Code agent catalogue (large collection) | dependency-manager | / | ✕ (no CVE/version-conflict signal) |
| market Claude Code agent catalogues (several) | error-detective | / | ✕ (no concrete incident beyond the Docker ports, already handled) |
| market Claude Code agent catalogue (large collection) | git-workflow-manager | / | ✕ (conventions already settled and stable: squash+delete, Draft MR, GCI naming) |
| market Claude Code agent catalogue (large collection) | code-reviewer/security-auditor/penetration-tester/debugger/test-automator/qa-expert/accessibility-tester/refactoring-specialist | / | ✕ (already covered by the per-stack reviewers/gandalf + the systematic-debugging/testing-doctrine-casebook/design:accessibility/simplify skills) |
| market Claude Code agent catalogue (large collection) | legacy-modernizer | / | ✕ (no framework migration under way) |
| market Claude Code agent catalogue (large collection) | typescript-pro | / | ✕ (generic and weak signal, no documented TS pain) |
| market Claude Code agent catalogue (large collection) | database-architect | / | ✕ (no schema design from scratch; covered by `tank`) |
| market Claude Code agent catalogue (large collection) | frontend-security-coder / backend-security-coder | / | ✕ (gandalf already runs /security-review + delegates to the stack reviewer) |
| market Claude Code agent catalogue (large collection) | devops-troubleshooter | / | ✕ (docker-proxy zombies already handled by a documented fix, not an agent-shaped need) |
| market Claude Code agent catalogue (large collection) | context-manager/team-lead/team-reviewer/team-implementer/team-debugger | / | multi-agent dispatch | ✕ (org-chart style implementation, architecture to be assessed, not an agent to write now) |
| market Claude Code agent catalogue (large collection) | git-pr-workflows plugin (code-reviewer) | / | ✕ (overlaps the per-stack reviewers/gandalf) |
| market Claude Code agent catalogue (large collection) | git-advanced-workflows skill | start-feature/finish | ✕ (a reference course, not an orchestrated agent) |
| market Claude Code agent catalogue | nestjs-expert / typescript-expert | future Node/NestJS project | ✕ (premature, to be revisited during the active NestJS+TS phase on the future Node project) |
| market Claude Code agent catalogue | react-expert | / | ✕ (useful only for reading colleagues' React code, not a production need for the operator) |
| market Claude Code agent catalogue | accessibility-expert / playwright-expert | / | ✕ (overlaps design:accessibility + verify-flow) |
| market Claude Code agent catalogue | architecture-documenter / contract-testing-expert / runbook-generator | / | ✕ (low confidence, occasional use, no recurring signal) |
| market Claude Code agent catalogue | core/code-reviewer, core/debugger, core/refactorer, core/architect, security-auditor, devsecops-engineer, ux-designer, ui-components-expert, code-documenter, orchestrators/*, postgresql-expert, redis-expert, graphql-expert, cypress-expert, jest-expert, e2e-testing-expert, operational/*, industry/* | / | ✕ (redundant with the existing roster or outside the confirmed stack) |
| market multi-agent orchestration framework | generalist org-chart (who talks to whom) | multi-agent dispatch | ✕ (no forced fresh context and no evidence/verdict mechanism; off topic for the GATE gap, stays a separate 🔎 architecture lead) |
| market React skill catalogue | `react-best-practices` (AGENTS.md) (perf/rendering/waterfall patterns with before/after code) | react-nextjs-conventions | ✅ |
| market React/Node skill catalogue | `redux-toolkit/SKILL.md` (typed createSlice, typed hooks, createAsyncThunk, memoised selectors) | react-nextjs-conventions | ✅ |
| market shadcn skill catalogue | `skills/shadcn/SKILL.md` (composition through a wrapper, cn(), folder structure) | react-nextjs-conventions | ✅ |
| market React linter | `oxlint-plugin-react-doctor`, ~780 deterministic rules (state/effects, perf, security, a11y), `error`-severity subset excluding niche frameworks taken into section 4 | react-nextjs-conventions | ✅ (content rewritten; the tool itself stays a separate 🔎 candidate for a future React CI gate, not installed, the operator has no React repo) |
| market Nuxt/Vue linter | `oxlint-plugin-vue-doctor`/`oxlint-plugin-nuxt-doctor` (locked to Vue 3 + Nuxt 4, explicitly inspired by its React equivalent; reactivity/composition, SSR hydration, security and h3 server-route rules taken into section 4) | vue-nuxt-vuetify-conventions | ✅ (content rewritten; separate 🔎 candidate for a future CI gate on the Nuxt/Vue frontend, not installed) |
| market Vue linter alternative | Vue-only alternative found while sourcing | vue-nuxt-vuetify-conventions | ✕ (no Nuxt coverage, the chosen linter is more complete and closer to the real stack) |
| market Vue linter alternative (another) | Vue alternative found while sourcing | vue-nuxt-vuetify-conventions | ✕ (less mature/fewer rules than the chosen linter on inspection) |
| market deletion-oriented review tool | `ponytail-review`/`ponytail-audit` (deletion angle only (dead code, reinvented stdlib, over-abstraction, yagni), per-category tags, net line score) | over-engineering-review | ✅ (mechanism and tags rewritten, new dedicated block) |
| market generalist dev skill catalogue | `code-review-and-quality` (many installs, Critical/Required/Nit/FYI severity taxonomy, diff size threshold, dependency checklist) | gandalf | ✅ (taxonomy + thresholds folded into steps 1/5/7 of the agent, not a separate block) |
| market open source TypeScript project | `typescript-review` (a11y blind spots (aria-label, modal focus) and bundle weight (default import, heavy module on a route)) | react-nextjs-conventions + vue-nuxt-vuetify-conventions | ✅ (2 items added to each block) |
| market Copilot instruction catalogue | `review-and-refactor`, reads `.github/instructions/*.md`, refactors to the project's conventions |, | ✕ (already covered by the `*-conventions` blocks + gandalf, nothing distinct) |
| market open source TypeScript project (same publisher) | `clojure-review` | / | ✕ (language outside the stacks in scope) |
| review plugin from a market IDE vendor | `thermo-nuclear-code-quality-review` |, | ✕ (same angle as over-engineering-review, less actionable, no tags/score) |
| internal skill catalogue from another vendor | `code-quality` | / | ✕ (specific to their proprietary per-context stack, the rest is already covered by the per-stack reviewers+conventions) |
| market architecture review tool | `architecture-review` | / | ✕ (exact SKILL.md path not confirmed; content already overlaps gandalf/galadriel/over-engineering-review, not differentiating enough) |
| market NestJS skill catalogue | `skills/nestjs-expert/SKILL.md` (module/controller/service, constructor DI, DTO+class-validator, HTTP exceptions, tests) | nestjs-node-conventions | ✅ |
| advanced market TypeScript skill | Zod+z.infer contracts, discriminated unions, mapped types/type guards on Prisma models | nestjs-node-conventions | ✅ |
| market React/Node skill catalogue | `prisma-development/SKILL.md` + `trpc/SKILL.md` + `zod-schema-validation/SKILL.md` | nestjs-node-conventions | ✅ |
| market Next.js skill catalogue | `next-best-practices` | react-nextjs-conventions | ✕ (repo archived, absorbed by Next.js itself (next dev 16.3+, nothing portable)) |
| market React/Node skill catalogue (same source) | `nextjs-react-typescript` | react-nextjs-conventions | ✕ (converted from an IDE vendor's generic rules, redundant and less precise than the chosen source) |
| market React/Node skill catalogue (same source) | `nextjs-react-redux-typescript` (variant converted from an IDE vendor's rules) | react-nextjs-conventions | ✕ (almost total duplicate of react + redux-toolkit combined) |
| market React/Node skill catalogue (same source) | `react` (generic) | react-nextjs-conventions | ✕ (generic senior-dev advice, overlaps the chosen source with less depth) |
| market React/Node skill catalogue (same source) | `express-typescript` | nestjs-node-conventions | ✕ (off target: the vision for the future Node/NestJS project is NestJS not Express, partial overlap with no added value) |
| market React/Node skill catalogue (same source) | `nodejs-development` | nestjs-node-conventions | ✕ (incoherent catch-all (CMS, Vue.js, generic)) |
| market React/Node skill catalogue (same source) | `typescript` (generic) | nestjs-node-conventions | ✕ (too generic, already repeated by the nestjs/trpc/zod blocks) |
| market shadcn-ui repo | shadcn-ui | react-nextjs-conventions | ✕ (repo not found/dead, only a third-party summary retrieved, not the source itself) |
| market shadcn audit tool | audit/discovery of existing shadcn components | react-nextjs-conventions | ✕ (different mechanism, a reviewer role rather than code conventions; keep as a separate lead) |
| official Anthropic skills repo | `webapp-testing` (reconnaissance/action split, never act on an unseen selector, wait for the page to settle before reading the DOM) | qa-exploratory-testing | ✅ (section 4 added, transposed from Playwright to our Browser pane tooling) |
| official Anthropic skills repo | `skill-creator`, `frontend-design`, `mcp-builder`, `claude-api`, document/creative skills (docx/pdf/pptx/xlsx, algorithmic-art, canvas-design, theme-factory, brand-guidelines, internal-comms, slack-gif-creator, web-artifacts-builder, doc-coauthoring) | / | ✕ (skill-creator overlaps writing-skills, frontend-design and mcp-builder already ruled out earlier, the rest is document/creative production outside the dev pipeline) |
| market per-technology agent catalogue (137 agents, one per library/framework) | `jwt-expert`, `oauth-oidc-expert`, `keycloak-expert`, `auth0-expert` → flow-level discipline extracted into a new block | auth-session-conventions | ✅ (the per-provider agents themselves ruled out: per-library fragmentation against our per-role doctrine; the auth gap they revealed was real and is now covered) |
| market per-technology agent catalogue (137 agents) | `kafka`/`rabbitmq`/`bullmq`/`sidekiq`/`celery`-expert (background jobs, retries, idempotency, dead-letter) | background-jobs-conventions | ✅ (broker-independent discipline extracted into a new block; the per-broker agents themselves ruled out as per-library fragmentation) |
| market per-technology agent catalogue (137 agents) | `github-actions-expert`, `gitlab-ci-expert`, `docker-expert`, `kubernetes-expert`, `terraform-expert`, `pulumi-expert` | devops-conventions | ✕ (CI/container platform specifics are infra reality, they stay outside this repo per rule C; the generic practice is already in devops-conventions) |
| market per-technology agent catalogue (137 agents) | `owasp-top10-expert`, `opentelemetry-expert`, `openapi-expert`, `rest-expert` | seraph / observability-instrumentation / api-design | ✕ (same sources already folded into the existing blocks) |
| market per-technology agent catalogue (137 agents) | ~120 remaining per-library experts (frameworks, DBs, test runners, cloud SDKs, ML libs, languages outside the stack) | / | ✕ (one agent per library is the opposite of our per-role doctrine: it would fragment the roster into near-duplicates and none of them carries a fresh-context or evidence mechanism we don't already have) |

### Depth parity with the org catalogue — a measured programme, 2026-09-07

Subject coverage was verified in September 2026 and is essentially complete: every generic rule in the
catalogue resolved to a block here except one (`default-project-stack`, closed in `skills/archi`). **Depth
is a different question and the honest answer is that this repo is thinner**, so the gap is recorded per
stack rather than left as an impression. Bodies are not in the permanent index — only descriptions are — so
closing this costs nothing that made this repo cheaper to load.

| stack | their skills / words | our blocks / words | deficit | ratio |
|---|---|---|---|---|
| laravel | 65 / 79,825 | 3 / 44,093 | −35,732 | x1.81 |
| csharp | 37 / 56,718 | 1 / 33,380 | −23,338 | x1.7 |
| python | 20 / 22,097 | 2 / 18,222 | −3,875 | x1.21 |
| flutter | 40 / 20,772 | 1 / 16,332 | −4,440 | x1.27 |
| nuxt | 21 / 19,869 | 1 / 14,503 | −5,366 | x1.37 |
| design-patterns | 7 / 12,179 | 1 / 9,393 | −2,786 | x1.3 |
| project-management | 10 / 14,536 | 2 / 13,614 | −922 | x1.07 |
| bi, design, xefi | 16 / 17,306 | 4 / 18,571 | +1,265 | x0.93 |
| global | 18 / 20,280 | 5 / 21,624 | +1,344 | x0.94 |
| react | 36 / 9,302 | 1 / 10,999 | +1,697 | x0.85 |

Recomputed by `bin/measure_depth.py`, which is where the composition below lives; `bin/test_measure_depth.py`
fails if this table stops matching what it measures. **Ratio** is theirs over ours on the same subject, so
lower is closer and below 1 is ahead.

**Status.** Passed: `react` (all 10 sections), `nuxt` (13), `flutter` (10), `python` (8, sectioned out of a
single file first), `code-baseline` (8) inside the `global` row, `inertia-conventions` (6),
`php-patterns` (5), `design-patterns` (6) and `dotnet-conventions` (7) — the last five sectioned out of a
single file first, all on 2026-09-08, and `laravel` (11) the day before. Every **stack** block in the
table has now had its pass. The programme was then extended to the other blocks a row aggregates, which
were still single-file and were holding their rows back: `product-ownership` and `spec` first, which
takes `project-management` from x4.7 to **x1.29**, then `interface-design`, `data-analytics`,
`ux-writing` and `accessibility`, which take `bi, design, xefi` from x2.94 to **x0.93**, then
`security-hardening`, `documentation-adr`, `api-design` and `observability-instrumentation`,
which take `global` from x1.71 to **x0.94**, and finally `data-pipeline-conventions`, which
takes `python` from x2.62 to **x2.03**. **No block counted in the table is single-file any
more.** The `bi, design, xefi` row stays ✕: it is
the internal landscape, and rule C keeps it out.

**Composition.** Each row names the blocks it aggregates, so that it can be re-measured rather than
remembered — the defect that produced two unreproducible rows before this script existed:

```
laravel: laravel-conventions 30,907, php-patterns 6,068, inertia-conventions 7,118
csharp: dotnet-conventions 33,380
python: python-conventions 14,939, data-pipeline-conventions 3,283
flutter: flutter-conventions 16,332
nuxt: vue-nuxt-vuetify-conventions 14,503
global: code-baseline 9,129, security-hardening 4,144, api-design 2,394, documentation-adr 2,909, observability-instrumentation 3,048
project-management: product-ownership 9,154, spec 4,460
design-patterns: design-patterns 9,393
react: react-nextjs-conventions 10,999
bi, design, xefi: data-analytics 4,520, interface-design 5,938, ux-writing 4,217, accessibility 3,896
```

A block's size is its **rules**: the router body of `SKILL.md` with the frontmatter excluded, plus every
file under `references/` except `origin.md`.

**A counting correction, 2026-09-08.** The nuxt and laravel rows now exclude `references/origin.md`, and
so should every other row from its next pass on. `origin.md` is provenance — where a rule came from, what was re-checked,
what a pass changed — and the catalogue being compared against has no equivalent of it, so counting ours
was measuring our own bookkeeping and calling it depth. It mattered: the Nuxt pass grew `origin.md` by
about 1,700 words, which on the old convention would have read as x1.34 rather than the x1.6 the rules
actually reach. Every row now applies that convention, because every row is computed by `bin/measure_depth.py` rather
than transcribed — so the caveat this paragraph carried for three days ("the rows not yet re-measured are
slightly flattering to us") no longer applies to any of them.

Two things this table is not. It is **not a word-count target**: a meaningful share of their depth is
per-skill boilerplate (one skill per rule restates its own context) and another share is org specifics that
cannot live in a publishable repo, so parity is per *subject treated to the same depth*, not per word.
And it is **not a licence to reproduce**: `global:no-skill-export` makes the catalogue internal IP, so each
pass is written from the underlying reality — framework behaviour, public practice, this repo's own recorded
incidents de-identified — which is also why a pass is slow.

**Done so far**: `laravel-conventions` §2, §4, §8 (166/261/137 → 873/875/769) then §6 and §1 (292/589 →
1,027/996) — five of eleven sections, 1,445 words → 4,700; then `vue-nuxt-vuetify-conventions` §10, §2
and §3 (113/211/174 → 875/944/899) on 2026-09-08, then §7 and §6 the same day (172/199 → 899/877), then
§11, §12, §8, §1 and §5 (241/251/284/363/404 → 842/870/795/747/925), then §4, §9 and §13
(537/553/560 → 997/973/972) — **the Nuxt block is complete, all thirteen sections**, 4,267 words →
11,623, x3.6 → **x1.6** of its counterpart in one day. Three defects were found by doing the pass rather
than by reading for them: §5 had two points numbered 6 and a citation pointing at the wrong one, §9
pointed at `§11.6` for a rule the §11 pass had moved to point 10, and a reflow had flattened §9's
sub-list and put a space inside a URL. All fifteen intra-block `§N.M` references were then re-checked
one by one against the current numbering. Then `laravel-conventions` §7, §10 and §5 (272/361/442 →
907/915/943), which brings that block's router and eleven sections to 10,131 words and the laravel stack
to x6.2.
**A queue correction**: this note previously said `laravel-conventions` §3 and §9 were next. Measuring
before writing showed **§3 already at 980 words** from an earlier pass — the queue had been written from
memory rather than from the counts. The order is now recomputed each time from the actual file sizes,
which is the only reason the table exists.
Then `laravel-conventions` §11 and §9 (515/655 → 1,019/1,073), which completes that block: **ten of its
eleven sections have had a pass**, and the eleventh (§3) was already at 980 by the bodies pass, which is
where these passes land. The laravel stack is at 13,718 against 79,825, x5.8.
Then `react-nextjs-conventions`, **all ten sections in one pass**: §4 116 → 1,005, §9 124 → 1,010, §8
145 → 944, §10 159 → 909, §7 193 → 922, §3 210 → 912, §2 275 → 940, §6 284 → 975, §1 300 → 952, §5
496 → 1,207. Router plus sections: 3,002 → 10,476 words, against that plugin's 9,302 — **the first block
in this table to pass its counterpart**, x3.1 → x0.89. It is also the cheapest crossing available: the
react plugin is the thinnest of the four stacks the operator's catalogue covers, so this row moving to ✔
says less about the pass than the laravel row still at x5.8 does. Twenty-eight intra-block references
re-checked one by one; four had been left pointing at the wrong rule by the renumbering and were
corrected, and the three point numbers cited by the block's own 2026-08-10 re-check stamp (§1.6,
§5.12-13, §10.1) were deliberately preserved.

**What the two completed blocks say about the rest of the table**, counted rather than assumed. Five
blocks are *sectioned* and so can take the same pass — read the section, name the failure each rule
prevents, keep the original: `vue-nuxt-vuetify-conventions` (14 files, done),
`laravel-conventions` (12, done), `react-nextjs-conventions` (11, done),
`flutter-conventions` (11, done) and `code-baseline` (9). The rest are single-file blocks with no `references/` at all —
`dotnet-conventions` 3,195 words, `python-conventions` 1,868, `inertia-conventions` 1,743,
`php-patterns` 991 — and deepening one of those means first deciding what its sections are, which is a
design decision per block rather than a writing pass. That distinction is where the remaining ~66,000
words on laravel actually live, and it is why the two numbers in this table's last column are not
interchangeable.

Then `flutter-conventions`, **all ten sections**: §4 138 → 951, §9 144 → 892, §5 157 → 949, §6
168 → 965, §8 217 → 1,045, §10 218 → 955, §3 299 → 993, §2 316 → 892, §1 494 → 921, §7 571 → 1,100.
Router plus sections: 3,380 → 10,321 against that plugin's 20,772, x6.1 → **x2.0**. This is the block with
no production experience behind it at all, so the pass was written from the framework's documented
behaviour and from what the platform does — the device-level failures it had never named are the ones worth
citing: a secure-storage read failing because the keystore was cleared, a session's data surviving a logout
on a shared phone, the process being killed in the background, a permission revoked while the app was
backgrounded, and a system permission prompt that can only be shown once per install. Thirty-six
intra-block references re-checked; ten were pointing at the wrong rule after the renumbering, and one —
§9's disposal citation pointing at §1's async-context rule — had been wrong since the section was written.

Then `code-baseline`, **all eight sections** and the last of the five sectioned blocks: §3 241 → 920,
§5 249 → 932, §7 310 → 932, §1 348 → 979, §2 448 → 974, §4 509 → 1,085, §6 549 → 1,095, §8 805 → 1,274.
Router plus sections: 4,397 → 9,129. This was the block with least room — already the deepest in the repo
— so most of the pass was the failure modes the sections were silent on rather than reasons they already
carried: §3's catch-scope, cleanup-on-failure and cause-preservation rules, §5's whole primitive-obsession
family (ids, units, money, a boolean pair encoding one state), §4's timeout/retry/idempotency policy and
the webhook receiver's three rules, and §6 reframed around the *debt* rather than the doctrine, which stays
in `skills/tdd`. Twenty-four intra-block references re-checked, including a stale `§4.6–§4.9` range inside
its own `origin.md`.

**The `global` row was marked stale here for a day, and that is now resolved.** `code-baseline` is one of
the five blocks that row aggregates, and the composition of the other four had never been written down —
the table was produced by hand, not by a script, despite a sentence further down claiming otherwise.
Recomputing an aggregate from a remembered composition is exactly the mistake corrected twice already on
this page, so rather than guess, the row was left with its old number and labelled. It was then fixed
properly: see **the table is now measured, not typed** below.

Then `python-conventions`, the first of the single-file blocks — where the work is a different kind,
because the sections have to be decided before they can be deepened. In this case the decision was already
made and never acted on: the block held **eight numbered sections inline in `SKILL.md`**, the shape every
other stack block had grown out of, so sectioning it was moving each one to `references/` and turning the
router into a table of triggers. Then the same depth pass: §1 typing 207 → 902, §2 none/failures/exceptions
188 → 902, §3 naming 162 → 846, §4 async 110 → 881, §5 structure and style 236 → 914, §6 DI and lifetimes
69 → 824, §7 ORM and migrations 149 → 892, §8 toolchain and tests 162 → 866. Sections 1,283 → 7,027;
router plus sections 1,629 → **7,697**.

Two sections were thin out of proportion to what can go wrong in them, and those are where the real
absences were. **§4 async** (110 words) had no line about a `gather` needing a decision about failure,
about concurrency without a bound opening as many connections as the data says, about cancellation arriving
as an exception that a broad `except` swallows into a hung shutdown, or about `async` not making shared
state safe — there is no lock, only the absence of pre-emption between awaits, which makes check-then-act
across an `await` a genuine race. **§6 DI** (69 words) had no line about the constraint that decides most
container bugs: a dependency's lifetime cannot exceed the lifetime of what it holds, so a singleton handed
a request-scoped session captures the first one and keeps using it after that request ended. §7 also gained
the transaction and migration failures it had implied and never stated. One entry moved out of the rules
entirely: the PEP 8 re-check note, which was provenance sitting inside §5 as a numbered rule, is now in
`references/origin.md` where the other stamps live.

**On this row's number.** For a day it was derived rather than measured — `python-conventions` is one of
the two blocks the row aggregates and the other was not identified anywhere — which is what prompted the
work below.

**The table is now measured, not typed.** `bin/measure_depth.py` holds the composition of every row and
recomputes the whole table from the repo; `bin/test_measure_depth.py` (21 checks, in the pre-push suite)
fails if the table in this file stops matching what the script measures. Seven rows' compositions were
recovered rather than invented, because they reproduce their recorded totals exactly — laravel
(13,718 across three blocks), nuxt, react, flutter, csharp, design-patterns and project-management (3,092 =
`product-ownership` 2,952 + `spec` 140). `bi, design, xefi` reproduces to within three words, an edit since.
Two could not be reproduced from any combination and are therefore **declared** rather than inherited: the
`global` row's five blocks, and the second block of the `python` row, which the previous total implied at
717 words and is `data-pipeline-conventions` at 749. Both moved as a result: `global` from a stale 7,585 to
a measured 11,886, and `python` from a derived 8,414 to 8,446.

The lesson is the repo's own §8 arriving on its own bookkeeping: a figure nobody can recompute is a claim,
and it had been sitting in the one document whose whole job is to say what is actually true. The check that
closes it is not the script — it is the test that fails when the document and the script disagree.

Then `inertia-conventions`, the second single-file block and the same two-step: decide the sections,
then deepen them. Like python it already carried its sections inline — five of them — so they moved to
`references/` under a router table, and one was added. §1 the controller and the page 150 → 958, §2
shared data and page props 170 → 1,017, §3 forms, validation and errors 116 → 995, §4 the override
boundary 601 → 1,030, §5 visits, navigation and the deployed app **new** → 1,082, §6 tests 77 → 760.
Sections 1,114 → 5,842; router plus sections 1,705 → **6,679**, which takes the `laravel` row from x5.82
to x4.27 — the widest deficit in the table, and the only row a single block can move by five thousand
words.

Two things constrained this pass. **§4 had to keep its number and every point number inside it**: it is
cited from three other blocks (`laravel-conventions` §6, and the intros of
`vue-nuxt-vuetify-conventions` and `react-nextjs-conventions`), and §4.5/§4.6 are cited from this block's
own guardrails — so that section was deepened in place, point by point, rather than restructured. Tests
could move from §5 to §6 because nothing outside the block cited it. And **§5 is the only genuinely new
section**: the original block said nothing at all about the visit lifecycle, which is where most of an
Inertia app's observable behaviour comes from — scroll and local state reset on every visit unless
preserved, the cancelled-visit rule that makes a search box correct for free, an asset version that has
to be wired to the build or a browser open across a deploy keeps running the old bundle, the page data
that lives in the browser's history entry and so survives a logout on a shared machine, prefetching that
issues real requests against `GET` routes with side effects, and SSR being an optional second process
rather than a flag. The other load-bearing additions are the ones about what the reader can actually
read: the props of a page are in the HTML document and in devtools whether a component renders them or
not (§2.6), which makes authorization the controller's job before the props are computed (§1.8) and
makes a negative assertion the only test that catches a leak (§6.5). Thirty intra-block references
re-checked against the new numbering, none dangling.

Then `php-patterns`, the third single-file block and the one that finishes the `laravel` row. Three
inline sections moved to `references/` and two were added. §1 typing 150 → 959, §2 error handling 116 →
946, §3 OOP and structure 168 → 948, §4 comparison, arrays and the standard library **new** → 948, §5
time, numbers and text **new** → 971. Router plus sections 960 → **5,386**, and the row goes from x4.27
to **x3.45** — 23,118 against 79,825, from x5.82 two passes ago. §1 kept its number and §1.1 its
position, because `laravel-conventions` §5.12 cites it by number as the rule it overrides.

The two new sections are the language's own traps, and both were completely absent. **§4** is where PHP's
defaults differ most from what the code looks like it says: `==` changed meaning for string-to-number
comparison in PHP 8, so conditions carried across that version boundary changed without being edited;
`in_array` is loose unless told otherwise, which matters because the arrays it runs against are usually
allow-lists; six values are falsy and two of them (`0`, `"0"`) are real data; `isset` and
`array_key_exists` answer different questions about a key holding null; `+` on arrays is a union while
`array_merge` renumbers; `array_filter` preserves keys, so a filtered list stops being a list and
`json_encode` emits an object instead of an array *depending on which element was removed*; and a
by-reference `foreach` leaves a live reference behind that the next loop uses to overwrite the last
element. **§5** is the three value kinds where a plausible line is wrong for some of the data:
`DateTime` mutating in place while also returning itself, a date with no timezone taking the server's
default, a month having no fixed length, floats not holding decimals, integer overflow becoming a float
in silence, byte-based string functions cutting a UTF-8 character in half — which then makes
`json_encode` return `false` and the response empty — and the four function choices that are security
decisions rather than style: `hash_equals`, `password_hash`, `random_int`, `preg_quote`.

The three original sections got the usual treatment, and the additions worth citing are the ones that
look like they are already handled: `catch (\Exception)` does not catch `\Error`, so the block written
to catch everything lets exactly the programmer errors through (§2.4); wrapping an exception without
passing it as `$previous` deletes its own cause from the log (§2.5); a `return` inside `finally`
discards a pending exception silently (§2.6); `assert()` is compiled out in production, so a check
written as an assertion holds only in development (§2.14); a typed property with no default is
uninitialised rather than null, which is a different error in a different place (§1.7); a variance
mistake is fatal at class-load time, i.e. on the first request that reaches the class rather than at
deploy (§1.12); `clone` is shallow (§3.9); and `unserialize` on anything a user can influence is remote
code execution (§3.13).

Then `design-patterns`, the last single-file block. Five inline sections moved to `references/` and a
sixth was added. §1 recognise-don't-apply 78 → 827, §2 the framework-already-does-it subtraction pass
418 → 974, §3 where they earn their place 228 → 809, §4 the seven entry conditions 710 → 1,286, §5 using
the name correctly 74 → 737, §6 when a pattern stops earning its place **new** → 898. Router plus
sections 2,347 → **6,333**, and the row goes from x5.19 to **x1.92** — the second-closest row in the
table. §4 kept its number and every point inside it, because `business/fintech-compliance` cites §4.5
(money is never a float) and `laravel-conventions` cites the transaction-boundaries rule twice. §2's
bullet list became numbered points with its text unchanged, so its verdicts can be cited like every
other rule in the repo.

**§6 is the section this block was missing most, and the gap was structural rather than an oversight.**
Everything here, and everything in the source catalogue, was about whether to *add* a pattern; nothing
said when to take one out — which is exactly why patterns accumulate in a codebase that has been
reviewed carefully at every step. So §6 states the deletion test (inline the pattern in your head and
see whether the code reads better: the net-line test applied to code somebody already merged) and then
the things nobody gets a notification about: the interface whose second implementation was
decommissioned, the state machine whose middle states a product change removed, the pool justified by a
measurement taken on a runtime version since upgraded, the pattern grown to fit a case that does not
share its axis until every implementation ignores half its own signature, the suite with a test per
implementation and none for the dispatch where the bugs actually live, and the ADR line that outlives
the structure it justified and gets the pattern reimplemented from the document. It also says the part
that keeps removals from happening: a removal is a normal reviewed change, not an apology for a decision
that was right when it was made.

The five original sections were deepened the usual way. Worth citing: a class hierarchy loses the
exhaustiveness check a discriminated union gives you, so a new subclass that forgets a method silently
inherits the parent's (§2.4); the concrete loss when a Repository wraps an ORM is eager loading, query
composition and seeing the query that ran — all re-exposed one method at a time until it is the ORM with
a different spelling (§2.9); a state machine's transitions are where concurrency bites, so the guard has
to be a conditional write rather than a read-decide-save (§4.2); a Null Object that hides a failure
instead of a legitimate absence is a no-op mailer reporting success (§4.3); same-typed neighbours are
what make a wide constructor dangerous rather than merely ugly (§4.4); a pipeline has to answer what a
failing stage does and whether a stage may mutate what later stages read, or it is worse than the
god-method it replaced (§4.6); and a job dispatched inside a transaction can be picked up before the
commit, so it reads a row that does not exist yet (§4.7).

**Two stale cross-references into this block were found and fixed in the same pass.**
`laravel-conventions` §4 and §8 both cited a seventh section of `skills/design-patterns` for
transaction boundaries, and that block has never had one — the rule is §4.7 there. Wrong since those
lines were written, and found by
resolving every reference rather than by reading — which makes four defects this programme has turned up
that predated it, after flutter §9 citing §1's async-context rule for disposal and `code-baseline`'s own
`origin.md` carrying a stale point range.

Then `dotnet-conventions`, which closes the programme. Seven inline sections moved to `references/`
and none was added — unlike the other single-file blocks, the seven already covered the subject; what
they lacked was the mechanism and the consequence behind each rule. §1 async and cancellation 225 → 885,
§2 dependencies and logging 469 → 1,010, §3 authorisation 95 → 784, §4 the prohibitions 715 → 1,139, §5
disposal, nullability and enumeration 339 → 847, §6 data access and portability 238 → 835, §7 language
idioms 285 → 705. Router plus sections 3,167 → **6,976**, x17.91 → **x8.13**. Every section number and
every point number preserved.

**§3 authorisation was the thinnest section relative to what can go wrong in it** (95 words) and gained
the most: authentication answers only "who", so a bare authorise marker admits every authenticated user;
an endpoint policy is never row-level authorisation, because the id in the route belongs to somebody; a
**default-deny fallback policy** is what makes "an endpoint with no declaration is a bug" enforceable
rather than aspirational, and the allow-anonymous marker overrides even that, which makes it the most
consequential attribute in the codebase and the one most often added while debugging; claims are input
whose trustworthiness is their issuer's; a queue consumer or webhook receiver is not reached by the HTTP
middleware at all; and the negative test is the only one that proves a policy is wired, since the
positive one passes just as happily with no policy.

§1 gained the cancellation half the original stated only as signatures — cancellation arriving as an
exception a broad catch turns into a false incident, cancellation being cooperative so a CPU loop has to
check the token, the request's token dying with the request and therefore being wrong for work that must
outlive it, `Task.WhenAll` reporting one exception and hiding the rest, an unbounded `WhenAll` over an
uncontrolled collection, and a timeout cancelling the caller's waiting rather than the remote work, so a
retry can duplicate the effect. §2 gained the container's own failure modes: a registration verified at
resolve rather than at build (and the startup validation that fixes it), a disposable resolved from the
root provider held until the process ends, last-registration-wins versus try-add, and the two logging
rules that cost money when broken — interpolation destroying the structured fields that are the whole
reason for a log aggregator, and a logged secret travelling to a system with different retention and a
different access list. §5 gained disposing only what you own, `await using`, annotations being
compile-time only so deserialised data ignores them, and `default(T)` bypassing a struct's constructor.
§6 gained N+1 and the projection that fixes it, which half of a query runs on the server, reading a
generated migration before committing it, `SaveChanges` as the transaction boundary, and storing an
instant with its offset.

**The row stays 🟡, and that was the reason it was left for last.** Depth is not dogfooding: nobody here
writes C#, so a thicker block is still an unconfronted one. What the pass buys is that the rules now say
*why*, which is what `theoden` needs to read them as questions rather than as assertions — and that is a
different thing from the row's status, which only a real project can change.

**Every row had had a pass at that point.** Ten rows, ten passes, over 2026-09-07 and 2026-09-08. The
table stood at **98,968 words of rules against 272,884**, the worst ratio at **x8.13** where it was
x17.91, and the median row at **x2.31**. `react` is the one row ahead of its counterpart, and that says less than
the `laravel` row at x3.45 does — react's plugin is the thinnest of the four stacks the catalogue covers,
so it was the cheapest crossing available. What the table cannot show is the part that matters next:
several blocks are still 🟡 for want of a real project, and the way to move those is to use them, not to
write more of them.
`dotnet-conventions` had the worst ratio (x17.9) and is the stack nobody here writes, which is why it was
kept for last — a deep block nobody can dogfood is exactly the 🟡 this catalogue exists to flag, and making
it thicker did not change that letter. It has now had its pass anyway (x8.13), because the mechanism
behind each rule is what `theoden` needs in order to read the block as questions; the status is a separate
question and only a real project answers it.
Progress is recorded here rather than in a commit message so that it can be read as a whole, and the
table itself is reproducible: `python3 bin/measure_depth.py`. That was claimed before it was true, denied
when the claim caught up with us, and is now enforced by a test.

**The order is by thinness, not by importance.** A 113-word section is not a short summary of a subject —
it is a subject whose failure modes were never written down, so an agent reading it agrees with the rule
and cannot apply it under pressure. The thick sections were already written that way, which is why they
are thick.

**Extension, 2026-09-08: the blocks a row aggregates.** Ten passes covered every *stack* conventions
block, and the table still carried rows held back by a block nobody had touched, because a row's figure
is the sum of every block in it. Eleven blocks counted in the table were still one file with no
`references/` at all. The first row taken this way is `project-management`, which was the worst remaining
ratio after `csharp`: x4.7 over two blocks, `business/product-ownership` at 2,952 words and `skills/spec`
at 140.

`product-ownership` became nine sections — the request that is not yet a story (738), ordering by
consequence (720), saying no (705), acceptance criteria (692), ready and done (648), the story document
(976), reviewing a story (875), decomposition and estimation (744), the author-is-the-builder
configuration (721) — 2,952 → **7,616**. §6 to §8 kept their numbers, since `references/README.md` and
this file both cite that range. `spec` became five, in the order the step runs them: the interview (642),
`CONTEXT.md` (659), the criteria (695), out of scope (642), ADRs (658) — 140 → **3,689**. The row goes
from x4.7 to **x1.29**, and the table to **107,181 against 272,884**, worst **x8.13**, median **x1.97**.

**`spec` was the thinnest block in the repo, and the reason is worth recording.** As a pipeline step it
was written as a procedure — do these five things — which is enough for an agent that already knows what
each deliverable is *for* and useless to one that does not. The five steps named the deliverables and
never said what makes each one correct. The additions that were real absences: recording an answer in the
words that were used, because a paraphrase makes a misunderstanding invisible; "not decided" versus "not
said", which is the difference between a question and a decision that needs an owner; naming the fixture
each criterion needs, since discovering at `tdd` that the case cannot be built is a blocked step whose
usual workaround is a test of a simpler case wearing the criterion's name; and a definition stating what
a term *excludes*, which is the half that settles arguments.

The pass also settled a boundary the two blocks had left ambiguous: both described acceptance criteria
without saying which was authoritative. `product-ownership` §4 owns what makes a *business* criterion
valid; `spec` §3 turns those into the technical contract `tdd` writes failing tests against, and now
points at `product-ownership` §4 rather than restating it.

**Second row of the extension, 2026-09-08: `bi, design, xefi`.** Four single-file blocks, all of them
holding the row back at x2.94: `business/interface-design` 2,041 → **5,938** in seven sections (§0 the
producing-versus-auditing mode, then tokens, containers, states, buttons and chips, icon and text,
gathering references), `business/data-analytics` 1,804 → **4,520** in five, `business/ux-writing` 1,005 →
**4,217** in five, and `skills/accessibility` 1,027 → **3,896** in four. No section was added to any of
them; the twenty-one already covered their subjects. The row goes from x2.94 to **x0.93** — the second
row ahead of its counterpart — and the table to **119,875 against 272,884**, worst still **x8.13**,
median **x1.81**.

**These four are the blocks where a broken rule raises no error, and that is what the depth is.** A wrong
string, a missing empty state, a plausible-looking total and an unnamed control all ship green: nothing
fails, and the only evidence is a behaviour — a retype, a second click, a support ticket, a number that
contradicts somebody's report. So each section kept its rules verbatim and gained what the reader does
when the rule is not followed, which is the half a developer needs in order to prioritise and a reviewer
needs in order to argue the point against someone who disagrees.

Numbers were pinned everywhere they are cited from outside: §1 to §5 of `data-analytics`, which
`agents/oracle` walks by number as its report structure, plus §2.4, §4.3, §5.2 and §5.3 cited by point
from that agent and from `investor-relations`, `sustainability-esg` and `people-ops`; §4.1 of
`ux-writing`, cited from `business/release-communication` §2; and §1.6 to §1.8 and §4.4 to §4.5 of
`accessibility`, which are the five WCAG 2.2 criteria the 2026-08-10 re-check closed and which that
block's own origin cites by number.

**No threshold was added to `accessibility`, deliberately.** Its figures are the ones already sourced
from WCAG; every point this pass added is a mechanism rather than a number, because a recalled threshold
is exactly the failure `skills/source-freshness` exists for — and `interface-design` §0.7 now states the
same rule from the design side, where it is the finding that gets a whole audit dismissed.

The additions worth citing across the four: an audit's findings being mostly *absence*, which is
invisible in a screenshot and therefore the part that reaches step 6 unresolved; two values both taken
from the scale still being wrong together when the gap inside a group exceeds the gap between groups; the
partial failure, the screen state nobody draws, where one region fails and the reader sees a
complete-looking screen with a silently missing number; a permission-scoped account returning a smaller
entirely valid-looking answer with nothing marking it as partial; the **grain** of a table deciding
whether a join fans out and a sum double-counts, which is invisible in a column list; zero being the
worst default for a missing value, because zero is a legitimate one; any figure someone is accountable
for becoming a target; a zero on a dashboard being a measurement and not an empty state; a
permission-empty list where "add your first item" is an instruction the reader cannot follow; a
half-translated screen failing silently because a missing key renders as its source text; a `role`
*replacing* semantics rather than adding to them; a state attribute set once at render asserting
something wrong half the time; and a disabled control announced as available while being unreachable by
keyboard.

**Third row of the extension, 2026-09-08: `global`.** Four single-file blocks beside `code-baseline`,
which had already had its pass: `skills/security-hardening` 1,030 → **4,144** in five sections,
`skills/documentation-adr` 841 → **2,909** in four, `skills/observability-instrumentation` 511 →
**3,048** in four, and `skills/api-design` 375 → **2,392** in three. No section added to any of them.
The row goes from x1.71 to **x0.94** and the table to **129,611 against 272,884**, worst still
**x8.13**, median **x1.76**. That leaves one single-file block counted anywhere in the table:
`data-pipeline-conventions`.

**`api-design` was the thinnest block in the repo at 375 rules words, and the reason is the one `spec`
had.** It was a checklist of principles an experienced reader already agrees with — contract-first,
don't expose internals, extend rather than fork — every one uncontroversial when read and useless under
pressure, because the pressure comes from a specific change that looks compatible and is not. So the
depth is almost entirely a catalogue of those cases, and the load-bearing pair is that **loosening is
compatible and tightening is not**: a validation rule added later breaks callers even though it makes
the contract stricter and more correct, and a widened type breaks every parser written against the
narrower promise.

**The other three share a different property: none of their failures is loud.** A missing authorisation
declaration returns the right data to the developer who wrote it; a log line written for the code rather
than for the incident looks fine in review and is useless at three in the morning; a deleted ADR leaves
a repo that works today and a reader who is wrong later. Each pass therefore kept its rules verbatim and
added the case where the rule gets skipped.

Numbers were pinned where they are cited from outside: §3 of `security-hardening`
(`business/data-protection`) and §2.4, the SSRF rule the 2026-08-10 OWASP check added; §1.2 and §4 of
`documentation-adr` (`skills/design-patterns` §5, and §4 also from `business/interface-design` §6); and
§1 and §2 of `observability-instrumentation`, cited from `api-design` and `security-hardening`
respectively — the second of which was added by this pass, since `security-hardening` §5 now says to
read what got logged during a hostile-value replay, which is a different exposure from the one under
test and one nothing else in that list surfaces.

The additions worth citing across the four: **default-deny** as what makes "every endpoint declares its
authorisation" enforceable rather than aspirational; every response *field* being subject to the same
decision as the endpoint; a webhook's authorisation being signature verification, since HTTP middleware
never reaches it; the lock file being the dependency inventory and the manifest the smaller half; a
dependency's install step running with your credentials before any review; cardinality being
*multiplicative*, so the fourth label added for one dashboard multiplies the bill; an error counter
incremented only on the branch somebody remembered reporting zero during an outage, which is worse than
having none; a value interpolated into a log message making every occurrence a distinct string and
defeating grouping; **duration as part of an alert's condition**, which is what separates a page from a
flap; **alerting on absence** — the job that did not run, the queue that stopped being consumed — the
class a symptom-based set misses unless written deliberately; an indefinite ADR status leaving half the
codebase compliant with both halves citing the file; and §4's asymmetry, that a held trade-off's cost is
readable in the code while its benefit is readable nowhere, so a reader comparing what they can see
against nothing concludes correctly from the available evidence and removes it.

**The extension is finished, 2026-09-08: `data-pipeline-conventions`.** The last single-file block
counted anywhere in the table, 749 → **3,212** in four sections: idempotence and reproducibility (761),
data quality (674), analytical modelling (652), performance and cost (634). No section added. The
`python` row goes from x2.62 to **x2.03** and the table to **132,073 against 272,884**, worst
**x8.13**, median **x1.76**.

**No block counted in the depth table is single-file any more.** Ten rows, and every block inside every
row now has a router in `SKILL.md` and one file per section under `references/`. The four passes of the
extension covered fifteen blocks and forty-nine sections, and added none: in every case the sections
already covered their subject and what they lacked was the mechanism.

`data-pipeline-conventions` is a subject where nothing announces itself — a non-idempotent pipeline
produces a plausible total, a skipped validation produces figures somebody acts on, a missing grain
produces a sum that double-counts, and a full reload works right up to the volume where it does not. The
additions worth citing: idempotence covering the *whole* run, so an upsert followed by a log append, a
counter or a notification is not idempotent and it is the side effect rather than the data that
duplicates; a partial run having to leave a state you can resume from or discard, since failing halfway
is the normal case; a run keyed on the wall clock being unbackfillable, which turns a one-line fix into
a manual reconstruction; late-arriving corrections making a forward-only window quietly stop matching
the source; a quarantine with a published count instead of a silent skip; the *number* of failing rows
being what makes an alert actionable; a validation with no owner getting loosened at the first
inconvenient hour and staying loosened; duplicates being defined by a business key whose wrong choice
deletes real data irrecoverably; a check that reads the pipeline's own output passing on any consistent
error; a deletion upstream being an event rather than an absence, or a historical count changes
retroactively with the evidence gone; and reusing the source's primary key letting a renumbering
upstream silently rewrite your history.

**What the table cannot show is still the part that matters.** Nine of the ten rows are at or under
x3.5 and only `csharp` remains above, at x8.13 — the stack nobody here writes. Several blocks are still
🟡 for want of a real project, and that letter is not moved by writing: `dotnet-conventions`,
`flutter-conventions`, `react-nextjs-conventions`, `php-patterns`, `accessibility`,
`data-pipeline-conventions` and `data-analytics` all say so in their own status lines. The way to move
them is to use them.

### Dogfooding, 2026-09-08: the `python` row

The way to move a 🟡 is to use the block, so the first one was used. Python is the only one of the four
🟡 stacks whose toolchain is present at all — `python3` 3.12 is installed; ruff, mypy, uv and pytest are
not, and installing them is refused by this repo's own guard, which turned out to matter.

A small stdlib-only project was written by following `python-conventions` and
`data-pipeline-conventions`: a pipeline that runs `bin/measure_depth.py --json` against a clone of this
repo, validates the payload, and stores each run in SQLite so the depth table has a history rather than
only a current value. 44 tests, green, run against the real repo. It lives outside this repo, with its
findings beside it.

**The first result is that the routers worked.** §4 (async), §6 (DI and lifetimes) and the mapper half
of §7 never applied, and the read-only-what-you-touch table kept them unread. That is the mechanism the
whole sectioning programme was for, exercised once on a real task rather than asserted.

**Four gaps, all now closed, none of which reading would have found:**

1. **The block's checkpoint could not be met in a repo with nothing installed.** `python-conventions`
   opens by saying every rule holds with nothing installed (rule A) and its checkpoint required
   `ruff check` and `mypy`, which §8.1 requires pinning. On a stdlib-only project where installs are
   refused by design, that checkpoint is unsatisfiable on code that is in fact compliant, and the block
   said nothing about what to do instead — so the honest outcomes were a false failure or a silently
   skipped checkpoint. Now §8.17 and the checkpoint state the fallback, and *no type checker available*
   is a finding rather than a pass nobody observed. This is the sharpest kind of gap: the block
   contradicted its own opening sentence, and only a project with nothing installed could show it.
2. **§8 was phrased entirely in pytest's vocabulary** — the plugin set, the test base, the fixtures —
   so the section with the most portable content in the block reads as inapplicable to a stdlib runner.
   §8.18 now states the mapping, including that `addCleanup` is what still runs after a failing
   assertion where a hand-written teardown does not.
3. **Nothing covered a database with no ORM and no migration tool**, which is what most small Python
   projects are. §7's sixteen points were mapper- and migration-tool-shaped; §7.8–§7.11 (transactions)
   turned out to be fully portable and are now said to be, and §7.18–§7.19 add the two failures the
   mapper would have handled: a create-if-not-absent script that sets up a fresh database correctly and
   silently never migrates an existing one, and the engine defaults nobody reads (referential integrity
   off unless enabled per connection, an upsert needing its conflict target named).
4. **`data-pipeline-conventions` §2.4 did not say at what granularity to quarantine.** Applied, the
   row-level version is impossible for half the checks: a duplicated key, a total disagreeing with its
   parts and an entity counted in two groups are properties of the *set*, so no row can be set aside.
   §2.4 now says the run is the quarantine unit in that case — refused by default, with a deliberate way
   to store it anyway, which is what the project implements.

**One finding landed on a hook rather than a block.** A test asserted the exact list of quality
dimensions a bad row produces, and a second dimension legitimately fired; the assertion was the defect,
not the code, and widening it is indistinguishable to `guard-test-changes.sh` from bending a test to
pass. `hooks/README.md` now carries it as a second false-positive shape, with the discipline that keeps
the two apart: **widen and pin** — narrow the original assertion to the fact it was really about, and
*add* the test stating the newly understood behaviour, so the suite grows rather than loosens. It went
from 43 tests to 44.

**Three rules carried the exercise**, and they are the argument for the pipeline block: §1.2
(traceability — source, code version, timestamp) became the raw-run table and is what makes a wrong
figure attributable at all; §1.4 (never write over the file you were handed) became the payload stored
byte for byte, so the raw layer is a table rather than a discipline; §2.7 (count rows in, out, rejected,
every run) became the most useful line of the command's output. All three were actionable with no
translation.

**The row does not turn 🟢.** One small stdlib project, written by the same agent that wrote the blocks,
is not production experience — `python-conventions` still carries its special status and `samwise` keeps
its question register. What the exercise bought is four defects that reading four times had not found,
which is the whole case for doing the other three.

### Dogfooding, 2026-09-09: the `php` row

Second of the four 🟡 stacks, and the toolchain question was settled by container rather than by
install: `php:8.4-cli` and `composer:2` images, so nothing was installed on the machine and the repo's
own `hooks/block-installs.sh` never had to be argued with.

A small framework-free PHP CLI was written against `skills/php-patterns` as its only reference: it
reports how old the dated source stamps behind each block in this repo are — one line per block, the age
of its newest stamp in whole days, a freshness verdict against a threshold, `--grep` over the claims and
a JSON mode. PHPUnit as the only dev dependency, 52 tests green, run against the real clone. It lives
outside this repo, with its findings beside it.

**Four gaps in `php-patterns`, all now closed, and one finding that landed on another block:**

1. **`createFromFormat` normalises an impossible day and reports it as a *warning*.** `'!Y-m-d'` against
   `2026-02-30` returns a valid object holding 2026-03-02, with `warning_count: 1` and `error_count: 0` —
   so the `=== false` check §2.9 teaches passes it, and so does a guard on the error count. §5.4 already
   stated calendar overflow for *arithmetic*; parsing is where it bites first, because the invalid day
   arrives from outside. This is the one that failed a test written against correct-looking code
   (§5.15).
2. **A `DateInterval`'s `days` is unsigned.** `$from->diff($to)->days` is the same number in both
   directions and only `invert` carries the sign, so a "days remaining" reads correctly on every fixture
   built in the expected order and becomes "days overdue" with the same figure on the screen for the rows
   in the other one. The block covered date arithmetic thoroughly and never mentioned the diff object,
   which is what every age, deadline and retention computation goes through (§5.16).
3. **`final` by default makes the class undoubleable, and the block never said which rule to reach
   for.** PHPUnit refuses a final class outright, the tempting fix is deleting the keyword, and the
   intended one was already there one section earlier — §3.2's interface at the edge, with the concrete
   class staying final and the test passing its own implementation. §3.5 and §3.2 are a pair and nothing
   said so (§3.15).
4. **The deep-copy fix in §3.9 fatals on a `readonly` property before PHP 8.3.** Reassigning a readonly
   property inside `__clone` is `Error: Cannot modify readonly property` up to 8.2 and legal from 8.3, so
   on a project pinned below that version the block prescribed a fix that dies the first time a clone
   runs. Measured both ways, same file: fatal on `php:8.2-cli`, an independent copy on `php:8.4-cli`
   (§3.16).

**The checkpoint also assumed the framework.** `## Output / checkpoint` routed to `gate` (7) and `review`
(8, `gimli`), both of which sit above the Laravel layer, and said nothing about how framework-free PHP
gets verified — the choice of PHPUnit here was the author's, not the block's. It now names the fallback,
and "no static analyser installed" is a finding rather than a checkpoint skipped in silence.

**One finding landed on `skills/source-freshness` rather than on the PHP block**, and it took a tool to
see: that block requires every external fact to carry the date it was verified, and both kinds of event
end up as bare prose dates. "Re-checked directly against the PSR-12 text on 2026-08-10" is a
verification; "sectioned and deepened 2026-09-08" is an edit; nothing marks which is which, so the newest
date in a file is whichever happened last. Measured on this repo: **all 21 blocks with an `origin.md`
report a newest stamp of 2026-09-08**, the depth pass — the question the block exists to answer,
unanswerable from the files that are supposed to answer it. §1 now asks a stamp to say which kind of
event it records.

**Two things the pass showed and deliberately did not change.** The router discriminates almost nothing
on a language-level block: typing, error handling, structure, arrays and dates were all touched, and only
the money and randomness points of §5 never applied — that is a property of the subject, not a defect in
the table. And **the row does not turn 🟢**: one small CLI written by the same agent that wrote the block
is not in-house production experience, the operator is still new to PHP, and `gimli` keeps its question
register.

### Dogfooding, 2026-09-09: the `csharp` row

Third of the four 🟡 stacks, container again rather than install: the `mcr.microsoft.com/dotnet/sdk:9.0`
image, nothing on the machine.

A small .NET 9 solution was written against `skills/dotnet-conventions` as its only reference — one
console project, one xunit project, `EnableNETAnalyzers` on, `AnalysisLevel` at `latest-recommended` and
`TreatWarningsAsErrors` on, which is what the block's guardrail actually means by iterating to zero new
warnings. It checks that every `§N.M` citation in a clone of this repo resolves to a section and to a
point inside it. 36 tests green. It lives outside this repo, with its findings beside it.

**The router worked again.** §3 (authorisation) never applied and stayed unread — no endpoint, no hub, no
consumer in a file-reading console app. The other six sections were all touched.

**Five gaps in `dotnet-conventions`, all now closed, and four of the five were found by the build rather
than by reading:**

1. **CA1822 turns a stateless collaborator into a static class, and the block had no position on it.** A
   class written the way §2.1 asks but holding no fields — a parser, a checker — trips *member does not
   access instance data and can be marked as static* on every method, which is a build failure under the
   guardrail. The three ways out are not equivalent, and the one the analyser wants takes the class out
   of the container, which is exactly the substitutability §2.2 argues for (§2.15).
2. **`ValidateOnStart` on its own validates nothing.** §2.8 asks for configuration bound and validated
   once at the composition root; the validate-on-start call only forces the *registered* validations to
   run early, and the data-annotations validator ships in a package the hosting metapackage does not
   bring in. So a chain that reads as validated can be running no validation at all, and the misspelled
   key still arrives as a default (§2.16).
3. **§4.15 and §7.8 together did not compile.** Numbering every enum member explicitly leaves no member
   holding zero, and the compiler then reports a `switch` expression over every named member as
   non-exhaustive, naming `(T)0` — a build failure where warnings are errors, on precisely the arm §7.8
   said an internal value did not need. §5.13 already stated the same fact for `default(T)`; the switch
   case was missing (§7.10).
4. **CA1707 made all 36 test names a build error.** The guardrail already said the public-API naming
   guidelines apply to shared library code only; it did not say that the analyser set is therefore
   *scoped*, and the place those rules bite hardest is the test project, where underscored names are the
   readable convention (guardrails).
5. **`InvariantGlobalization` makes §6.5's human-facing half throw.** The switch — commonly set for
   container size, trimming or AOT, and usually by whoever chose the base image — makes naming any
   culture raise `CultureNotFoundException`, so the current-culture half of §6.5 stops being a wrong
   result and becomes an exception, and a test for culture-dependent formatting cannot be written at all.
   Found by a failing test (§6.13).

**What the tool then found in this repo is the bigger half.** 1,270 citations across 84 blocks. Ten did
not resolve, and eight of them were one defect repeated: **a `§N.M` is not attributable on its own**. The
number carries no block, so a reader takes the nearest block named before it on the line — and in eight
places that name was not the intended target. The sharpest shape is an `Origin` section listing who cites
what, where the natural phrasing (a backquoted block name followed by a number) states the reverse of
what it means: `business/data-analytics` claimed a §5.3 in a block that has three sections, and
`security-hardening` did the same. `api-design` named `deprecation-migration` and then cited two points
of its own third section. `design-patterns` put three citations in one sentence, two of them local and
none marked.

Four of the eight were introduced by the depth programme itself, when sections moved and origin files
started describing who cites what. All eight are fixed, plus the two sentences that described a citation
defect *in* citation notation — the repo now resolves **1,270 of 1,270**. `maintaining-blocks` §1.3 has
asked for this check since it was written and it had never been run; §1.5 now states the rule that makes
it mechanisable, which is what the ten failures were really about.

**The row does not turn 🟢.** One console solution written by the same agent that wrote the block is not
the real .NET production project this file is waiting for, and `theoden` keeps its question register.
What the exercise bought is five mechanical defects a compiler found, and a cross-reference check the
repo had been prescribing to itself and never running.

### Dogfooding, 2026-09-09: the `flutter` row

Last of the four 🟡 stacks, container again rather than install: the `ghcr.io/cirruslabs/flutter:stable`
image (Flutter 3.44, Dart 3.12), nothing on the machine.

A small Flutter app was written against `skills/flutter-conventions` as its only reference. It reads a
bundled JSON catalogue of this repo's own blocks and shows each one's source stamp as a freshness, with a
filter, a paged list, a detail screen reached by identifier, a first-run threshold behind a route guard,
and one setting. 45 Dart files, 3,419 lines, **63 tests green**, `flutter analyze` clean under
`flutter_lints` — which is what the block's guardrail means by no new lint. It lives outside this repo,
with its findings beside it.

**The router held up, with one honest exception.** §8's permissions half never applied — the app asks the
platform for nothing. §1's *first* half never applied either, and that turned out to be a finding rather
than an omission: a screen that follows §7.8 and §7.15 has no widget-side `await` at all, so §1.2's three
shapes are advice about the code the rest of the block tells you not to write.

**Seven gaps in `flutter-conventions`, all now closed, and five of the seven were found by a failing test
or a failed resolve rather than by reading:**

1. **`on Exception` misses half of what the framework throws.** The boundary that maps a load failure
   onto §4's states, written the disciplined narrow way, let a `FlutterError` for a missing asset
   straight through: `Error` is not `Exception`, and neither is a failed assertion, a bad cast or an
   unassigned `late` read. Found by a test that expected the mapped state and got the raw framework
   error (§7.18).
2. **An awaited call into the holder does not say whether it worked.** Once §7.5 puts the failure in the
   state, the method completes normally either way — so a screen that awaited a save and then left, left
   on a failed save too, with the error message rendering for one frame behind the transition. Fixed by
   moving the reaction to §7.15's listener, which also removed the widget's only `await` (§7.19).
3. **A status enum plus a nullable payload keeps the impossible combination representable**, so the
   widget asserts on the payload or invents a rendering for a state that cannot happen — the fabricated
   state §4.15 exists to prevent. The enum is still right for the flags; sealed types are what remove the
   combination rather than documenting it (§7.20).
4. **A parse moved off the main isolate is invisible to a widget test.** §8.9's advice is right and it
   moves the work outside the harness's zone: the result never reaches the awaiting future, so the test
   hangs to its timeout naming nothing. Confirmed both ways — it passes in a plain test, and inside the
   harness only with the real-async escape hatch. The seam a widget test fakes has to sit above the hop
   (§8.18).
5. **The localisation layer is generated code and it pins its own dependency.** §9.1's typed keys come
   from the framework's generator, which is the step §9.15 says not to introduce; and the SDK's
   localisation package pins one exact version of the formatting library, so adding it the ordinary way
   makes the project unresolvable while the message blames the SDK. Found by the resolver (§9.16).
6. **An unconditional settle does not hang in a widget test, it fails in under a second.** The settle
   advances a *fake* clock and gives up after ten minutes of it, and the message names the settle rather
   than the animation — so the obvious move is to allow it more time, which cannot work. §10.13's
   mechanism was right and its symptom was wrong. In the same pass: `find.byType` matches the framework's
   own copies of a widget (a page transition contributed four extra fades), and a screen with one text
   field has two scrollables, so a scroll helper cannot tell which to drive (§10.17).
7. **The composition root has nowhere to live in §10.3's two layers.** A centralised route table imports
   every feature's screens, so it is not technical; it belongs to no feature, so it is not functional.
   Met by construction on the first route, and answered with a third top-level folder that imports both
   layers and is imported by neither (§10.18).

**And the rules that held, which is the other half of the exercise.** §4.13's forced-failure switch made
all four screen states reachable from the command line, so the loading and error screens were looked at
rather than assumed; §6.7's in-flight flag turned three next-page triggers in one frame into one request;
§4.10's stale marker was the one place the obvious code would have silently gone on showing old data; and
§9.8's reduce-motion fallback, written for accessibility, is the only reason a settle on the loading
screen returns at all.

**The row does not turn 🟢.** One small app written by the same agent that wrote the block is not the
production mobile experience this block has always said it lacks, and `faramir` keeps asking questions
rather than asserting. `flutter-conventions` 10,321 → **11,195**, the `flutter` row x2.01 → **x1.86**.

**That closes the dogfooding pass over the four 🟡 stacks** — python, php, csharp, flutter — one small
real project each and twenty gaps between them, most of them surfaced by a compiler, a resolver or a
failing test rather than by a reading. Not one row turned 🟢, which is the honest outcome: the exercise
proves the rules are mechanically true, not that they have been through production.

### Citations, 2026-09-09: the number nothing checked

The `csharp` dogfood project above was a citation resolver, and it found ten wrong citations in this repo
the first time it ran — which left the question that entry deliberately did not answer: a check living in
a project outside the repo runs when somebody remembers it. It is now `bin/check_citations.py` (stdlib
Python, `--json` and `--root`), and `bin/test_check_citations.py` puts it in the gate. Nine suites, **201
checks**.

**Re-implementing the same check found four more defects of the same shape.** The second version
attributes more strictly and counts every `§` in the repo rather than only those inside a block: 1,828
citations resolved, and all four it added were the class `skills/maintaining-blocks` §1.5 names — a number
sitting after a backquoted block name, meaning the citing block's own section. Three were in this file and
one in `spec`'s `Origin`, and all four are in paragraphs *about* citation defects. They are reworded
rather than renumbered: the numbers were right, the attribution was not. Which is also the tool's one
known limit — a sentence describing a wrong citation cannot state it in citation notation, so those
sentences now say it in words.

**The attribution rules are checked against fixtures, not against the repo.** A checker whose only test
is "the repo is clean" passes just as happily once somebody loosens it into finding nothing, so the suite
builds a two-block repo in a temporary directory and asserts each rule on its own: the `here` marker, a
name inside a closed parenthetical, a sentence break handing the number back to the citing block, a
document name rather than a block name, a bare name without backticks, both section-heading shapes, and a
single-file block whose sections are inline. Two checks failed on the first run — one fixture of mine
cited a point that legitimately existed, and the assertion that the gate runs this suite was true only
after I wired it.

### Dogfooding, 2026-09-09: the `hooks/` pair, wired into a real repo

`hooks/README.md` and two rows of the backlog above carried the same line for a month — *per-repo wiring
still to do*. A hook nobody wired is a script, so the three scripts went into a real project: a NestJS
repo of ours, `.claude/hooks/` plus the `.claude/settings.json` block the README prescribes, an evidence
directory, nothing installed.

**The limit first, because it bounds everything below.** The headless CLI in that environment could not
authenticate (`OAuth session expired`), so no live session was refused by these hooks. What was exercised
is the layer under that: the real `PreToolUse` payloads the runtime sends, on stdin, from that repo, over
its own files — every command its `package.json` declares (39 scripts), the dozen an agent types by hand,
and seven edits to one of its spec files. 52 commands and 7 edits. That is enough to find what a fixture
cannot, and not enough to call the pair dogfooded in the sense a session is.

**Four defects, all now fixed.**

1. **`pnpm exec` was refused as "a node package manager install".** It is how a single test file gets run
   in that repo, and it fetches nothing — `pnpm exec` runs a binary already in `node_modules`. Worse, the
   same action spelled `pnpm prisma …` went straight through, so the guard contradicted itself between
   two spellings of one command, and its message named an install the agent had not attempted, which
   sends the agent looking for another wording rather than reading the refusal. `exec` is out of the
   install verbs; `npm exec` stays blocked because it is `npx` under another name, and `dlx`/`npx`/`bunx`
   are untouched — they do fetch.
2. **A formatted assertion hid its expected value from the guard.** Prettier puts the value on its own
   line, so changing `retentionDays: 30` to `60` touched no line matching an assertion pattern and the
   edit was allowed — the exact move `skills/debug` §3.4 names, in the dominant formatting style of a
   TypeScript repo. The guard now reads an assertion as the matching line *plus every line it spans until
   its brackets balance*.
3. **The hunk alone does not carry the assertion.** The smallest edit that changes an expected value
   contains no `expect(` at all, so even statement-level comparison saw nothing in it. The file is now
   read from disk and the replacement applied to it (`replace_all` included) before comparing.
4. **A reformat read as a removal.** Inlining a multi-line assertion, or re-indenting one, changed its
   text and was blocked although it weakened nothing. Comparison is now whitespace-collapsed, with a
   comma before a closing bracket dropped — the one a formatter deletes when it inlines a call.

**Renaming the symbol under test still blocks, and that is now written down with its cost.** The
assertion text changed and no heuristic here can tell a rename from a retargeting. The escape hatch is an
environment variable scoped to the *task*, not to the edit, so an agent that learns to set it for a
legitimate rename has switched the guard off for everything after — a false positive on a routine
refactor does not merely annoy, it teaches the bypass.

**What the wiring itself taught, which no test could.** That repo ignores `.claude/` wholesale, like most
repos: everything the README tells you to write lands untracked, so the hooks protect the machine that
wired them and no colleague who clones. And the README says to *copy* the scripts in — which forks them
at copy time, the precise failure `bin/install-git-hooks.sh` was rewritten to stop doing for this repo's
own gate (`test_git_hooks.py` exists because a copied hook reported green while running an older suite).
Both are now stated at the wiring instructions as decisions to take, not defaults to inherit.

**The gate pair is inert outside the pipeline**, confirmed rather than assumed: that repo produces no
`test-results.json`, so `verify-gate.sh` guards a file that does not exist and `record-read.sh` writes a
log nobody reads. The README already said to wire `block-installs.sh` first and alone; it now says why
from measurement.

**A fifth defect, found by the check written for the fourth.** `hooks/block-installs.sh` has been in
this repo without its executable bit since it was added on 2026-08-07 — the one hook the README tells you
to wire first, and the runtime runs a hook by executing its path. The dogfood did not catch it because
the script that wired it ran `chmod +x` on the copies, which is exactly how a packaging defect stays
invisible. `bin/test_hooks.py` now asserts the bit on every file in `hooks/`, and the same commit that
found this had dropped it on two more files by editing them.

`bin/test_hooks.py` 68 → **77 checks** (72 commands, plus one per hook for the executable bit),
`bin/test_guard_test_changes.py` 12 → **18**, six of them the formatted shape. The gate is nine suites,
**216 checks**. No row turns 🟢: these hooks have still never refused a live tool call, and that is the
next real occasion to wait for rather than to manufacture.

### Widening, 2026-09-09: the `csharp` row, against the platform rather than the catalogue

The `csharp` row was the furthest behind in the table (x7.57) and the question it raised had already been
answered once: coverage. All 37 of the source catalogue's skills were re-diffed on 2026-09-07 and 22 were
already covered here, so the deficit was never a list of missing rules — it is a code example per rule on
their side against a mechanism per rule on ours. Padding that gap would be writing their block.

So this pass asked a different question: **what does the platform now do that this block says nothing
about?** Checked against the vendor's own current documentation — HTTP resilience, native AOT and
trimming, reflection versus source-generated serialisation, enumerator cancellation, the lock-object
proposal, the time-abstraction testing page, EF Core split queries and the bulk update and delete
statements. Two sections and nine points came out of it, none of them a version number:

**§8, resilience and throttling at the boundary.** The standard resilience handler retries every HTTP
method unless told otherwise, so a `POST` duplicates the first time an attempt times out after the server
committed; the four nested timeouts have to be arithmetic, because a per-attempt budget larger than the
total means the retry never happens; backoff without jitter synchronises the herd it exists to spread; a
circuit breaker buys stability with silence, since once it is open the errors stop reaching the log;
inbound limiting is middleware and not a client strategy, and its position decides whether the partition
key can be anything but the address; the limiter answers 503 rather than 429 unless told, which makes our
own limit unreadable to the client that caused it; and liveness against readiness, where the same check
wired to the wrong one restarts the process instead of taking it out of the pool. The generic half stayed
where it was — `code-baseline` §4 and `background-jobs-conventions` — and the new section cites both
rather than restating them.

**§9, what only breaks at publish.** Reflection-based serialisation is disabled in a trimmed or
ahead-of-time publish, so the code that used it throws at the first request instead of failing the build;
trimming keeps what it can see, so reflection over a computed name loses a member and the error names
something you did not write; the publish warnings are the review surface and a baseline of them is a list
of things that will throw; single-file publishing empties the assembly's own location, so a path resolved
relative to it silently reads the working directory; and one smoke test against the published artefact is
what turns the whole section from advice into a check. This is the section a block written from analysers
could not have: every rule in it is invisible to the compiler.

Seven more points landed in the existing sections, and the two worth naming here are both silent by
construction: **a bulk update or delete bypasses the change tracker and with it the global query
filters**, soft delete included, so it reaches rows the application considers deleted; and **an async
iterator's cancellation token is not the consumer's** without the enumerator-cancellation annotation, so
`await foreach` cancels nothing and the compiler's warning is the only sign. The others: two collection
includes multiplying the rows and split queries paying for it in round trips with no transaction, raw
SQL's two forms differing by one character and a vulnerability class, keyed registrations as the answer to
two implementations of one interface, the three options interfaces being three lifetimes (a snapshot in a
singleton is a captive dependency with no symptoms), a cross-origin policy not being authorisation, and
the backing-field keyword and extension members with the traps each one carries.

`dotnet-conventions` 7,490 → **9,727**, the row x7.57 → **x5.83**. **The status does not move.** Nobody
here writes C# on a real project, `theoden` keeps its question register, and a thicker block read by
nobody is still 🟡 — what the pass buys is that the block now covers the failures that appear after the
build, which is where a stack with no production experience was least likely to be right.

### Widening, 2026-09-09: the `design-patterns` row, against the source catalogue's own examples

The 2026-08-10 coverage pass checked every one of the classic 22 patterns against this file's verdicts and
found all 22 already resolved — subtracted, dismissed, entry-conditioned or named an escape valve. That
pass never asked the other question: whether the org catalogue's per-pattern *implementation* skills, read
directly from the installed clone, named a failure mode this file's seven entry conditions say nothing
about. They did, seven times, and none of the seven restates the pattern — each is a mechanism a first
implementation gets wrong.

**§4.7, transaction boundaries, gained the three ways the boundary breaks silently once it exists.** A
flush is not a commit — sending statements to the database makes rows visible to *that* connection only,
so a test asserting through the same connection can pass on an operation that never committed. A
transaction opened inside a transaction is usually a savepoint, not a second transaction: its rollback
undoes only the inner part, and the outer commit keeps going regardless, which is the opposite of what
"nested transaction" suggests to someone who has not read the driver's behaviour. And a model's own
lifecycle events fire *inside* the boundary that wraps the operation touching that model, so a listener
reacting to created or saved runs before the row is guaranteed to survive — the same failure §4.7 already
named for a job dispatched inside the transaction, just triggered by the framework itself instead of by
application code.

**§4 gained seven more points**, one per pattern shape the source catalogue's implementation files
decide and this file had left implicit: an illegal state transition has to be an exception, because a
boolean return is a promise every caller is free to ignore; the enum name stays queryable data once its
behaviour moves into classes — replacing rather than shadowing it breaks every report that groups by it;
a resolver needs three different answers for a key it cannot find, and which one applies depends on
where the key came from — our own code (a bug), a request or payload (input, rejected at the boundary),
or a legitimately optional integration (§4.3's Null Object); a pipeline's halt needs two distinct
signals, because "nothing left to do" and "the run must fail" read as the same return type and are not
the same outcome; several ways to construct one thing are named constructors, and the word *factory* is
what turns that into an unnecessary class; a boolean parameter that changes what a method does is two
methods sharing one signature, which is Strategy's precondition rather than a case for one; and a value
object never crosses the wire in either direction, because serialising it couples the API's contract to
the domain's and deserialising into it skips the validation it exists to guarantee.

**§1 gained the rule its twelve points had never stated: how to introduce a pattern into code that
already has the shape without the name.** Most work arrives on a status column with a `switch` in four
places, not on a blank file, and the two failure directions are opposite each other — introducing the
pattern in the same change as new behaviour hides which one broke a test, and refusing the fifth branch
of an existing `switch` on the grounds that refactoring is out of scope lets the thing this file exists to
prevent keep growing. The refactor is its own change, with the existing behaviour pinned by tests first.

`design-patterns` 6,333 → **7,369 words**, the row x1.92 → **x1.65** — the closest it has been, and closer
than three of the seven other stack rows in the table. **Status unchanged**: the new points are read from
a source rather than confirmed by a real review, closer in kind to §4's original seven entries than to
§1/§2/§3/§6, which this repo's own review history produced.

### Splitting the roster, 2026-09-09: `morpheus` into eight Laravel layer agents

The comparison against a per-stack Claude Code agent catalogue's own roster surfaced one structural gap
this repo's mining passes had never asked about: they run eight agents on the same stack, one per layer
(design, data, HTTP, async, console commands, tests, debugging, clarity), and `morpheus` did all of it in
one. Padding `morpheus`'s prose would not close that gap — the value in their roster is the boundary
between roles, not extra words inside one.

**`design-patterns` §1.13's own rule governed whether to build this at all**: introduce a structure only
at the second real case, never on the strength of "it might help". The second real case here is not
speculative — it is the same failure `writing-agents`' step 1 exists to catch, just inverted: a single
agent covering eight distinct failure surfaces (a migration, a controller, a queued job, a scheduled
command, a test tier decision, a stack trace, a refactor, a design decision) is exactly the shape a
reviewer cannot hold in their head at once, which is why the source roster split it in the first place.

**Eight new agents**, each the single 7-pillar template (`writing-agents`), none copying the source
roster's actual prompts — only the boundary and the name, credited the way `morpheus` already credits its
own market inspiration:

- **`laravel-architect`** — plans a feature before any code exists (schema, API surface, permission
  model, the breakdown handed to the seven below); read-only, `opus`, `effort: xhigh` (a wrong design
  decision is expensive to walk back after five builders have executed it).
- **`laravel-eloquent-expert`** — models, migrations, casts, relationships, factories, seeders.
- **`laravel-api-expert`** — routes, controllers, Form Requests, API Resources, lomkit endpoints.
- **`laravel-events-expert`** — events, listeners, queued jobs, notifications, mail; states the
  transaction-boundary rule explicitly (`design-patterns` §4.7 — a job dispatched inside a transaction
  can be picked up before the commit).
- **`laravel-commands-expert`** — Artisan commands and their scheduling, with the overlap guard a
  scheduled command needs the moment it can run twice at once.
- **`laravel-testing-expert`** — the Feature-vs-Unit tier decision and factory-driven PHPUnit tests,
  explicitly deferring to `dozer`'s default-FAIL contract where both apply.
- **`laravel-debugger`** — root-cause before fix (`skills/debug`), fixes the implementation, never
  loosens an assertion without the human-decision path `skills/debug` §3.4 and
  `hooks/guard-test-changes.sh` already state.
- **`laravel-simplifier`** — a behaviour-preserving clarity pass, matching the altitude of the generic
  `simplify` skill (reuse/simplification/efficiency, never a bug hunt) applied to this stack; a real
  defect spotted mid-pass is named and handed off, never folded into the refactor.

**`morpheus` did not disappear.** It stays the generalist for a change too small to justify picking a
specialist, or one that genuinely spans several layers in one sitting — the same reasoning `elrond`
already applies on the review side (one router, several specialists, plus a generalist path where
splitting would cost more than it buys).

**One naming exception, stated rather than hidden.** Every other build/audit agent in this repo carries
either a Lord-of-the-Rings name (review, never edits) or a Matrix name (build/audit, takes part in the
dev cycle) — the two-family convention `README.md` documents as a readable guarantee. The eight new
agents are named for their layer instead, on purpose: the whole point of the split is a legible mapping
from failure surface to agent, which a themed name would obscure. They still hold the guarantee the
families exist to signal — `laravel-architect` never writes, the seven builders never review their own
diff — the frontmatter enforces it (`disallowedTools` on `laravel-architect`), the name doesn't have to.

Registry: 25 agents → **33**. `bin/test_frontmatter.py` and `bin/test_rule_c.py` both pass against the
eight new files unchanged — no new suite, no new check, because nothing about an agent file's shape
changed. None of the eight is dogfooded; that is next real work on this stack, not a status this pass can
claim for itself.

### Widening, 2026-09-09: the `react` row, against the current React/TanStack Query surface

`react` was already the first row in the table to cross its counterpart on volume (x0.89, 2026-09-08).
Crossing a source catalogue on word count answers one question and not the other — the source catalogue
was mined at a point in time, and the ecosystem it describes keeps moving. So this pass, run the same
week as the `csharp` and `design-patterns` widenings, asked the same question of this stack: what does
the *platform* now do that this block says nothing about? Checked against React's own release notes and
TanStack Query's v5 documentation, not against the catalogue — the catalogue comparison stays settled.

**§5 gained four points on React's Actions model**, which the block predates: `useActionState` for a
form submission, collapsing the pending/result/error state §5.12 already warns against splitting across
several `setState` calls into the one shape the framework tracks together; `useFormStatus` for a submit
button that reads pending state from inside the `<form>` without prop-drilling; `useOptimistic` for the
update a user should see immediately, with §6.6's invalidate-don't-hand-write rule still governing what
the real state is once the response lands; and `use()` for reading a promise or a context conditionally,
which is exactly the case §5.1's rules-of-hooks restriction otherwise pushes above a pointless early
check. A fifth point states what changes, not what's new: a project with automatic memoisation enabled
turns §5.4's "just in case" `useMemo` from unmeasured into genuinely redundant, without repealing the
correctness exception the point already carves out.

**§6 gained two points from TanStack Query v5's own contract.** `useSuspenseQuery` accepts a narrower
option set than `useQuery` — no `enabled`, no `placeholderData` — because it is a different contract
about how the query behaves, not a stricter version of the same one; reaching for it and then trying to
bolt `enabled` back on is the tell the wrong hook was picked. And prefetching in a Server Component
buys nothing on its own: a `useQuery` in the Client Component below it refetches on mount unless the
prefetched cache is explicitly dehydrated and rehydrated, which is the usual reason a page fetches
everything twice — once on the server, once in the browser, racing the first paint.

`react-nextjs-conventions` 10,476 → **10,999 words**, the row x0.89 → **x0.85** — still the strongest
ratio in the table, now by a wider margin. Nothing added here answers the catalogue comparison a second
time; every point is dated to a current release rather than to a source that could have been checked in
2026-08.

### Widening, 2026-09-09: the `laravel` row, against the current Pest testing surface

`laravel` is the worst ratio in the table by a wide margin (x3.39) and the eleven prior passes on
`laravel-conventions` already exhausted the catalogue-comparison method — closing the remaining gap needs
many more such passes than one turn can carry, and this pass does not claim to close it. What it checked
instead, same method as `csharp`/`design-patterns`/`react` the same week, is whether §9 still describes how
Laravel tests are actually written today: the section's two-tier/routing/anti-pattern argument predates
Pest becoming the ecosystem's default runner, and said nothing about it.

Four points added to `09-tests-static-analysis.md`: Pest's `it()`/expectation-API closures are a syntax
choice on the same two-tier rule (point 1), not a third tier, and mixing them with a PHPUnit class in one
file is point 7's half-migration problem under a different name; a dataset (`->with([...])`) replaces one
assertion repeated over many inputs, never cases that diverge in what they assert; an architecture test
(`arch()->expects(...)`) makes a structural rule this block already states in §1/§5 fail in CI instead of
depending on a reviewer remembering it; and mutation testing is point 18's "a line executed is not a line
asserted" made automatic — a surviving mutant is a test that would not have caught the regression.

`laravel-conventions` 11,053 → **11,317 words**; the `laravel` row (with `php-patterns` and
`inertia-conventions`) 23,531 → **23,795**, x3.39 → **x3.35**. Still the worst ratio in the table and
still tracked as a programme in §2, not a claim — nothing here answers the catalogue comparison a second
time.

### Widening, 2026-09-09: the `python` row, against the current async/tooling surface

Same method as `csharp`/`design-patterns`/`react`/`laravel` the same week, checked against the language and
toolchain's current state rather than the source catalogue (settled 2026-09-07). §4 gained `TaskGroup` as
the structured form of the block's existing gather-failure-handling point — cancelling siblings and raising
an `ExceptionGroup` by construction, caught with `except*` — plus cancellation reaching a context manager's
own `__aenter__`/`__aexit__`, the same leak shape as the block's swallowed-cancellation point arriving from
library internals. §8 gained `pytest-asyncio`'s auto mode as a config-block decision rather than a per-test
marker (a test missing the marker under strict mode collects silently as an unawaited coroutine and reports
passed), and named the faster type checkers (Pyright, Pyrefly, ty) as a one-tool swap under the existing
one-tool-per-job rule, not a personal substitution.

`python-conventions` 8,203 → **8,494 words**; the `python` row 22,097/11,486 (x1.92) → **22,097/11,777,
x1.88**. Still no production experience behind this block — depth from documented behaviour and tooling,
not review feedback, per the block's own stated caveat.

### Widening, 2026-09-09: the `flutter` row, against Riverpod's current codegen surface

Same method as the other widenings this week, checked against the state-management library's current
documented behaviour rather than the catalogue: §7's Cubit-first guidance predates `@riverpod` code
generation becoming the ecosystem default. Three points added: a generated provider disposes itself the
instant nothing watches it unless `keepAlive: true` overrides it, which is the block's own scope-is-a-decision
point made *for* the author by default; `ref.watch` (rebuild on change, inside `build`) and `ref.read`
(current value once, outside `build`) are different questions, and `read` inside `build` silently opts a
widget out of the rebuild contract; and a family provider's cache key uses the parameter's own equality, so
a parameter without `==`/`hashCode` refetches on every call for identical values.

`flutter-conventions` 11,195 → **11,412 words**; the `flutter` row 20,772/11,195 (x1.86) → **20,772/11,412,
x1.82**. Status stays 🟡 — this pass is documentation depth, not new dogfooding.

### Widening, 2026-09-09: the `nuxt` row, against Nuxt 4.4's current data-fetching surface

Same method as the other widenings this week, checked against Nuxt's own current release notes rather than
the catalogue. §9 gained two points: two `useFetch`/`useAsyncData` calls sharing a key now share one
`data`/`error`/`status` outright, so a `transform`/`default` at the second call site does not rerun for a
fetch the first already resolved — the block's explicit-key rule stops an accidental collision, this is the
same sharing invoked on purpose; and a shared `useFetch` factory wrapping the base URL, error handling and
auth header once is the fix for options repeated at every call site, keeping the block's error-handling and
context-forwarding rules centralised rather than copy-pasted per page.

`vue-nuxt-vuetify-conventions` 12,443 → **12,625 words**; the `nuxt` row x1.6 → **x1.57**.

### Widening, 2026-09-09: the `project-management` row, against the current AI-assisted-triage trend

Same method as the other widenings this week, applied to the one genuinely new thing since the block was
written: AI drafting stories and scoring backlog priority is now common tooling. Two points added rather
than a new section, because both are the block's existing argument meeting a faster way to skip it: a
tool-drafted story is still a draft, not a finding — it answers from the wording of the request rather
than from the person who has the problem, so it cannot stand in for the interview; and a tool's priority
score is an input to the impact half of the ranking, not the ranking itself, since publishing it as the
order lets the loudest-request bias back in looking objective because a number produced it.

`product-ownership` 7,616 → **7,825 words**; the `project-management` row x1.29 → **x1.26**.

### Widening, 2026-09-09: the `laravel` row, second pass — job middleware and batches

§8 covered job ordering, idempotence and failure but nothing on the framework's own coordination
mechanisms. Two points added: job middleware (`WithoutOverlapping`, `RateLimited`, `ThrottlesExceptions`)
as the declared answer to "not two of these at once" rather than a hand-rolled lock reinventing the
section's ordering point — `WithoutOverlapping` releases rather than drops a job, which still needs the
section's idempotence point; and `Bus::batch()` as coordination-for-reporting, not coordination-for-data,
since its callbacks fire once for the whole batch and a job needing another job's result is still a chain.

`laravel-conventions` 11,317 → **11,480 words**; the `laravel` row x3.35 → **x3.33**. Still the worst ratio
in the table, still tracked as a programme.

### Widening, 2026-09-09: the `laravel` row, third pass — PHP 8.4's property hooks and asymmetric visibility

`php-patterns` §1 predates PHP 8.4's property hooks and asymmetric visibility. Checked against the
language's own release notes: asymmetric visibility (`public private(set)`) added as the section's
`readonly` point generalised for a property a method legitimately mutates later, where `readonly` would
refuse the mutation outright; and a property hook added as a fix for the section's
uninitialised-property-bug point, but only where the hook computes rather than causes a side effect.

`php-patterns` 5,799 → **5,974 words**; the `laravel` row x3.33 → **x3.31**.

### Widening, 2026-09-09: the `laravel` row, fourth pass — Inertia v2's async surface

`inertia-conventions` §2 and §5 described `Inertia::lazy()` and hand-rolled polling/hover-prefetch as the
state of the art; v2 shipped first-class async mechanisms on the same underlying decisions. §2 gained
`Inertia::defer()` (fires on load, with grouping to batch several deferred props into one request) and
`<WhenVisible>` (a third trigger, on scroll-into-view, for a section far enough down that neither the
initial payload nor a deferred batch is the right cost). §5 gained `router.reload({ interval })` as the
existing interval-reload point turned into an option that stops itself on unmount, and `<Link prefetch>`
as the existing hover-prefetch point made declarative, with a `mount` trigger that multiplies the
request-count warning across every link on the page.

`inertia-conventions` 6,679 → **7,034 words**; the `laravel` row x3.31 → **x3.26**.

### Widening, 2026-09-09: the `laravel` row, fifth pass — Precognition and outbound concurrency

`laravel-conventions` §6 gained two points: `HandlePrecognitiveRequests` runs the same FormRequest the
real submission runs, which is what makes the section's validation rules reusable for as-you-type feedback
without a second endpoint — with the trap that a rule only valid once the operation runs has to be scoped
to skip during a precognitive request; and `Http::pool()` as the outbound-call equivalent of the
async-gather rule other stacks in this repo already state, with the same per-response failure decision.
`inertia-conventions` §3 gained one point closing the same loop from the frontend side: the wiring is now
the route's middleware, not a separate client-side integration, since Inertia v2.3 built Precognition into
`useForm` directly.

`laravel-conventions` 11,480 → **11,649 words**, `inertia-conventions` 7,034 → **7,118**; the `laravel` row
x3.26 → **x3.23**.

### Widening, 2026-09-09: the `laravel` row, sixth pass — `chaperone()` and `lazy()`/`cursor()`

`laravel-conventions` §4 gained two points: `chaperone()` as the framework's fix for the section's
existing N+1 point — a child reaching back for its own parent — hydrating the parent from the eager load
instead of a query per child; and `lazy()` versus `cursor()` as two different answers to the section's
chunking point, not interchangeable, since `cursor()` drops back to a full collection the moment a
Collection-only method is called on it and `lazy()` does not.

`laravel-conventions` 11,649 → **11,834 words**; the `laravel` row x3.23 → **x3.2**.

### Widening, 2026-09-09: the `laravel` row, seventh pass — `shouldBeStrict()` and generated columns

`laravel-conventions` §4 gained `Model::shouldBeStrict()` as the section's N+1 rule turned into a thrown
exception rather than a review checkpoint, bundled with two sibling checks (silent mass-assignment discard,
a read of a missing attribute) — environment-specific by design, so running it in production too trades a
caught bug for a 500 on every affected user. §3 gained the generated column (`virtualAs`/`storedAs`) as the
answer when a computed value has to be filtered, sorted or indexed by the database, distinct from an
accessor, which covers the same computation for a value nothing ever queries by.

`laravel-conventions` 11,834 → **12,034 words**; the `laravel` row x3.2 → **x3.18**.

### Widening, 2026-09-09: the `laravel` row, eighth pass — `Response::deny()`

`laravel-conventions` §2 gained one point: a policy returning `Response::deny($message)` instead of
`false` carries the reason for a 403, which is what makes the denial actionable rather than identical to
every other refusal — still a policy decision, not validation, so the message explains why this caller
may not, never what is wrong with the payload.

`laravel-conventions` 12,034 → **12,133 words**; the `laravel` row x3.18 → **x3.16**.

### Widening, 2026-09-09: the `laravel` row, ninth pass — `withExceptions()`

`laravel-conventions` §11 gained one point: `dontReport()`, `throttle()` and `stopIgnoring()` in
`bootstrap/app.php` as where the section's tracker-must-know-the-difference argument is actually enforced
— naming a class as expected once rather than catching it at every throw site, sampling a class that fires
legitimately at volume instead of either silence or flooding the tracker, and reversing the framework's
default ignore list where a spike in an otherwise-routine status is itself the signal.

`laravel-conventions` 12,133 → **12,246 words**; the `laravel` row x3.16 → **x3.15**.

### Widening, 2026-09-09: the `laravel` row, tenth pass — `Isolatable`

`laravel-conventions` §7 gained one point: the `Isolatable` interface as the section's overlap policy for
a command triggered outside the scheduler — a manual rerun, a webhook, two deploys close together — where
`withoutOverlapping` alone leaves it unprotected. The lock key defaults to the command's name, so
`isolatableId()` has to fold the arguments in or two runs with different arguments serialise work that was
actually safe to run in parallel.

`laravel-conventions` 12,246 → **12,350 words**; the `laravel` row x3.15 → **x3.14**.

### Widening, 2026-09-09: the `laravel` row, eleventh pass — `array_first()`/`array_last()` (PHP 8.5)

`php-patterns` §4 gained one point: the new functions read the first/last element without
`reset()`/`end()`'s internal-pointer mutation, without the destructive side effect of
`array_shift()`/`array_pop()`, and without the key-vs-value confusion of
`array_key_first()`/`array_key_last()` — returning `null` on an empty array, so the section's
falsy-collapse point still applies to the result.

`php-patterns` 5,974 → **6,068 words**; the `laravel` row x3.14 → **x3.13**.

### Structural pilot, 2026-09-09: five standalone triggered skills extracted from `laravel-conventions`

Eleven widening passes moved the `laravel` row from x3.39 to x3.13 at ~150-200 words each — a slow
lever against a gap that is largely a shape mismatch, not a content gap: the org catalogue's Laravel
plugin is 65 short, single-rule, individually-triggered files (~1,380 words average, mostly
frontmatter and per-file overhead), against this repo's 3 large router+sections blocks. Continuing to
add points to `references/*.md` under-credits the depth already there and over-credits the
catalogue's per-file repetition.

Piloted the alternative instead: `laravel-no-db-enums`, `laravel-no-cascade-delete`,
`laravel-no-observers`, `laravel-throw-dont-return-errors` and `laravel-no-queries-in-loops` — five
of `laravel-conventions`'s most mechanical "never do X" rules (§3.1–§3.3, §3.5–§3.10, §1.2,
§11.1–§11.5, §4.1–§4.2), each extracted to its own thin `SKILL.md` with a precise trigger and a
compressed restatement of the rule, pointing back to the parent section for the mechanism and the
full argument rather than duplicating it. This is deliberately not folded into `bin/measure_depth.py`'s
`laravel` row: these are trigger surfaces over existing reasoning, not additional depth — counting
their word count would double-count `laravel-conventions`'s own sections. The point of this pilot is
triggering granularity (does the right rule fire on a narrow, precise cue instead of only through the
whole block), not word volume; if it holds up under real use, the remaining mechanical rules in
`laravel-conventions` (no-model-scopes, no-fat-models, no-magic-strings, no-html-in-php,
mail-via-notifications, prefer-find-or-fail, and more) are candidates for the same treatment, and
other stacks after that.

### Structural pilot, 2026-09-09: second batch — five more standalone triggered skills

Confirmed the pattern holds and scaled it to five more `laravel-conventions` mechanical rules:
`laravel-scope-dont-check-after-fetch` (`laravel-conventions` §2.4 — scope the query rather than
checking after the fetch), `laravel-prefer-orfail-fetch` (`laravel-conventions` §4.3),
`laravel-mail-via-notifications` (`laravel-conventions` §6.16 and §8.7), `laravel-no-fat-models`
(`laravel-conventions` §1.1) and `laravel-no-magic-strings` (`laravel-conventions` §5.3). Same shape
as the first batch:
a precise trigger, a compressed restatement, a pointer back to the parent section — not folded into
`bin/measure_depth.py`'s `laravel` row for the same reason as the first five. Ten of `laravel`'s
mechanical rules are now covered this way; the remaining candidates (no-html-in-php,
seed-new-features, the `strict_types` default, and others across §3/§7/§9/§10) and the same treatment
for other stacks (python, flutter, nuxt) are next, on the user's confirmation to keep going in both
directions.

### Structural pilot, 2026-09-09: extended to `python-conventions`

User confirmed both directions: keep extracting `laravel-conventions`'s remaining mechanical rules,
and apply the same restructuring to the other stacks (python, flutter, nuxt). First python batch:
`python-no-implicit-truthiness` (`python-conventions` §2.1–§2.2), `python-no-bare-except`
(`python-conventions` §2.8–§2.11), `python-async-no-blocking-calls` (`python-conventions` §4.4–§4.5),
`python-no-db-cascade-delete` (`python-conventions` §7.1) and `python-no-magic-strings`
(`python-conventions` §3.7). Same shape and same reason for staying out of `bin/measure_depth.py`.
`python-no-db-cascade-delete` mirrors `laravel-no-cascade-delete` — same defect, different framework.

### Structural pilot, 2026-09-09: extended to `flutter-conventions`

Second stack in the pilot: `flutter-context-after-await` (`flutter-conventions` §1's opening rule and
§1.2), `flutter-no-controller-in-build` (`flutter-conventions` §1.14),
`flutter-dispose-what-you-create` (`flutter-conventions` §1.12–§1.13), `flutter-four-async-states`
(`flutter-conventions` §4.1–§4.2) and `flutter-no-future-in-state` (`flutter-conventions` §7.6). Same
shape, same
reason for staying out of `bin/measure_depth.py`. `flutter-context-after-await` extracts `flutter-conventions` §1's own
opening rule rather than a numbered point — that rule is the block's single most load-bearing one
("read it when always, before anything else on this stack"), and giving it its own trigger is exactly
the case this pilot exists for.

### Structural pilot, 2026-09-09: extended to `vue-nuxt-vuetify-conventions`

Third stack: `nuxt-no-props-destructure` (`vue-nuxt-vuetify-conventions` §1.9),
`nuxt-child-never-mutates-prop` (`vue-nuxt-vuetify-conventions` §1.14), `nuxt-define-store-once`
(`vue-nuxt-vuetify-conventions` §2.4), `nuxt-no-hydration-nondeterminism`
(`vue-nuxt-vuetify-conventions` §9.1–§9.2) and `nuxt-semantic-element-first`
(`vue-nuxt-vuetify-conventions` §7.1). Same shape, same reason for staying out of
`bin/measure_depth.py`. 20 standalone triggered skills now exist across four stacks
(laravel/python/flutter/nuxt); `project-management` remains, along with the rest of
`laravel-conventions`'s uncovered mechanical rules.

### Structural pilot, 2026-09-09: third `laravel-conventions` batch — idempotency and seed data

Five more mechanical rules, this time clustered around idempotency and seed data:
`laravel-pruning-fires-delete-events` (`laravel-conventions` §3.13–§3.14),
`laravel-idempotent-data-commands` (`laravel-conventions` §7.7–§7.9), `laravel-idempotent-seeders`
(`laravel-conventions` §7.12 and §9.10), `laravel-seed-new-features` (`laravel-conventions` §9.11) and
`laravel-idempotent-jobs` (`laravel-conventions` §8.2). Fifteen of `laravel`'s mechanical rules are
now covered; remaining candidates include no-html-in-php, the `strict_types` default (§5.12), and a
few more across §6/§9/§10.

### Structural pilot, 2026-09-09: fourth `laravel-conventions` batch — HTTP contract and versioning

Five more: `laravel-post-may-run-twice` (`laravel-conventions` §6.15),
`laravel-no-hand-rolled-content-negotiation` (`laravel-conventions` §6.13), `laravel-api-breaking-changes`
(`laravel-conventions` §6.14), `laravel-precognitive-request-scoping` (`laravel-conventions` §6.17) and
`laravel-support-window-date` (`laravel-conventions` §10.3). Twenty of `laravel`'s mechanical rules are
now covered by standalone triggers. Considered `product-ownership` (the closest business block to
"project management") for the same treatment and declined it: its rules are human-process guidance
(how to write a story, when to say no in a meeting) with no code-pattern trigger to fire on, unlike
every stack covered so far — forcing the same shape there would fragment it without the benefit the
pilot exists for, and business blocks are 🟡-capped by contract regardless.

### Structural pilot, 2026-09-09: fifth `laravel-conventions` batch

Five more: `laravel-permissions-not-roles` (`laravel-conventions` §2.1–§2.2),
`laravel-strict-types-default` (`laravel-conventions` §5.12), `laravel-date-via-localised-accessors`
(`laravel-conventions` §5.8), `laravel-recognise-state-machine-or-pipeline` (`laravel-conventions`
§1.5, a recognition trigger rather than a "never do X" rule — exactly the shape this pilot targets)
and `laravel-aggregate-in-database` (`laravel-conventions` §4.5). Twenty-five of `laravel`'s
mechanical rules and recognition triggers are now covered by standalone skills.

### Structural pilot, 2026-09-09: extended to `dotnet-conventions`

Fifth stack: `dotnet-dispose-what-you-own` (`dotnet-conventions` §5.9–§5.10),
`dotnet-no-swallow-exceptions` (`dotnet-conventions` §5.5), `dotnet-null-pattern-matching`
(`dotnet-conventions` §5.6), `dotnet-no-ambient-static-state` (`dotnet-conventions` §4.1) and
`dotnet-options-lifetime-mismatch` (`dotnet-conventions` §2.18). Same shape, same reason for staying
out of `bin/measure_depth.py`. 45 standalone triggered skills now exist across five stacks
(laravel/python/flutter/nuxt/dotnet).

### Widening, 2026-09-10: parallel background passes on the two worst ratios

Two background subagents, dispatched to go faster on "worst-ratio-first" widening without waiting on
each other: one widened `dotnet-conventions`' three thinnest sections (§7, §1, §4 — 10,432 → 11,762
words, x5.44 → x4.82), the other widened `laravel-conventions`' three thinnest sections (§2, §5, §8 —
15,419 → 16,839 words, taking `laravel` from x3.13 to x2.99). Both stayed inside the same constraint as
every widening pass: no XEFI marketplace content read, only public official documentation (Microsoft
Learn for .NET, Laravel's own docs for Sanctum/broadcasting/notifications) synthesised in mentis's own
voice, and neither agent touched `CATALOG.md`/`README.md` or committed — that integration stayed in the
main session. `bin/check_citations.py` stayed at 0 unresolved after both passes. Six widening passes total
on `csharp` this week; still the two worst ratios in the table (`laravel` x2.99, `csharp` x4.82), and both
still have four-to-five-figure word deficits left — this pass closes thousands of words, not tens of
thousands.

### Widening, 2026-09-10: three parallel background passes, bigger chunks

Three background subagents dispatched together, each widening more sections per file than the
previous round (5 files per stack instead of 2-3, 500-700 words each): `csharp` (§2, §3, §6, §8,
§9 of `dotnet-conventions`, x4.82 → x3.97), `laravel` (§1, §3, §4, §6, §7, §10, §11 of
`laravel-conventions`, x2.99 → x2.69) and `python` (§1, §2, §3, §5, §6 of `python-conventions`,
x1.88 → x1.52). All three sourced only from public official documentation (Microsoft Learn,
Laravel's own docs, PEP/stdlib docs) plus this repo's own existing text — no XEFI marketplace
content read. One of the three background attempts (the first `laravel` dispatch) delegated to a
nested sub-agent instead of doing the work directly and reported success with zero files changed;
caught by checking `git status` before trusting the report, and re-dispatched with an explicit
"do this yourself, no nested Agent calls" instruction. `bin/check_citations.py` stayed at 0
unresolved across all three passes combined. Six stacks now still under parity
(`design-patterns`, `flutter`, `nuxt`, `project-management` untouched this round); `csharp` and
`laravel` remain the two worst ratios, each still with a four-to-five-figure word deficit.

### Widening, 2026-09-10: three more parallel background passes

Continuing worst-ratio-first: `csharp` (x3.97 → x3.31, 5 more sections of `dotnet-conventions`),
`laravel` (x2.69 → x2.48, 5 more sections of `laravel-conventions`, all files in that block now
widened at least once) and `flutter` (x1.82 → x1.48, 5 sections of `flutter-conventions`, its
first widening pass). All three sourced from public official documentation only (Microsoft
Learn/.NET Blog, Laravel docs, flutter.dev/dart.dev) — no XEFI marketplace content read, and this
round's agent prompts explicitly forbade writing the marketplace's literal filesystem path into
any file (an earlier pass had written it into `origin.md` and tripped the secrets-scan suite in
`bin/pre-push`). `bin/check_citations.py` stayed at 0 unresolved. `csharp` and `laravel` remain
the two worst ratios; `flutter` moved from mid-table to ahead of `nuxt` and `design-patterns`.

### Widening, 2026-09-10: fourth round, three more parallel background passes

Continuing worst-ratio-first: `design-patterns` (x1.65 → x1.3, first widening pass on this block —
its five thinnest sections), `nuxt` (x1.57 → x1.37, five sections of `vue-nuxt-vuetify-conventions`)
and `csharp` (x3.31 → x2.88, a fourth pass on `dotnet-conventions`, now every section widened at
least twice). All sourced from public documentation only (refactoring.guru/GoF-style pattern
literature, vuejs.org/vuetifyjs.com, Microsoft Learn/.NET Blog) — no XEFI marketplace content
read, no literal marketplace path written anywhere. `bin/check_citations.py` stayed at 0
unresolved; one agent introduced a self-citation typo (`§8` where the block has no §8) and caught
and fixed it itself before reporting. `laravel` and `csharp` remain the two worst ratios, both
still with a five-figure word deficit; `design-patterns` and `nuxt` are now both under x1.4.

### Widening, 2026-09-10: fifth round, three more parallel background passes

Continuing worst-ratio-first: `csharp` (x2.88 → x2.43, a fifth pass on `dotnet-conventions`),
`laravel` (x2.48 → x2.25, a fourth pass on `laravel-conventions`) and `project-management`
(x1.26 → x1.07, first widening pass, split across `business/product-ownership` and `skills/spec`
— now within a thousand words of parity, the closest any under-parity stack has come). All
sourced from public documentation only (Microsoft Learn/.NET Blog/Polly docs, Laravel 12.x docs,
public product-ownership/agile literature) — no XEFI marketplace content read, no literal
marketplace path written. `bin/check_citations.py` stayed at 0 unresolved. `laravel` and `csharp`
remain the two worst ratios by a wide margin (both still five-figure word deficits); every other
tracked stack is now under x1.55.

### Widening, 2026-09-10: sixth round, three more parallel background passes

Continuing worst-ratio-first: `csharp` (x2.43 → x2.12, a sixth pass on `dotnet-conventions`),
`laravel` (x2.25 → x2.1, a fifth pass on `laravel-conventions`) and `python` (x1.52 → x1.39, a
second pass, this time on the three sections the first pass hadn't reached). The first `python`
dispatch found nothing left to add — it correctly detected that a prior pass in this same session
had already widened its five assigned files and reported that honestly instead of duplicating
content, so it was re-dispatched at the three untouched files instead. All sourced from public
documentation only — no XEFI marketplace content read, no literal marketplace path written.
`bin/check_citations.py` stayed at 0 unresolved. `laravel` and `csharp` are now both just above
x2, the closest they've been; every other stack is under x1.5.

### Widening, 2026-09-10: seventh round — csharp and laravel both drop below x2

Continuing worst-ratio-first: `csharp` (x2.12 → x1.89, a seventh pass on `dotnet-conventions`),
`laravel` (x2.1 → x1.96, a sixth pass on `laravel-conventions`) and `flutter` (x1.48 → x1.27, a
second pass on `flutter-conventions`, its five previously-untouched sections). This is the first
time either `csharp` or `laravel` has been below x2 since this widening programme started — both
began the day at x5+ (`csharp` x5.83, `laravel` x3.13 as tracked earlier in this log). All sourced
from public documentation only — no XEFI marketplace content read, no literal marketplace path
written. `bin/check_citations.py` stayed at 0 unresolved (one agent introduced a stale
self-citation off-by-one, `§1.40` where the section only reached point 39, and caught and fixed
it before reporting). Every tracked stack is now under x2; `python` (x1.39), `nuxt` (x1.37) and
`design-patterns` (x1.3) are the next thinnest after `flutter`.

### Widening, 2026-09-10: eighth round — every stack now under x1.85

Continuing worst-ratio-first: `laravel` (x1.96 → x1.81, a seventh pass), `csharp` (x1.89 → x1.70,
an eighth pass) and `python` (x1.39 → x1.21, a third pass, its five original files re-widened).
All sourced from public documentation only — no XEFI marketplace content read, no literal
marketplace path written. `bin/check_citations.py` stayed at 0 unresolved across all three. Every
tracked stack is now under x1.85; `nuxt` (x1.37), `flutter` (x1.27), `design-patterns` (x1.3) and
`project-management` (x1.07) are the remaining gaps, all under 6,000 words each.

## 3. The rule that keeps us "in control" (reminder)

We never wire a repo in as a dependency. We read → we extract the mechanism → we **rewrite** it
in the single template → we credit `Origin`. See the adoption checklist in `CONVENTIONS.md`.
That's what guarantees: nobody upstream breaks our workflow, and everything is written the same
way (maintainable). The backlog above is our enrichment queue, we dip into it when a step has a
real gap, not to pile things up.
