---
name: release-communication
description: Use when a change ships and someone outside the team needs to know — release notes, a changelog entry, a feature announcement, a deprecation notice, an internal heads-up. Written from the reader's side, not from the commit log.
---

# release-communication

Business layer (`business/README.md`), after step 10 of the dev pipeline. Release notes get generated
from commit messages, which is why nobody reads them: a commit log answers "what did we change", and
every reader is asking "does this affect me, and must I do something".

## When
When a change ships that someone outside the team can notice: a user-visible feature, a behaviour
change, a fix for something people reported, a deprecation, a breaking change, a migration requiring
action.

## Steps

### 1. Sort by what the reader must do
Before writing, put each item in one of three buckets, because they need different treatment:
1. **You must act** — a breaking change, a required migration, a removed feature. Goes first, always,
   with the deadline and the action.
2. **You'll notice this** — a changed behaviour, a moved control, a new feature. Say what changed and
   where.
3. **Fixed** — the thing people reported. Say what was broken in the reader's words, not "fixed
   NullPointerException in OrderService".

Anything that fits none of these buckets is internal and doesn't belong in an external note. Refactors,
dependency bumps and test additions are noise to a reader and dilute the two items that mattered.

### 2. Write each entry from the outside
1. **The subject is the reader, not the system.** "You can now export a filtered list" beats "Added
   export endpoint to the products resource".
2. **Name the screen or the thing**, using the same term the product uses (`business/ux-writing` §4.1).
   An internal module name means nothing to anyone.
3. **A fix entry says what was wrong**, so the person who hit it recognises it and knows to stop
   working around it.
4. **Don't oversell.** A note that presents every bump as a milestone stops being read, and then the
   breaking change in the middle gets missed.

### 3. Breaking changes and deprecations
1. **Announce a deprecation before removal, not with it**, and say when removal happens. See
   `skills/deprecation-migration` for the mechanics on the code side.
2. **State the migration path concretely**: from this, to that. "Please migrate" with no path is
   an instruction to go and read the source.
3. **Say what happens if they do nothing** — that's the sentence that determines whether anyone acts.
4. **Never quietly change a behaviour someone depends on.** An unannounced change is discovered as a
   bug report, and the reporter is right to be annoyed.

### 4. Keep the trail
1. **A changelog entry per shipped change, written when it ships.** Reconstructing three weeks later
   loses exactly the detail readers need, and the person who knew has moved on.
2. **Dates and versions**, so someone can tie behaviour to a version when debugging later.
3. **Never rewrite history to look tidier.** An entry that quietly disappears is worse than an awkward
   one: someone is relying on it.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the three buckets in order, entries written from
the reader's side, deprecations carrying a path and a date, and no internal-only items in an external
note.

## Guardrails
- **Never announce something not yet available**, and never in the present tense (see
  `business/product-marketing` §2.3).
- **Never bury a breaking change** in the middle of a list of improvements.
- Never include internal detail that shouldn't leave: infrastructure specifics, internal repo or
  service names, security fix detail before people have had time to update.
- **A security fix is a special case**: say enough that people update, not enough to build the exploit
  against those who haven't. If in doubt, ask whoever owns security.
- Where a company already has a release-communication owner or format, they win; this block is the
  fallback, not an override.

## Origin
Assembled from public sources: the widely used keep-a-changelog conventions (grouping by kind of
change, chronological entries, never rewriting released history) and standard deprecation-notice
practice. Written **without internal technical-writing or comms expertise**. The three-bucket ordering
by required action, and the rule that anything fitting none of them is internal noise, are ours — they
come from the observation that generated-from-commits notes are the reason nobody reads them.
