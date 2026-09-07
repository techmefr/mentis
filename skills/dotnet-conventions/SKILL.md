---
name: dotnet-conventions
description: "Use when writing or reviewing C#/.NET: async/await with cancellation, injection and service lifetimes, the type and visibility prohibitions, authorisation, disposal, nullability, EF Core."
---

# dotnet-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of C#/.NET code. **Special status**:
like `go-conventions`, no production experience behind this file yet — content comes from the Roslyn
analyzers (`Microsoft.CodeAnalysis.NetAnalyzers`, enabled by default since .NET 5), Meziantou.Analyzer and an
org catalogue for the stack, not from real review feedback. A solid base to be confronted with the first real
.NET project, not proven doctrine.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its authorisation attribute, its allowed-package list, its
deployment targets — and overrides this block wherever the two differ. Several rules below are deliberately
strict prohibitions; they come from a real house style and are stated as such, because "allowed but rare" is
not a reviewable rule.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## When
As soon as C#/.NET code is written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Async, cancellation, threading
1. All I/O, concurrent and long-running work goes through `async`/`await` + `Task`/`Task<T>`. Raw threading
   primitives (`new Thread`, `Thread.Sleep`, `ThreadPool.QueueUserWorkItem`, `BackgroundWorker`, APM
   `Begin*`/`End*`, `Task.Factory.StartNew`) don't appear in new code.
2. An async method is named with the `Async` suffix, takes a `CancellationToken` as its **last** parameter,
   and **propagates that token to every downstream await**. A token accepted and then dropped is worse than
   no token: the signature promises cancellation the implementation doesn't deliver.
