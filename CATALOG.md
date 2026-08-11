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
| Vue/Nuxt | `nuxt` (21) | `skills/vue-nuxt-vuetify-conventions`, rewritten self-contained (12 sections) |
| React | `react` (36) | `skills/react-nextjs-conventions`, rewritten self-contained (10 sections) |
| Python | `python` (20) | `skills/python-conventions`, rewritten self-contained (8 sections) |
| C#/.NET | `csharp` (15) | `skills/dotnet-conventions`, rewritten self-contained (6 sections) |
| Design system | `design` (10) | **`business/interface-design`** (new): token discipline, container decision tree, required screen states, button hierarchy, chips by kind, icon-text coupling, reference gathering — **house values deliberately excluded** |
| Story management | `project-management` (9) | `business/product-ownership` §6–§8: story anatomy, label discipline, criticality, review axes, review output, decomposition, estimation-needs-the-code |
| Patterns | `design-patterns` (4) | `skills/design-patterns` §4: the concrete entry condition per pattern (strategy, state, null object, object construction), on top of the whether-to-reach-for-one decision that remains ours |

Two subjects were **not** brought over, on purpose: mockup accessibility stays with `skills/accessibility`
(which cites its standard rather than a remembered number) and mockup copy stays with
`business/ux-writing` — both already own the rendered-code side, and a design-time twin would be the second
source `maintaining-blocks` §4 exists to catch. `go-conventions` and `java-conventions` have no counterpart
and are untouched.

