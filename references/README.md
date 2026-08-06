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
| Scouting comparison | `VEILLE.md` (root) | doc | **Int** | ✅ |
| Infra / ports / SSO reality | `CHALLENGE.md`, `FRICTIONS.md` (root) | doc | **Int** | ✅ |
| **Design system** (4px grid, spacing, chips, buttons, containers, icons, ux-writing) | `xefi-claude-skills` plugin → `design:*` skills | skills | Pub | ✅ (index) |
| **RGAA accessibility** | `design:accessibility` skill | skill | Pub | ✅ (index) |
| **Testing** (test-casebook: data-test-*, persona matrix, ≥90%; env-attr-cleaner) | `test-casebook` repo + `doctrine-test-back-laravel-lomkit.md` | repo/doc | Pub | ✅ (index) |
| **Frontend conventions** (Nuxt/Vue/Vuetify: shorthand props, is/has booleans, i18n in a computed, no non-existent Vuetify prop) | *scattered in memory* | / | Pub (generic) | 🔜 **to write** `conventions-front.md` |
| **Backend conventions** (Laravel/lomkit: filters to the max, status+message responses, simplicity > number of calls) | `doctrine-test-back-laravel-lomkit.md` + memory | doc/ | Pub (generic) | 🔜 **to write** `conventions-back.md` (points at the doctrine) |
| **Git / commits / MR** (conventional, lowercase; MR comments short and emoji-free) | *scattered in memory* | / | Pub | 🔜 **to write** `git-mr.md` |
| **Code smells** (baseline cited by the Standards axis of `review`) | to be formalised | / | Pub | 🔜 **to write** `code-smells.md` |
| Agents (aragorn/gimli/legolas/gandalf…) | `.claude/agents/*` | defs | Int | ✅ (registry in CATALOG) |
| **Current library/framework docs** (upstream, beyond any training cutoff) | `context7` MCP server, on demand | tool | Pub | ✅ installed (see below) |
| **Social platform publishing access** (who gates posting, what it costs, what's not worth it) | `references/social-platforms.md` | doc | Pub | ✅ (dated 2026-08-06, six-month window) |

\* `CATALOG.md`: the structure is publishable, but its backlog names internal repos/layers → keep it internal until we've separated them.

## Usage rules
- **Don't duplicate**: if a subject already has a skill (design, testing), we **point** at it, we
  don't copy it over. A skill that needs a number reads it from the source, not hard-coded.
- **Filling a gap = a single doc** here, cited by every block concerned.
- **Publishable** (Pub) → can live in a future public repo; **Internal** (Int) → never. A
  "Pub (generic)" doc names **no** real project/colleague (rule C).

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
