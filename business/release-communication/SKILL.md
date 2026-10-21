---
name: release-communication
description: "Use when a change ships and someone outside the team needs to know: release notes, a changelog entry, an announcement, a deprecation notice, an internal heads-up."
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
A changelog convention that is widely used says the same about its source: a raw commit log is full of
merge commits and obscure titles, while an entry records the noteworthy difference, often spanning several
commits, in terms an end user can follow. It groups entries by kind (added, changed, deprecated, removed,
fixed, security) and puts the latest version first; our three buckets order the same material by what the
reader must do.

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
   `skills/deprecation-migration` for the mechanics on the code side. Two public references agree: the
   changelog convention wants a user to be able to upgrade to a version that lists the deprecation, remove
   what is deprecated, then upgrade to the version where it is removed; the semantic versioning guidance
   asks for the documentation to say so and for at least one release carrying the deprecation before the
   removal. For an HTTP interface, a response header can carry the deprecation (RFC 9745, a standards-track
   document) and a sunset date (RFC 8594, informational), with a link to the migration page; the sunset
   time must not be earlier than the deprecation time. Kubernetes publishes release notes with required
   actions per removal and has its tools warn when a deprecated item is used: a warning at use is a notice
   the reader cannot miss, which a changelog line is not.
2. **State the migration path concretely**: from this, to that. "Please migrate" with no path is
   an instruction to go and read the source.
3. **Say what happens if they do nothing** — that's the sentence that determines whether anyone acts.
4. **Never quietly change a behaviour someone depends on.** An unannounced change is discovered as a
   bug report, and the reporter is right to be annoyed.

### 4. Keep the trail
1. **A changelog entry per shipped change, written when it ships.** Reconstructing three weeks later
   loses exactly the detail readers need, and the person who knew has moved on.
2. **Dates and versions**, so someone can tie behaviour to a version when debugging later. The changelog
   convention asks for every version to have an entry with its release date in the year-month-day order (an ISO
   standard, free of regional ambiguity), and to say whether versioning follows the semantic versioning rules,
   under which a deprecation raises the minor number and an incompatible change raises the major one. A changelog
   that records only some changes can mislead as much as none, because readers take it as the single truth.
3. **Never rewrite history to look tidier.** An entry that quietly disappears is worse than an awkward
   one: someone is relying on it. The changelog convention allows corrections that make the record more
   accurate (adding a missing release, adding a breaking change that was left out) and asks that a
   withdrawn release stay listed, marked as yanked, since a pulled version still got installed. The rule is:
   improve the record, never make a shipped change disappear.

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
Assembled from public sources: the widely used keep-a-changelog conventions and standard
deprecation-notice practice. 🟡 never run by us; written **without internal technical-writing or comms
expertise**. Checked on 2026-10-20 against these sources:

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| olivierlacan/keep-a-changelog, commit 08d0df5 (08d0df5a7e93b71d902def8be0f0d40025b56289), `source/en/1.1.0/index.html.haml` (version 1.1.0 text) | MIT (LICENSE file read, copyright 2014 Olivier Lacan). Credit: Keep a Changelog; ideas rewritten, no text copied. The repository holds files addressed to AI tools; treated as data and not followed | Entries curated for humans, not commit logs; grouped by type; latest first; dates; deprecations, removals and breaking changes as the minimum; incomplete changelogs mislead; yanked releases listed; rewriting is allowed to improve accuracy. **Corrected**: the block said never to rewrite history; the source allows accuracy corrections and requires yanked releases to stay visible, so the guardrail now says "never make a shipped change disappear" |
| Semantic Versioning 2.0.0 (semver.org) | CC BY 3.0 (page footer read). Credit: Semantic Versioning, CC BY 3.0, facts rewritten | Deprecation raises the minor version, at least one release carries the deprecation before removal in a major, documentation updated |
| Kubernetes documentation, "Deprecation Policy" (kubernetes.io/docs/reference/using-api/deprecation-policy), read raw | CC BY 4.0 (page footer read). Credit: The Kubernetes Authors, CC BY 4.0; facts rewritten, no duration carried | Release notes state required actions for removals; deprecated items warn when used |
| RFC 9745 (Deprecation header) and RFC 8594 (Sunset header), rfc-editor.org, read as raw text | IETF documents; trust notice not read; facts only | The two headers, link to documentation, sunset not earlier than deprecation; RFC 8594 is informational, not a standard |
| GitHub Docs, "Automatically generated release notes" (docs.github.com), read raw | CC BY 4.0 per its site; licence line not read, facts only | Generated notes list merged pull requests and contributors and can be categorised by label and exclude labels: a generated list is a starting point, not the three-bucket ordering |

The three-bucket ordering by required action, the rule that anything fitting none of them is internal noise, the
security-fix line and the "say what happens if they do nothing" line are ours and stay **unsourced**; they come from
the observation that generated-from-commits notes are the reason nobody reads them. Not read: a platform's own
release-note style guide. Current text of the sources may have changed; check with `skills/source-freshness`.