**Same audit, applied to the `test-casebook` family** (MIT, `techmefr/*`, ours — `test-casebook` 1.1.0 for
the frontend, `test-casebook-back-js` 0.10.0 and `test-casebook-back-php` 0.14.0 for the backends, all three
on npm as of 2026-08-06): it ships the testing
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
| vue-nuxt-vuetify-conventions | 6 | several market Vue/Nuxt/Vuetify skill catalogues (Vue patterns, Nuxt4, Nuxt composables, Vuetify) + a market Nuxt/Vue linter (correctness/security) + a market open source TypeScript project (a11y/bundle) + de-identified internal review feedback (recurring patterns); re-checked directly against the public vue.doctor/nuxt.doctor tools on 2026-08-10, which surfaced 2 real gaps (compiler-macro import, useAsyncData key default) now closed | 🟡 |
| react-nextjs-conventions | 6 | a market React skill catalogue (best practices) + a market React/Node skill catalogue (redux-toolkit) + a market shadcn skill catalogue + a market React linter (correctness/security section) + a market open source TypeScript project (a11y/bundle); re-checked directly against the public React Doctor tool (react.doctor) on 2026-08-10, which surfaced 3 real gaps (prop drilling, setState-count/useTransition, missing alt) now closed | 🟡 (written, not dogfooded yet) |
| over-engineering-review | 9 | a market deletion-oriented review tool (deletion angle, tags, net line score) | 🟡 |
| nestjs-node-conventions | 6 | a market NestJS skill catalogue + an advanced market TypeScript skill + a market React/Node skill catalogue (prisma/trpc/zod) | 🟡 (written, not dogfooded yet; first mentis block for the Node backend) |
| typescript-patterns | 6 | internal synthesis (real production experience from the operator on pure TS/JS) | 🟢 |
| php-patterns | 6 | PHP-FIG (PSR-12) + official PHP docs; re-checked directly against the PSR-12 text on 2026-08-10 — almost all of it is formatting already covered by Pint/PHP-CS-Fixer, `declare(strict_types=1)` was the one real gap (the one PSR-12 rule with runtime effect); §1.1 corrected 2026-08-11 against the real, installed `xefi-claude-skills` `laravel` plugin (`no-strict-types`) — Laravel deliberately omits the declaration at its framework boundary (loose scalars in from routes/requests/config, Larastan does the static enforcement instead), a real, dogfooded, currently-installed reversal of the PSR-12 default that neither this block nor `laravel-conventions` named explicitly until now | 🟡 (sourced from the market, same uncertainty status as gimli (the operator is new to PHP)) |
| go-conventions | 6 | golangci-lint (errcheck/govet/staticcheck/gosimple/ineffassign/unused) + uber-go/guide; re-checked directly against the Uber Go Style Guide on 2026-08-10, filtered for what a linter doesn't catch mechanically — 3 real gaps closed (no panic in library code, comma-ok type assertion, os.Exit/log.Fatal confined to main()) | 🟡 (no internal production experience) |
| python-conventions | 6 | PEP 484/526/604/695/8 + ruff + mypy/pyright + an org catalogue (20 skills), mined and de-identified; re-checked against PEP 8/ruff on 2026-08-10, re-verified unchanged | 🟡 (no internal production experience, same status as go-conventions) |
| code-baseline | 6 | an org cross-language rule set (14 skills), mined and de-identified; the floor every per-stack block sits on; §7 added 2026-08-11 from a 15th skill (`extend-dont-override`) added to the real catalogue after the original mining pass — narrowest-supported-mechanism-first before copying or replacing a vendor file | 🟡 |
| laravel-conventions | 6 | an org catalogue (45 skills), mined and de-identified; fills the framework gap `php-patterns` explicitly left open; re-checked against the real house doc (doc.stacktim.com) on 2026-08-11, 1 internal contradiction fixed (§1.1 said "action/service", `code-baseline` already bans the `*Service` bag-name — the source's explicit no-Service/no-Repository rule settled it) plus the explicit `boot()` prohibition added to §1.2 | 🟡 |
| flutter-conventions | 6 | an org catalogue (37 skills), mined and de-identified; replaced the earlier "no mobile block" position; §7 deepened 2026-08-11 against the real house BLoC/Cubit doc (doc.stacktim.com) — the one section in this block now sourced from actual production use, not a catalogue description | 🟡 (no mobile production experience at all, `faramir`'s question register applies) |
| java-conventions | 6 | Effective Java (Bloch) + SpotBugs/Error Prone + established Spring conventions; re-checked against Effective Java's item list on 2026-08-10, 2 real gaps closed (equals/hashCode contract, final-by-default) plus a Spring/JPA gap (lazy loading / N+1, mirroring python-conventions' ORM section) | 🟡 (sourced from the market, no internal production experience, same status as go-conventions) |
| seo | 6 | Google Search Central + web.dev (Core Web Vitals, structured data); re-checked item by item against the current SEO starter guide on 2026-08-10, 2 real gaps closed (hreflang, nofollow/anchor text) | 🟡 (sourced from the market, no dedicated SEO production experience in house) |
| accessibility | 6 | WCAG 2.2 (AA) + MDN + W3C ARIA APG; re-checked against the 6 success criteria genuinely new in 2.2 (not carried over from 2.1) on 2026-08-10, 5 real gaps closed (Focus Not Obscured, Dragging Movements, Target Size, Redundant Entry, Accessible Authentication Minimum), Consistent Help left out deliberately | 🟡 (sourced from the market, no dedicated a11y production experience in house) |
| qa-exploratory-testing | 8 (complement) | established exploratory testing literature (session-based testing) + ISTQB (boundary testing) | 🟡 (sourced from the market, no dedicated QA production experience in house) |
| devops-conventions | 6 (infra/CI) | 12-factor app + DORA metrics (Accelerate) + established GitOps/IaC practices | 🟡 (sourced from the market, no dedicated production experience in house) |
| data-pipeline-conventions | 6 (data) | dbt conventions + DAMA-DMBOK (quality dimensions) + Kimball dimensional modelling | 🟡 (sourced from the market, no dedicated production experience in house) |
| auth-session-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate jwt/oauth-oidc/keycloak/auth0 agents, no equivalent here) + a documented internal incident on a token refresh flow + OWASP session management; §4 (reference login flow) extracted from our two real frontend implementations read side by side; re-checked directly against the OWASP Session Management Cheat Sheet on 2026-08-10, 3 real gaps closed (privilege-change invalidation, absolute session lifetime, Clear-Site-Data on logout) plus an explicit CSRF note | 🟢 (§4 describes code already in production on two frontends; the rest still to dogfood) |
| security-hardening | 6 | a market generalist dev skill catalogue (`security-and-hardening`) + OWASP Top 10/ASVS/escaping cheat sheets; the writing-time vs audit-time split is ours | 🟡 (written, not dogfooded yet) |
| background-jobs-conventions | 6 | gap found while scouting a market per-technology agent catalogue (separate kafka/rabbitmq/bullmq/sidekiq/celery agents, no equivalent here) + established distributed-systems practice (at-least-once, idempotency keys, bounded retries, dead-letter) | 🟡 (written, not dogfooded yet) |
| webperf | 6 | a market generalist dev skill catalogue (`webperf`) + web.dev performance guidance + bundle-weight items from a market open source TypeScript project | 🟡 (written, not dogfooded yet) |
| domain-modeling | 3 | a recognised market skill author (`domain-modeling`) + DDD staples; states-not-flags is ours | 🟡 (written, not dogfooded yet) |
| deprecation-migration | cross-cutting | a market generalist dev skill catalogue (5 questions + 4 patterns) | 🟢 (direct rewrite, mechanism taken as-is) |
| api-design | 3 | a market generalist dev skill catalogue (Hyrum's law, One-Version Rule) | 🟢 (direct rewrite) |
| observability-instrumentation | 6 | a market generalist dev skill catalogue (on-call questions, RED/USE, anti-cardinality) | 🟢 (direct rewrite) |
| documentation-adr | 3 | a market generalist dev skill catalogue (5-6 field ADR template); "When"/Guardrails corrected 2026-08-11 against the real, installed `xefi-claude-skills` `global` plugin (`no-project-docs`) — an ADR is proposed, never committed as a file, unless asked, an ADR folder already exists, or the proposal is accepted; the original phrasing had this block volunteering a new doc file the moment a decision qualified | 🟢 (direct rewrite) |
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
| design-patterns | 3 / 6 | the Gang of Four catalogue as published on `refactoring.guru` (22 patterns, re-verified 2026-08-10, all 22 now carry an explicit verdict — subtracted, dismissed, entry-conditioned or escape-valve); the catalogue pages carry **no overuse caution**, which is the whole gap — recognise-don't-apply, the second-real-case threshold, the framework-already-does-it subtraction and the Repository-over-ORM verdict are ours | 🟡 |
| shell-scripting-conventions | 6 | public defensive-shell baseline (`set -euo pipefail`, quoting, `shellcheck`); §2 and §4 are this repo's own `verify-gate.sh` bugs — fail-open on a missing parser, dropped exec bit, CRLF from Windows | 🟡 (the four bugs it prevents were real, so the content is validated even though the block hasn't been run as a block) |
| bug-triage | 7 (entry) | local video-reading Claude skills (`claude-real-video`, `watch-video-skill`: scene-change frames + dedup + subtitle-or-Whisper transcript on `ffmpeg`, MIT) for the evidence step, named as optional so nothing depends on it; the queue framing is native Claude Code (`/loop`/`/schedule`, proactive loops); the rest is ours — observation vs the reporter's theory, "cannot reproduce" owing its own evidence list, severity by impact | 🟡 (fills a real pipeline hole: `debug` assumed a runnable failing case) |
| product-ownership | product | an org catalogue's 9 story-management skills, mined and de-identified (anatomy, review axes, criticality, estimation); public sources for given/when/then criteria and definition-of-ready/done | 🟡 (ours is the priority/refusal/criteria layer and tying "done" to the two guarantees; the tracker mechanics stay out) |
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

