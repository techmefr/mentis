# release-notes-writing-pitfalls §2 — Entries and breaking changes

A reader who stops after two bullets should have read the two that could break their build.

## 2.1 Write the entry from the effect
1. **State what changed, then why a reader cares, in one to three sentences.** The length is the source's
   working budget, not a published rule.
2. **Lead with the observable effect**; put the mechanism after it or drop it.
3. **Rewrite internal vocabulary into product terms**: ticket identifiers, service codenames and module names
   that outsiders never see.
4. **Stay flat and specific.** Marketing adjectives make a technical reader stop reading.

```
Weak:   Implemented a caching layer for dashboard endpoints (TICKET-123)
Better: Dashboards load faster on accounts with large workspaces.

Weak:   Revolutionary new streaming experience, rebuilt from the ground up!
Better: Add stream() to the client for token-by-token responses.
```

5. **Order within a category by consumer impact, breaking items first.**
6. **Keep one tense inside a release.** Imperative present if the project's convention requires it, past tense
   otherwise; never mix them.

## 2.2 Breaking entries have three parts
1. **What breaks**: the observable behaviour, not the internal cause.
2. **Who is hit**: the affected subset (one SDK, one setting, callers of one endpoint). "Everyone" is rarely
   true, and overusing it teaches readers to skip the marker.
3. **What to do**: one line, plus a link when the fix is longer than a rename.

```
Breaking: client.send() now rejects payloads over 1 MB instead of truncating them.
Affects callers that relied on silent truncation. Chunk the payload or catch PayloadTooLarge.
See the version 3 migration guide.
```

## 2.3 Where breaking entries go
1. **Put them first in their category**, and complete: an entry that lacks any of the three parts is not
   finished (§3.2 checks this).
2. **If the fix is longer than a rename, the note links to a migration guide and does not try to be one.**

## 2.4 Keep the version honest
1. **Major means breaking, minor means additive, patch means fixes.**
2. **A "Removed" entry in a minor release is a defect** in the notes or in the version. Say so instead of
   shipping it: readers who trust version ranges get broken silently.

## 2.5 Announce deprecations
1. **Announce a deprecation in a release that removes nothing**, naming the replacement and the earliest
   version that removes it.
2. **Reference that announcement again in the release that performs the removal.**
3. **The mechanics of the removal itself** (advisory or compulsory, the expand and contract steps) are in
   `deprecation-migration`.

## 2.6 Verify
Take the first breaking entry and ask three questions of it: what breaks, who is hit, what to do. If the answer
to any of them requires opening the code, rewrite it.
