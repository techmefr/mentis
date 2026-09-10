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

**Fourth pass, §11 and §9, 2026-09-08.** 515 → 1,019 and 655 → 1,073; 6 → 14 points and 13 → 19. Both
sections were already well argued, so this pass added the failure modes they did not reach rather than
restating the ones they did.

§11 owned the throw-versus-return argument end to end and stopped at the throw. Added: a failure carries
what the caller needs in order to act — per-field detail for a validation failure, identifiers as data on
a domain exception rather than baked into a string a caller would have to parse; the exception message is
for developers while the user-facing sentence is the handler's decision, which also keeps internal detail
out of the response; **inside a transaction a throw is the rollback**, so catching and continuing there
commits the half-finished unit of work the transaction existed to prevent, and irreversible side effects
belong outside it because a rollback cannot recall an email; a retry re-runs everything before the failure
point, so anything retryable is idempotent by construction; **an external call fails in five ways, not
one** — timeout, refused connection, 5xx, rate limit, malformed body — and one `catch (Exception)` treats
a rate limit as a bug; an expected failure is not a defect and reporting 422s beside real exceptions
raises the volume until the real ones are unfindable; a report carries identifiers, not payloads, since
dumping a request body puts personal data in a third-party tool under someone else's retention policy;
and the failure path is asserted, or the first refactor turns the throw back into the returned error
response point 1 forbids with nothing going red.

§9 had the two tiers, the routing table and the seed-data bar. Added: **a test that has never failed
proves nothing** — write it red, or break the behaviour once and watch it, which is the repo's own
default-is-failure guarantee applied to its output; freeze time and randomness, because a suite reading
the real clock fails on the first of the month and in the CI timezone; each test stands alone, since
order-dependent tests read as infrastructure trouble rather than as the coupling they are; **assert the
refusal, not only the success** — authorisation is tested per persona and the personas that matter are the
ones who must not see the thing, because that is the failure that becomes an incident rather than a bug;
coverage is a smoke detector and a line executed is not a line asserted; and a slow suite gets skipped, so
its speed is part of its design. Point 13 was widened from the factory-with-an-outbound-listener trap to
faking every external boundary, and point 12's continuation indent was corrected.

Block now at 11,053 words for the router and eleven sections; the laravel stack (with `php-patterns` and
`inertia-conventions`) at 13,718 against 79,825, x5.8. **Ten of the eleven sections have now had a depth
pass** — §2, §4, §8, then §6, §1, then §7, §10, §5, then §11, §9. The one that has not is §3, and it does
not need one from this programme: the bodies pass above already took it to 980 words, which is where these
passes land. So the block is done, and what remains for the laravel stack is `php-patterns` (960 words,
no `references/` at all) and `inertia-conventions` (1,705, same) — both single-file blocks, which is a
different shape of work from deepening sections that already exist.

**Both of those landed the next day, 2026-09-08**, and the row is now 23,118 against 79,825, **x3.45**:
`inertia-conventions` 1,705 → 6,679 (five inline sections moved to `references/`, a sixth added for the
visit lifecycle) and `php-patterns` 960 → 5,386 (three moved, two added for the standard library's
comparison and array semantics and for time/money/text). Two boundary rules of this block are cited by
name from there and both still hold: §6's REST-resource guidance is scoped by `inertia-conventions` §4 to
controllers that actually return JSON for a non-Inertia consumer, and §5.12's no-`strict_types` default
is the override of `php-patterns` §1.1 — which kept its number for exactly that reason.

**Widened against the current Pest testing surface, 2026-09-09.** All eleven prior passes closed the
catalogue-comparison gap or added failure modes the block was silent on; none checked whether §9 still
described how tests are actually written today, since the block predates Pest becoming the ecosystem's
default runner. Checked against Pest's own current documentation, not against the catalogue: §9 gained
four points — Pest's `it()`/expectation-API closures are a syntax choice on top of the same two-tier rule
(point 20), a dataset replaces repeated inputs to one assertion and never diverging behaviours (point 21),
an architecture test (`arch()`) makes an existing structural rule from §1/§5 fail in CI instead of relying
on a reviewer to remember it (point 22), and mutation testing is what point 18's "coverage is a smoke
detector" argument becomes automatic and actionable (point 23). Nothing here answers the catalogue
comparison a second time — every point is dated to Pest's current feature set rather than to the source
catalogue mined in 2026-08. Word counts re-measured with `bin/measure_depth.py` after the edit; see
`CATALOG.md` for the updated row.

**Second pass same day: §8, job middleware and batches.** The section covered ordering, idempotence and
failure but had nothing on the framework's own coordination mechanisms. Two points added: job middleware
(`WithoutOverlapping`, `RateLimited`, `ThrottlesExceptions`) as the declared answer to "not two of these at
once", rather than a hand-rolled lock reinventing point 1's ordering problem — and `WithoutOverlapping`
releasing rather than dropping a job, which still needs point 2's idempotence; and `Bus::batch()` as
coordination-for-reporting, not coordination-for-data, since its callbacks fire once for the whole batch
and a job needing another job's *result* is still a chain. Word counts re-measured; see `CATALOG.md`.

**Third pass same day: §6, Precognition and outbound concurrency.** Two points added: `HandlePrecognitiveRequests`
runs the same FormRequest the real submission runs, which is what makes point 5's rules reusable for
as-you-type validation without a second endpoint — with the trap that a rule only valid once the operation
runs (a uniqueness check against a row about to be created) has to be scoped to skip during a precognitive
request; and `Http::pool()` as the outbound-call equivalent of the async-gather rule other stacks in this
repo state, with the same per-response failure decision a naive "the pool failed" treatment loses.

