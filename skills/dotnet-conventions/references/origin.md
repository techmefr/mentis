# dotnet-conventions — origin and source stamps

> Provenance of `skills/dotnet-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Ideas taken from: the `Microsoft.CodeAnalysis.NetAnalyzers` Roslyn analyzers (CA2007, CA1849, CA2000, CA1063,
CA1851 cited); Meziantou.Analyzer (async/disposal/culture-invariance); the EF Core documentation (tracking vs
no-tracking); the "captive dependency" pattern documented by the .NET community; **an org skill catalogue for
this stack (15 skills: async/await with cancellation propagation, constructor injection, logger injection,
cross-platform APIs, restrictive access, explicit types, and the prohibitions on globals, nested classes,
local functions, tuple returns, anonymous types, unsafe, volatile and bitwise, plus per-endpoint
authorisation)** — rules extracted, de-identified and rewritten generically, with the internal attribute and
package names deliberately left out (rule C). Mechanisms rewritten, no copied text. Stamped 2026-08-06.

**Bodies pass 2026-09-07.** The org catalogue for this stack has gone from the 15 skills above to 37, and
this pass re-diffed all 37 against §1–§6. 22 were already covered. What was not, and is now: the typed
options binding and source-generated logging on hot paths (§2.8–§2.9); explicit enum values, the read-only
return interface with its view-not-a-barrier caveat, and the casing/suffix rule (§4.15–§4.17); the pattern
form of a null test with its equality-operator mandate, one lookup per dictionary access, and reading the
size from the receiver (§5.6–§5.8); the ambient clock and the culture/comparison boundary (§6.4–§6.5); a new
**§7** for the four language idioms (type patterns, the expression form of a switch, collection expressions,
argument guards); and the analyser guardrail, whose second half — build what you touched and iterate to zero
before claiming done — is the half that gets skipped. Left out under rule C: the house `.NET`/`C#` version
baseline (the rules are stated as "where the language version supports it"), the internal analyser package
and attribute names. Two source rules were folded rather than added, because they were already implied:
restrictive access by default (§4.10) and the no-primary-constructor conclusion (§2.1), which this catalogue
states as its own skill and which this block had already reached with the fuller PHP contrast.

**Sectioned and deepened 2026-09-08**, closing the depth programme. The block was a single `SKILL.md` of
3,167 rules words carrying its seven sections inline; they moved to one file each under `references/` with a
router table in `SKILL.md`. Every section number and every point number was preserved. No section was added:
unlike the other single-file blocks, the seven here already covered the subject — what they lacked was the
mechanism and the consequence behind each rule, which for a block with no production experience is the part
that lets a reader judge whether a rule applies to their case.

This block had the worst ratio in the table by a distance (x17.91) and it was deliberately left for last,
for a reason that has not changed: **depth is not dogfooding**. Nobody here writes C#, so a thicker block is
still unconfronted, and its status stays 🟡. What the pass does buy is that the rules now say *why*, which is
what `theoden` needs in order to read them as questions rather than as assertions.

**Widening, 2026-09-10 — huitième pass.** Still the worst ratio in the catalogue; five files touched, chosen
as the thinnest remaining after seven earlier widening passes: `01-async-cancellation.md`,
`04-types-and-visibility.md`, `06-data-access-portability.md`, `07-language-idioms.md`,
`08-resilience-throttling.md`. New points appended after the existing ones in each file, none renumbered.
Sourcing: cross-checked against the file's own existing coverage to avoid restating a point already made, then
synthesised from the C# 14 / .NET 10 and EF Core 9–10 language and library docs (Microsoft Learn's "What's new
in C# 14" and EF Core 9/10 "what's new" pages, the `dotnet/runtime` and `dotnet/efcore` repositories and issue
trackers) — never from the marketplace XEFI. New material: null-conditional assignment, partial
constructors/events, lambda parameter modifiers, unbound-generic `nameof`, widened `Span<T>` conversions,
user-defined compound assignment operators, and EF Core 10's `LeftJoin`/`RightJoin` operators (§7); partial-type
sealed/abstract propagation, interceptors, `UnsafeAccessorAttribute`/`UnsafeAccessorType`,
`DynamicallyAccessedMembersAttribute`, and sealed-class devirtualisation (§4); `AsNoTrackingWithIdentityResolution`
against JSON columns, JSON-aware `ExecuteUpdateAsync`, its new plain-lambda overload, complex-type column
uniquification, automatic compiled-model detection, and querying into a JSON column's own structure (§6); rate
limiter algorithm trade-offs (fixed/sliding window, token bucket), chaos-strategy placement in a pipeline,
`TimeProvider`-driven pipeline testing, `SlidingWindowRateLimiter` memory cost, and `RateLimitLease` metadata
(§8); `TimeProvider` overloads on `Task.Delay`/`Task.WaitAsync`/`CancellationTokenSource`, `System.Threading.Lock`
scope versus scheduling, `Task.Factory.StartNew`'s unwrap and `LongRunning` gaps, and the `DisposeAsyncCore` seam
(§1).

