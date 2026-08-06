---
name: design-patterns
description: Use when reaching for a named design pattern (Factory, Strategy, Observer, Repository…), or when reviewing code that has one, to check the structure earns its name — most of the classic catalogue is already provided by our frameworks, and a pattern introduced before the second real case is over-abstraction with a respectable name.
---

# design-patterns

Steps 3 (`archi`) and 6 (`code`) of the pipeline (`WORKFLOW.md`), and a reading angle during `review`.

The classic catalogue is 22 patterns across three families. Every one of them was extracted from code
that already existed: they are **names for structures people kept rediscovering**, not a menu to order
from. Read as a menu, the catalogue reliably produces the thing `over-engineering-review` tags as
`over-abstraction` — with the difference that a named pattern is harder to delete, because it looks like
a decision.

The useful skill here is subtraction. Two thirds of the catalogue is already in the framework you're
using, and naming a structure you don't have yet is how a one-caller interface gets built.

**Relation to an org skill catalogue.** Where a company ships per-pattern implementation skills with
language-specific references, those are the authority on **how** to shape each pattern in that house style.
This block owns **whether to reach for one at all**, plus the entry conditions below — the trigger that says
a given pattern is now earned. Where such a catalogue is installed, follow its shape and this block's
threshold.

## When
When about to introduce a pattern by name; when a design discussion produces one as an answer; when
reviewing code that names one; when the same shape has appeared for the third time and needs a name.

## Steps

### 1. Recognise, don't apply
1. **A pattern earns its name after the structure exists**, not before. If the code already has three
   interchangeable behaviours behind one call site, that's a Strategy — naming it helps everyone read it.
2. **If it doesn't exist yet, you're predicting.** That's `yagni` (`over-engineering-review`), and the
   pattern name is the disguise.
3. **The threshold is the second real case**, in the code, today. Not a plausible one. Same rule as
   `when-stuck`'s three-occurrence threshold for extracting an abstraction.

### 2. Check the framework doesn't already do it
This is where most of the catalogue goes. Before writing one, look for what's already there:
- **Object construction and wiring** — the DI container resolves and configures. A hand-written factory
  usually reimplements it with less capability, and a hand-written **Singleton** replaces a managed
  lifetime with a hidden global that tests can't reset.
- **Notification / decoupling** — the framework's events, listeners and queued jobs are Observer and
  Command, already instrumented and already testable.
- **Wrapping behaviour around a call** — middleware, pipelines and interceptors are Decorator, with
  ordering handled.
- **Interchangeable behaviour** — in a typed language, a map of functions or a discriminated union does
  what a Strategy class hierarchy does, in a fraction of the lines. Reach for classes when the behaviours
  carry state.
- **Iteration, state machines, templates** — generators/iterables exist; and a state machine is better
  modelled as data (`domain-modeling` §states-not-flags) than as a class per state.

**A Repository over an ORM is the recurring local case.** It pays only when there's a genuine second
implementation or a real intention to swap the store. Otherwise it's a one-caller wrapper over an API
that was already the abstraction, and it hides the query optimiser you'll want later (`tank`).

### 3. Where they do earn their place
Not a rejection of the catalogue — the cases that hold up in our stacks:
1. **Adapter and Facade at a third-party boundary.** This is rule B in code: an external API gets one
   wrapper we own, so a breaking change upstream is one file. Even here, one caller is fine — the
   justification isn't reuse, it's containment.
2. **Strategy when the branches are real and growing**, and each has its own tests.
3. **Builder when construction genuinely has many optional parts** and the alternative is a constructor
   nobody can read.
4. **Command when work must be queued, retried or audited** — usually meaning the framework's job
   abstraction (`background-jobs-conventions`).
5. **State when the transitions are the domain** and getting them wrong is the bug you're preventing.

### 4. The four with a concrete entry condition
For these, the trigger is mechanical enough to state — which is what makes them reviewable rather than a
matter of taste. Each still passes §1's second-real-case threshold first.

