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

**Boundary with the `xefi-claude-skills` plugin.** Its `design-patterns` plugin holds per-pattern
implementation skills (`state`, `strategy`, `null-object`, `object-construction`) with language-specific
references. Those answer **how** to implement one well. This block answers **whether to reach for one at
all** — and once the answer is yes, the plugin's skill for that pattern is the authority on the shape, not
this file. Two responsibilities, one boundary; don't restate their content here.

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

### 4. If you use the name, use it correctly
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

A dedup audit on 2026-08-06 found the installed `xefi-claude-skills` marketplace already ships four
per-pattern implementation skills. The boundary stated above is the resolution: they own the shape of each
pattern, this block owns the decision to use one — which none of them covers, since a skill about a pattern
assumes you've decided to use it.

What's ours: recognise-don't-apply with the second-real-case threshold, the framework-already-does-it
subtraction pass (which is where most of the catalogue goes in our stacks), Adapter/Facade justified by
containment rather than reuse, the Repository-over-ORM verdict, and wiring the whole thing to the
existing `over-abstraction`/`yagni` tags so a named pattern gets no discount at review.
