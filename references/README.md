# mentis: knowledge map (references)

> "Seeing all the `.md` files you need" to extract, improve, speed up, maintain.
> **Discipline (rule B applied to docs): a single source per subject.** A reference doc either
> **holds** knowledge that has no home, or **indexes** an existing source, **never a copy**. The
> blocks (`skills`) and agents *point* at those sources, they don't re-explain them.
> Publishable/Internal follows rule C (`CONVENTIONS.md`).

## The map

| Subject | Single source of truth | Type | Pub/Int | Status |
|---|---|---|---|---|
| Method / pipeline | `mentis/WORKFLOW.md` | doc | Pub | ✅ |
| Governance + template | `mentis/CONVENTIONS.md` | doc | Pub | ✅ |
| Block registry + backlog | `mentis/CATALOG.md` | doc | Int* | ✅ |
| Scouting still to triage | `mentis/SOURCING-INBOX.md` | doc | Int | ✅ |
| Scouting comparison | `VEILLE.md` — **outside this repo**, in the operator's own working folder | doc | **Int** | ✅ (exists, deliberately not committed here: rule C) |
| Infra / ports / SSO reality | `CHALLENGE.md`, `FRICTIONS.md` — **outside this repo**, same folder | doc | **Int** | ✅ (exist, deliberately not committed here: they name real servers) |
| **Design system** (token discipline, spacing, chips, buttons, containers, icons) | an org design catalogue (10 skills) | skills | Pub | ✅ (mined → `business/interface-design`, house values excluded) |
| **RGAA accessibility** | an org design catalogue's accessibility skill (mockup) + `skills/accessibility` (rendered code, cites WCAG) | skill | Pub | ✅ (index — deliberately not mined, see `CATALOG.md` §0) |
| **Laravel framework layer** (models, authorisation, schema, queries, tests, config) | an org catalogue (45 skills) | skills | Pub | ✅ (mined → `skills/laravel-conventions`; `php-patterns` stays below it, on the language) |
| **Nuxt/Vue structure & style** (components, toolkit, typing, stores, naming, i18n) | an org catalogue (21 skills) | skills | Pub | ✅ (mined → `skills/vue-nuxt-vuetify-conventions`, self-contained) |
| **React structure & style** (naming, hooks, typing, server-state library) | an org catalogue (36 skills) | skills | Pub | ✅ (mined → `skills/react-nextjs-conventions`, self-contained) |
| **C#/.NET rules** (async/cancellation, DI, prohibitions, authorisation) | an org catalogue (15 skills) | skills | Pub | ✅ (mined → `skills/dotnet-conventions`, self-contained) |
| **Python toolchain & framework** (ruff/uv/mypy-strict, errors-as-values, is-None, ORM) | an org catalogue (20 skills) | skills | Pub | ✅ (mined → `skills/python-conventions`, self-contained) |
| **Flutter / mobile** (layers, state holders, widgets, async UI states, disposal) | an org catalogue (37 skills) | skills | Pub | ✅ (mined → `skills/flutter-conventions`, which replaced the earlier "mentis writes no mobile block" position) |
| **Stack-agnostic code shape** (file size, no god classes, no comments, owned API client) | an org catalogue (14 skills) | skills | Pub | ✅ (mined → `skills/code-baseline`; `over-engineering-review` scores deletions, it doesn't set the thresholds) |
| **Story artefact & tracker mechanics** (structure, review axes, labels, breakdown + estimation) | an org catalogue (9 skills) | skills | Pub | ✅ (mined → `business/product-ownership` §6–§8; tracker mechanics excluded) |
| **Testing doctrine** (data-test-* selectors, `task-test.md` plan, persona/permission matrix, coverage floor, per-stack guides, `env-attr-cleaner`) | the `test-casebook` **npm package** (MIT, `techmefr/test-casebook`) — installed per project, ships its own `.claude/` skills, agents and plan-before-tests hook | package | Pub | ✅ (index — authority where installed; `tdd`/`dozer` defer to it, see below) |
| **Frontend conventions** (shorthand props, is/has booleans, i18n in a computed, no non-existent toolkit prop) | `skills/vue-nuxt-vuetify-conventions` §12 | skill | Pub (generic) | ✅ (was 🔜 `conventions-front.md`; the block absorbed it, no separate doc needed) |
| **Backend conventions** (framework filters to the max, status+message responses, simplicity > number of calls) | `skills/laravel-conventions` §4 and §6 | skill | Pub (generic) | ✅ (was 🔜 `conventions-back.md`; the block absorbed it) |
| **Git / commits / MR** (conventional, lowercase; MR comments short and emoji-free) | *scattered in memory* | / | Pub | 🔜 **to write** `git-mr.md` |
| **Code smells** (baseline cited by the Standards axis of `review`) | to be formalised | / | Pub | 🔜 **to write** `code-smells.md` |
| Agents (aragorn/gimli/legolas/gandalf…) | `.claude/agents/*` | defs | Int | ✅ (registry in CATALOG) |
| **Current library/framework docs** (upstream, beyond any training cutoff) | `context7` MCP server, on demand | tool | Pub | ✅ installed (see below) |
| **MR review plumbing** (API-first dump, batching, restricted scope, REPORT/POST, discussions, inline posting and its four traps) | `references/mr-review-plumbing.md` | doc | Pub | ✅ (extracted 2026-08-06 from `boromir`; cited by all eight readers, which keep only their default mode and paths) |
| **The review scripts themselves** (prefetch dump, batched blob search, inline posting with position resolution) | `bin/*.py`, documented in `references/mr-review-plumbing.md` | code | Pub | ✅ (shipped 2026-08-06; host from `GITLAB_HOST`, scratch from `MR_SCRATCH`, nothing hard-coded, `--dry-run` on the posting one) |
| **Cross-cutting review axes** (accessibility, trust boundary, tests owed, hot-path cost, diagnosability, contract, deletion, user-visible words) | `references/review-axes.md` | doc | Pub | ✅ (written 2026-08-06 from real reviews that came back silent on all eight; cited by the eight readers and by `skills/review`) |
| **Social platform publishing access** (who gates posting, what it costs, what's not worth it) | `references/social-platforms.md` | doc | Pub | ✅ (dated 2026-08-06, six-month window) |

\* `CATALOG.md`: the structure is publishable, but its backlog names internal repos/layers → keep it internal until we've separated them.

## Usage rules
- **Don't duplicate**: if a subject already has a skill (design, testing), we **point** at it, we
  don't copy it over. A skill that needs a number reads it from the source, not hard-coded.
- **An org skill catalogue is the authority on its own house style where installed** — 211 skills across ten
  plugins, versioned and already installed org-wide. But mentis does **not** depend on it being installed:
  its rules were mined, de-identified and rewritten generically into the per-stack blocks, so every block
  works on a plain repo (rule A). Where the catalogue is present and disagrees, it wins as a house override,
  and the block says so explicitly. See `CATALOG.md` §0 for what landed where.
- **Filling a gap = a single doc** here, cited by every block concerned.
- **Publishable** (Pub) → can live in a future public repo; **Internal** (Int) → never. A
  "Pub (generic)" doc names **no** real project/colleague (rule C).

## Owning a source without depending on it: `test-casebook`

Three sibling packages, one method, split by what the tests actually drive — a project installs the one
that matches its stack, and nothing forces a project to install more than one:

| Package | Covers | npm (2026-08-06) |
|---|---|---|
| `test-casebook` | frontend/DOM (Nuxt, React, Vue, Svelte, Astro, Laravel/Livewire) | 1.1.0 |
| `test-casebook-back-js` | Node/TypeScript backends (NestJS, Adonis, Express, Fastify, Hapi, Koa, tRPC, GraphQL) | 0.10.0 |
| `test-casebook-back-php` | PHP backends (Laravel/Lomkit, Symfony, Slim, Mezzio, CodeIgniter 4) | 0.14.0 |

The PHP one publishes on **npm, not Packagist**: what it distributes is a doctrine plus a Claude Code
skill, never autoloaded PHP, so there is no service provider to provide. Its `npx` entry point is a Node
wrapper that forwards to the same `bin/casebook-back-init.php` scaffolder.

The two backend packages sit at `0.x` on purpose — the doctrine is written and the frameworks are
documented from real runs, but neither playbook has been run end to end on a real project yet. Same honesty
as a 🟡 here.

`test-casebook` is ours (MIT, public, `techmefr/test-casebook`), which makes it tempting to wire in as a
dependency of this repo. **Don't.** Ownership comes from the licence and the repo, not from the direction of
the dependency; wiring it in only adds coupling, and the bill arrives at distribution — every team
installing mentis would need that package too, or step 5 breaks for them.

The split that gives the update propagation anyway:

- **In a project** — `npm i -D test-casebook`, pinned (`^1`). Its `.claude/` skills, agents and hook arrive
  with the package, so **publishing a new version is what propagates the doctrine**. That's where
  auto-update belongs.
- **In mentis** — no dependency. `tdd` and `dozer` point at it, defer to it where it's installed, and carry
  a version stamp. Every block must still work with plain git and nothing installed.

**Two gates, not a duplicate.** `test-casebook`'s `PreToolUse` hook refuses a test file with no
`task-test.md` plan above it; mentis's `hooks/verify-gate.sh` refuses a `passes: true` claim with no read
evidence. Different promises, and they chain — plan before tests, then evidence before passing. Both stay.

**Resolved (2026-08-06).** This section used to record three divergent numbers for the frontend package —
npm at 1.0.4, `package.json` at 1.0.10, the CHANGELOG at 1.1.0 — which meant "I update it and it
propagates" was false: the missing step was the publish, not any plumbing here. All three now agree at
1.1.0, and the two backend siblings were published for the first time. Worth keeping as the failure mode:
the propagation story is only as true as the last `npm publish`.

## Live upstream docs: `context7`

A written convention drifts the day the framework ships a major. `context7` is an MCP server that
returns **current** documentation for a named library on demand, which is the one thing a training
cutoff cannot provide. It's the retrieval side of `skills/source-freshness`.

Wiring (user scope, one machine, once):

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

An API key is optional and only raises the rate limit (`--api-key <key>`, or `CONTEXT7_API_KEY` in the
environment); without one it connects anonymously against shared limits. There's also a plugin
marketplace install if you prefer that route. Verified 2026-08-06 against the upstream install docs.

**Two rules, both from rule B:**
- **Authoring-time only.** It's used while writing or refreshing a block, never by a pipeline step at
  runtime. Every block must keep working with the network off — `context7` being unavailable means
  "the block is as fresh as its stamp", never a blocked step.
- **Read it, then write our rule.** Fetched docs are the fact; the convention around it stays ours, and
  the version read goes in `Origin`.

Concretely, this is what `vue-nuxt-vuetify-conventions`, `nestjs-node-conventions`,
`react-nextjs-conventions`, `php-patterns` and the other version-pinned blocks get refreshed against,
instead of from memory.

## To write (real gaps, in order of usefulness)
1. `conventions-front.md`, cited by `review` and `code` (the most used).
2. `git-mr.md`, cited by `ship` and `review`.
3. `conventions-back.md`, points at `doctrine-test-back-laravel-lomkit.md`, consolidates the rest.
4. `code-smells.md`, cited by `review` (Standards axis).

**These docs seed themselves automatically**: the `extract-conventions` block reads the real code
and produces a `references/observed/<project>.md` draft (internal); the generic publishable
version is the human distillation of it. Writing by hand is the fallback, not the default.