**Fourth pass same day: §4, `chaperone()` and the `lazy()`/`cursor()` distinction.** Two points added:
`chaperone()` as the framework's fix for the specific N+1 point 2 already names — a child reaching back
for its own parent — hydrating the parent from the eager load rather than issuing a query per child; and
`lazy()` versus `cursor()` as two different answers to point 8's chunking need, not interchangeable —
`cursor()` is cheaper on memory but drops back to a full collection the moment a Collection-only method is
called on it, `lazy()` keeps chunking under the hood through the same call.

**Fifth pass same day: §4 and §3, `shouldBeStrict()` and generated columns.** §4 gained
`Model::shouldBeStrict()` as point 1's N+1 rule turned into a thrown exception rather than a review
checkpoint, bundled with two sibling checks (silent mass-assignment discard, a read of a missing
attribute) — environment-specific by design, so running it in production as well as locally trades a
caught bug for a 500 on every affected user. §3 gained the generated column (`virtualAs`/`storedAs`) as
the answer when a computed value has to be filtered, sorted or indexed by the database, distinct from an
accessor, which covers the same computation for a value nothing ever queries by.

**Sixth pass same day: §2, `Response::deny()`.** One point added: a policy returning `Response::deny($message)`
instead of `false` carries the reason for a 403, which is what makes the denial actionable rather than
identical to every other refusal — still a policy decision, not validation, so the message explains why
this caller may not, never what is wrong with the payload.

**Eighth pass same day: §7, `Isolatable`.** One point added: the `Isolatable` interface as point 11's
overlap policy for a command triggered outside the scheduler — a manual rerun, a webhook, two deploys
close together — where `withoutOverlapping` alone leaves it unprotected; the lock key defaults to the
command's name, so `isolatableId()` has to fold the arguments in or two runs with different arguments
serialise work that was actually safe to run in parallel.

**Seventh pass same day: §11, `withExceptions()`.** One point added: `dontReport()`, `throttle()` and
`stopIgnoring()` in `bootstrap/app.php` as where point 12's tracker-must-know-the-difference argument is
actually enforced — naming a class as expected once rather than catching it at every throw site, sampling
a class that fires legitimately at volume instead of either silence or flooding the tracker, and reversing
the framework's default ignore list where a spike in an otherwise-routine status is itself the signal.

**Widening, 2026-09-10 — §2, §5 and §8 gain 12 points.** The three thinnest sections got the pass, applying
the standard rule: extend, don't renumber, because 25 standalone `skills/laravel-*` files already cite exact
§N.M positions in this document. §2 (authorisation) gained `Gate::before()` for a single-declaration
super-admin bypass instead of a role check copy-pasted into every policy, Sanctum token abilities as a
narrower layer under the user's own permissions, treating an authorisation denial as a tested contract the
same as the success path, and policy-discovery naming — a policy that breaks the convention denies silently
rather than throwing, which reads as a strict app instead of a wiring bug. §5 (naming, typing, style) gained
`readonly` promoted properties for value objects and DTOs as point 6 taken one step further, boolean
predicate naming for properties and parameters (not just methods, which point 13 already covered), backed
enum type choice (string for a label, int only for something genuinely ordinal), and `final` by default with
an abstract base as the deliberate exception. §8 (jobs, notifications, realtime) gained `ShouldBeUnique`
versus `WithoutOverlapping` as answers to two different questions — stopping a duplicate from being queued
versus stopping two queued copies from running at once — presence channels as private channels plus a
roster rather than a separate authorisation model, on-demand notification routing for a recipient with no
`User` record, and `ShouldBeEncrypted` for a job payload carrying something sensitive, extending point 3's
reference-not-snapshot reasoning to the case where the snapshot must exist anyway.

**Widening, 2026-09-10 — pass élargie.** Five more files widened with the same extend-don't-renumber method,
this time against Laravel's own current official documentation (laravel.com/docs) rather than the org
catalogue — the ~25 standalone `skills/laravel-*` files citing exact `§N.M` positions (`check_citations.py`)
are why nothing existing was renumbered:

- **§1 (where behaviour lives), 996 → ~1,750 words**, points 11–15: contextual binding declared once in a
  provider instead of scattered per-consumer; a bound interface earned by a genuine second implementation, not
  for testability alone; `Macroable` kept to framework classes built for it rather than a project's own
  classes; a service provider grouped by domain, not by framework primitive; a deferred provider's boot-time
  work has to survive being deferred.
- **§7 (configuration and commands), 1,011 → ~1,750 words**, points 17–21: `config:cache` as the deploy step
  that actually surfaces point 1's `env()` trap; the signature string's optionality/array/flag syntax; a
  scheduled entry's own timezone against server drift; `->after()`/`->before()` chaining over one command
  calling another; testing a command by invoking it (`assertExitCode`) rather than extracting its logic to
  unit-test around it.
- **§3 (data model and schema), 1,071 → ~1,850 words**, points 17–21: a custom cast class earned by a
  transformation no built-in cast covers; `Attribute::make` replacing the accessor/mutator pair; composite
  index column order following the leftmost-prefix rule; a foreign key's `onDelete` action as a decision about
  the child's fate (cascade/restrict/set null); a JSON column's path filters not indexed unless promoted to a
  generated column (§3.16).
- **§4 (queries), 1,169 → ~1,950 words**, points 15–19: constrained eager loading versus `whereHas` answering
  different questions; `morphWith()` for polymorphic type-specific eager loads; a correlated subquery select
  over a per-row loop for a value like "latest child"; `whereHas` versus a direct join at scale; a transaction
  retry count for a deadlock, safe only because §4.11 already keeps side effects out of the callback.
