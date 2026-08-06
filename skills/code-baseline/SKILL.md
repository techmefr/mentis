---
name: code-baseline
description: Use when writing or reviewing code in any language, for the rules that hold regardless of stack, no comments, no god classes or bag-names, a file size ceiling, domain-specific exceptions instead of generic ones, every external API behind a client we own, parsed files wrapped in typed objects, distinct domain concepts as distinct types, no ticket references or AI attribution in the code, and the test obligations on new behaviour. The floor every per-stack conventions block sits on.
---

# code-baseline

Step 6 of the pipeline (`WORKFLOW.md`), and a reading angle at `review` (8). These are the rules that don't
change with the language, so each per-stack block (`laravel-conventions`, `python-conventions`,
`react-nextjs-conventions`, `vue-nuxt-vuetify-conventions`, `dotnet-conventions`, `go-conventions`,
`java-conventions`, `flutter-conventions`, `nestjs-node-conventions`, `php-patterns`,
`typescript-patterns`) can stop restating them.

**Relation to an org skill catalogue.** Where a company ships its own cross-language rule set, it is the
authority on the numbers (its file-size ceiling, its coverage floor) and overrides this block. The thresholds
below are stated as defaults with the reason attached, so a project can move one deliberately rather than by
drift.

## When
On every code edit, in any language. Checked at `gate` (7) and `review` (8).

## Steps

### 1. Comments
1. **No comments.** The one exception is a documentation block on a function, method, class or module.
   Nothing else: no inline comment in a body, no comment above a statement, no end-of-line note, no
   commented-out code, no "why" comment.
2. The reason isn't aesthetic: a comment is the only part of the file nothing verifies, so it decays into a
   confident false statement. What the comment wanted to say goes into a name, a type, a test, or an ADR
   (`documentation-adr`).
3. **No ticket or story identifier anywhere in the code** — not in a docblock, not in a variable, method or
   test name, not as "the story" or "user story 4.2". The tracker key means nothing once the tracker moves,
   and it describes when the code was written rather than what it does. It belongs in the commit and the MR.
4. **No AI attribution**: no co-author trailer naming an assistant, no "generated with" footer in a commit or
   MR body, no authorship note in the code. The team owns the code it ships.

### 2. Size and shape
1. **A source code file stays under ~200 lines.** Past that, the edit that would push it over is the moment
   to split — not a later cleanup that never gets scheduled. This applies to code, not to data, generated
   files, or documentation.
2. **No god class, and no bag-name.** A class whose name ends in `*Service`, `*Repository`, `*Manager`,
   `*Helper`, `*Util`, `*Handler` is an invitation for unrelated methods to accumulate, because nothing in the
   name can ever be "not about that". Name the class after **what it does** — the noun of its
   responsibility — and the file stays honest by itself.
3. Both rules are symptoms-first, not metrics: the ceiling is there to make a design problem visible early.
   Splitting a 250-line file into two 125-line files that import each other's internals fixes the number and
   nothing else.

### 3. Errors
1. **Never throw a generic built-in exception with a message string** (`Exception`, `RuntimeException`,
   `Error`, `ValueError`, a bare `errors.New` at a boundary). Define a named, domain-specific exception type.
2. The reason is the caller: a generic type forces every handler to match on the message, so an
   error-handling path breaks the day someone improves the wording. A named type is a contract the compiler
   or the type checker can see.
3. An error that crosses a public boundary is part of that boundary's contract, and gets the same care as a
   return type (`python-conventions` §2 for the failures-as-values form of this).

### 4. Boundaries
1. **Every call to an external HTTP API goes through a dedicated client object we own** — never a raw
   `Http::get` / `fetch` / `axios.get` / `requests.get` at the call site. The client owns the base URL, auth,
   timeouts, retries, error mapping and response typing.
2. This is rule B in code (`CONVENTIONS.md`): the third party's breaking change hits **one file**. Scattered
   raw calls turn a provider's rename into a search-and-replace across the codebase, and each site invents
   its own timeout policy — usually none.
3. One client per external system, not one per endpoint.
4. **Anything parsed from disk or the wire is wrapped in a typed object** before use: a config file, a
   manifest, a plugin descriptor, a schema, an env payload. A class with named accessors, a struct, a
   validated model. Reaching into a raw parsed map with string keys pushes every typo to runtime and gives no
   place to state a default or a required field.
5. A payload from an untrusted boundary is validated at that boundary, not sanity-checked at each consumer.

### 5. Domain types
1. **Distinct domain concepts stay distinct types**, even when they look identical today. Two status enums
   that share four values are two enums; one shared type is the coupling you can't undo the day one side
   grows a fifth value the other must not have.
2. The same holds for models and tables: shared shape is not shared meaning
   (`laravel-conventions` §3.4, `domain-modeling`).
3. Where two concepts genuinely are one, saying so in an ADR costs one paragraph and settles it.

### 6. Tests owed by new code
Stated here because it's language-agnostic; the doctrine of *how* to test lives in `skills/tdd` and in the
testing package it points at.
1. **New behaviour ships with a test** — a function, endpoint, controller, job, listener, command, model
   event, domain rule, composable, component or page. No exceptions by language.
2. **Run the test you just wrote**, read the output, and iterate until it passes for the right reason — or
   fails for the right reason, for an expected-failure test. A generated test never executed is not a test,
   it's a claim (`WORKFLOW.md`, the default-is-failure guarantee, and `hooks/verify-gate.sh` refuses the
   claim without read evidence).
3. **The coverage bar is on the diff, not the project**: aim for ≥80% of the lines added or changed being
   exercised by a test in the same change. It works whether the project sits at 10% or 100% total coverage,
   and it can't be satisfied by tests someone else wrote years ago.

## Output / checkpoint
No separate checkpoint: this is the floor `gate` (7) and `review` (8) check on every diff. A finding here is
not a nit — each of these rules exists because its violation was expensive.

## Guardrails
These govern **new and modified** code. An existing 800-line god class with commented-out blocks stays until
someone decides to migrate it (`skills/simplify`), and that decision is its own task — silently rewriting a
file you were passing through is scope the requester didn't ask for. Never delete an existing comment that
carries knowledge nothing else records: move it to a docblock, a test name or an ADR first. Where an org rule
set is installed and its numbers differ, **its numbers win**.

## Origin
**An org skill catalogue's cross-language rule set (14 skills: no comments, no ticket references, no AI
attribution, file size limit, no god classes, no generic exceptions, external APIs behind an owned client,
parsed files as typed manifests, distinct concepts as distinct types, layered architecture, test new
features, run generated tests, diff coverage)** — rules extracted, de-identified and rewritten generically,
with everything naming an internal repository, package or channel deliberately left out (rule C). The layered
architecture rule was **not** duplicated here: it already lives in `skills/archi` and
`skills/domain-modeling`, and the per-stack blocks carry the language form of it. Mechanisms rewritten, no
copied text. Stamped 2026-08-06.
