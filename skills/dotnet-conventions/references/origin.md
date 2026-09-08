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