### Domain agents (invoked by steps 8/10)
| Agent | Role | Maturity |
|---|---|---|
| aragorn / gimli | MR review, house style (Nuxt/Vue · PHP/Laravel) | 🟢 (real production use, every MR on `skera-front-web`/`skera-api` — the two stacks actually worked day to day) |
| legolas | MR review, house style (React · Next.js) | 🟢 (real production use, both React and Next.js MRs run through it) |
| boromir / theoden / frodo | MR review (Go · C#/.NET · generic JS/TS backend) | ✅ (sourced from the market for Go/.NET, no real MR on those stacks yet) |
| samwise / faramir | MR review (Python · Flutter/Dart) | 🟡 (added by the catalogue-completion pass: 20 Python and 37 Flutter skills there meant those stacks are worked on and `elrond` routed them nowhere; both now read `python-conventions` / `flutter-conventions` first and treat an installed catalogue as the house override) |
| elrond | review orchestrator: detects the stack, delegates, never reviews itself | 🟢 (real production use, routes every MR to aragorn/gimli today) |
| gandalf | final MR gate (`/code-review` + `/security-review`) | 🟢 (real production use; known limit logged separately: its nested sub-agents don't surface their findings back to it, see `gandalf-nested-agents-lose-results` in memory — consolidate/call readers directly meanwhile) |
| **galadriel** (GATE, formerly "evaluator") | judge with a clean context, **no Write/Edit**, returns PASS/NEEDS_WORK with cited evidence | ✅ (written; the hook pair now exists in `hooks/`, per-repo wiring not done yet, not dogfooded yet) |
| neo | Vue3/Nuxt3 implementation (Composition API, reactivity, perf) in functional/ | ✅ (not dogfooded yet) |
| tank | SQL tuning (MySQL/SQL Server) and Elasticsearch-Scout mapping/indexing | 🟢 (dogfooded 2026-08-07 on `skera-api`/`skera-front-web`: found a real Scout mapping/filter-type mismatch across 7 files, distinct from the known SKR-7421 case, and said explicitly what it couldn't confirm without a live ES container) |
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

## 2. Sourcing backlog: ideas/agents to rewrite in order to complete/improve

Market scouting is done continuously (last pass 2026-08, including the official Anthropic skills
repo and a 137-agent per-technology catalogue). Each line = an idea to **rewrite here**,
not to install; sources are anonymised by category (Claude Code agent/skill catalogues, stack
linters, orchestration frameworks, etc. on the market).

| Source category | Idea / agent to take | Enriches | Status |
|---|---|---|---|
| market long-running agent patterns | `evaluator.md` (fresh-context evaluator pattern) → `galadriel` agent | gate | ✅ (agent written) |
| the current wave of credential-stealing packages, and agents told to install them by text they read | `hooks/block-installs.sh` (PreToolUse on `Bash`): refuses every install, one-shot runner and `curl \| bash`, then resolves what a `package.json` script actually runs; names pnpm as the way to install and asks where the instruction came from | every agent, `CONVENTIONS.md`, `references/review-axes.md` §2 | ✅ (68 cases, blocked and allowed both; limits documented rather than oversold — it is an interlock, not a sandbox) |
| market long-running agent patterns | `verify-gate.sh` (PreToolUse default-FAIL hook on read evidence) | gate | ✅ (rewritten as the `hooks/` pair; ours: fail-closed only on the guarded path so a repo without a parser still works, plus a read log so "produced" and "looked at" are distinguished; tested against 6 cases, per-repo wiring still to do) |
| named directly by the operator (a build agent editing a failing test's expectation instead of the implementation) | `hooks/guard-test-changes.sh`+`.py` (PreToolUse on Edit/Write): a pre-existing assertion line disappearing without `MENTIS_ALLOW_TEST_CHANGES` set is blocked | `skills/debug` §3.4, `skills/code`, `skills/tdd`, `galadriel` | ✅ (internal synthesis, no external source; tested against 12 cases across 5 ecosystems, `bin/test_guard_test_changes.py`, per-repo wiring still to do) |
| **Anthropic's `claude-for-legal`** (13 vertical legal plugins, official) | freshness gate on bundled reference content, `[verify]` tag for unsourced claims, jurisdiction assumptions surfaced, "every output is a draft for attorney review — the attorney, not the plugin, owns the position" | `source-freshness`, `business/legal-documents`, `business/regulatory-watch` | ✅ (mechanisms taken and generalised; its practice-profile + research-connector architecture is aimed at law firms and stays out of scope) |
| community legal skills for Claude (contract review, policy generators, a 30-framework GRC pack) | *generating* terms/NDAs/policies and scoring contracts; the GRC pack tracks versions and dates precisely | / | ✕ (they produce the legal document, which is exactly the step we refuse — a business block routes to counsel, it doesn't draft; the GRC pack also has no update mechanism, so its careful dates rot silently, which is the argument for `source-freshness`) |
| `context7` MCP server | current library/framework documentation on demand, beyond any training cutoff | `source-freshness` §3, `references/README.md` | ✅ installed (user scope, verified connected 2026-08-06); authoring-time only, never a runtime dependency of a pipeline step — rule B |
| `claude-mem` (npm, `thedotmack/claude-mem`) | session memory compression across Claude Code sessions, worker process, native auto-memory left enabled alongside it | README Quickstart §6 | ✅ installed 2026-08-10 (user scope, provider `claude`, runtime `worker`); kept alive by a plain hourly cron (`~/.claude-mem/keepalive.sh`), not a native loop — the worker is a background daemon `/loop`/`/schedule` can't reach, not wired into any pipeline step — rule B |
| `graphify` (personal skill) | turns a repo into a queryable knowledge graph (`graphify-out/`), community detection, honest EXTRACTED/INFERRED/AMBIGUOUS trail | README Quickstart §6 | ✅ installed (personal skill, no package); refreshed check-at-use (graph age checked on invocation, `--update` runs itself past 24h) rather than a timed loop, since `--update` needs a live agent session — authoring-time convenience only, rule B |
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

## 3. The rule that keeps us "in control" (reminder)

We never wire a repo in as a dependency. We read → we extract the mechanism → we **rewrite** it
in the single template → we credit `Origin`. See the adoption checklist in `CONVENTIONS.md`.
That's what guarantees: nobody upstream breaks our workflow, and everything is written the same
way (maintainable). The backlog above is our enrichment queue, we dip into it when a step has a
real gap, not to pile things up.
