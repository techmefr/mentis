# release-notes-writing-pitfalls §3 — Tier, gate and note files

How much announcement a release earns, what must be true before the notes go out, and where the notes
should have been written in the first place.

## 3.1 Tier by reader impact
1. **Set the tier by expected reader impact, never by engineering effort.** A quarter of work nobody can see is
   the lowest tier; a one-line default change that breaks callers is a high one. Ranking by effort
   under-announces exactly the cheap changes that break people.
2. **Four tiers in the source**: a new product (a launch, owned elsewhere); a noticeable impact on most users or
   one that requires user action (changelog, release body, hosted page, email, in-product note); a noticeable
   impact on some users with no action needed (changelog, release body, hosted page); no noticeable impact for
   most (changelog and release body only). The tier definitions follow a published company handbook the source
   cites and that we did not read; the surface lists are the source's adaptation.
3. **User action required promotes the in-product note and the email.** A breaking change nobody read about is
   discovered as an outage.
4. **Delete the surfaces you cannot staff** and say which; an email list you do not have is not carried
   release after release.

## 3.2 Verification gate
Four checks before the notes go out, and the rule under them:
1. **Traceability**: every entry maps to at least one commit or pull request in the range, and the claim can
   be checked in that diff.
2. **Coverage**: every consumer-observable change has an entry or a listed exclusion; show the exclusion list,
   never drop silently. The source's 100 percent bars are its own targets; where "consumer-observable" is
   contested, record where you drew the line.
3. **No number without a measurement**: delete the number rather than estimate it.
4. **Breaking completeness**: every breaking entry carries what breaks, who is hit and what to do, and a link
   when one exists.
5. **The reviewable unit is the claim-to-diff mapping.** Tone, order and grouping are cheap to fix after
   publication; a sentence describing a change the code did not make is not. A review that does not put the
   diff next to the sentence checks nothing.

## 3.3 Keep one note per change with the code
1. **When many contributors write notes, keep each entry as a small file in the same patch as the code.**
   Entries written at release time are reconstructed from memory, weeks after the change.
2. **Recommend it once**, rather than at every release.

## 3.4 Hand off
1. **Name what still needs a human**: an unmeasured performance number, a missing migration guide, a security
   entry that needs an advisory reference.
2. **Two readers, two versions.** When one release serves integrators and end users, write the integrator
   version first (complete, with the breaking set at the top) and derive the user-facing one from it.

## 3.5 Verify
Pick three entries at random and open the diff each one points to. If one of them does not show what the
sentence says, the gate has not been run.
