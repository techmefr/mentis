# oss-compliance-programme §2 — Evidence per release

> Section 2 of `skills/oss-compliance-programme`. Read it when the question is what can be shown for a given
> release. Source: `Example-Generic-Company-Policy-Text.md` of the OpenChain Reference-Material repository
> (commit `e79a0b7`), re-read 2026-10-16. Periods in square brackets in the source are placeholders and are
> not carried. Sentences marked "own guidance" are ours.

1. **Keep a decision log.** Every decision about an open-source component is written down with its background,
   the decision, the date, who asked and who decided. The source keeps it in a ticketing system; the medium is
   your choice, the five fields are the point.
2. **Cross-reference the log to releases.** Each entry points to the release or releases it concerned, so that
   the entries for one release can be pulled out and shown as proof that the process ran. The log is reviewed
   at a fixed interval and entries about code no longer in use are flagged; what happens to flagged entries
   (archive, anonymise, delete) and when is a retention decision for the owner and counsel, because the
   source's figures are placeholders (own guidance).
3. **Produce a component list for every released version.** The source asks for a bill of materials that
   accompanies each version of the software, in a standard exchange format such as SPDX, made as part of
   producing the release. A list written afterwards from memory is not evidence. Generating it from the build
   is the way to make it happen every time (own guidance).
4. **Assemble a compliance bundle per release.** For each component, the source gathers the artifacts that its
   licence calls for: source code where required, attribution and copyright notices, the licence text, notices
   of modification, written offers, the component list. The set is called the compliance log book in the
   source; call it what you like but keep it per release.
5. **Where a licence requires text, include the text.** The source notes that a licence may require its text and
   not just a link, and says it prefers to include the whole text even when part would be enough. Whether a
   link is acceptable for a given licence is counsel's call.
6. **Publish where the way of delivery calls for it.** The source publishes the bundle online where the mode of
   distribution requires. For a hosted-only product the distribution artifacts may not apply, and this is for
   counsel to decide (own guidance).
7. **Keep the bundles of past releases.** The source retains artifacts for earlier releases; how long is a
   decision for the owner and counsel, not a number to copy.
8. **Name the missing piece when a release lacks one.** If a release has no component list or no bundle, record
   that as a gap in the decision log with the release and the owner, and do not backfill silently.