- **§6 (HTTP surface), 1,196 → ~2,000 words**, points 19–23: a named rate limiter instead of an inline
  `throttle:N,1`; a resource's conditional attributes (`whenLoaded`/`when`/`mergeWhen`) keeping the payload
  honest about what was fetched; a resource collection's pagination metadata generated from the paginator
  rather than hand-built; a custom validation rule earned by reuse, not by a single use; the `api`/`web`
  middleware groups' differing session/CSRF defaults as part of a route's contract.

Sourcing: every new point is either a mechanism already present in `laravel-conventions`/`php-patterns`/
`inertia-conventions` restated at a different angle (composite indexes, transaction retries, resource
serialisation) or synthesised fresh from Laravel's public documentation for the mechanism named (contextual
binding, `Macroable`, deferred providers, config caching, command signatures, scheduling, `Attribute::make`,
custom casts, `morphWith`, rate limiters, conditional resource attributes) — never read, copied or paraphrased
from the XEFI marketplace, whose file contents were not opened for this pass. `02-authorisation.md`, `05-naming-typing-style.md`,
`08-jobs-realtime.md` and `09-tests-static-analysis.md` were left untouched, already widened in the prior
passes above.

**Widening, 2026-09-10 — second pass, §10 and §11 gain 6 points each.** The two files the prior same-day pass
left out — `10-architecture.md` (915 words, the single thinnest file in the block) and `11-failures.md`
(1,132 words) — go through the same extend-don't-renumber method against Laravel's own current
documentation. §10 (architecture) gains points 16–21: contextual binding (`when()->needs()->give()`) as the
container-level answer to point 4's "prefer the framework's own mechanism"; a deferred service provider's
cost trade-off, and why one with a side effect in `boot()` cannot be deferred without silently losing it; a
middleware group's declared order as part of the architecture, not an artifact of file layout — a
rate-limiter registered before `auth` throttles every guest under one shared bucket; a feature toggle as a
config value with an environment default rather than a conditional shipped then reverted; package
auto-discovery as a Composer convenience that still counts against point 2's "check what's already
standardised on"; and a facade's binding as swappable per-request until the facade is first resolved, which
caches the instance for the rest of that request. §11 (failures) gains points 16–21: a queued job's
`failed()` as the place for the side effect retries cannot cause, not a second attempt at the job itself; a
retried job re-dispatching from `handle()` rather than resuming, which makes point 10's idempotency
non-optional; `Http::fake()`'s silent generic response for a route nobody stubbed, and `assertSent()` as what
actually proves the request shape; `ValidationException` versus a bespoke domain exception for a 422-shaped
failure; a rate-limit exception and its `Retry-After` header as an expected outcome rather than an incident,
the queue-and-HTTP-layer sibling of point 12's tracker-noise argument; and asserting an exception's message or
data, not only its class, so a refactor that swaps in a same-class exception with the wrong payload still
fails the test.

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/
`php-patterns` at a different angle (idempotent retries, tracker-noise for expected failures, the
prefer-the-framework's-own-mechanism argument) or is synthesised fresh from Laravel's public documentation
for the mechanism named (service container contextual binding, deferred providers, middleware group
ordering, package auto-discovery, facade resolution, queued-job `failed()`, `Http::fake()`,
`ValidationException`, rate limiting) — `laravel.com/docs/12.x/{container,rate-limiting,http-client}`, read
2026-09-10 — never the XEFI marketplace, whose file contents were not opened for this pass.

**Widening, 2026-09-10 — troisième pass.** The five thinnest remaining files after the first two same-day
passes — `05-naming-typing-style.md`, `08-jobs-realtime.md`, `09-tests-static-analysis.md`,
`01-where-behaviour-lives.md` and `07-configuration-commands.md` — each gain 5–7 new points appended after
the existing numbering (never renumbering what was already there). §5 (naming/typing) adds PHPStan/Larastan
level discipline as a project-wide ratchet rather than a per-file choice, Larastan's own Eloquent model
making hand-written `@property` blocks redundant, named arguments over a comment explaining a positional
one, first-class callable syntax for method references, union vs. intersection types as honest contracts
instead of `mixed`, and a named enum case standing for one record as a sign the enum modeled a row instead
of a category. §8 (jobs/realtime) adds `ThrottlesExceptions`' two arguments (exception budget vs. cooldown
minutes), a released job still counting against `tries`/`maxExceptions`, `retryUntil()` as a wall-clock bound
distinct from attempt count, a queue connection's `retry_after` needing to exceed the job's real runtime, a
private channel's authorisation callback staying a pure yes/no, and batching's `allowFailures()` as an
explicit choice rather than a silent default. §9 (tests/static analysis) adds `RefreshDatabase`'s per-driver
strategy (SQLite transaction vs. migrate-fresh) and what defeats it, parallel testing's per-worker database
and the `ParallelTesting` facade, a boundary fake needing to model failure paths and not only the happy one,
`assertDatabaseHas`/`assertDatabaseCount` not proving which operation produced the row, snapshot tests as a
narrow exception rather than a shortcut, and testing a form request or policy in isolation as an addition to
the feature test, never a replacement. §1 (where behaviour lives) adds `singleton()` vs. `scoped()` container
lifetimes, the actual boundary between a banned repository wrapper and an allowed query class, a concern
trait documenting the shape it expects from its host class, named pipeline stages over inline closures, a
global scope's invisibility as a feature for tenant isolation and a liability for conditional business rules,
and eager-loading declared with the producing query rather than patched on afterward. §7
(configuration/commands) adds config-key collision across cascading files, `Context` for request/job-scoped
cross-cutting data, a command's exit code as a contract for `&&`-chaining and CI, `schedule:list`/
`schedule:test` for verifying a scheduled entry without waiting for its cron minute, a non-interactive
command never blocking on an unguarded prompt, and environment branching done through config rather than an
`environment()` conditional in application code.

