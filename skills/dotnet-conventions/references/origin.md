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

