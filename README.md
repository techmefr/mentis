# mentis

My own version of an equivalent framework seen on the open source market,
kept under my control. An agent-and-skill framework for Claude Code covering
the whole dev cycle, not just review, built by rewriting the best ideas on
the market in my own voice, without ever depending on a third-party repo.

> Test repo for my way of working with Claude Code (g.compigni).
> `xefi-mr-review` (separate repo) is the specialised implementation of the
> review/gate step alone, wired into GitLab CI. This repo covers everything
> else: brainstorm, spec, plan, TDD, code, debug, gate, ship.

## Contents

- [How I write and govern my agents](./doc/HOW-WE-WRITE-OUR-AGENTS.md), the doc to read to understand everything, with diagrams
- [Why my own version](#why-my-own-version)
- [Positioning](#positioning)
- [The pipeline](#the-pipeline)
- [What's inside](#whats-inside)
- [The rule that keeps me in control](#the-rule-that-keeps-me-in-control)
- [Quickstart](#quickstart)
- [Status](#status)
- [Licence](#licence)

## Why my own version

An equivalent framework on the open source market already encodes solid
generic discipline: brainstorming, TDD, systematic debugging, fresh-context
review. But a generic method does not carry my Xefi conventions, my real
stacks (Nuxt/Vuetify, Laravel, React), nor my own core requirement,
default = failure: work declared "done" is never taken on trust, it has to
be proven. That is the role of `galadriel`, the agent that embodies this rule
and that none of the market sources I looked at covers.

Rather than installing such a framework as-is, I rewrote every useful idea
in my own template, with my voice, my examples, my stack. I never depend on
an external repo to keep my pipeline running.

## Positioning

- **This repo** = the **method**: *how* the work flows (skills) and *who*
  executes it (agents).
- **`xefi-mr-review`** (separate repo) = a specialised implementation: the
  review/gate step only, wired into GitLab CI, one folder per stack.
- **Domain agents** (`neo`, `morpheus`, `tank`,
  the per-stack reviewers, `gandalf`, `galadriel`) = the layer that actually
  does the work, plugged into the pipeline slots below.

## The pipeline

```mermaid
flowchart LR
    A[brainstorm] --> B[spec]
    B --> C[archi]
    C --> D[plan]
    D --> E[tdd]
    E --> F[code]
    F --> G[debug]
    G --> H[gate: galadriel]
    H --> I[review: per-stack reviewers]
    I --> J[ship: gandalf]
    J --> K[finish]
```

Two guarantees hold the whole pipeline together. Fresh context: whoever
judges or reviews never watched the code being written (`galadriel`, the
reviewers, `gandalf`). Default = failure: I believe nothing without a cited
piece of evidence.

Step-by-step detail, the step → block routing table and the reasoning behind
each responsibility split: [`WORKFLOW.md`](./WORKFLOW.md).

## What's inside

### Skills: the pipeline

| Skill | Step | What it does |
|---|---|---|
| `using-mentis` | 0 | Discipline for using the framework, entry point |
| `start-feature` | 0 | Starts a feature (worktree) |
| `brainstorm` | 1 | Explores intent/need before any code |
| `spec` | 2 | Frames the need as verifiable criteria |
| `domain-modeling` | 3 | What is this concept, what's always true about it, where the rules live |
| `archi` | 3 | Architecture decisions, before the plan |
| `api-design` | 3 | Contract-first API design (Hyrum's law, extension vs breakage) |
| `documentation-adr` | 3 | Documents a significant decision (ADR template, never deleted) |
| `deprecation-migration` | cross-cutting | Frames a deprecation/migration (Strangler, Adapter, Feature Flag, Expand/Contract) |
| `wayfinder` | cross-cutting | Breaks an uncertain piece of work into a map of Jira tickets (parent + typed children) |
| `plan` | 4 | Breaks the work into verifiable steps |
| `tdd` | 5 | Test-driven development, test-casebook doctrine |
| `code` | 6 | Implementation |
| `typescript-patterns` | 6 | Pure TS/JS patterns (typing, async, closures), real production experience |
| `php-patterns` | 6 | Pure PHP patterns (typing, OOP, errors), sourced from PSR/the market |
| `vue-nuxt-vuetify-conventions` | 6 | Nuxt/Vue/Vuetify conventions, real production experience |
| `react-nextjs-conventions` | 6 | React/Next.js conventions, sourced from the market |
| `nestjs-node-conventions` | 6 | NestJS/Node conventions (DI, DTO, Zod, Prisma) |
| `go-conventions` | 6 | Go conventions: concurrency, errors, context (sourced from the market) |
| `dotnet-conventions` | 6 | C#/.NET conventions: async, IDisposable, DI, EF Core (sourced from the market) |
| `python-conventions` | 6 | Python conventions: typing, errors, async (sourced from the market) |
| `java-conventions` | 6 | Java conventions: immutability, errors, concurrency, Spring (sourced from the market) |
| `shell-scripting-conventions` | 6 | Shell fails silently by default: fail closed, quote everything, test the failure cases |
| `design-patterns` | 3 / 6 | Recognise a pattern the code already has; most of the catalogue is already in the framework |
| `auth-session-conventions` | 6 | Tokens, sessions, refresh and permission checks: the surface where a regression stays invisible |
| `security-hardening` | 6 | Trust boundaries while writing: validation, escaping per context, access control, uploads |
| `background-jobs-conventions` | 6 | Async work: idempotency, bounded retries, dead-letter, overlap; nobody is watching when it fails |
| `webperf` | 6 | Diagnose slowness from a measurement, not from intuition |
| `seo` | 6 | Technical SEO checklist for public pages (sourced from Google/web.dev) |
| `accessibility` | 6 | Technical a11y checklist (semantics, keyboard, contrast, ARIA), sourced from WCAG 2.2 |
| `qa-exploratory-testing` | 8 (complement) | Manual/exploratory testing of a flow, distinct from tdd, sourced from ISTQB/session-based testing |
| `devops-conventions` | 6 (infra/CI) | CI/CD, IaC, monitoring/alerting and incident response conventions, sourced from 12-factor/DORA |
| `data-pipeline-conventions` | 6 (data) | ETL/ELT, data quality and analytical modelling conventions, sourced from dbt/DAMA-DMBOK |
| `observability-instrumentation` | 6 | What to log, which metric, which label; complements devops-conventions at code level |
| `handoff` | cross-cutting | Handover document between two sessions on the same task, without duplicating |
| `testing-anti-patterns` | 5 / review | Mock theatre, incomplete mocks, timing guesses: how a green suite lies |
| `bug-triage` | 7 (entry) | Turn a report into a reproducible case with evidence, before any debugging |
| `debug` | support | Trace the cause backwards to its origin, then make the class of bug impossible |
| `when-stuck` | cross-cutting | The approach itself is the problem: unify, invert, push the scale, name the pattern |
| `gate` | 7 | Cold verification before merge, see the `galadriel` agent |
| `review` | 8 | Diff review, see the per-stack reviewer agents |
| `over-engineering-review` | 9 | Deletion angle only: dead code, over-abstraction, yagni |
| `simplify` | 9 | Applies the identified simplifications |
| `ship` | 10 | Merge + notification, see the `gandalf` agent |
| `finish` | 11 | Cleans up the worktree, updates the base branch |
| `merge-worktree` | 11 | Multi-worktree merge mechanics |
| `extract-conventions` | maintenance | Generates conventions from the real existing code |
| `choose-model` | cross-cutting | Decides Haiku/Sonnet/Opus for a new agent or a one-off task |
| `dispatch-parallel` | cross-cutting | Splits a task across parallel subagents on disjoint scopes |
| `writing-skills` | cross-cutting (meta) | How to write/revise a skill in this framework |
| `writing-agents` | cross-cutting (meta) | How to write/revise an agent in this framework (7-pillar template) |
| `testing-blocks` | cross-cutting (meta) | Prove a block changes behaviour under pressure, before calling it done |
| `distributing-blocks` | cross-cutting | Install/update for other teams: they pull and merge, we never push |
| `maintaining-blocks` | cross-cutting (meta) | Audits this corpus: dangling references, stale statuses, blocks that duplicate each other |
| `source-freshness` | cross-cutting (meta) | External facts carry a source and an expiry; refresh against real docs (`context7`), never memory |
| `portless-ready` | infra | Makes a stack portless (HTTPS alias, port hygiene) |

### Business layer (second layer, weaker contract)

[`business/`](./business/README.md) holds blocks for the company's other functions. Same
template, but they **never gate anything** and they claim no evidence: the two
guarantees above need citable artefacts, and a positioning statement has none.
Keeping them in a separate folder is what stops the dev core's claims being
diluted by association. Each one states in its `Origin` that it was written
without internal expertise in that function.

| Block | Function | What it does |
|---|---|---|
| `data-protection` | legal | Which GDPR questions must reach a lawyer/DPO before the code is written, and what the code then owes |
| `licence-compliance` | legal | Recognise the licence category before installing, escalate copyleft, meet attribution mechanically |
| `legal-documents` | legal | Which public documents apply (terms, policies, DPA, SLA), and the factual pack a lawyer needs before drafting |
| `regulatory-watch` | legal | Jurisdiction first, primary source or `[verify]`, and a deadline past its window is unverified |
| `ux-writing` | UI/UX | Errors with a next action, buttons naming the outcome, empty states that aren't "No data" |
| `product-marketing` | marketing | Positioning in four sentences; every factual claim carries a source before it ships |
| `sales-support` | sales | Estimate ≠ commitment, never a date in the room, demos show what exists |
| `release-communication` | communication | Sort by what the reader must do; deprecations carry a path and a date |
| `incident-communication` | communication | First message before the cause is known, announced cadence, no speculation, no blame |
| `internal-communication` | communication | The ask in the first line; a decision that lives only in a call isn't announced |
| `content-creation` | communication | Start from work actually done, mine the pipeline's own artefacts, and keep the hook honest |
| `community-management` | communication | The replies, every day: sort and route, never delete criticism, and what a CM must never answer alone |
| `product-ownership` | product | Whether it should exist, in what order, and how anyone knows it's done — the story artefact stays with the plugin |
| `social-publishing` | communication | One message adapted per platform, never four truths; an agent drafts, a human publishes |

### Agents

Two name families, and the family tells you what the agent is allowed to do:

- **Lord of the Rings = watching.** Review and gate only. These agents read a
  diff, judge it and report. None of them holds Write/Edit on the repo under
  review.
- **The Matrix = the dev cycle.** Everything that takes part in producing the
  work: the implementers, and the auditors that probe a running app or a repo.

So the name is a readable guarantee: a LotR name never decides anything about
your code beyond a verdict, and it never touches it.

| Agent | Role | Status |
|---|---|---|
| `galadriel` | Fresh-context GATE: PASS/NEEDS_WORK verdict, never edits, never gives the benefit of the doubt | Real production experience |
| `gandalf` | Final MR gate: test gate + delegates the review + `/code-review` + `/security-review` | Real production experience |
| `elrond` | Orchestrator: detects the stack and delegates to the right reviewer, never reviews itself | Real production experience |
| `aragorn` | Nuxt/Vue/Vuetify reviewer | Real production experience |
| `gimli` | PHP/Laravel reviewer, uncertainty phrased as questions (g.compigni is new to this stack) | Real production experience |
| `legolas` | React reviewer | Sourced via test-casebook |
| `boromir` | Go reviewer, uncertainty phrased as questions | Sourced from the market |
| `theoden` | C#/.NET reviewer, uncertainty phrased as questions | Sourced from the market |
| `frodo` | Generic JS/TS backend reviewer (NestJS/Node), real expertise, assertive style | Real expertise |
| `neo` | Implements Vue3/Nuxt3 code (never reviews its own code) | Written, not dogfooded yet |
| `morpheus` | Implements Laravel/Eloquent code (never reviews its own code) | Written, not dogfooded yet |
| `trinity` | Implements NestJS/Node code (contracts first, never reviews its own code) | Written, not dogfooded yet |
| `tank` | SQL tuning (MySQL/SQL Server) and Elasticsearch-Scout mapping/indexing | Written, not dogfooded yet |
| `dozer` | Writes the test suite (test-casebook, default-FAIL); tests only, never implementation | Written, not dogfooded yet |
| `keymaker` | Technical SEO audit of a live page/site, never edits | Written, not dogfooded yet |
| `link` | Technical a11y audit of a live page/site, never edits | Written, not dogfooded yet |
| `mouse` | Manual/exploratory testing of a flow on a running app, never edits | Written, not dogfooded yet |
| `seraph` | Dedicated static security audit (code/config/dependencies), read-only, complements the native `/security-review` | Written, not dogfooded yet |
| `architect` | Periodic architecture-debt audit (git hot-spots, deletion test), never edits | Written, not dogfooded yet |

Full detail: [`CATALOG.md`](./CATALOG.md) (registry + sourcing backlog, with
every idea credited to its real source) and
[`CONVENTIONS.md`](./CONVENTIONS.md) (the single template and rules A/B/C).

## The rule that keeps me in control

I never wire an external repo in as a dependency. I read → I extract the
mechanism → I rewrite it in my single template → I credit the source in
`CATALOG.md`. That guarantees two things: nobody upstream can break my
pipeline by changing their repo, and everything is written the same way (so
it stays maintainable). Detail in [`CONVENTIONS.md`](./CONVENTIONS.md).

## Quickstart

Every skill/agent is a self-contained markdown file (frontmatter + body), in
Claude Code's native format:

1. Copy the file(s) you want into `.claude/agents/` or `.claude/skills/` in
   the target repo.
2. Pipeline skills are invoked in sequence (`brainstorm` → `spec` → ... →
   `finish`) or à la carte depending on the need.
3. Agents are invoked through Claude Code's `Agent` / `Task` tool, directly
   by name (e.g. `elrond` for a multi-stack review, or `aragorn`/`gimli`/...
   directly if the stack is already known).

## Where this is going

Four stages, in this order, and the order is the point:

1. **Build the blocks** (here, ongoing): the workflow, the agent roster, the
   skills. Each one rewritten our way, credited, under the single template.
2. **Dogfood them on real projects**: every block runs at least once on real
   work before it counts. Today most of the roster is written but never run,
   which `CATALOG.md` marks honestly as 🟡.
3. **Share it across the company**: other teams install it and use it.
4. **Keep it updated** for those users, without becoming the thing rule B
   warns about.

### Stages 3 and 4: rule B, applied to myself

Rule B exists so that **nobody upstream can break my workflow**. The moment
this gets distributed, *I become that upstream* for every colleague who
installs it. The mechanism is in [`distributing-blocks`](./skills/distributing-blocks/SKILL.md),
and it's deliberately boring: consumers clone a repo they own, updates are a
merge **they** pull and read, conflicts are theirs to resolve, and staying on
an older version on purpose has to remain possible.

- **No silent auto-update.** An update that rewrites someone's agents without
  them reading it is precisely what rule B forbids others from doing to me.
- **The ours-vs-theirs boundary needed no invention.** I had this listed as an
  unsolved design problem requiring a folder convention before the first
  install. It doesn't: consumers' customisations are commits, so git already
  models the boundary and they survive a merge by construction.
- **Rule C is load-bearing here, not just for a hypothetical public release.**
  Sharing across the company means many teams: a block hard-coding one team's
  project name is useless to the others and leaks to everyone. Some blocks are
  therefore deliberately kept out of this repo, and stay local.
- **Order still matters against rule A.** Distributing blocks that have never
  been run spends the credibility of the first colleagues who try it, and
  that's the hardest credit to win back. [`testing-blocks`](./skills/testing-blocks/SKILL.md)
  is the cheap validation (does the block change behaviour under pressure?);
  real use on real work is the expensive one. Neither substitutes for the other.

## Status

Active demonstrator: my doctrine (template, rules A/B/C, default = failure,
fresh context) is stable and applied, some agents have real production
experience (`aragorn`, `gimli`, `gandalf`, `galadriel`, `elrond`), others are
written but not dogfooded yet (`neo`, `morpheus`,
`tank`) or sourced from the market with no internal experience yet
(`boromir`, `theoden`, `go-conventions`, `dotnet-conventions`). The exact
line-by-line detail is in `CATALOG.md`.

## Licence

No licence chosen yet, internal repo for now, not meant to be public as-is.