Sourcing: every new point is synthesised from Laravel's own public documentation for the mechanism named —
queues (job middleware, batching, unique/overlapping jobs), database testing and parallel testing, the
service container (`singleton`/`scoped` lifetimes), configuration and the scheduler
(`laravel.com/docs/{12.x,13.x}/{queues,database-testing,container,configuration,scheduling}`) — plus
Larastan's own documented level/extension model for the PHPStan-facing points, all read 2026-09-10; the
rest restates a mechanism already present in `laravel-conventions`/`php-patterns` at a new angle. The XEFI
marketplace's file contents were never opened for this pass.

**Widening, 2026-09-10 — quatrième pass.** The five thinnest files remaining after the first three same-day
passes — `02-authorisation.md` (2,040 words after its own earlier pass this same day), `10-architecture.md`
(2,111), `03-data-model-schema.md` (2,166), `04-queries.md` (2,296) and `06-http-surface.md` (2,251) — each
gain another 5–7 points, same extend-don't-renumber method: nothing already numbered moved, everything new
appended after the last existing point, because the standalone `skills/laravel-*` files' `§N.M` citations
(`bin/check_citations.py`) depend on the numbering holding still.

§2 (authorisation) adds points 15–21: `Gate::after()` only widening a `null` result, never overruling one a
policy already settled; `authorizeResource()`'s seven-action mapping and the silent gap it leaves for a
custom controller action; a policy's own `before()` as point 11's bypass shape scoped to one model instead
of every ability; a ternary permission check still needing a named ability instead of an inline fallback; a
middleware `can:` check and a controller `$this->authorize()` drifting once both exist for the same route; a
frontend's conditional rendering never substituting for the server-side check; and a permission's removal or
rename as a data migration on the pivot rows, not just a code change.

§10 (architecture) adds points 22–28: `register()`/`boot()` load order as the reason cross-provider
resolution belongs in `boot()`; a published config file forking from the package's own and falling behind
silently; a swapped container binding needing to be unbound so it doesn't leak into the next test; a
request-scoped value frozen into a `singleton()` closure at boot time; a queued job dispatched before commit
racing its own not-yet-committed data; `env()` outside `config/*.php` going invisible under `config:cache`;
and a shared trait versus an interface as different guarantees for callers, not interchangeable ways to say
"several models need this."

§3 (data model and schema) adds points 22–28: `foreignId()->constrained()` as the two-part shorthand where
the constraint is not implied by the column alone; an unnamed foreign key silently detaching from a table
rename; `upsert()` needing a real unique key behind the columns it checks, or every call re-inserts; a
composite primary key requiring `$primaryKey`/`$incrementing` set explicitly on the model; a foreign key not
being, by itself, a good index for every filter on that table; the add-nullable/backfill/tighten-to-`NOT
NULL` migration ordering a populated environment enforces that an empty CI database never catches; and
storing timestamps in UTC rather than local time for cross-timezone and DST correctness.

§4 (queries) adds points 20–26: `upsert()`'s collision columns needing a real unique constraint behind
them, the query-layer half of §3's new point 24; `chunkById` as point 8's ordering trap solved by
construction rather than a faster `chunk()`; `joinSub`/`leftJoinSub` for a value pulled alongside a list
versus `whereHas`'s "which parents" question; `withExists()` avoiding a discarded `COUNT` for a plain
existence check; a sortable/filterable column needing an allow-list beyond the binding that already
protects the value; a soft-deleted row still occupying a unique index unless the index itself excludes it;
and a query-builder bulk update or delete skipping model events the same way point 9 already covers casts
and scopes.