3. Never sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`): a classic deadlock on a
   synchronisation context, and it burns a thread while it waits.
4. `async void` is reserved for event handlers. Elsewhere its exceptions can't be caught and it doesn't
   compose with `await`.
5. A `Task` never awaited or stored (implicit fire-and-forget) silently swallows its exceptions. If
   fire-and-forget is genuinely wanted, it's explicit, logged, and its failure path is written down.
6. `Task.Run` is for **CPU-bound** work only — wrapping I/O in it adds a thread hop and buys nothing.
7. Independent async work composed with `Task.WhenAll`, not awaited one after another in a loop.
8. `ConfigureAwait(false)` in shared library code (CA2007); less critical on the ASP.NET Core server side
   (no synchronisation context) but worth being explicit rather than accidental.
9. `CancellationToken.None` is a real value with a real meaning — "this genuinely cannot be cancelled" —
   not a placeholder to make a signature compile.

### 2. Dependencies and logging
1. Dependencies injected **through the constructor**, as `private readonly` interface fields, written as an
   **explicit constructor** — not a primary constructor on the class header. The two look like the same
   feature but aren't: a primary-constructor parameter carries no `readonly` modifier at all and stays
   assignable from any member the moment something reads it, and there's no constructor body for a
   multi-statement guard or a computed field. (This is the opposite conclusion from PHP's constructor
   property promotion, which *is* mandatory there — a promoted PHP parameter carries `private readonly` in
   the signature itself, so it's the full property declaration; a C# header parameter carries neither.)
   **Where primary constructors stay**: `record`/`record struct` (their parameters become public init-only
   properties, not a hidden mutable capture field — the objection doesn't apply), a plain `struct`, test
   fixtures, and generated/scaffolded code. Existing primary constructors in older files stay; a new class
   follows this rule regardless of what sits next to it.
2. **Never the Service Locator** (`IServiceProvider.GetService`/`GetRequiredService`) inside a class doing
   work: it hides the dependency from the constructor, so nothing fails at composition time and everything
   fails at runtime.
3. A service depends only on a service whose lifetime is **equal to or longer than its own**. A `Scoped`
   service injected into a `Singleton` (captive dependency) freezes for the app's lifetime — a `DbContext`
   shared between concurrent requests is the canonical disaster.
4. A `Singleton` or background worker that needs a scoped service creates a scope explicitly
   (`IServiceScopeFactory`), never injects the scoped service directly.
5. Every working class injects a generic logger parameterised by itself (`ILogger<TSelf>`): the type
   parameter sets the log category, which is what lets ops filter and route logs at all.
6. Too many constructor parameters is a design signal, not a formatting problem: the class is doing several
   jobs.
7. Composition happens at the application root, in one place, not scattered across the modules being
   composed.
8. **Configuration reaches code as a typed object.** Each section is bound and validated **once** at the
   composition root, and what gets injected is the typed accessor — business code never takes the raw
   configuration abstraction and never reads a key by string. What this buys is when the failure happens: a
   misspelled or missing key becomes a boot error with the section named, instead of a null two hours into
   the first request that needed it.
9. **A log call on a per-item, per-request or per-tick path is declared, not interpolated.** Where the
   platform ships a source generator for log methods, the hot path calls a generated method and pays no
   boxing or string work when the level is disabled; the ordinary logger call stays right for a cold path.
   Everything else about logging — the injected category, the level choice, no interpolation into the
   template — is point 5 and unchanged.

### 3. Authorisation
1. **Every endpoint** — controller action, hub method, minimal-API route — carries an explicit authorisation
   declaration naming the policy it requires, alongside its HTTP verb and response declarations. Per-action
   rather than per-controller: an inherited attribute is invisible at the place a reader is looking.
2. An endpoint with no authorisation declaration is treated as a bug, not as "public by design" — public is
   also a decision that gets written down.
3. Minimal API: per-endpoint validation and filters are less visible than in classic controllers. Check they
   exist rather than assuming they're inherited from elsewhere.

### 4. Types and visibility: the prohibitions
1. **No mutable global state**: no `public`/`internal static` mutable field or property, no singleton class
   with a static `.Instance` holding mutable state, no `[ThreadStatic]`. Ambient static reads
   (`DateTime.Now`, a static current-context accessor) are injected instead — that's also what makes them
   testable.
2. **No nested class**, with no private exception: it hides a type from search and from the file layout.
   Give it its own file.
3. **No local function** doing real work or capturing the enclosing method's locals: it's a method that
   avoided being named and tested.
4. **No tuple returned across a public or internal boundary**: a tuple names no concept, carries no
   behaviour and validates nothing. Return a record.
5. **No anonymous type crossing a boundary** — returned from a non-private method, serialised into a
   response, stored in a field that outlives the method, or passed as `object`/`dynamic`. It has no name to
   reference and no contract to check.
6. **Explicit types over `var`**, and `dynamic` not at all: an explicit type keeps a diff readable without an
   IDE and surfaces an API change at the call site. `var` stays acceptable where the type is stated on the
   same line (`new`, a cast).
7. **No `unsafe`**, no pointer types, no native allocators, no reinterpret-casts. Business code has no
   reason to leave the verifiable subset.
8. **No `volatile`.** It's a memory-barrier hint, not synchronisation: it doesn't make `counter++` atomic and
   provides no mutual exclusion. Reach for the actual primitive (`lock`, `Interlocked`, a concurrent
   collection).
9. **No bitwise operators** in business code — they belong to cryptography, binary protocols and low-level
   systems work. `&`/`|` on `bool` operands is also a real bug source: they don't short-circuit, so both
   sides evaluate, side effects included.
10. Every member starts at the **most restrictive** access modifier that works (default `private`) and is
    widened one rung only when a real caller requires it. Widening a member so a test can call it is a design
    smell: test it through its public surface.
11. **Every new concrete class is `sealed` by default.** Inheritance is an explicit design decision made
    once, not a default left open "in case" — polymorphism runs through an interface, and a base class
    meant to be extended says so by being unsealed on purpose, not by omission.
12. **A data-carrying type (DTO, wire payload, command/query payload, value object) defaults to a `sealed`
    positional record**, or a `readonly record struct` for a small value type — value equality and
    immutability come from the language instead of a hand-rolled `Equals`/`GetHashCode`/mutable setters. This
    is also where a primary constructor is the right tool (point 1's carve-out): a record's parameters become
    public init-only properties, not a hidden mutable field.
13. **File-scoped namespaces** (`namespace Foo;` on its own line) on every new file, never the braced wrapper
    — one indentation level saved on every type in the file, for no loss of information.
14. **No `#region`.** It's unenforced structure nothing checks — a region can silently stop matching what's
    actually inside it after a few edits, and it invites cramming unrelated things under one folded heading
    instead of splitting the file. Split into a smaller type instead of folding it.
15. **Every enum member carries an explicit numeric value.** The implicit ordinals the compiler assigns are
    what the ORM writes into the database and what the serialiser puts on the wire, so inserting a member in
    the middle or reordering two of them silently changes the meaning of data that already exists — with no
    migration, no error and no test failing. Pinning the values costs one line per member and makes the
    reorder harmless.
16. **A member that returns a sequence declares the read-only interface**, not the concrete list or array.
    Understand what it buys before over-claiming: it is a **view, not a barrier** — the caller can't add or
    remove through it, but it is not a defensive copy. The half with no override is the other one: private
    collection state is never exposed through a mutable declared type, because that hands out a live handle
    on the object's own invariant.
17. **One casing per kind, one role suffix per type**, applied to new code and to renames you were asked to
    make. Existing names stay: renaming a public type is a contract change, never a drive-by cleanup.

### 5. Disposal, nullability, enumeration
1. An `IDisposable` created locally is disposed on **every** path, exception paths included
   (`using`/`using` declaration) — CA2000.
2. The full `Dispose(bool)` pattern with `GC.SuppressFinalize` if `IDisposable` is implemented by hand
   (CA1063): never a partial `Dispose()`.
3. Nullable Reference Types enabled across the whole project, not partially. `!` (null-forgiving) is not a
   way to silence the compiler: every use has to be justifiable.
4. A LINQ query re-enumerated several times on a deferred `IEnumerable` re-runs on every iteration:
   materialise it (`.ToList()`) if the source is expensive or has a side effect (CA1851 — known blind spots,
   so check by eye too).
