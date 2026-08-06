# mentis: block catalogue & sourcing backlog

> **mentis = superpowers, the Xefi version, one we control.** A framework *of our own*,
> continuously enriched by **rewriting** (rule B, `CONVENTIONS.md`) the best ideas/agents from
> other repos on the market, never by depending on them. This file holds: **1)** what we have,
> **2)** what we could rewrite to complete/improve it. Living document: we extend it as we go.
> Statuses: ✅ rewritten here / 🟡 written, not dogfooded yet / 🔜 to wire up / 🔎 to mine / ✕ ruled out.

## 1. Block registry

### Skills: the pipeline (`WORKFLOW.md` §2)
| Block | Step / layer | Origin (idea rewritten) | Maturity |
|---|---|---|---|
| start-feature | 0 (worktree) | internal starfleet + a market skill for worktree management | 🟡 |
| brainstorm | 1 | native `brainstorming` | 🟡 |
| spec | 2 | a market skill catalogue (grill-with-docs) + internal | 🟡 |
| archi | 3 | internal graphify (+ dedup still to build) | 🔜 |
| plan | 4 | a market skill catalogue (planning-and-task-breakdown) | 🟡 |
| tdd | 5 | Xefi `test-casebook` + market long-running agent patterns (default-FAIL contract) | 🟡 |
| code | 6 | native + internal | 🟡 |
| vue-nuxt-vuetify-conventions | 6 | several market Vue/Nuxt/Vuetify skill catalogues (Vue patterns, Nuxt4, Nuxt composables, Vuetify) + a market Nuxt/Vue linter (correctness/security) + a market open source TypeScript project (a11y/bundle) + de-identified internal Xefi review feedback (recurring patterns) | 🟡 |
| react-nextjs-conventions | 6 | a market React skill catalogue (best practices) + a market React/Node skill catalogue (redux-toolkit) + a market shadcn skill catalogue + a market React linter (correctness/security section) + a market open source TypeScript project (a11y/bundle) | 🟡 (written, not dogfooded yet) |
| over-engineering-review | 9 | a market deletion-oriented review tool (deletion angle, tags, net line score) | 🟡 |
| nestjs-node-conventions | 6 | a market NestJS skill catalogue + an advanced market TypeScript skill + a market React/Node skill catalogue (prisma/trpc/zod) | 🟡 (written, not dogfooded yet; first mentis block for the Node backend) |
| typescript-patterns | 6 | internal synthesis (real production experience from g.compigni on pure TS/JS) | 🟢 |
| php-patterns | 6 | PHP-FIG (PSR-12) + official PHP docs | 🟡 (sourced from the market, same uncertainty status as gimli (g.compigni is new to PHP)) |
| python-conventions | 6 | PEP 484/526/604/8 + ruff + mypy/pyright | 🟡 (sourced from the market, no internal production experience, same status as go-conventions) |
| java-conventions | 6 | Effective Java (Bloch) + SpotBugs/Error Prone + established Spring conventions | 🟡 (sourced from the market, no internal production experience, same status as go-conventions) |
| seo | 6 | Google Search Central + web.dev (Core Web Vitals, structured data) | 🟡 (sourced from the market, no dedicated SEO production experience at Xefi) |
| accessibility | 6 | WCAG 2.2 (AA) + MDN + W3C ARIA APG | 🟡 (sourced from the market, no dedicated a11y production experience at Xefi) |
| qa-exploratory-testing | 8 (complement) | established exploratory testing literature (session-based testing) + ISTQB (boundary testing) | 🟡 (sourced from the market, no dedicated QA production experience at Xefi) |
| devops-conventions | 6 (infra/CI) | 12-factor app + DORA metrics (Accelerate) + established GitOps/IaC practices | 🟡 (sourced from the market, no dedicated production experience at Xefi) |
| data-pipeline-conventions | 6 (data) | dbt conventions + DAMA-DMBOK (quality dimensions) + Kimball dimensional modelling | 🟡 (sourced from the market, no dedicated production experience at Xefi) |
| deprecation-migration | cross-cutting | a market generalist dev skill catalogue (5 questions + 4 patterns) | 🟢 (direct rewrite, mechanism taken as-is) |
| api-design | 3 | a market generalist dev skill catalogue (Hyrum's law, One-Version Rule) | 🟢 (direct rewrite) |
| observability-instrumentation | 6 | a market generalist dev skill catalogue (on-call questions, RED/USE, anti-cardinality) | 🟢 (direct rewrite) |
| documentation-adr | 3 | a market generalist dev skill catalogue (5-6 field ADR template) | 🟢 (direct rewrite) |
| wayfinder | cross-cutting | a recognised market skill author (parent ticket with 5 sections + typed children) | 🟢 (direct rewrite, adapted to Jira) |
| handoff | cross-cutting | a recognised market skill author (reference by path, never duplicate) | 🟢 (direct rewrite) |
| debug | support 6 | native `systematic-debugging` | 🟡 |
| extract-conventions | setup/maintenance | graphify + recognised market skill authors | 🟡 (generates the references from the real code) |
| choose-model | cross-cutting | internal synthesis (no external source taken as-is) | 🟡 (grid written, not yet applied retroactively to all existing agents) |
| dispatch-parallel | cross-cutting | a market skill/agent framework (dispatching-parallel-agents + subagent-driven-development, merged) | 🟡 (written, partial experience via elrond→aragorn/gimli/legolas) |
| writing-skills | cross-cutting (meta) | a market skill/agent framework | 🟡 (written, applies the single template + rule B checklist) |
| writing-agents | cross-cutting (meta) | internal synthesis (formalises the 7-pillar template already in use) | 🟢 |
| portless-ready | setup/infra | a market portless tool (wiring is ours) | 🟡 (makes a stack portless: HTTPS alias + port hygiene) |
| **gate** | 7 | market long-running agent patterns (`default-FAIL hook` + `fresh-context evaluator`) | 🟡 (agent `arbitre` written; per-repo default-FAIL hook still to be laid down) |
| review | 8 | a recognised market skill author (two-axis code review) + Xefi agents + native | 🟡 |
| simplify | 9 | native `simplify` | 🟡 |
| ship | 10 | internal (`/SHIP`, gandalf) | 🟡 |
| finish | 11 | internal (`finish_task`) | 🟡 |
| merge-worktree | 11 | a market context-engineering kit (`git-worktrees`) | 🟡 |

### Domain agents (invoked by steps 8/10)
| Agent | Role | Maturity |
|---|---|---|
| aragorn / gimli / legolas | MR review, Xefi style (Nuxt/Vue · React) | ✅ |
| valerianus | review triage/rewording (anti-argument) | ✅ |
| gandalf | final MR gate (`/code-review` + `/security-review`) | ✅ |
| tuteur-laravel | teaching (outside the pipeline) | ✅ |
| **arbitre** (GATE, formerly "evaluator") | judge with a clean context, **no Write/Edit**, returns PASS/NEEDS_WORK with cited evidence | ✅ (written; per-repo default-FAIL hook not laid down yet, not dogfooded yet) |
| vue-nuxt-builder | Vue3/Nuxt3 implementation (Composition API, reactivity, perf) in functional/ | ✅ (not dogfooded yet) |
| sql-es-tuner | SQL tuning (MySQL/SQL Server) and Elasticsearch-Scout mapping/indexing | ✅ (not dogfooded yet) |
| laravel-builder | Laravel/Eloquent implementation (API, queues, perf), distinct from tuteur-laravel | ✅ (not dogfooded yet) |
| seo-auditor | technical SEO audit of a live page/site, never edits | ✅ (not dogfooded yet) |
| accessibility-auditor | technical a11y audit of a live page/site, never edits | ✅ (not dogfooded yet) |
| qa-tester | manual/exploratory testing of a flow on a running app, never edits | ✅ (not dogfooded yet) |
| security-auditor | dedicated static security audit (OWASP, secrets, dependencies), read-only, never active exploitation | ✅ (not dogfooded yet) |
| architecture-debt-auditor | periodic architecture-debt audit (git hot-spots, deletion test, prioritised report) | ✅ (not dogfooded yet) |

## 2. Sourcing backlog: ideas/agents to rewrite in order to complete/improve

Market scouting is done continuously (last pass 2026-08). Each line = an idea to **rewrite here**,
not to install; sources are anonymised by category (Claude Code agent/skill catalogues, stack
linters, orchestration frameworks, etc. on the market).

| Source category | Idea / agent to take | Enriches | Status |
|---|---|---|---|
| market long-running agent patterns | `evaluator.md` (fresh-context evaluator pattern) → `arbitre` agent | gate | ✅ (agent written) |
| market long-running agent patterns | `verify-gate.sh` (PreToolUse default-FAIL hook on read evidence) | gate | 🟡 (mechanism identified, per-repo wiring still to do) |
| recognised market skill author | grill-with-docs → CONTEXT.md+ADR | spec | ✅ |
| recognised market skill author | non-polluting two-axis code review | review | ✅ |
| recognised market skill author | `wayfinder` → `wayfinder` skill, `handoff` → `handoff` skill, `improve-codebase-architecture` → `architecture-debt-auditor` agent | plan / session resumption / architecture audit | ✅ |
| recognised market skill author | `domain-modeling` | archi | 🔎 (partially overlaps documentation-adr, not yet isolated as a dedicated block) |
| market generalist dev skill catalogue | `observability-and-instrumentation` → `observability-instrumentation` skill, `api-and-interface-design` → `api-design` skill, `documentation-and-adrs` → `documentation-adr` skill, `deprecation-and-migration` → `deprecation-migration` skill | code/api/docs/migration | ✅ |
| market generalist dev skill catalogue | `security-and-hardening`, `webperf`, `context-engineering` | new blocks | 🔎 (context-engineering = meta on writing prompts/CLAUDE.md, not a dev skill (relevant for improving this repo itself, not a daily use)) |
| market generalist dev skill catalogue | `browser-testing-with-devtools` | gate (already overlaps `qa-tester`/`verify-flow`) | ✕ (redundant) |
| market skill/agent framework | `dispatching-parallel-agents`, `subagent-driven-development`, `writing-plans` | plan / orchestration | 🔎 (already native skills → to be *owned*) |
| market Claude Code agent catalogues (several) | `git-advanced-workflows` (advanced worktrees) | start-feature / finish | 🔎 (reference cited, to be verified) |
| market live-state tool | live state from reality + socket API | FLEET | 🔎 (after dogfooding) |
| market replay/audit tool | post-hoc replay/audit | FLEET / graphify | 🔎 (nice-to-have) |
| market token compression tool | compression + per-call token measurement | Taskling | 🔎 (rewrite vs consume the native one (to be decided)) |
| market voice→vault pipeline | voice→vault pipeline | Lumia | 🔎 (reference, rewrite with a read-only classifier) |
| market multi-agent orchestration framework | org-chart coordinator+agents | multi-agent dispatch | 🔎 (architecture reference only) |
| market Vue skill catalogue | `skills/vue/` (script-setup-macros, core-new-apis, advanced-patterns) | vue-nuxt-vuetify-conventions | ✅ |
| market Nuxt skill catalogue | `skills/nuxt4-patterns/SKILL.md` | vue-nuxt-vuetify-conventions | ✅ |
| market Nuxt skill catalogue (another) | `skills/nuxt/references/nuxt-composables.md` (useState/useCookie/useRequestFetch discipline, limited extract) | vue-nuxt-vuetify-conventions | ✅ |
| market Vuetify skill catalogue | `.deprecated/vuetify-4/SKILL.md` + `references/patterns/` | vue-nuxt-vuetify-conventions | ✅ |
| market context-engineering kit | `plugins/git/skills/git-worktrees/SKILL.md` ("How to Merge Worktree" section) | merge-worktree | ✅ |
| market Claude Code agent catalogue | `vue-expert` (frameworks) → `vue-nuxt-builder` agent | domain agents (frontend build) | ✅ |
| market Claude Code agent catalogue (large collection) | confirmed absence of a Vue/Nuxt agent (grep across 203 agents) → confirms the gap filled by `vue-nuxt-builder` | domain agents (frontend build) | ✅ (cross-reference) |
| market Claude Code agent catalogue (another) | `sql-pro` (02-language-specialists) → `sql-es-tuner` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue (large collection) | `sql-pro`, `database-optimizer` → `sql-es-tuner` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue | `elasticsearch-expert` → `sql-es-tuner` agent | domain agents (data) | ✅ |
| market Claude Code agent catalogue (another) | `laravel-specialist` (02-language-specialists) → `laravel-builder` agent | domain agents (backend build) | ✅ |
| market Claude Code agent catalogue (large collection) | `php-pro` (web-scripting), no Laravel specialisation → confirms the gap filled by `laravel-builder` | domain agents (backend build) | ✅ (cross-reference) |
| market long-running agent patterns | kill-switch / steer (operator hooks) | / | ✕ (a human is present) |
| market output-compression style | output compression | / | 🟡 re-assessed: the fully telegraphic style stays ruled out (unreadable), but the principle "short output by default, to limit output-token spend" is kept as a cross-cutting guarantee (see `doc/HOW-WE-WRITE-OUR-AGENTS.md` §5) |
| market frameworks for fully agentic autonomy | 24/7 / end-to-end autonomy | / | ✕ (counter-example: no-auto-merge) |
| market Vue skill catalogue (another) | `skills/vue/` (usage of a third-party JSON→Vue rendering lib) | vue-nuxt-vuetify-conventions | ✕ (not a generic Vue convention, outside Xefi needs) |
| market Nuxt skill catalogue (another) | `skills/nuxt-modules/` (authoring a published/npm Nuxt module) | vue-nuxt-vuetify-conventions | ✕ (out of scope: g.compigni writes app code, not modules) |
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
| market Claude Code agent catalogue (large collection) | code-reviewer/security-auditor/penetration-tester/debugger/test-automator/qa-expert/accessibility-tester/refactoring-specialist | / | ✕ (already covered by the per-stack reviewers/gandalf/kobold + the systematic-debugging/testing-doctrine-casebook/design:accessibility/simplify skills) |
| market Claude Code agent catalogue (large collection) | legacy-modernizer | / | ✕ (no framework migration under way) |
| market Claude Code agent catalogue (large collection) | typescript-pro | / | ✕ (generic and weak signal, no documented TS pain) |
| market Claude Code agent catalogue (large collection) | database-architect | / | ✕ (no schema design from scratch; covered by `sql-es-tuner`) |
| market Claude Code agent catalogue (large collection) | frontend-security-coder / backend-security-coder | / | ✕ (gandalf already runs /security-review + delegates to the stack reviewer) |
| market Claude Code agent catalogue (large collection) | devops-troubleshooter | / | ✕ (docker-proxy zombies already handled by a documented fix, not an agent-shaped need) |
| market Claude Code agent catalogue (large collection) | context-manager/team-lead/team-reviewer/team-implementer/team-debugger | / | multi-agent dispatch | ✕ (org-chart style implementation, architecture to be assessed, not an agent to write now) |
| market Claude Code agent catalogue (large collection) | git-pr-workflows plugin (code-reviewer) | / | ✕ (overlaps the per-stack reviewers/gandalf) |
| market Claude Code agent catalogue (large collection) | git-advanced-workflows skill | start-feature/finish | ✕ (a reference course, not an orchestrated agent) |
| market Claude Code agent catalogue | nestjs-expert / typescript-expert | future Node/NestJS project | ✕ (premature, to be revisited during the active NestJS+TS phase on the future Node project) |
| market Claude Code agent catalogue | react-expert | / | ✕ (useful only for reading colleagues' React code, not a production need for g.compigni) |
| market Claude Code agent catalogue | accessibility-expert / playwright-expert | / | ✕ (overlaps design:accessibility + verify-flow) |
| market Claude Code agent catalogue | architecture-documenter / contract-testing-expert / runbook-generator | / | ✕ (low confidence, occasional use, no recurring signal) |
| market Claude Code agent catalogue | core/code-reviewer, core/debugger, core/refactorer, core/architect, security-auditor, devsecops-engineer, ux-designer, ui-components-expert, code-documenter, orchestrators/*, postgresql-expert, redis-expert, graphql-expert, cypress-expert, jest-expert, e2e-testing-expert, operational/*, industry/* | / | ✕ (redundant with the existing roster or outside the confirmed stack) |
| market multi-agent orchestration framework | generalist org-chart (who talks to whom) | multi-agent dispatch | ✕ (no forced fresh context and no evidence/verdict mechanism; off topic for the GATE gap, stays a separate 🔎 architecture lead) |
| market React skill catalogue | `react-best-practices` (AGENTS.md) (perf/rendering/waterfall patterns with before/after code) | react-nextjs-conventions | ✅ |
| market React/Node skill catalogue | `redux-toolkit/SKILL.md` (typed createSlice, typed hooks, createAsyncThunk, memoised selectors) | react-nextjs-conventions | ✅ |
| market shadcn skill catalogue | `skills/shadcn/SKILL.md` (composition through a wrapper, cn(), folder structure) | react-nextjs-conventions | ✅ |
| market React linter | `oxlint-plugin-react-doctor`, ~780 deterministic rules (state/effects, perf, security, a11y), `error`-severity subset excluding niche frameworks taken into section 4 | react-nextjs-conventions | ✅ (content rewritten; the tool itself stays a separate 🔎 candidate for a future React CI gate, not installed, g.compigni has no React repo) |
| market Nuxt/Vue linter | `oxlint-plugin-vue-doctor`/`oxlint-plugin-nuxt-doctor` (locked to Vue 3 + Nuxt 4, explicitly inspired by its React equivalent; reactivity/composition, SSR hydration, security and h3 server-route rules taken into section 4) | vue-nuxt-vuetify-conventions | ✅ (content rewritten; separate 🔎 candidate for a future CI gate on the Nuxt/Vue frontend, not installed) |
| market Vue linter alternative | Vue-only alternative found while sourcing | vue-nuxt-vuetify-conventions | ✕ (no Nuxt coverage, the chosen linter is more complete and closer to the real stack) |
| market Vue linter alternative (another) | Vue alternative found while sourcing | vue-nuxt-vuetify-conventions | ✕ (less mature/fewer rules than the chosen linter on inspection) |
| market deletion-oriented review tool | `ponytail-review`/`ponytail-audit` (deletion angle only (dead code, reinvented stdlib, over-abstraction, yagni), per-category tags, net line score) | over-engineering-review | ✅ (mechanism and tags rewritten, new dedicated block) |
| market generalist dev skill catalogue | `code-review-and-quality` (many installs, Critical/Required/Nit/FYI severity taxonomy, diff size threshold, dependency checklist) | gandalf | ✅ (taxonomy + thresholds folded into steps 1/5/7 of the agent, not a separate block) |
| market open source TypeScript project | `typescript-review` (a11y blind spots (aria-label, modal focus) and bundle weight (default import, heavy module on a route)) | react-nextjs-conventions + vue-nuxt-vuetify-conventions | ✅ (2 items added to each block) |
| market Copilot instruction catalogue | `review-and-refactor`, reads `.github/instructions/*.md`, refactors to the project's conventions |, | ✕ (already covered by the `*-conventions` blocks + gandalf, nothing distinct) |
| market open source TypeScript project (same publisher) | `clojure-review` | / | ✕ (language outside Xefi scope) |
| review plugin from a market IDE vendor | `thermo-nuclear-code-quality-review` |, | ✕ (same angle as over-engineering-review, less actionable, no tags/score) |
| internal skill catalogue from another vendor | `code-quality` | / | ✕ (specific to their proprietary per-context stack, the rest is already covered by the per-stack reviewers+conventions) |
| market architecture review tool | `architecture-review` | / | ✕ (exact SKILL.md path not confirmed; content already overlaps gandalf/arbitre/over-engineering-review, not differentiating enough) |
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

## 3. The rule that keeps us "in control" (reminder)

We never wire a repo in as a dependency. We read → we extract the mechanism → we **rewrite** it
in the single template → we credit `Origin`. See the adoption checklist in `CONVENTIONS.md`.
That's what guarantees: nobody upstream breaks our workflow, and everything is written the same
way (maintainable). The backlog above is our enrichment queue, we dip into it when a step has a
real gap, not to pile things up.