1. **Strategy** — a `switch`/`match` on a `type`/`channel`/`provider`/`mode`/`kind` field with **3+ branches
   that keeps growing**, or sibling classes differing only in one method. The axis of variation must be
   **one**: two axes means you're about to build a matrix, and a map of functions keyed by the pair is
   smaller. Each strategy owns its tests.
2. **State** — one object moves through **named statuses** (`pending` → `approved` → `paid` → `refunded`) and
   its behaviour shifts at each step, with the `if`/`match` on that field repeated across **several**
   methods. The trigger is the repetition, not the existence of a status field: a status read in one place is
   a status field, not a state machine. What you're really buying is that an invalid transition becomes
   unrepresentable — if the transitions don't matter, this is over-abstraction.
3. **Null Object** — the same "is this collaborator absent?" branch repeats (`if ($logger)`, `if ($user)`,
   optional constructor arguments defaulted to null, a lookup returning null for an unknown key, a
   guest/anonymous case). Substitute an instance that does nothing, so the caller stops asking. It pays when
   the branch is **repeated**; a single null check is a null check.
4. **Object construction** — the honest answer to "this constructor has too many parameters", and the
   smallest fix wins: a **parameter object** (group the ones that travel together), a **named constructor**
   (`::fromX`, a `from_x` classmethod) when there are several distinct valid ways to build the thing, a
   **readonly class / dataclass / validated model** when it's really a value, and a **fluent builder** only
   when construction genuinely has many optional parts. Reach for the builder last: it's the most code and
   the least type safety of the four.

### 5. If you use the name, use it correctly
1. **A misnamed pattern is worse than an unnamed structure.** "Factory" on something that isn't one
   sends every future reader looking for indirection that doesn't exist.
2. **Name it in the code or in the ADR, once** — not in a comment (`documentation-adr` §1.2, and no
   comments where the naming can carry it).
3. **When a pattern is deliberately not used**, and someone will wonder why, that's a line in the ADR
   (`documentation-adr` §4).

## Output / checkpoint
No separate checkpoint: this feeds `archi`, `code` and `review`. What it owes at review time — for every
named pattern in the diff, the second real case exists, the framework doesn't already provide it, and the
structure is smaller with the pattern than without. Failing any of the three, it's a
`simplify` candidate.

## Guardrails
- **Never introduce a pattern before the second real case.** "We'll need it" is the whole failure mode.
- **Never hand-roll what the container, the event bus or the middleware stack already does.**
- **Apply the net-line test** (`over-engineering-review`): if the pattern adds lines and removes none,
  it bought nothing today.
- **Never let a pattern name end a design discussion.** It's a label for an answer, not the answer.
- Don't refactor working code purely to make it match a pattern.

## Origin
The catalogue itself is the classic Gang of Four set as published on the widely used
`refactoring.guru` reference — 5 creational, 7 structural, 10 behavioural patterns, verified 2026-08-06.
Its catalogue pages describe when each pattern applies and carry **no caution about overuse**, which is
the gap this block exists to fill: taken at face value, a catalogue is read as a menu.

Section 4's entry conditions come from **an org skill catalogue's four per-pattern skills** (state, strategy,
null object, object construction), extracted and rewritten generically: their triggers are precise and
worth owning here, while their language-specific implementation references stay with them (rule C — nothing
naming an internal library or project crossed over). Where that catalogue is installed it remains the
authority on the shape; this block keeps the decision and the trigger, which a skill about a pattern can't
cover, since it assumes you've already decided to use it.

What's ours: recognise-don't-apply with the second-real-case threshold, the framework-already-does-it
subtraction pass (which is where most of the catalogue goes in our stacks), Adapter/Facade justified by
containment rather than reuse, the Repository-over-ORM verdict, and wiring the whole thing to the
existing `over-abstraction`/`yagni` tags so a named pattern gets no discount at review.