§6 (HTTP surface) adds points 24–30: `apiResource`/`apiResources` excluding `create`/`edit` by default and
what it means when a controller adds them back; `only()`/`except()` narrowing which conventional actions
exist as an authorisation surface, not just a route list; a single-action controller's `__invoke()` as the
one-off answer that stops being one-off past a second unrelated route; route model binding scoped to a
column (`{post:slug}`) as the framework's own mechanism for a non-numeric public URL; `withoutMiddleware()`
stripping protection from one route inside a group, deserving the same visibility as a stated public
carve-out; a child resource composing its payload via `parent::toArray()` instead of duplicating near-
identical field lists; and a hand-written route beside its resource siblings drifting from their shared
naming/middleware/throttling convention because nothing forces it to match.

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/
`php-patterns` at a different angle (idempotent upserts, the account-for-mass-operations argument, prefer-
the-framework's-own-mechanism, the tested-refusal argument) or is synthesised fresh from Laravel's current
public documentation for the mechanism named — authorization (`Gate::after`, `authorizeResource`, policy
`before()`), the service container and providers, migrations (`foreignId`/`constrained`, named foreign
keys), the query builder (`upsert`, `chunkById`, `joinSub`, `withExists`), and controllers/routing
(`apiResource`, resource action filtering, route model binding by column) — `laravel.com/docs/12.x/
{authorization,providers,migrations,queries,controllers}`, read 2026-09-10. The XEFI marketplace's file
contents were never opened for this pass.

**Widening, 2026-09-10 — cinquième pass.** The five thinnest files by an actual `wc -w` measurement at the
start of this pass — `11-failures.md` (1,634), `08-jobs-realtime.md` (1,773), `05-naming-typing-style.md`
(1,812), `09-tests-static-analysis.md` (1,815) and `07-configuration-commands.md` (1,834) — each gain
another 5–8 points, same extend-don't-renumber method as every prior same-day pass: nothing already
numbered moved, everything new appended after the last existing point, because the standalone
`skills/laravel-*` files' `§N.M` citations (`bin/check_citations.py`) depend on the numbering holding still.

§11 (failures) adds points 22–28: an exception's own `report()`/`render()` methods, called automatically
when present, for handling that belongs to one exception class rather than to `bootstrap/app.php`;
`report()`'s `stop()` to suppress the framework's default logging without losing the custom handling;
`respond()` customising the whole response shape versus `render()` customising one exception; the framework's
`dontReportDuplicates()` collapsing one failure reported twice in a single request; `Context` set before a
throw travelling into the report automatically; a `Fiber`-based concurrent call (`Concurrency`, `Http::pool()`)
failing per branch rather than as a whole; and a `terminate()` failure having no request left to answer, only
a tracker.

§8 (jobs/realtime) adds points 24–29: `toOthers()` excluding the triggering socket from its own broadcast;
`ShouldBroadcastNow` for the immediacy cases where a queued broadcast would already be stale; `withoutRelations()`
stripping an eagerly-loaded relation from a queued model's payload before it is serialised twice; job-priority
routing via `->onQueue()` only mattering if a worker's `--queue` flag actually lists that name; `$batch->add()`
growing a batch from inside one of its own jobs; and `Concurrency::run()` as parallel I/O with no retry and no
`failed()`, not a queue substitute.

§5 (naming/typing) adds points 32–37: PHP 8.3 typed class constants; a whole-class `readonly` declaration
versus repeating the keyword per property; the `never` return type for a method that always throws or aborts;
an enum implementing a shared interface (`HasColour`, `HasLabel`) instead of a `match` copied across callers;
the nullsafe operator's actual scope (a legitimately optional relationship, not a loud bug hidden quiet); and
PHP 8.4 asymmetric visibility (`private(set)`) as the middle ground between `readonly` and a public setter.

§9 (tests/static analysis) adds points 30–36: `Bus::fake()->assertChained()` proving job order, not just
dispatch; `Notification::fake()` proving the trigger while a direct `toMail()`/`toArray()` assertion proves
the content; `Event::fake(except: [...])` keeping a model's own maintained-column listener switched on while
faking the rest; `Http::fake()`'s response sequencing for exercising a retry path end to end; `Queue::fake()`'s
chain-specific assertions (`assertPushedWithChain`/`assertPushedWithoutChain`); `Mail::fake()`'s content
assertions (recipient, locale) versus proving only that some mailable of the right class went out; and
`Storage::fake()` assertions naming the exact path, not just existence.

§7 (configuration/commands) adds points 28–33: Laravel Prompts (`search()`, `suggest()`, `spin()`) replacing
`ask()`/`choice()` for anything richer than one line, still bound by the non-interactive rule already stated;
`Config::string()`/`integer()`/`boolean()` as typed reads over `config()`'s `mixed`; `Schedule::job()`'s queue
dispatch versus `Schedule::command()`'s full process spawn, and the cost difference at high frequency;
`php artisan about` for confirming the effective cached configuration instead of guessing; the
`InteractsWithIO` output helpers (`$this->components->info()/task()`) for consistent command output across a
project; and `route:cache`/`event:cache` as `config:cache`'s siblings carrying the same closure-breaks-the-cache
trap.

Word counts re-measured with `wc -w` after the edits: `11-failures.md` 1,634 → 2,180 (+546),
`08-jobs-realtime.md` 1,773 → 2,292 (+519), `05-naming-typing-style.md` 1,812 → 2,328 (+516),
`09-tests-static-analysis.md` 1,815 → 2,284 (+469), `07-configuration-commands.md` 1,834 → 2,316 (+482).

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/`php-patterns`
at a different angle, or is synthesised fresh from Laravel's own current public documentation for the
mechanism named — error handling (`report()`/`render()` on the exception, `stop()`, `respond()`,
`dontReportDuplicates()`), broadcasting (`toOthers()`, `ShouldBroadcastNow`), queues (`withoutRelations()`,
batch `add()`, `Concurrency`), PHP 8.3/8.4 language features (typed class constants, asymmetric visibility),
Pest/PHPUnit fakes (`Bus`, `Event`, `Http`, `Queue`, `Mail`, `Storage`), and console/config tooling (Laravel
Prompts, typed config accessors, the scheduler, `artisan about`, cache-clearing commands) —
`laravel.com/docs/12.x/{errors,broadcasting,queues,console-tests,http-tests,mocking,artisan,prompts,configuration,scheduling}`
plus `php.watch`'s coverage of PHP 8.3/8.4, all read 2026-09-10. The XEFI marketplace — referred to here only
as "the marketplace XEFI" — was never opened for this pass: no file under it was read, only the fact that a
content gap existed was known going in.

**Widening, 2026-09-10 — sixième pass.** The five thinnest files by a fresh `wc -w` measurement —
`01-where-behaviour-lives.md` (1,907), `02-authorisation.md` (2,040), `10-architecture.md` (2,111),
`03-data-model-schema.md` (2,166) and `11-failures.md` (2,180) — each gain 6 new points, same
extend-don't-renumber method as every prior same-day pass: nothing already numbered moved, everything new
appended after the last existing point, because the standalone `skills/laravel-*` files' `§N.M` citations
(`bin/check_citations.py`) depend on the numbering holding still.

§1 (where behaviour lives) adds points 22–27: a single-action `__invoke()` controller reserved for a route
that isn't one of a resource's seven verbs; PHP 8.4 asymmetric visibility (`private(set)`) for a value
object's own property instead of a private field plus a getter; `once()` for request-scoped memoisation,
correctly bounded where a static property would leak past the request on a long-lived worker; `Conditionable`'s
`when()`/`unless()` keeping a query's own conditional narrowing inside the query builder instead of an
external `if`/`else` around near-duplicate query blocks; a queued job's `handle()` resolving its
collaborators through method injection rather than the constructor, so they are fetched fresh at execution
time instead of serialised stale alongside the job; and a PHP enum implementing an interface so every case
is guaranteed a method, which a `match` scattered across callers cannot enforce at analysis time.

§2 (authorisation) adds points 22–27: a broadcast channel's authorisation in `routes/channels.php` as its
own real-time surface, not inherited from the HTTP route rendering the page; a `FormRequest::authorize()`
left returning `true` as the framework's one authorisation hook silently disabled rather than a harmless
placeholder; a policy method's extra parameters comparing a second model, not only the user and the primary
resource; a notification's `via()` channel needing the same already-scoped notifiable the caller was
checked against, not a fresh lookup by id; `$request->user()->cannot()` outside a controller returning a
boolean that has to be turned into an explicit throw, since nothing renders a 403 for it on its own; and a
policy method typed to require a non-null user silently denying every guest instead of deliberately
allowing one.

§10 (architecture) adds points 26–31: Laravel 12's `bootstrap/app.php` centralising what used to be spread
across kernel classes; a model's `$connection` property as the one place a multi-database app states which
store owns it, instead of a `DB::connection()` call repeated at every call site; the `/up` health-check
route as load-balancer infrastructure, not an endpoint to gate behind the app's own auth; `sticky` read-replica
routing as a deliberate global trade of replica lag for read-your-own-write correctness, not a free upgrade;
anything cached in-process being invisible to every other worker behind a load balancer; and a raw
cross-domain join for a reporting query as an undeclared dependency between two domains' schemas.

§3 (data model and schema) adds points 29–34: `HasUuids`/`HasUlids` as a primary-key generation choice with
an index-locality consequence (random UUID inserts fragmenting the index versus a time-ordered ULID
staying append-like); an explicit morph map surviving a model's later namespace move where a stored FQCN
would not; `immutable_datetime` protecting a shared model instance from being mutated in place by one
caller and read differently by another; a spatial/geography column depending on a database extension the
migration itself does not provision; `Model::preventLazyLoading()`/`preventSilentlyDiscardingAttributes()`
turning two silent defects (an N+1, a dropped mass-assigned field) into loud exceptions in development; and
`DB::transaction()`'s attempts argument as the framework's own deadlock retry, in place of a hand-written
retry loop around the same closure.

§11 (failures) adds points 29–34: `rescue()`'s fallback-and-report contract as legitimate only where point
3's "committed degraded default" already applies, never as a shortcut around a `catch` a caller needs to
react to; `Http::retry()`'s `$when` closure as what keeps it from retrying a request that will never
succeed (a 404, a 422) alongside the ones that should be retried; a job's `$backoff` releasing it back to
the queue instead of blocking the worker with an in-process sleep; `Sleep::fake()` making a retry loop's
delay testable the way `Http::fake()` already makes the network call testable; rethrowing with the caught
exception passed as `$previous`, or the tracker loses the original stack trace; and `report_if()`/`report_unless()`
keeping point 12's expected-failure condition searchable as its own tracker entry point instead of buried
inside a plain `if`.

Word counts re-measured with `wc -w` after the edits: `01-where-behaviour-lives.md` 1,907 → 2,462 (+555),
`02-authorisation.md` 2,040 → 2,578 (+538), `10-architecture.md` 2,111 → 2,662 (+551),
`03-data-model-schema.md` 2,166 → 2,703 (+537), `11-failures.md` 2,180 → 2,724 (+544).

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/`php-patterns`/
`inertia-conventions` at a different angle (idempotent retries, the prefer-the-framework's-own-mechanism
argument, the tested-refusal argument, the UTC-storage discipline) or is synthesised fresh from Laravel's
own current public documentation and PHP 8.4's release notes for the mechanism named — broadcasting channel
authorisation, form-request authorisation, policy method parameters, notification routing, the service
container and `bootstrap/app.php`, database connections and read replicas, primary-key generation
(`HasUuids`/`HasUlids`), polymorphic morph maps, immutable dates, generated/spatial columns, model strict
mode, transaction retries, `rescue()`, HTTP client retries, job backoff, `Sleep::fake()`, exception chaining,
and conditional reporting helpers — `laravel.com/docs/12.x/{broadcasting,validation,authorization,container,
database,eloquent,queues,http-client,errors}` and PHP 8.4's own asymmetric-visibility/property-hooks RFC
notes, all read 2026-09-10. The marketplace XEFI was never opened for this pass.

**Widening, 2026-09-10 — septième pass.** The five thinnest files by a fresh `wc -w` measurement —
`06-http-surface.md` (2,251), `09-tests-static-analysis.md` (2,284), `08-jobs-realtime.md` (2,292),
`04-queries.md` (2,296) and `07-configuration-commands.md` (2,316) — each gain 6–7 new points, same
extend-don't-renumber method as every prior same-day pass: nothing already numbered moved, everything new
appended after the last existing point, because the standalone `skills/laravel-*` files' `§N.M` citations
(`bin/check_citations.py`) depend on the numbering holding still.

§6 (HTTP surface) adds points 31–37: signed URLs (`URL::temporarySignedRoute()`) as the credential for a
link with no session or bearer token; a Sanctum token's own abilities (`tokenCan()`) as a narrower check
than "is this user authenticated"; `prepareForValidation()` versus `passedValidation()` as two different
moments to normalise input, not interchangeable; cursor pagination trading random page access for stability
under concurrent writes, unlike offset pagination; a resource's `wrap()`/`withoutWrapping()` decided once
for the whole API rather than per resource; `Http::retry()` bounding an outbound call's own retries,
composing with (not replacing) `Http::pool()`; and CORS as one config file rather than a header set by hand
per controller.

§9 (tests/static analysis) adds points 37–43: `Http::preventStrayRequests()` turning a forgotten
`Http::fake()` into a hard failure instead of a real network call; `Process::fake()` as the same
external-boundary rule applied to a shelled-out binary; Larastan generic collection annotations
(`Collection<int, Invoice>`) as what actually lets it check contents, not just presence; a Pest architecture
preset (`->preset()->php()/->security()`) bundling structural rules instead of hand-writing each one;
`assertOnlyJsonPath` catching an extra serialised field `assertJsonPath` alone would miss; freezing
`CarbonImmutable::setTestNow()` specifically when the codebase reads that class rather than plain `Carbon`;
and `RefreshDatabase` not covering a second database connection a command manages on its own.

§8 (jobs/realtime) adds points 30–36: a job's own `$afterCommit` property as a per-job override of the
connection-wide `after_commit` setting; `Bus::chain()->catch()` firing once for the chain, a different
signal from one job's own `failed()`; `displayName()` for a dashboard-legible name on a job class reused
across distinct payloads; `$deleteWhenMissingModels` as a deliberate "a missing subject is fine here"
statement rather than a blanket setting; a notification's `via($notifiable)` choosing channels per
recipient, not just per class; `Queue::before()`/`Queue::after()` listeners for logging or metrics across
every job from one place; and `broadcastAs()`/`broadcastWith()` decoupling the wire event name and payload
from the PHP class name and public properties.

§4 (queries) adds points 27–33: `doesntHave`/`whereDoesntHave` carrying `whereHas`'s correlated-subquery
cost for its negative case too; `firstOr(fn () => ...)` for a missing row that is a different value to
compute, not a 404; scoping `withoutGlobalScope()` to the one query that needs it rather than a model-wide
toggle; `whereBelongsTo($model)` reading a relation's own foreign/owner key instead of hardcoding it;
`simplePaginate()`/`cursorPaginate()` skipping the `COUNT` query a numbered page control needs but an
infinite-scroll UI never uses; `when()`/`unless()` for inline conditional query clauses instead of an `if`
reassigning the query variable; and `withoutTimestamps()` as a deliberate exception to a bulk write silently
skipping `updated_at`, distinct from the query-builder gap point 26 already names.

§7 (configuration/commands) adds points 34–40: a scheduled entry's `->appendOutputTo()`/`->emailOutputTo()`
as a concrete destination for point 11's "somewhere for a failure to surface"; `vendor:publish --tag=`
scoping a republish to one file group instead of overwriting everything a package can publish; `env()`'s
narrow boolean/null coercion versus a `.env` value written as `"1"`/`"0"` that never becomes an actual
boolean before `Config::boolean()`; `$this->trap(SIGTERM, ...)` letting a long-running command finish its
current unit of work instead of dying mid-write on a deploy restart; `config:show <key>` inspecting one
resolved value instead of the whole merged tree; `db:seed --class=` running one seeder in isolation without
the full `DatabaseSeeder` chain; and `make:command --command=` separating a command's PHP class name from
its artisan signature name.

Word counts re-measured with `wc -w` after the edits: `06-http-surface.md` 2,251 → 2,978 (+727),
`09-tests-static-analysis.md` 2,284 → 2,939 (+655), `08-jobs-realtime.md` 2,292 → 2,960 (+668),
`04-queries.md` 2,296 → 2,967 (+671), `07-configuration-commands.md` 2,316 → 2,930 (+614).

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/`php-patterns`
at a different angle (idempotent bulk writes, the prefer-the-framework's-own-mechanism argument, the
external-boundary-must-be-faked rule) or is synthesised fresh from Laravel's own current public
documentation for the mechanism named — signed URLs, Sanctum token abilities, form-request lifecycle hooks,
cursor pagination, JSON resource wrapping, the HTTP client's retry and CORS handling, `Http::preventStrayRequests()`
and `Process::fake()`, Larastan's generic collection typing, Pest architecture presets and JSON test
assertions, job middleware and batching (`$afterCommit`, chain `catch()`, `displayName()`,
`$deleteWhenMissingModels`), notification channel routing, queue job events, broadcast event customisation,
query-builder negatives and conditionals (`doesntHave`, `firstOr`, `withoutGlobalScope`, `whereBelongsTo`,
`simplePaginate`/`cursorPaginate`, `when()`/`unless()`, `withoutTimestamps()`), and console/scheduling
tooling (`emailOutputTo`, `vendor:publish --tag`, `env()` coercion, signal trapping, `config:show`,
`db:seed --class`, `make:command --command`) — `laravel.com/docs/12.x/{urls,sanctum,validation,pagination,
eloquent-resources,http-client,routing,queues,notifications,broadcasting,eloquent,artisan}`, all read
2026-09-10. The marketplace XEFI was never opened for this pass.

**Widening, 2026-09-10 — huitième passe.** The five thinnest files by a fresh `wc -w` measurement —
`05-naming-typing-style.md` (2,328), `01-where-behaviour-lives.md` (2,462), `02-authorisation.md` (2,578),
`10-architecture.md` (2,662) and `03-data-model-schema.md` (2,703) — each gain 6 new points, same
extend-don't-renumber method as every prior same-day pass: nothing already numbered moved, everything new
appended after the last existing point, because the standalone `skills/laravel-*` files' `§N.M` citations
(`bin/check_citations.py`) depend on the numbering holding still.

§5 (naming/typing) adds points 38–43: PHP 8.4 property hooks as the plain-PHP-class counterpart to
`Attribute::make`, and why the two are not interchangeable (one runs through Eloquent's cast pipeline, the
other works on any class); a property hook's `set` clause enforcing an invariant on every reassignment, not
only at construction; PHP 8.4 lazy objects (`newLazyGhost()`) as the language-native version of "build it on
first access," distinct from `once()`'s per-request memoisation of a callback's result; `UnitEnum::cases()`
as the single source of truth an enum's own value list, so a parallel hard-coded array drifts the moment a
case is added; the short nullable notation (`?Type`) over a two-member union for the common case; and PSR-12
as the named baseline a house style otherwise re-litigates one bracket-placement comment at a time.

§1 (where behaviour lives) adds points 28–33: a module's own routes registered from that module's own
`RouteServiceProvider` rather than appended to the app-wide routing file; a cross-module dependency bound to
an interface in a service provider instead of a concrete class from another domain; job middleware
(`WithoutOverlapping`, `RateLimited`, `ThrottlesExceptions`) as where a job's cross-cutting concerns belong,
not an `if` inside `handle()`; route middleware declared through `HasMiddleware`'s static method now that
Laravel 11 removed the controller constructor's `$this->middleware()`; `Model::unguard()` called globally
lifting mass-assignment protection for the whole request, not just the call site that needed it; and a
collection chain naming its intermediate value once a side-effecting `each()` and a transforming `map()`
would otherwise read alike in a diff.

§2 (authorisation) adds points 28–33: `scopeBindings()` as the mechanism that actually scopes a nested
resource's implicit binding to its parent, since nesting the routes alone does not; `Gate::authorize()` as
the same throw-on-denial contract a controller's `$this->authorize()` gets, usable from a command or a job
with no controller to inherit it from; `Gate::inspect()` returning the full `Response` (and its denial
message) where `can()`/`cannot()` collapse it to a boolean; password confirmation as a session-freshness gate
distinct from the permission check itself; `Gate::any()`/`Gate::none()`/`@canany` as a named batch check
instead of a hand-rolled loop that can silently under-enumerate; and a Sanctum token's `currentAccessToken()`
returning null for a session-authenticated request, which a `tokenCan()` call has to guard against.

§10 (architecture) adds points 35–40: a module's `RouteServiceProvider` as point 5's structural enforcement
applied to routing, not the app's `bootstrap/app.php` collecting every module's routes; a cross-module
dependency bound to an interface in a provider rather than instantiated as another module's concrete class;
a local module package installed through a Composer path repository instead of copied into `vendor/` or
published to a registry too early; a shared-kernel package still being a dependency direction to declare, not
an exemption from point 1; Horizon's queue-name grouping as the only thing that actually isolates one
module's jobs from another's; and the container itself enforcing none of point 36's interface-boundary
discipline at runtime — it is a static-analysis rule to keep, not a guarantee Laravel provides for free.

§3 (data model and schema) adds points 35–40: `foreignIdFor(Model::class)` picking the referenced model's
own key type instead of always assuming `UNSIGNED BIGINT`; a unique index needing `deleted_at` folded in (or
a partial index) so a soft-deleted row stops blocking reuse of its unique value; SQLite's foreign-key pragma
needing to be turned on per connection, or a constraint violation that fails loudly elsewhere passes silently
in a SQLite test suite; `schema:dump` squashing migration history, after which a data backfill left inside an
old migration's `up()` never runs again on a fresh install; `chunkById()`/`lazyById()` anchoring pagination to
the primary key instead of `OFFSET`, which stays correct while rows are deleted mid-backfill; and a database
check constraint enforcing a cross-column invariant no second writer sharing the database can bypass, unlike
a validation rule that only protects rows written through this one application.

Word counts re-measured with `wc -w` after the edits: `05-naming-typing-style.md` 2,328 → 2,978 (+650),
`01-where-behaviour-lives.md` 2,462 → 3,056 (+594), `02-authorisation.md` 2,578 → 3,199 (+621),
`10-architecture.md` 2,662 → 3,265 (+603), `03-data-model-schema.md` 2,703 → 3,352 (+649).

Sourcing: every new point either restates a mechanism already present in `laravel-conventions`/`php-patterns`
at a different angle (the prefer-the-framework's-own-mechanism argument, the stream-don't-load-into-memory
rule, the account-for-mass-operations argument) or is synthesised fresh from Laravel's own current public
documentation and PHP 8.4's release notes for the mechanism named — service providers and routing, the
service container, queue job middleware, Sanctum, authorization (`scopeBindings`, `Gate::authorize`,
`Gate::inspect`, `Gate::any`/`none`), migrations (`foreignIdFor`), database configuration (SQLite foreign
keys), migration squashing, Eloquent chunking, Horizon queue grouping, and PHP 8.4 property hooks and lazy
objects — `laravel.com/docs/12.x/{providers,routing,queues,sanctum,authorization,migrations,database,
eloquent,horizon}`, PHP 8.4's property-hooks and lazy-objects RFCs, and PSR-12, all read 2026-09-10. The
marketplace XEFI was never opened for this pass.