Where the depth went. §3 authorisation was the thinnest section relative to what can go wrong in it (95
words) and gained the most: authentication answering only "who" so a bare authorise marker admits every
authenticated user; an endpoint policy never being row-level authorisation, so the id in the route belongs
to somebody; a **default-deny fallback policy** being what makes "an endpoint with no declaration is a bug"
enforceable rather than aspirational; the allow-anonymous marker overriding even that, which makes it the
most consequential attribute in the codebase and the one most often added while debugging; claims being
input whose trustworthiness is that of their issuer; a queue consumer or webhook receiver not being reached
by HTTP middleware at all; and the negative test being the only one that proves a policy is wired.

§1 gained the cancellation half the original stated as signatures only: cancellation arriving as an
exception that a broad catch turns into a false incident, cancellation being cooperative so a CPU loop has
to check the token, the request's token dying with the request and therefore being wrong for work that must
outlive it, `Task.WhenAll` reporting one exception and hiding the rest, a `WhenAll` over an uncontrolled
collection being unbounded parallelism, a timeout cancelling the caller's waiting rather than the remote
work (so a retry can duplicate the effect), and `await` inside a `lock` being impossible rather than
inadvisable. §2 gained the container's own failure modes: a registration verified at resolve rather than at
build, which the host can be told to validate at startup; a disposable resolved from the root provider
being held until the process ends; last-registration-wins versus try-add; and the two logging rules that
cost money when broken — interpolating destroys the structured fields that are the whole reason for a log
aggregator, and a logged secret or body travels to a system with different retention and a different access
list. §5 gained disposing only what you own, the shared HTTP client as that rule in both directions,
`await using` for an async resource, nullable annotations being compile-time only so deserialised data
ignores them, and `default(T)` bypassing a struct's own constructor. §6 gained N+1 and the projection that
fixes it, knowing which half of a query runs on the server, reading a generated migration before committing
it, the `DbContext` not being thread-safe, `SaveChanges` being the transaction boundary (the same rule as
`skills/design-patterns` §4.7), connection resiliency constraining a manual transaction, and storing an
instant with its offset. §7 gained `required` members, raw string literals, `with` being a shallow copy, and
a `switch` expression throwing at run time for an unlisted value — which is right for an internal value and
wrong for one that arrives from outside.

Router plus sections: 3,167 → 6,976, x17.91 → x8.13 — still the worst ratio in the table, and still
the row whose 🟡 depth cannot move.

**Dogfooded once, 2026-09-09.** A small .NET 9 solution was written against this block as its only
reference — one console project and one xunit project, `EnableNETAnalyzers` on, `AnalysisLevel` at
`latest-recommended`, `TreatWarningsAsErrors` on, which is what the guardrail's zero-new-warning rule
actually means in practice. It checks that every `§N.M` citation in a `mentis` clone resolves to a section
and to a point inside it: 1,260 citations across 84 blocks. 36 tests green, run on the
`mcr.microsoft.com/dotnet/sdk:9.0` image with nothing installed on the host. It lives outside this repo,
with its findings beside it.

Five gaps came back, all closed here, and four of the five were found by the *build* rather than by
reading:

- **CA1822 turns a stateless collaborator into a static class** and the block had no position on it. A
  class written the way §2.1 asks but holding no fields trips *can be marked as static* on every method,
  which is a build failure under the guardrail — and the three ways out are not equivalent, since making
  it static takes it out of the container and un-substitutes it (§2.15).
- **`ValidateOnStart` alone validates nothing.** §2.8 asks for configuration validated once at the root;
  the validate-on-start call only runs the *registered* validations, and the data-annotations validator
  ships in a package the hosting metapackage does not bring in. A chain that reads as validated can be
  running no validation at all (§2.16).
- **§4.15 and §7.8 together did not compile.** Numbering every enum member explicitly (§4.15) leaves no
  member holding zero, and a `switch` expression over the named members is then reported as non-exhaustive
  naming `(T)0` — a build failure where warnings are errors, on exactly the arm §7.8 said was
  unnecessary for an internal value. §5.13 already stated the same fact for `default(T)` (§7.10).
- **CA1707 made 36 test names a build error**, which is the analyser-scoping decision the guardrail
  implied and never stated (guardrails).
- **`InvariantGlobalization` makes §6.5's human-facing half throw** rather than merely return a wrong
  result, and it is usually the container's decision rather than the code's. Found by a failing test
  (§6.13).

**The status still does not change.** One small console solution written by the same agent that wrote the
block is not the real .NET production project this file is waiting for, and `theoden` keeps its question
register. What the exercise bought is five mechanical defects, four of which only a compiler with
warnings-as-errors could have surfaced — and a check of this repo's own cross-references that had been
prescribed by `maintaining-blocks` §1.3 and never run.