5. An empty `catch {}` or a `catch (Exception) {}` with no log or rethrow swallows a real bug: never a
   silent catch.
6. **Null tested with the pattern form** (`is null` / `is not null`) rather than the equality operator, and
   the roundabout not-null spellings avoided. Preference in ordinary code, informed override accepted — with
   one place where it is not a preference at all: **inside an equality-operator body, using the equality
   operator is infinite recursion**, not a style choice.
7. **One lookup per dictionary access.** Ask for the value and the existence together when you need the
   value, use the insert-if-absent call when inserting, and keep the pure existence check for the case where
   no value is read. The double probe is the one unambiguous performance claim in this section: the
   existence check and the indexer run the same hash-and-probe, so doing both runs it twice. Never route a
   lookup through the keys or values projection — that is a linear scan wearing a lookup's clothes.
8. **Read the size from the receiver's own member** where its type exposes one, and reserve the LINQ count
   method for a sequence that genuinely has none. On a lazy sequence the question "is there anything in
   here" has its own call, which stops at the first element instead of walking the whole thing. The honest
   reason is intent, not micro-optimisation — the folklore version of this rule overstates the cost.

### 6. Data access and portability
1. `AsNoTracking()` on every read-only EF Core query: without it there's a measured cost (~2x slower at
   scale) and unwanted state tracking.
2. Middleware order checked by eye (`UseRouting`/`UseAuthentication`/`UseAuthorization`): no analyzer covers
   it, and getting it wrong fails open.
3. Cross-platform APIs by default even on a single-OS target today: `Path.Combine` over hardcoded
   separators, the framework's folder-path API over an absolute `C:\…`, a hosted `BackgroundService` over a
   Windows-only service host, the configuration abstraction over the registry. The port is cheap now and
   expensive later.
4. **Never read the ambient clock in business logic.** The local-time properties answer according to the
   host machine's timezone and DST state, so the same code gives one result on a developer's box and another
   in a UTC container — a correctness bug, not a style point. A class built by the container takes the
   platform's time abstraction as a dependency; that is also what makes "expires in 30 days" testable
   without waiting.
5. **State the culture and the comparison instead of inheriting the ambient one.** Two halves of one
   boundary, not a rule with a footnote: machine-facing text — identifiers, keys, wire and file formats —
   parses and formats with the invariant culture and compares **ordinally**; human-facing text parses,
   formats and sorts with the current culture, chosen deliberately rather than by omission. The
   invariant-culture *comparison* is never the answer to either: it is linguistic collation with a frozen
   locale, which is not ordinal.

### 7. Language idioms
Preferences rather than prohibitions, all four: propose the form below, accept an informed override, and
never rewrite existing code to them unprompted (`code-baseline` §0).
1. **Test and bind in one step.** A type pattern that checks and names the value at once, rather than a
   conversion followed by a null check, an existence test followed by a separate cast, or a runtime
   type comparison. Multi-field conditions fold into property and relational patterns instead of a chain of
   member accesses that each have to be re-read for null.
2. **The expression form of a `switch` when every arm yields a value** — every branch assigning the same
   local, or every branch returning. Keep the statement form when the branches do work: an expression whose
   arms have side effects is harder to read than the statement it replaced, not easier.
3. **A collection expression where the target type is written on the left.** The spread form is an opt-in
   rewrite rather than a default, because it changes *when* the sources are enumerated — which matters for a
   lazy or side-effecting source, and for nothing else.
4. **Arguments guarded at the top of the method**, through the platform's own throw-if helpers where they
   exist: the argument-exception family is the framework's vocabulary for "the caller passed something
   wrong", and a hand-rolled check throws the wrong type. Where a guard is still written by hand, the
   parameter is named symbolically rather than as a typed string. And **never turn a literal that is
   *data* — a wire field, a config key, a policy name — into a symbol reference just because it happens to
   match an identifier today**: the day the identifier is renamed, the data silently changes with it.

## Output / checkpoint
Code compliant with the sections above, and a build with no new
`Microsoft.CodeAnalysis.NetAnalyzers`/Meziantou warning introduced by the diff. Checked by `gate` (7) and
`review` (8).

## Guardrails
**Analyser configuration is a requirement, not advice.** Detect what the project has configured on the first
edit and write code that already passes it, rather than introducing findings someone else clears; its
baseline is not a licence to add to the baseline. Then **build what you touched and iterate to zero new
warnings before reporting the work done** — the second half is the one that gets skipped, and an unbuilt
claim is exactly what the pipeline's default-is-failure guarantee exists to catch (`WORKFLOW.md` §3).

No comments in the code produced. This block hasn't been confronted with a real production .NET project yet;
if a rule here diverges from a real observed need, fix this block rather than treating it as settled. The
Framework Design Guidelines (public API naming) only apply to shared library code, not to internal
application code. Existing threading, existing `var`, existing nested classes stay until migrated — these
rules govern **new** code, and a mass rewrite is its own decision (`skills/simplify`, not this block). Where
an org catalogue is installed and disagrees, **it wins**.

## Origin
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
