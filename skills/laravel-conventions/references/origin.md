# laravel-conventions — origin and source stamps

> Provenance of `skills/laravel-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Ideas taken from: **an org skill catalogue for this stack (45 skills: thin models, events over observers,
behaviour as opt-in traits, no markup in PHP, owning the domain, permissions not roles, permissions for
access only, no DB enums, enums with behaviour, no cascade delete, no superficial factorisation, soft deletes
requiring pruning, application-side defaults, no queries in loops, relation accessors, OrFail fetches,
intent-revealing naming, no magic strings, native type declarations, docblock style, constructor property
promotion, string interpolation, whitespace, control flow, code in English, REST routing, CRUD via the REST
mechanism, validation as arrays, mail via notifications, config conventions, command conventions, running
commands, deterministic job ordering, broadcasting, two-tier testing, one test style, seeder and factory
rules, static-analysis awareness, layered scaffolding, preferred packages)** — rules extracted, de-identified
and rewritten generically, with the internal package names, architecture scaffold, broadcaster and MCP
tooling deliberately left out (rule C); the framework's own documentation for the mechanisms cited.
Mechanisms rewritten, no copied text.

Section 10 point 4 (the Composer-package-per-layer structure) added 2026-08-10 from `xefi/laravel-osdd`
(github.com/xefi/laravel-osdd), read that date. Named directly rather than de-identified: it's the
company's own published open-source package, publicly readable outside the company like `test-casebook`
— rule C's generic-citation default is for internal/private facts, not for a real tool the company itself
ships publicly (`CONVENTIONS.md` rule C). Confirms the same layer-package shape as the Nuxt-side convention
referenced in `vue-nuxt-vuetify-conventions` §5.6: each domain a self-contained package with its own
tests/migrations, not a shared folder.
**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here: the full cost of a DB-level
cascade (audit, search index, cache, external sync, notifications, denormalised counters — none of which fails
loudly), the keep-the-FK-drop-the-cascade shape, cascade through a listener class streaming its children, the
never-both rule, the three cases where a DB cascade is fine, the "a listener that isn't firing is usually a
cascaded FK" diagnostic, the five reasons behind the no-DB-enum rule, the runtime-configurable-values carve-out
(that's a table, not an enum), and the test tiers with their routing table, their one-Act shape and their four
anti-patterns. Stamped 2026-08-06.

**Fills a real gap**: `php-patterns` covers the language and explicitly stopped at the framework boundary,
leaving Laravel — the stack with the largest catalogue of the set — with no block at all on the mentis side.

**§1.1/§1.2/§7.3 corrected 2026-08-11** against the company's own internal house documentation (its
methods section, read that date). §1.1 previously said business logic "goes in an action/service", which quietly allowed the
exact `*Service`/`*Repository` bag-name `code-baseline` already forbids — an internal contradiction the real
doc caught: it explicitly bans `UserManager`/`UserService`/`XxxRepository` and requires one verb-plus-noun
action or query class per behaviour (`RegisterUser`, `GetActiveSessionsForUser`), with the reasoning that a
repository over an ORM already abstracting persistence is a layer maintained for no benefit. §1.2 gained the
explicit `boot()` prohibition (a lifecycle closure in `boot()` is the same hidden-effect problem as an
Observer, moved one line over) — the source's own convention page states it as a **non-negotiable** rule,
stronger than this block's existing generic phrasing. The source also names concrete required packages
(`spatie/laravel-permission`, `-activitylog`, `-medialibrary`, `-translatable`, `-sluggable`, `tymon/jwt-auth`,
Pulse, Telescope, Pint, Larastan) — left out here per rule C: those are the org's own package-list authority,
already the domain of the installed org catalogue's Laravel plugin, not something to duplicate
generically.

**Bodies pass on the org catalogue, 2026-09-07.** The catalogue this block was mined from has grown from 45
skills to 65 since the 2026-08-06 pass, and that pass read descriptions before the 2026-08-06 deepening read
bodies. Re-diffed skill by skill against §1–§10: 48 were already covered. What was not, and is now:

- **§11 is new — failures.** The block had no rule at all on what happens to an error, which was the largest
  single hole in it: throw rather than return a built error response (a returned failure never reaches error
  tracking, so the endpoint fails and the error rate stays flat); reporting to a tracker without throwing
  makes the operation look successful; a `catch` earns its place by doing something; an exception whose
  meaning is always one HTTP status is HTTP-native rather than mapped in a render callback, because such a
  callback's return value is used verbatim and is therefore forced to re-implement content negotiation; and
  no hand-rolled JSON-versus-HTML branch. `code-baseline` §3 already governed what an exception *is*, which
  is why that half is referenced rather than repeated.
- **§1.4** — a concern trait owns its concept end to end (relationship, casts, scopes, accessors together),
  which resolves a real tension: §1.1 listed "simple scopes" as model-body furniture, the source moves them
  into the trait that owns the concept. §1.1 was corrected to match rather than left contradicting §1.4.
- **§1.5** — recognising a state machine and a pipeline from their Laravel-shaped triggers rather than from
  pattern vocabulary. Taken from two source skills that exist purely to be *seen* and hand off; the handoff
  target here is `skills/design-patterns` §4 and `skills/domain-modeling`.
- **§3.14** — pruning is deleting: a mass-prune trait, event suppression, a quiet delete, a truncate or a
  raw `DELETE` cron is §3.5's cascade bypass arriving from the other direction, and a summary event with a
  count is not a substitute for per-row events.
- **§3.12** — widened from "one table" to table/model/abstraction, with the earned-by test (shared meaning
  and shared change, never shared shape or shared screen).
- **§4.5** — every table reached through its model, pivots included; the raw query-builder facade skips
  casts, accessors, global scopes and events.
- **§5.8** — a date rendered as text goes through the date library's localised accessors.
- **§7.4** — a command earns its place by running more than once; a one-off data change is a migration.
- **§9.11** — a change to persisted data ships its seed data in the same change.
- **§10.3** — a branch past its security-fix end of life is a date, not an opinion.

Deliberately left out: the house package list and static-analysis ruleset, the house faker extension, the
MCP-for-AI-APIs tooling rule, and an admin-panel column-visibility rule too specific to one package to
generalise (rule C, and rule A for the last one). Mechanisms rewritten, no copied text.

**§10.6 added 2026-08-11, landed 2026-09-07.** Boost's skill surface, under the same rule-C carve-out as
§10.5: `laravel/boost` is Laravel's own first-party public package, not an internal fact. Sourced against the
real, installed org `laravel` plugin (its `boost` skill, rewritten 2026-08-11) after it stopped treating
Boost as MCP-only. The point worth keeping here is narrow and durable — skills and guidelines are separate
install surfaces, and the non-interactive install drops the former while reporting success — not the
plugin's own install-flow prose, which can drift. Written against §10 while it still lived inline in
`SKILL.md`; re-applied here after the section moved into `references/`, which is the only reason it is
stamped twice.

**Depth pass on §2, §4 and §8, 2026-09-07.** Measured rather than felt: the org catalogue this block
was mined from carries 65 skills and 79,825 words of body against this block's 9,198, and the gap is
not spread evenly — it sits in the sections that were written as pointers. §2 was 166 words against
their ~2,500 on permissions, §4 was 261 against ~6,900 on queries and models, §8 was 137 against
~2,350 on jobs, notifications and broadcasting. Those three are also the daily surface of the stack
this repo actually ships on, which is why they went first rather than the worst ratio (`csharp`, at
x17.9, is a stack nobody here writes).

What was added is failure modes and carve-outs, not restated rules: how an ownership check after the
fetch differs from a scoped query, why an aggregate beside a scoped list is part of that list's
contract, why a nested existence check is usually a column that was already there, why a search
index returns empty instead of erroring when the filter names the wrong field, why a chunked read
skips rows when the rows are mutated, why dispatching inside a transaction is intermittent, and why
a broadcast is a hint rather than a state update. Sources are the framework's own documented
behaviour plus this repo's recorded incidents, de-identified per rule C — no catalogue prose was
reproduced, and `global:no-skill-export` is why that line matters.

**Second pass, §6 and §1, same day.** §6 went 292 → 1,027 words and §1 589 → 996. §6 is where the
gap was widest after the first three, because a route table looks like the simple part: what it was
missing is the input surface nobody validates (query parameters, sort columns, page size), the three
different contracts of `nullable`/`sometimes`/absent on a partial update, using the validated payload
rather than reading the request again past validation, serialising through a resource so a new column
does not reach the API the day it is migrated, and the status code as contract. §1 gained the action's
own shape (one public method, returns a value and never a response — otherwise the console cannot
reuse it), the read/write split, the two refusals that carry the most weight in review (do not factor
out what protects nothing, do not build the extension point before the second real case) and the
accessor that is an N+1 wearing the clothes of a field.

Still short of parity on this block: ~66,000 words, tracked in `CATALOG.md` §2 as a programme rather
than a claim.

**Third pass, §7, §10 and §5, 2026-09-08.** The queue in `CATALOG.md` §2 said §3 and §9 next; measuring
before writing showed §3 already at 980 words from an earlier pass, so the order was recomputed from the
actual counts and the note corrected. The three thinnest were §7 (272), §10 (361) and §5 (442); they are
now 907, 915 and 943. Same method as the Nuxt block passes earlier the same day: originals kept, mechanism
and consequence attached, new points only where a section was silent.

§7 was a config-and-commands checklist that stopped before the operational half. Added: a secret committed
once is compromised even after removal, so the response is rotation rather than editing; a config file is
data and anything non-serialisable in it breaks the cache — or works locally and fails at boot in
production; a data-changing command is idempotent or refuses a second run, because someone will run it
again after a timeout; it reports counts, since "Done" and a no-op are indistinguishable; a destructive one
confirms and prefers a dry run, and validates its arguments as strictly as a request; a long one batches
and resumes from state in the database rather than from a position in a dead process; a scheduled one
declares its overlap policy and somewhere for a failure to surface, or it can stop working for weeks; a
seeder upserts by natural key; a factory defines the valid minimum with named states rather than the happy
path; and a backfill inside a migration is written against the schema, never against a model that will
change under it. Point 1 also gained why the `env()`-outside-config rule bites: local development has no
cached config, so the code works on the machine it was written on and reads null on the deploy that
cached it.

§10 had the layer split, the dependency-decision rule, the support-window date and the two package-specific
overrides, and nothing on how a boundary is held. Added: the dependency direction is enforced by a tool
rather than a paragraph (the `code-baseline` §8 argument applied to architecture); say whether the boundary
is a folder convention or a Composer package, since treating the first as the second is how two domains
grow a dependency nobody approved; a domain is entered through a stated surface, not by reaching into its
internals; **the database is a boundary too — two domains writing one table are one domain with two
names**; events decouple at the cost of traceability, so they belong where the producer genuinely must not
know its consumers; a new abstraction is earned by the second real case; don't add a queue, cache or search
engine for something the database still handles; keep the dependency set current continuously or the
support-window rule becomes unreachable; and an architecture decision not written down gets re-litigated.

§5 covered casing, typing and the strict-types override thoroughly. Added: a method that answers reads as a
question and one that acts is named for its effect, the costly case being the middle ground that does both;
a class named after a pattern has no subject, and the Laravel-specific instance is `*Repository`, since
Eloquent is already the data-access layer so the wrapper forbids nothing and gets bypassed; **an enum every
caller `match`es on is an enum missing a method**, and a `match` with a default arm makes the duplication
silent; a migration's file name is the only place its intent is legible; route, ability and queue names are
string contracts whose rename is a repository-wide search with nothing failing at compile time; a long
collection pipeline gets named steps or a reviewer can only trust it; `array` and `mixed` are the absence of
a type; and an exception is named for the condition rather than for the layer, which the stack trace already
gives.

Block now at 10,131 words for the router and the eleven sections, excluding this file — see the counting
correction in `CATALOG.md` §2, which stopped counting provenance as depth.