**Widened against the current platform, 2026-09-09.** The volume gap against the org catalogue for this
stack (x8.13 at the time, its 37 skills against this block's seven sections) had already been answered
once on coverage — every one of the 37 was re-diffed on 2026-09-07 and 22 were found already covered — so
this pass asked the other question instead: what does the *platform* now do that this block says nothing
about? Checked against the vendor's own current documentation and release notes rather than against the
catalogue: the HTTP resilience guidance and its standard handler, the native-AOT and trimming pages, the
serialisation reflection-versus-source-generation page, the enumerator-cancellation reference, the
lock-object language proposal, the time-abstraction testing page, and the EF Core pages on split queries
and on the bulk update and delete statements. Two new sections and nine points came out of it, and every
one names a mechanism a reader can check rather than a version number:

- **§8, resilience and throttling** — the standard handler retries every method by default (so a `POST`
  duplicates), the four nested timeouts and what a per-attempt budget larger than the total does, jitter,
  a circuit breaker buying stability with silence, inbound limiting being middleware rather than a client
  strategy, the 503-not-429 default, and liveness against readiness. The generic half stays where it was:
  `skills/code-baseline` §4 and `skills/background-jobs-conventions`.
- **§9, what only breaks at publish** — reflection-based serialisation disabled in a trimmed or AOT
  publish (an exception at the first request, not a build failure), trimming removing what it cannot see,
  the publish warnings as the review surface, the empty assembly location under single-file, and running
  one smoke test against the published artefact.
- **§1.17–§1.18** — an async iterator's token needing the enumerator-cancellation annotation or the
  consumer's cancellation reaches nothing, and the dedicated lock type choosing its behaviour by the
  static type, so assigning it to `object` silently reverts to monitor semantics.
- **§2.17–§2.18** — keyed registrations as the answer to two implementations of one interface (the
  alternatives being the service locator again, or injecting them all), and the three options interfaces
  being three lifetimes, so a snapshot in a singleton is §2.11's captive dependency with no symptoms.
- **§3.13** — a cross-origin policy is not authorisation; what it does decide is whether another site can
  read an authenticated response, which is why any-origin with credentials is refused at run time.
- **§6.14–§6.16** — two collection includes multiplying the rows and split queries paying for it with
  round trips and no transaction, a bulk update or delete bypassing the change tracker *and the global
  query filters* (soft delete included), and raw SQL's two forms differing by one character and by a
  vulnerability class. §6.4 gained the platform's own time abstraction and its controllable fake.
- **§7.11–§7.12** — the backing-field keyword and its two traps, and extension members belonging to
  foreign types only, never as a hiding place for a dependency.

Ratio x8.13 → **x5.83**, and the remaining distance is now mostly implementation shape: the source
catalogue carries a code example per rule, this block carries the mechanism and the consequence. The
status is unchanged and for the unchanged reason — nobody here writes C# on a real project.

**Widening, 2026-09-09 — §9 gained three points.** csharp had the worst measured ratio in the table
(x5.83), so the thinnest section (§9, 441 words) was checked against current public Native AOT and
trimming guidance (Microsoft Learn's Native AOT deployment overview, the .NET Blog's AOT-compatible-
libraries guidance, and community documentation of common AOT/trimming pitfalls) for gaps the existing
five points did not cover: a suppressed publish warning removing the only signal a bug hadn't been
found yet rather than removing the bug (§9.6); Native AOT's inability to generate code at run time
being a categorically different failure from trimming, since a dynamic proxy or a runtime expression
compiler has nothing to fall back to and never worked to begin with, checked before adoption rather
than discovered in the published binary (§9.7); and a third-party package's trim/AOT compatibility
being read from the publish warnings, not assumed from its passing local tests (§9.8). §9 441 → 812
words.

**Widening, 2026-09-09 — §8 gained two points.** Still the worst ratio (x5.7 at the start of this
pass), so the next-thinnest section (§8, 591 words) was checked against current public guidance on
`Microsoft.Extensions.Http.Resilience` and ASP.NET Core rate limiting (Microsoft Learn's HTTP
resilience patterns page and rate-limiting middleware page): stacking more than one resilience
handler on the same client makes the total retry/timeout behaviour unreadable from the registration,
since it lives in whichever handler ran last (§8.8); and outbound rate limiting against a dependency
needs its own strategy distinct from inbound throttling, with a token-bucket-style limiter tolerating
a natural burst where a fixed-window one either starves it or lets one straddle the window boundary
(§8.9). §8 591 → 763 words.

**Widening, 2026-09-09 — §5 and §3 each gained points.** Still worst ratio, continuing down the
thinnest-section list. §5 gained the `DisposeAsyncCore` split for a type owning several async
resources rather than exposing two dispose entry points (§5.14), a double dispose needing to be a
guarded no-op rather than a second failure (§5.15), and a generic type parameter's nullability
needing its own constraint rather than inheriting the caller's (§5.16). §3 gained a custom
`IAuthorizationHandler` that calls `Succeed` unconditionally short-circuiting every other handler for
the same requirement, so denial has to be an explicit `Fail` (§3.14), and a real-time connection's
authorisation being checked once at the handshake, not re-validated as claims or permissions change
mid-connection (§3.15). §5 847 → 1,145 words; §3 900 → 1,090 words.

**Widening, 2026-09-10 — pass élargie.** csharp kept the worst measured ratio in the table, so this pass
widened five sections at once instead of the usual two or three — the thinnest remaining (§9, §8) plus
the two untouched since the sectioning pass (§2, §6) plus §3, checked each against a distinct gap in
current public .NET/ASP.NET Core/EF Core documentation rather than against the org catalogue (already
re-diffed 2026-09-07):

- **§9** gained the source-generated regex as the AOT-safe replacement for `RegexOptions.Compiled`'s
  runtime codegen, `RequiresUnreferencedCode`/`DynamicallyAccessedMembers` for a method's own reflection
  surfacing at its call site instead of at publish, `TrimmerRootAssembly` as an escape hatch that cancels
  trimming for the assembly it roots, Native AOT and ReadyToRun solving different problems (so enabling
  one for the other's guarantees is how this whole section arrives as a surprise), and the
  configuration-binding source generator as point 1's list-as-build-artefact trade applied to options
  binding (§9.9–§9.13). 671 → 1,233 words.
- **§8** gained wiring the standard handler's retry/break/timeout events to telemetry, inbound vs outbound
  limiters answering to different partition keys, load-shedding vs queueing limiters failing overload two
  different ways, a fallback strategy as the last layer rather than a replacement for fixing the call
  underneath it, and fault injection (a chaos strategy through the same pipeline abstraction) as the only
  way to observe that the timeout arithmetic in §8.2 actually holds (§8.10–§8.14). 738 → 1,244 words.
- **§2**, untouched since the sectioning pass, gained registering a named/typed `HttpClient` instead of
  constructing one (where §5.10's disposal rule actually starts), decorating a registered service at the
  composition root instead of a class wrapping its own dependency, a logging scope carrying a value across
  every log call in a unit of work without threading a parameter through each one, a `BackgroundService`
  whose unhandled exception takes the whole host down rather than just that worker, and cross-field
  validation as an `IValidateOptions<T>` run at the same startup point §2.16 already established
  (§2.19–§2.23). 1,488 → 1,962 words.
- **§3** gained resource-based authorisation as the second check after the endpoint policy once the row is
  loaded, a custom `IAuthorizationRequirement` for a rule that doesn't reduce to a role or claim, output
  caching a personalised response unless the cache key varies by whatever the policy depended on, a
  minimal-API endpoint filter's position in the pipeline versus middleware, and a background job carrying a
  stored identity needing re-validation at execution time rather than trusting the payload (§3.16–§3.20).
  1,048 → 1,539 words.
- **§6**, also untouched since the sectioning pass, gained a pooled `DbContext`'s own state surviving the
  pool's reset and leaking across requests, `AsSplitQuery`/`AsSingleQuery` as a per-query override of the
  global split-query default, a `SaveChangesInterceptor` as the one place a cross-cutting write concern
  belongs instead of copied into every call site, a filtered/ordered `Include` doing in the query what §6.6
  already argues for doing there, and a compiled EF Core model trading a startup cost for a per-request one
  (relevant to §9's Native AOT case). 1,296 → 1,787 words.

Sourced from current Microsoft Learn and vendor documentation only, per this file's rule C: the .NET
`GeneratedRegex`/trimmer-annotation and Native-AOT-vs-ReadyToRun pages, the configuration-binding
source-generator docs, `Microsoft.Extensions.Http.Resilience`'s telemetry and chaos-engineering pages, the
rate-limiting middleware's partition-key guidance, ASP.NET Core's minimal-API filters and output-caching
pages, and the EF Core pages on context pooling, split queries, `SaveChangesInterceptor`, filtered includes
and compiled models. No org catalogue file was read for this pass.

**Widening, 2026-09-10 — §7, §1 and §4 gained points.** csharp still carries the worst measured
ratio, so this pass took the three thinnest sections (§7, §1, §4) rather than one, and checked each
against a gap the existing points didn't already name — not against the org catalogue (already
re-diffed 2026-09-07) but against current public C# language and BCL documentation (Microsoft Learn's
C# 11/12/13 "what's new" pages, the `nameof`-scope, checked-operators and list-pattern feature
specs, the `CancellationTokenSource` and `ValueTask` API docs, and the static-abstract-members /
generic-math preview and release documentation). §7 gained `nameof`'s extended scope for a name that
must track its declaration, list patterns for a shape check instead of a length-then-index pair, the
`u8` literal for wire-level byte constants, `global using` and its dependency-visibility trade, and a
`params` parameter typed as a collection rather than only an array (§7.13–§7.17). §1 gained linked
token sources for combining a caller's token with a local timeout, `ValueTask`'s single-consumption
rule, `AsyncLocal<T>`'s one-way flow into a child `await`/`Task.Run` and never back, and
`IProgress<T>` capturing its synchronisation context at construction rather than at the call that
reports (§1.19–§1.22). §4 gained the `file` access modifier as a narrower scope than nested classes
without their search cost, `readonly struct` removing the defensive copy an `in` parameter otherwise
pays for silently, static abstract interface members for a numeric algorithm shared across types with
no boxing, and partial properties pairing a generated backing implementation with a hand-written
declaration (§4.18–§4.21). §7 1,041 → ~1,760 words; §1 1,102 → ~1,780 words; §4 1,139 → ~1,850 words.

**Widening, 2026-09-10 — troisième pass.** csharp still had the worst measured ratio in the table, so
this pass took the five thinnest reference files by raw word count (§5, §9, §8, §1, §3) rather than the
usual two or three, each checked against a gap not already covered — not against the org catalogue
(already re-diffed 2026-09-07) but against current Microsoft Learn / .NET Blog / dotnet-runtime
documentation for that section's own topic:

- **§5** (disposal, nullability, enumeration) gained `ArgumentNullException.ThrowIfNull` next to a
  null-forgiving operator as a contradiction rather than belt-and-braces, `await foreach`'s implicit
  `DisposeAsync` on an early `break`/`return`, `SafeHandle` versus a raw `IntPtr` finalizer race,
  `Nullable<T>` inside a zero-initialised struct colliding as dictionary keys, a mutating source making
  re-enumeration silently see less rather than repeat the same work, and `ConditionalWeakTable<TKey,
  TValue>` versus a plain dictionary keyed by reference (§5.17–§5.22). 1,027 → 1,629 words.
- **§9** (publish-time failures) gained `InvariantGlobalization` silently changing comparison/casing
  behaviour instead of throwing, constructing a named culture throwing only once that mode is on and
  only at the call site, Native AOT's lack of COM/WinRT interop support as a third invisible-until-publish
  gap, a source generator quietly absent from one build configuration reverting silently to reflection,
  and `PublishReadyToRun`'s same-RID restriction producing IL-only output with no build error
  (§9.14–§9.18). 1,233 → 1,734 words.
- **§8** (resilience and throttling) gained the in-memory rate limiter's counters not surviving a scale-out
  (needing a shared/Redis-backed store), an unbounded caller-supplied partition key as its own DoS surface,
  `SocketsHttpHandler.PooledConnectionLifetime` for DNS/failover staleness on pooled connections, a hedging
  strategy's duplication risk versus a retry's, and a concurrency (bulkhead) limiter versus a rate limiter
  versus graceful shutdown as server-side resilience (§8.15–§8.20). 1,244 → 1,903 words.
- **§1** (async, cancellation, threading) gained thread-pool starvation as a queue-length problem
  masquerading as a slow dependency, `Parallel.ForEachAsync` as the built-in bounded-parallelism API,
  `TaskCompletionSource` without `RunContinuationsAsynchronously` running continuations inline on the
  setting thread, `PeriodicTimer` awaited in a loop versus the older timer's overlapping-tick risk, and
  why a synchronisation context turns `.Result` into a deadlock in some hosts and a mere wasted thread in
  others (§1.23–§1.27). 1,472 → 2,000 words.
- **§3** (authorisation) gained `IClaimsTransformation`'s execution point and per-request cost, a scope
  claim answering a different question than a role claim, the On-Behalf-Of flow versus forwarding the
  inbound token to a downstream API, a GraphQL field resolver as its own entry point independent of the
  root query, and a Blazor/SPA `AuthenticationStateProvider`'s cached state going stale independently of
  the server-side check (§3.21–§3.25). 1,539 → 2,101 words.

Sourced from current Microsoft Learn and the .NET Blog only, per this file's rule C: the
globalization-invariant-mode and ICU documentation, the Native AOT interop-limitations and
`PublishReadyToRun` restrictions pages, the .NET 9 networking blog post on
`SocketsHttpHandler`/`HttpClientFactory` pooled-connection defaults, the ASP.NET Core rate-limiting
middleware and partitioning guidance, the thread pool and `Parallel.ForEachAsync`/`PeriodicTimer` API
docs, and the ASP.NET Core claims-transformation and resource-based-authorisation pages. No org
catalogue file was read for this pass. References total (excluding this file): 16,571 → ~19,423 words.

**Widening, 2026-09-10 — quatrième pass.** csharp still had the worst measured ratio in the table, so
this pass again took the five thinnest reference files by raw word count — §4, §7, §5, §9, §6, each
a second or third pass — checked against a gap not already covered, not against the org catalogue
(already re-diffed 2026-09-07) but against current Microsoft Learn / .NET Blog / dotnet-runtime and
dotnet-docs documentation for that file's own topic:

- **§4** (types and visibility) gained a `ref struct` implementing an interface or flowing through a
  generic method under C# 13's `allows ref struct` constraint without losing its ordinary restrictions,
  a discriminated union as a sealed hierarchy of sealed records rather than an enum with a bolted-on
  payload field, `protected internal` (union) versus `private protected` (intersection) as two different
  accessibility sets, an implicit/explicit conversion operator's information-loss test, an operator
  overload reserved for a type with one unambiguous mathematical meaning, and generic variance (`in`/`out`)
  declared only where every member of the interface actually respects it (§4.22–§4.27).
- **§7** (language idioms) gained the index/range operators over hand-computed offsets, a `using`
  declaration over the braced form, a target-typed conditional expression, a primary constructor's
  parameters read directly rather than re-copied into a parallel field, the `ArgumentOutOfRangeException`
  numeric guard family, and a target-typed `new()` for a collection whose type the left-hand side already
  states (§7.18–§7.23).
- **§5** (disposal, nullability, enumeration) gained `[EnumeratorCancellation]` as the only way an
  `IAsyncEnumerable<T>` iterator actually receives the caller's token, a linked `CancellationTokenSource`
  needing its own disposal distinct from the tokens it links, the pattern form (`is { } bound`) over a bare
  `.Value` access on a nullable value type, an object pool's `Return` path resetting every accumulated
  field or leaking state across unrelated callers, and a third-party package's incomplete nullable
  annotations suppressed narrowly rather than through a project-wide `#nullable disable` (§5.23–§5.27).
- **§9** (publish-time failures) gained Blazor WebAssembly's partial-by-default trimmer granularity
  leaving an unannotated package whole in the bundle, an `AppContext` feature switch only shrinking the
  trimmed output when declared as a `RuntimeHostConfigurationOption` rather than flipped at runtime,
  `SatelliteResourceLanguages` trimming resource assemblies for cultures never shipped, a source generator
  reading a sibling file at compile time versus the file on disk at run time, and `DynamicDependencyAttribute`
  as the narrow, per-member alternative to rooting a whole assembly (§9.19–§9.23).
- **§6** (data access and portability) gained a concurrency token turning a lost update into a loud
  `DbUpdateConcurrencyException`, `ComplexProperty`/owned types mapping a value object without giving it
  its own table identity, a `ValueConverter` configured once in the model rather than by hand in a getter,
  keyset pagination replacing offset paging once `Skip` has to walk past what it discards, a connection
  string never checked in as the literal secret, and a keyless entity type as read-only by construction, not
  a shortcut around defining a real key (§6.22–§6.27).

Sourced from current Microsoft Learn, the .NET Blog and dotnet/runtime and dotnet/efcore documentation
only, per this file's rule C: the C# 13 `ref struct`/`allows ref struct` and params-collections pages,
the access-modifiers and operator-overloading language reference, the generic-variance (`in`/`out`)
reference, the enumerator-cancellation and `CancellationTokenSource` API docs, `ObjectPool<T>`/
`ArrayPool<T>` usage guidance, Blazor WebAssembly's trimmer-configuration page, the
`RuntimeHostConfigurationOption`/feature-switch and `SatelliteResourceLanguages` MSBuild references,
`DynamicDependencyAttribute`'s API docs, and the EF Core pages on concurrency tokens, complex/owned
types, value conversions, and keyless entity types. No org catalogue file was read for this pass.
References total (excluding this file): ~19,423 → ~22,456 words.

**Widening, 2026-09-10 — cinquième pass.** csharp still carried the worst measured ratio in the table, so
this pass took the five thinnest reference files by raw word count (§8, §2, §1, §5, §7) — the same five
touched across the earlier passes above, now a further round — each checked against a gap not already
covered, not against the org catalogue (already re-diffed 2026-09-07) but against current Microsoft Learn
and vendor documentation for that file's own topic:

- **§8** (resilience and throttling) gained strategy-registration order deciding which one wraps which in a
  resilience pipeline builder, the pooled execution context's borrowed-for-one-call lifetime, a gRPC
  channel's own retry policy compounding with the pipeline's when both apply to the same call, a chained
  rate limiter's rejection coming from whichever limiter in the chain ran first, a pipeline built once per
  client versus rebuilt per call losing the circuit breaker's memory between calls, an unnamed pipeline's
  telemetry being indistinguishable from another one, and a cancellation token forwarded into pipeline
  execution stopping the whole retry loop rather than only the in-flight attempt (§8.21–§8.27).
- **§2** (dependencies and logging) gained `PostConfigure` running after every `Configure`/binding call
  regardless of registration order, `ServiceProviderOptions.ValidateOnBuild` defaulting on only in
  Development, `ActivatorUtilities.CreateInstance` as constructor injection that still bypasses the
  composition root, log-then-rethrow producing two records of one failure, `IServiceProviderIsService` as
  the registration check that doesn't resolve, a distributed trace's own identifiers replacing a
  hand-rolled correlation id, and last-registration-wins applying to a keyed registration the same as an
  unkeyed one (§2.24–§2.30).
- **§1** (async, cancellation, threading) gained a bounded `Channel<T>`'s backpressure versus an unbounded
  one deferring the same failure to memory, `Task.Yield` forcing a scheduler hop a completed-task await
  would not, `SemaphoreSlim.WaitAsync`'s timeout overload as the way out of an indefinite wait,
  `IHostedService.StartAsync` blocking the whole host's readiness when long-running work belongs in
  `ExecuteAsync` instead, an unawaited task racing whatever the caller does next regardless of how properly
  it was logged, and `CancelAfter`'s timer living as long as the token source that scheduled it
  (§1.28–§1.33).
- **§5** (disposal, nullability, enumeration) gained dependency-ordered disposal for hand-torn-down fields
  where nested `using` gives that for free, `WeakReference<T>`/`TryGetTarget` as a cache mechanism rather
  than a substitute for deterministic release, a boxed struct enumerator behind an interface-typed `foreach`,
  `GC.SuppressFinalize` called from the public `Dispose()` rather than from the shared protected method,
  `IMemoryOwner<T>`'s rented buffer being reused by the next renter the instant it's disposed, and a settable
  record property breaking the value-semantics guarantee `with` depends on (§5.28–§5.33).
- **§7** (language idioms) gained a custom interpolated string handler for a conditionally-run formatted
  string, `checked` arithmetic for a calculation where overflow is a bug rather than the algorithm,
  `StringSyntaxAttribute` for editor awareness of an embedded language with no run-time effect, extended
  property patterns nesting a member access with its null guard built in, tuple deconstruction in a `foreach`
  header, `in` parameters reserved for a struct actually too large to pass by value, and a discard stating a
  position was considered and deliberately ignored (§7.24–§7.30).

Sourced from current Microsoft Learn, the .NET Blog, the Polly documentation site and dotnet/runtime API
references only, per this file's rule C: the Polly v8 resilience-pipeline ordering and execution-context
pages, `System.Threading.Channels`'s bounded-channel and backpressure documentation, the options-pattern
`PostConfigure`/binding-order and `ServiceProviderOptions.ValidateOnBuild` reference pages,
`ActivatorUtilities` and `IServiceProviderIsService` API docs, the `IHostedService`/`BackgroundService`
lifecycle reference, `SemaphoreSlim.WaitAsync` and `CancellationTokenSource.CancelAfter` API docs,
`WeakReference<T>`/`ConditionalWeakTable` and `IMemoryOwner<T>`/`MemoryPool<T>` reference pages, and the C#
language reference on interpolated string handlers, `checked`/`unchecked`, `StringSyntaxAttribute`, extended
property patterns and `in` parameters. No org catalogue file was read for this pass.
References total (excluding this file): ~22,456 → ~26,970 words (measured below).

**Widening, 2026-09-10 — sixième pass.** csharp still carried the worst measured ratio in the table, so
this pass took the five thinnest reference files by raw word count (§3, §4, §9, §6, §8) — each checked
against a gap not already covered, not against the org catalogue (already re-diffed 2026-09-07) but
against current Microsoft Learn, the .NET Blog and the Polly documentation site for that file's own
topic:

- **§3** (authorisation) gained `IAuthorizationService.AuthorizeAsync`'s resource-taking overload as the
  declared alternative to a hand-rolled comparison after the row is loaded, a custom
  `IAuthorizationMiddlewareResultHandler` replacing the default failure handling for every endpoint rather
  than only the one it was written for, a dynamic `IAuthorizationPolicyProvider` resolving a policy name at
  evaluation time rather than at startup (so a typo fails open or allow-nothing depending on the provider),
  the `required` modifier removing the "was this ever set" question a resource-based check silently depended
  on, a step-up/MFA requirement as a second decision layered on the first rather than a stronger version of
  the same policy, and a permission claim replacing a role-name comparison so a new title is administration
  rather than a redeploy (§3.26–§3.31). 2,101 → 2,743 words.
- **§4** (types and visibility) gained the `required` modifier from the constructor side (why it can't be
  `private`), `SetsRequiredMembersAttribute` as an unverified promise, a default interface implementation
  changing behaviour for every existing implementer versus the pre-DIM breaking change it replaces, a
  `static` (non-abstract) interface member as a non-polymorphic mechanism distinct from the numeric
  static-abstract case, a `readonly` member on an otherwise-mutable struct as a per-member promise, `params`
  accepting a span under C# 13 and what that costs the parameter's own contract, and a type alias trading
  searchability for a local nickname (§4.28–§4.34). 2,146 → 2,925 words.
- **§9** (publish-time failures) gained MVC controllers being outside Native AOT's support surface entirely
  rather than a trim-warning source, the Request Delegate Generator compiling minimal-API handlers to
  source-generated code only once AOT/trimming is on, a pre-compiled EF Core query needing the same
  regenerate-on-model-change discipline as the compiled model, a size-optimised "chiseled" container image
  missing native libraries an AOT binary still calls into, and trimming-without-AOT as a third distinct
  failure profile from the trimmed+AOT and R2R cases already covered (§9.24–§9.28). 2,216 → 2,794 words.
- **§6** (data access and portability) gained a compiled query (`EF.CompileQuery`) as a narrower, hand-kept-
  in-sync optimisation distinct from the compiled model, table splitting's optional-load trade, a shadow
  property invisible to direct object access, a global query filter applying through a navigation the
  calling code never named, the command timeout versus the connection timeout as two different ceilings,
  a provider-specific relational feature (a JSON or computed column) as a portability decision spent without
  being chosen, and `SaveChanges` batching as a real round-trip-versus-blast-radius trade rather than a free
  default (§6.28–§6.34). 2,345 → 3,120 words.
- **§8** (resilience and throttling) gained the standard handler's default `Retry-After` honouring on a 429
  or 503, a hand-rolled retry loop needing its own delay generator to get the same behaviour, a health-check
  publisher as its own unthrottled outbound call one layer above the endpoint §8.7 already covers, a streamed
  response's idle timeout as a separate knob from the request timeout the arithmetic in §8.2 governs, and a
  hedge or retry against a non-idempotent stream duplicating an indeterminate prefix rather than a whole
  response (§8.28–§8.32). 2,677 → 3,273 words.

Sourced from current Microsoft Learn, the .NET Blog and the Polly/`Microsoft.Extensions.Http.Resilience`
documentation only, per this file's rule C: the resource-based and policy-provider authorization reference
pages, the `required`/`SetsRequiredMembers` and default-interface-member language reference, the C# 13
`params`-collections and `readonly` struct-member pages, the Native AOT MVC-compatibility and Request
Delegate Generator pages, the EF Core compiled-queries, table-splitting, shadow-properties and query-filter
documentation, and the `HttpStandardResilienceOptions`/`Retry-After` handling guidance. No org catalogue
file was read for this pass.
References total (excluding this file): ~26,970 → ~30,665 words (measured: `wc -w` over the nine
`0N-*.md` files, excluding this one).

**Widening, 2026-09-10 — septième pass.** csharp still carried the worst measured ratio in the table, so
this pass took the five thinnest reference files by raw word count (§1, §2, §5, §3, §9) — each checked
against a gap not already covered, not against the org catalogue (already re-diffed 2026-09-07) but
against current Microsoft Learn and the .NET Blog for that file's own topic, favouring .NET 9/10 and
C# 13/14 material specifically:

- **§1** (async, cancellation, threading) gained `Task.WhenEach` streaming completions instead of
  collecting them (the as-completed alternative to `WhenAll`/`WhenAny`), `Task.WaitAsync` timing out the
  wait without cancelling the underlying work, `ConfigureAwaitOptions`' `SuppressThrowing` flag as a
  narrow, explicit alternative to a swallowed fire-and-forget, LINQ over `IAsyncEnumerable<T>` (.NET 10)
  taking its cancellation on the operator chain rather than the source, `Lock.TryEnter`'s timeout staying
  a synchronous-only answer to the semaphore's async wait problem, and a `CancellationToken` captured in a
  closure freezing at closure-creation time rather than re-reading a field (§1.34–§1.39).
- **§2** (dependencies and logging) gained keyed `AddHttpClient` registration (.NET 9) as point 19's
  disposal rule extended to more than one client configuration, `[FromKeyedServices]` on a constructor
  parameter as the keyed-resolution path that still never touches `IServiceProvider` directly, the
  `[AllowedValues]`/`[DeniedValues]`/`[Base64String]` data-annotation attributes covering a class of
  options-validation rule that used to need a hand-written validator, `TimeProvider` as an injectable
  service making the clock substitutable in tests the same way a repository is, a `Meter`'s counters and
  histograms as the aggregation-shaped signal a log line isn't, and a logging provider's own reload-token
  subscription making a configured log level change take effect without a restart (§2.31–§2.36).
- **§5** (disposal, nullability, enumeration) gained `[MemberNotNull]`/`[MemberNotNullWhen]` letting a
  guard method narrow nullability for its caller instead of resetting flow analysis at the call site,
  `[NotNullIfNotNull]` for a pass-through method's linked nullability, C# 13's `allows ref struct`
  constraint letting a `ref struct` implement `IDisposable` and be disposed through generic code, a
  collection expression's spread element enumerating (and not disposing) its source, a `using`
  declaration's block-length scope holding a resource open longer than an equivalent nested `using`
  statement would, the `ArgumentOutOfRangeException` numeric guard family read the same way as a null
  guard, and an `init`-only property not exempting a struct from point 13's zeroed-`default` trap
  (§5.34–§5.40).
- **§3** (authorisation) gained ASP.NET Core's built-in authentication/authorisation metrics as the
  production-visible version of the negative test, cookie authentication's heuristic 401-vs-redirect split
  for API-shaped requests, a WebAuthn/passkey credential changing what "a second factor" means for a
  step-up policy, `RequireAuthorization()` chained on a group and an endpoint adding requirements rather
  than replacing them, minimal API's built-in validation filter running after authorisation rather than
  before it, and rate-limiter placement relative to authentication deciding whether it partitions by
  identity or by a shared anonymous key (§3.32–§3.37).
- **§9** (publish-time failures) gained a file-based app (.NET 10) publishing Native AOT by default so a
  script inherits this section's rules the moment it's published, packing a .NET tool as trimmed/AOT
  (.NET 10) surfacing the same failures at the packaging step rather than the code-change step, the AOT/
  trim analyzers catching more at build time without replacing the CI-must-publish rule, the .NET 9
  feature-switch attribute model stating a switch's trim behaviour next to its name, and hybrid
  globalization mode as a third point on the ICU-versus-invariant axis rather than a safer version of
  either (§9.29–§9.33).

Sourced from current Microsoft Learn and the .NET Blog only, per this file's rule C: the `Task.WhenEach`
and `Task.WaitAsync` API docs, the `ConfigureAwaitOptions` reference, the .NET 10 `System.Linq.
AsyncEnumerable` and IAsyncEnumerable-interface-change documentation, the `System.Threading.Lock`
reference, the .NET 9 keyed-`IHttpClientFactory` and `[FromKeyedServices]` documentation, the options-
validation data-annotations reference, the `TimeProvider` and `System.Diagnostics.Metrics` API docs, the
C# 13 `allows ref struct` and collection-expression language reference, the `using`-declaration scoping
and `ArgumentOutOfRangeException` guard-clause reference, the ASP.NET Core authentication/authorisation
metrics and cookie-authentication-for-APIs release notes, the ASP.NET Core Identity passkey/WebAuthn
documentation, the minimal-API validation-filter ordering page, the file-based-apps and .NET-tool-
packaging (.NET 10) publish documentation, the .NET 9 feature-switch attribute model reference, and the
hybrid-globalization-mode documentation. No org catalogue file was read for this pass.
References total (excluding this file): measured before/after via `wc -w` on the five touched files only
— §1 2,687 → 3,311, §2 2,696 → 3,320, §3 2,743 → 3,383, §5 2,741 → 3,538, §9 2,794 → 3,348 (+3,239 words
across the five). Full nine-file total (excluding this file): 29,087 words.

