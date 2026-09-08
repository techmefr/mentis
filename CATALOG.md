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
| C#/.NET | `csharp` (15 at mining, 37 at the 2026-09-07 bodies pass) | `skills/dotnet-conventions`, rewritten self-contained (7 sections: §7 and 10 points added 2026-09-07) |
| Design system | `design` (10) | **`business/interface-design`** (new): token discipline, container decision tree, required screen states, button hierarchy, chips by kind, icon-text coupling, reference gathering — **house values deliberately excluded** |
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
| spec | 2 | a market skill catalogue (grill-with-docs) + internal | 🟡 |
| archi | 3 | internal graphify + a three-way dedup pass (name, shape, call site) with the negative result recorded | 🟡 (dedup mechanism written, not dogfooded yet) |
| plan | 4 | a market skill catalogue (planning-and-task-breakdown) | 🟡 |
| tdd | 5 | our own `test-casebook` + market long-running agent patterns (default-FAIL contract); the no-test-tampering sibling rule for the code step added 2026-08-11 | 🟡 |
| code | 6 | native + internal; no-test-tampering guardrail added 2026-08-11, named directly by the operator | 🟡 |
| vue-nuxt-vuetify-conventions | 6 | several market Vue/Nuxt/Vuetify skill catalogues (Vue patterns, Nuxt4, Nuxt composables, Vuetify) + a market Nuxt/Vue linter (correctness/security) + a market open source TypeScript project (a11y/bundle) + de-identified internal review feedback (recurring patterns); re-checked directly against the public vue.doctor/nuxt.doctor tools on 2026-08-10, which surfaced 2 real gaps (compiler-macro import, useAsyncData key default) now closed; §13 added and §4 deepened 2026-09-07 by a **bodies pass** over the same org catalogue (21 skills): the first pass had read descriptions only, the bodies carried four mechanisms it could not see — BEM's out-of-scheme shapes, the class/style split and its extract-to-computed threshold, opting a folder into the framework's import scan, and the typed-client layer whose real weight is the hydration-typing trap and the shared applied state between two handles on one record; **depth pass 2026-09-08** on the three thinnest sections (§10 realtime 113 → 875 words, §2 composables/stores 211 → 944, §3 typing 174 → 899), which stated rules without the failures they prevent — two of the additions are real absences rather than restatements: module-scope state shared *across SSR requests* (a cross-account leak the block never named) and a private channel "authorised" by a name the client itself composes; **second pass the same day** on §7 accessibility (172 → 899) and §6 i18n (199 → 877), both of which were true-but-terse checklists — §7 gained the placeholder-as-label, unattached-error, colour-as-sole-meaning, removed-focus-outline, hover-only-action and no-page-language failures plus the voice-control consequence of an accessible name that omits the visible text, and §6 the mistakes that are correct in the source language and wrong elsewhere (a `n > 1` ternary for plurals, concatenated sentences, a translation rendered as HTML, hand-formatted dates, German's ~30% expansion, one key reused for two meanings) | 🟡 |
| react-nextjs-conventions | 6 | a market React skill catalogue (best practices) + a market React/Node skill catalogue (redux-toolkit) + a market shadcn skill catalogue + a market React linter (correctness/security section) + a market open source TypeScript project (a11y/bundle); re-checked directly against the public React Doctor tool (react.doctor) on 2026-08-10, which surfaced 3 real gaps (prop drilling, setState-count/useTransition, missing alt) now closed; **depth pass 2026-09-08 on all ten sections** (3,002 → 10,476 words of rules), each original rule kept verbatim and given the mechanism plus what a reader sees when it breaks — the additions that were real absences rather than elaborations are a `NEXT_PUBLIC_` variable as published content, a Server Component's props being serialised into the HTML payload, a cookie-only `POST` route handler having no origin check where a Server Action does, changing the wrapper element unmounting the subtree it wraps, a cleanup running on every dependency change, browser-seeded state breaking hydration, a query key missing an input so two requests share a cache entry, and reading cookies opting a whole route tree out of static rendering | 🟡 (written, not dogfooded yet — depth is not dogfooding, and this block still has no React repo behind it) |
| over-engineering-review | 9 | a market deletion-oriented review tool (deletion angle, tags, net line score) | 🟡 |
| nestjs-node-conventions | 6 | a market NestJS skill catalogue + an advanced market TypeScript skill + a market React/Node skill catalogue (prisma/trpc/zod) | 🟡 (written, not dogfooded yet; first mentis block for the Node backend) |
| inertia-conventions | 6 (new 2026-08-11) | official Inertia.js documentation (shared data via `HandleInertiaRequests`, `useForm`, partial/lazy/deferred reloads) + current Laravel+Inertia integration practice (typed props from the same DTO/resource, Laravel Precognition); §4 (the override against `laravel-conventions`/Nuxt-Next-specific sections) is ours, written after a real conflict: a Laravel+Inertia repo reviewed against REST/lomkit and Nuxt-runtime expectations that don't hold for that architecture, and neither this repo nor the installed org catalogue (its Laravel and Nuxt plugins) covered Inertia at all before this; §4.5/§4.6 went through two revisions the same day — a project-level "is the REST package a dependency" test was too coarse for a project running **both** Inertia (pages) and the REST package (a separate real API) at once, a real reported case; the fix checks the specific controller (what it returns, where it's routed) instead; §4 point 7 added 2026-08-11 — a CdP running the fixed version still had their own Claude session say "conflict between mentis and the house rules" and deleted their whole setup over a case that was already resolved, so every stack block's override paragraph now says explicitly to apply the resolution and move on, never report it as an open conflict; **sectioned and deepened 2026-09-08** — the five sections that lived inline in `SKILL.md` moved to one file each under `references/`, a sixth was added, the router became a table of triggers, and every section took the same depth pass as the sectioned blocks (1,705 → 6,679 words of rules, taking the `laravel` row from x5.82 to x4.27). §4 kept its number and every point number inside it, because three other blocks cite it and this block's own guardrails cite §4.5/§4.6; tests moved from §5 to §6, which nothing outside the block cited. The new §5 is the visit lifecycle, on which the block had said nothing: scroll and local state reset on every visit unless preserved, the cancelled-visit rule that makes a search box correct for free, an asset version that has to be wired to the build or a browser open across a deploy keeps running the old bundle, page data living in the browser's history entry and so surviving a logout on a shared machine, prefetch issuing real requests against `GET` routes with side effects, SSR being an optional second process. The other addition worth citing is what the reader can actually read: a page's props are in the HTML and in devtools whether a component renders them or not (§2.6), which is why authorization belongs in the controller before they are computed (§1.8) and why a negative assertion is the only test that catches a leak (§6.5) | 🟡 (no in-house Inertia production experience yet; `laravel-conventions` §6 and `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`' intros now point here) |
| typescript-patterns | 6 | internal synthesis (real production experience from the operator on pure TS/JS) | 🟢 |
| php-patterns | 6 | PHP-FIG (PSR-12) + official PHP docs; re-checked directly against the PSR-12 text on 2026-08-10 — almost all of it is formatting already covered by Pint/PHP-CS-Fixer, `declare(strict_types=1)` was the one real gap (the one PSR-12 rule with runtime effect); §1.1 corrected 2026-08-11 against the real, installed org catalogue's Laravel plugin (`no-strict-types`) — Laravel deliberately omits the declaration at its framework boundary (loose scalars in from routes/requests/config, Larastan does the static enforcement instead), a real, dogfooded, currently-installed reversal of the PSR-12 default that neither this block nor `laravel-conventions` named explicitly until now; **sectioned and deepened 2026-09-08** — the three sections that lived inline in `SKILL.md` moved to one file each under `references/`, two were added, the router became a table of triggers (960 → 5,386 words of rules, finishing the `laravel` row at x3.45). §1 kept its number and §1.1 its position, since `laravel-conventions` §5.12 cites it by number as the rule it overrides. The new §4 (comparison, arrays and the standard library) and §5 (time, numbers and text) were completely absent and are pure language: `==` changing meaning for string-to-number comparison in PHP 8, `in_array` comparing loosely against what are usually allow-lists, `isset` versus `array_key_exists` on a key holding null, `+` being a union while `array_merge` renumbers, `array_filter` preserving keys so `json_encode` emits an object instead of an array depending on which element was filtered out, a by-reference `foreach` leaving a live reference the next loop overwrites with, `DateTime` mutating in place while returning itself, a date with no timezone taking the server's default, floats not holding decimals and integer overflow becoming a float in silence, byte-based string functions cutting a UTF-8 character in half so `json_encode` returns `false` and the response is empty, and the four function choices that are security decisions rather than style (`hash_equals`, `password_hash`, `random_int`, `preg_quote`) | 🟡 (sourced from the market, same uncertainty status as gimli (the operator is new to PHP)) |
| go-conventions | 6 | golangci-lint (errcheck/govet/staticcheck/gosimple/ineffassign/unused) + uber-go/guide; re-checked directly against the Uber Go Style Guide on 2026-08-10, filtered for what a linter doesn't catch mechanically — 3 real gaps closed (no panic in library code, comma-ok type assertion, os.Exit/log.Fatal confined to main()) | 🟡 (no internal production experience) |
| python-conventions | 6 | PEP 484/526/604/695/8 + ruff + mypy/pyright + an org catalogue (20 skills), mined and de-identified; re-checked against PEP 8/ruff on 2026-08-10, re-verified unchanged; **sectioned and deepened 2026-09-08** — the eight sections that lived inline in `SKILL.md` moved to one file each under `references/`, the router became a table of triggers, and every section took the same depth pass as the five already-sectioned blocks (1,629 → 7,697 words of rules). The real absences were in the two sections that were thin out of proportion to what can go wrong in them: §4 async (110 words) had nothing on `gather`'s failure semantics, unbounded concurrency, cancellation-as-an-exception or the fact that `async` provides no lock — only the absence of pre-emption between awaits — and §6 DI (69 words) had nothing on a dependency's lifetime being unable to exceed the lifetime of what it holds. The PEP 8 re-check note moved out of §5, where it was provenance sitting among the rules, into `references/origin.md` | 🟡 (no internal production experience, same status as go-conventions — depth does not change that, and `samwise` keeps its question register) |
| code-baseline | 6 | an org cross-language rule set (14 skills), mined and de-identified; the floor every per-stack block sits on; §7 added 2026-08-11 from a 15th skill (`extend-dont-override`) added to the real catalogue after the original mining pass — narrowest-supported-mechanism-first before copying or replacing a vendor file; **depth pass 2026-09-08 on all eight sections** (4,397 → 9,129 words of rules) — the block with least room, since it was already the deepest here, so the additions are the failure modes the sections were silent on: catch scope, cleanup on the failure path and cause preservation in §3; the primitive-obsession family (two ids of one primitive type, units, money as amount-plus-currency, a boolean pair encoding one state, a nullable field carrying two meanings) in §5; timeout, retry-with-backoff, idempotency on an outbound write, testing the client at the transport layer rather than mocking the client, and the webhook receiver's own three rules in §4; §6 reframed around the debt rather than the doctrine; and five more shapes in §8, including enforced-on-the-happy-path-only and verify-by-reading-the-system's-answer | 🟡 |
| laravel-conventions | 6 | an org catalogue (45 skills), mined and de-identified; fills the framework gap `php-patterns` explicitly left open; re-checked against the company's own internal house documentation on 2026-08-11, 1 internal contradiction fixed (§1.1 said "action/service", `code-baseline` already bans the `*Service` bag-name — the source's explicit no-Service/no-Repository rule settled it) plus the explicit `boot()` prohibition added to §1.2; **bodies pass 2026-09-07** against the same catalogue, now 65 skills: 48 already covered, and the gaps closed were §11 (new — failures: throw rather than return, reporting is not handling, an HTTP-native exception rather than a render callback, no hand-rolled content negotiation), §1.4 (a concern trait owns its concept end to end, which corrected §1.1's "simple scopes"), §1.5 (recognising a state machine or a pipeline from Laravel-shaped triggers), §3.14 (pruning is deleting), §3.12 (widened to model/abstraction with the earned-by test), §4.5 (every table through its model), §5.8 (localised date accessors), §7.4 (a command runs more than once), §9.11 (a data change ships its seed data) and §10.3 (the support-window date); §10.6 landed 2026-09-07 from `laravel/boost` (github.com/laravel/boost, named directly, same rule-C carve-out as §10.5 — a real public first-party Laravel package) after the real, installed org catalogue's Laravel plugin stopped treating Boost as MCP-only: install it with `--skills`, not the MCP server alone, since the layer-package layout of §10.5 is how its own skill actually resolves | 🟡 |
| flutter-conventions | 6 | an org catalogue (37 skills), mined and de-identified; replaced the earlier "no mobile block" position; §7 deepened 2026-08-11 against the company's own internal BLoC/Cubit documentation — the one section in this block now sourced from actual production use, not a catalogue description; **depth pass 2026-09-08 on all ten sections** (3,380 → 10,321 words of rules, x6.1 → x2.0), written from documented framework and platform behaviour since there is no production experience to draw on — the additions that were real absences are the device-level ones: a secure-storage read failing after the keystore is cleared, a session's data outliving a logout on a shared phone, the process being killed in the background, a permission revoked while backgrounded, a one-shot system prompt, an overflow being silent in release, the reader's font scale making a fitted row overflow, and a media query answering about the window rather than the widget; a stale `§1.2` citation for disposal (§1's disposal half starts at point 5) was found by doing the pass, and ten more references were realigned | 🟡 (no mobile production experience at all, `faramir`'s question register applies — the depth pass does not change that) |
| java-conventions | 6 | Effective Java (Bloch) + SpotBugs/Error Prone + established Spring conventions; re-checked against Effective Java's item list on 2026-08-10, 2 real gaps closed (equals/hashCode contract, final-by-default) plus a Spring/JPA gap (lazy loading / N+1, mirroring python-conventions' ORM section) | 🟡 (sourced from the market, no internal production experience, same status as go-conventions) |
| seo | 6 | Google Search Central + web.dev (Core Web Vitals, structured data); re-checked item by item against the current SEO starter guide on 2026-08-10, 2 real gaps closed (hreflang, nofollow/anchor text) | 🟡 (sourced from the market, no dedicated SEO production experience in house) |
| accessibility | 6 | WCAG 2.2 (AA) + MDN + W3C ARIA APG; re-checked against the 6 success criteria genuinely new in 2.2 (not carried over from 2.1) on 2026-08-10, 5 real gaps closed (Focus Not Obscured, Dragging Movements, Target Size, Redundant Entry, Accessible Authentication Minimum), Consistent Help left out deliberately | 🟡 (sourced from the market, no dedicated a11y production experience in house) |
| qa-exploratory-testing | 8 (complement) | established exploratory testing literature (session-based testing) + ISTQB (boundary testing) | 🟡 (sourced from the market, no dedicated QA production experience in house) |
| devops-conventions | 6 (infra/CI) | 12-factor app + DORA metrics (Accelerate) + established GitOps/IaC practices; §2 point 4 (protected shared resources) added 2026-08-11 from the org catalogue's hard-interdiction skill on protected shared databases | 🟡 (sourced from the market, no dedicated production experience in house) |
| data-pipeline-conventions | 6 (data) | dbt conventions + DAMA-DMBOK (quality dimensions) + Kimball dimensional modelling | 🟡 (sourced from the market, no dedicated production experience in house) |
| auth-session-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate jwt/oauth-oidc/keycloak/auth0 agents, no equivalent here) + a documented internal incident on a token refresh flow + OWASP session management; §4 (reference login flow) extracted from our two real frontend implementations read side by side; re-checked directly against the OWASP Session Management Cheat Sheet on 2026-08-10, 3 real gaps closed (privilege-change invalidation, absolute session lifetime, Clear-Site-Data on logout) plus an explicit CSRF note | 🟢 (§4 describes code already in production on two frontends; the rest still to dogfood) |
| security-hardening | 6 | a market generalist dev skill catalogue (`security-and-hardening`) + OWASP Top 10/ASVS/escaping cheat sheets; the writing-time vs audit-time split is ours | 🟡 (written, not dogfooded yet) |
| background-jobs-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate kafka/rabbitmq/bullmq/sidekiq/celery agents, no equivalent here) + established distributed-systems practice (at-least-once, idempotency keys, bounded retries, dead-letter) | 🟡 (written, not dogfooded yet) |
| webperf | 6 | a market generalist dev skill catalogue (`webperf`) + web.dev performance guidance + bundle-weight items from a market open source TypeScript project | 🟡 (written, not dogfooded yet) |
| domain-modeling | 3 | a recognised market skill author (`domain-modeling`) + DDD staples; states-not-flags is ours | 🟡 (written, not dogfooded yet) |
| deprecation-migration | cross-cutting | a market generalist dev skill catalogue (5 questions + 4 patterns) | 🟢 (direct rewrite, mechanism taken as-is) |
| api-design | 3 | a market generalist dev skill catalogue (Hyrum's law, One-Version Rule) | 🟢 (direct rewrite) |
| observability-instrumentation | 6 | a market generalist dev skill catalogue (on-call questions, RED/USE, anti-cardinality) | 🟢 (direct rewrite) |
| documentation-adr | 3 | a market generalist dev skill catalogue (5-6 field ADR template); "When"/Guardrails corrected 2026-08-11 against the real, installed org catalogue's cross-cutting plugin (`no-project-docs`) — an ADR is proposed, never committed as a file, unless asked, an ADR folder already exists, or the proposal is accepted; the original phrasing had this block volunteering a new doc file the moment a decision qualified | 🟢 (direct rewrite) |
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
| design-patterns | 3 / 6 | the Gang of Four catalogue as published on `refactoring.guru` (22 patterns, re-verified 2026-08-10, all 22 now carry an explicit verdict — subtracted, dismissed, entry-conditioned or escape-valve); the catalogue pages carry **no overuse caution**, which is the whole gap — recognise-don't-apply, the second-real-case threshold, the framework-already-does-it subtraction and the Repository-over-ORM verdict are ours; §4 grew 3 more entries 2026-08-11 (value object, pipeline, transaction boundaries) from the real, installed org catalogue's design-patterns plugin, which had grown from 4 to 7 skills since the original mining pass — these are real recurring shapes outside the 22-pattern GoF set, not a gap in that set; **sectioned and deepened 2026-09-08** — the five sections that lived inline in `SKILL.md` moved to one file each under `references/`, a sixth was added, the router became a table of triggers (2,347 → 6,333 words of rules, x5.19 → x1.92). §4 kept its number and every point inside it, since `business/fintech-compliance` cites §4.5 and `laravel-conventions` cites the transaction rule at §4.7 twice; §2's bullets became numbered points, text unchanged. The new §6 (when a pattern stops earning its place) closes a structural gap rather than an oversight: the source catalogue, and every section here, was about whether to *add* a pattern, and nothing said when to take one out — hence the deletion test, the interface whose second implementation was decommissioned, the pool justified by a measurement on a runtime since upgraded, the pattern grown to fit a case that does not share its axis, the suite with a test per implementation and none for the dispatch, and the ADR line that outlives the structure and gets the pattern reimplemented from the document. Two stale references into this block were fixed in the same pass: `laravel-conventions` §4 and §8 both cited a §7 this block has never had | 🟡 |
| shell-scripting-conventions | 6 | public defensive-shell baseline (`set -euo pipefail`, quoting, `shellcheck`); §2 and §4 are this repo's own `verify-gate.sh` bugs — fail-open on a missing parser, dropped exec bit, CRLF from Windows | 🟡 (the four bugs it prevents were real, so the content is validated even though the block hasn't been run as a block) |
| bug-triage | 7 (entry) | local video-reading Claude skills (`claude-real-video`, `watch-video-skill`: scene-change frames + dedup + subtitle-or-Whisper transcript on `ffmpeg`, MIT) for the evidence step, named as optional so nothing depends on it; the queue framing is native Claude Code (`/loop`/`/schedule`, proactive loops); the rest is ours — observation vs the reporter's theory, "cannot reproduce" owing its own evidence list, severity by impact | 🟡 (fills a real pipeline hole: `debug` assumed a runnable failing case) |
| product-ownership | product | an org catalogue's 9 story-management skills, mined and de-identified (anatomy, review axes, criticality, estimation); public sources for given/when/then criteria and definition-of-ready/done; §8.2/§8.3 and §9 added 2026-09-07 — the catalogue's tenth skill (decomposition behind a hard confirmation gate, the tracker write being a consequence of an approved plan) plus two rules from a real organisational change: a story is sized to one MR, and §9 covers the configuration where the story's author builds it, naming what replaces §7's independent reader (the epic above, the fresh-context gate below) instead of pretending the separation survives | 🟡 (ours is the priority/refusal/criteria layer and tying "done" to the two guarantees; the tracker mechanics stay out) |
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
| ux-writing | UI/UX | published content guidelines of the major design systems; the domain-modeling consistency link, the no-concatenation rule and the empty/no-match/failed-to-load split are ours | 🟡 (no internal UX-writing expertise, no tone-of-voice reference available) |
| product-marketing | marketing | published positioning structure (audience / alternative / outcome / boundary); claim-needs-a-source as `default = failure` applied outside code, and technical claims read by a builder, are ours | 🟡 (no internal marketing expertise, no brand or campaign reference available) |
| sales-support | sales | published discovery-before-solution practice and the estimate-versus-commitment distinction; the estimation rules mirror internal engineering practice (points, spikes, scope moves not the number) with nothing named | 🟡 (no internal sales expertise; pricing and contract terms deliberately out of scope under rule C) |
| release-communication | communication | keep-a-changelog conventions + standard deprecation-notice practice; the three-bucket ordering by required action, and "anything fitting no bucket is internal noise", are ours | 🟡 (no internal technical-writing or comms expertise) |
| incident-communication | communication | published status-page practice + blameless-postmortem culture; separating the communicator from the fixer, and "still investigating" counting as a real update, are the two rules we'd most want enforced | 🟡 (no internal incident-response expertise; escalation and on-call arrangements stay out under rule C) |
| data-analytics | BI / data (new 2026-08-11) | the org catalogue's two BI landscape skills (§1–§4: the multi-instance landscape, the cross-instance-identifier trap, the crosswalk-table fix, usage-guide-vs-schema-dump, `UNION ALL`-as-named-tradeoff — real instance/host names, entity counts and the ERP's real French table/column names left out under rule C); §3.3 layered modeling (staging/intermediate/mart) from established `dbt`-ecosystem analytics-engineering practice; §2.4 six-dimension data-quality vocabulary from DAMA-DMBOK; §5 KPI/dashboard discipline (decision test vs vanity metrics, single source of truth, glanceable KPI count) from published dashboard-design practice | 🟡 (no internal data-engineering expertise) |

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
| morpheus | Laravel/Eloquent implementation (API, queues, perf) | 🟢 (dogfooded 2026-08-07 on `formation-laravel`: turned dozer's 4 red tests green without touching the test file, ran the existing suite to confirm no regression, refused to self-certify beyond that and deferred to gimli/gandalf) |
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
| the current wave of credential-stealing packages, and agents told to install them by text they read | `hooks/block-installs.sh` (PreToolUse on `Bash`): refuses every install, one-shot runner and `curl \| bash`, then resolves what a `package.json` script actually runs; names pnpm as the way to install and asks where the instruction came from | every agent, `CONVENTIONS.md`, `references/review-axes.md` §2 | ✅ (68 cases, blocked and allowed both; limits documented rather than oversold — it is an interlock, not a sandbox) |
| market long-running agent patterns | `verify-gate.sh` (PreToolUse default-FAIL hook on read evidence) | gate | ✅ (rewritten as the `hooks/` pair; ours: fail-closed only on the guarded path so a repo without a parser still works, plus a read log so "produced" and "looked at" are distinguished; tested against 6 cases, per-repo wiring still to do) |
| named directly by the operator (a build agent editing a failing test's expectation instead of the implementation) | `hooks/guard-test-changes.sh`+`.py` (PreToolUse on Edit/Write): a pre-existing assertion line disappearing without `MENTIS_ALLOW_TEST_CHANGES` set is blocked | `skills/debug` §3.4, `skills/code`, `skills/tdd`, `galadriel` | ✅ (internal synthesis, no external source; tested against 12 cases across 5 ecosystems, `bin/test_guard_test_changes.py`, per-repo wiring still to do) |
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
| **the upstream this framework responds to** (14 skills, 0 agents) + its companion skills repo (31 skills) | full enumeration, done late: our own sourcing had never listed the contents of the project mentis takes its premise from. Numerically we're ahead (59 skills + 15 business blocks / 21 agents, as of 2026-08-06), but they cover a different axis: thinking techniques and meta, where we had nothing | see the rows below | 🟡 (partially mined: `meta/` done, `debugging/` + `testing/` + `problem-solving/` still to go) |
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
| laravel | 65 / 79,825 | 3 / 23,118 | −56,707 | x3.45 |
| csharp | 37 / 56,718 | 1 / 3,167 | −53,551 | x17.91 |
| python | 20 / 22,097 | 2 / 8,446 | −13,651 | x2.62 |
| project-management | 10 / 14,536 | 2 / 3,092 | −11,444 | x4.7 |
| bi, design, xefi | 16 / 17,306 | 4 / 5,877 | −11,429 | x2.94 |
| flutter | 40 / 20,772 | 1 / 10,321 | −10,451 | x2.01 |
| global | 18 / 20,280 | 5 / 11,886 | −8,394 | x1.71 |
| nuxt | 21 / 19,869 | 1 / 12,443 | −7,426 | x1.6 |
| design-patterns | 7 / 12,179 | 1 / 6,333 | −5,846 | x1.92 |
| react | 36 / 9,302 | 1 / 10,476 | +1,174 | x0.89 |

Recomputed by `bin/measure_depth.py`, which is where the composition below lives; `bin/test_measure_depth.py`
fails if this table stops matching what it measures. **Ratio** is theirs over ours on the same subject, so
lower is closer and below 1 is ahead.

**Status.** Passed: `react` (all 10 sections), `nuxt` (13), `flutter` (10), `python` (8, sectioned out of a
single file first), `code-baseline` (8) inside the `global` row, `inertia-conventions` (6),
`php-patterns` (5) and `design-patterns` (6) — the last four sectioned out of a single file first, all on
2026-09-08, and `laravel` (11) the day before. That completes the whole `laravel` row (13,718 → 23,118,
x5.82 → x3.45) and every single-file block except one. Still to do: `dotnet-conventions` — the worst
ratio in the table, and the stack nobody here writes, which is why it was left last. The `bi, design, xefi` row stays ✕: it is
the internal landscape, and rule C keeps it out.

**Composition.** Each row names the blocks it aggregates, so that it can be re-measured rather than
remembered — the defect that produced two unreproducible rows before this script existed:

```
laravel: laravel-conventions 11,053, php-patterns 5,386, inertia-conventions 6,679
csharp: dotnet-conventions 3,167
python: python-conventions 7,697, data-pipeline-conventions 749
flutter: flutter-conventions 10,321
nuxt: vue-nuxt-vuetify-conventions 12,443
global: code-baseline 9,129, security-hardening 1,030, api-design 375, documentation-adr 841, observability-instrumentation 511
project-management: product-ownership 2,952, spec 140
design-patterns: design-patterns 6,333
react: react-nextjs-conventions 10,476
bi, design, xefi: data-analytics 1,804, interface-design 2,041, ux-writing 1,005, accessibility 1,027
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
`laravel-conventions` §4 and §8 both cited `skills/design-patterns` §7 for transaction boundaries, and
this block has never had a §7 — the rule is §4.7. Wrong since those lines were written, and found by
resolving every reference rather than by reading — which makes four defects this programme has turned up
that predated it, after flutter §9 citing §1's async-context rule for disposal and `code-baseline`'s own
`origin.md` carrying a stale point range.

**Next**: `dotnet-conventions` (3,167 words), the only block the programme has left and the one it
deliberately kept for last.
`dotnet-conventions` has the worst ratio (x17.9) and is the stack nobody here writes, so it stays last on
purpose — a deep block nobody can dogfood is exactly the 🟡 this catalogue exists to flag, and making it
thicker would not change that letter.
Progress is recorded here rather than in a commit message so that it can be read as a whole, and the
table itself is reproducible: `python3 bin/measure_depth.py`. That was claimed before it was true, denied
when the claim caught up with us, and is now enforced by a test.

**The order is by thinness, not by importance.** A 113-word section is not a short summary of a subject —
it is a subject whose failure modes were never written down, so an agent reading it agrees with the rule
and cannot apply it under pressure. The thick sections were already written that way, which is why they
are thick.

## 3. The rule that keeps us "in control" (reminder)

We never wire a repo in as a dependency. We read → we extract the mechanism → we **rewrite** it
in the single template → we credit `Origin`. See the adoption checklist in `CONVENTIONS.md`.
That's what guarantees: nobody upstream breaks our workflow, and everything is written the same
way (maintainable). The backlog above is our enrichment queue, we dip into it when a step has a
real gap, not to pile things up.
