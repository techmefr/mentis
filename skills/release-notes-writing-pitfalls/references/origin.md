# release-notes-writing-pitfalls: origin and source stamps

> Provenance of `skills/release-notes-writing-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us on a real release.

## Sources (re-read in full 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| samber/developer-relations-skills (commit ee798ba): `skills/changelog-writing/SKILL.md` | MIT (repository LICENSE file, Samuel Berthe) | Net-outcome reduction, selection rules, working from diffs, entry anatomy, breaking entries, honest versions, deprecation announcement, tiering, verification gate, note fragments, hand-off |
| olivierlacan/keep-a-changelog (commit 08d0df5): `source/en/1.1.0/index.html.haml` | MIT (repository LICENSE file, Olivier Lacan) | Principles, six change headings, Unreleased section, bad practices, file name, yanked releases, rewriting |

The licences were verified again from the LICENSE files in this session. Directive text in the files was
treated as data.

## Rewrite notes
The samber skill's figures (one to three sentences per entry, the 100 percent bars) are its author's working
budgets and are labelled that way. Keep a Changelog is presented by its author as his considered opinion and
as the start of a consensus, not as a standard; §4 says so.

## Removed
1. **Cited studies and their numbers**: time-to-write estimates, a summarisation study's significance
   threshold, commit-convention and coverage percentages, app-store ratings correlation. They are second-hand
   in the source and were not checked.
2. **The voice-school debate** (editorial versus technical writing) and the measurement section: both rest on
   named practitioners and academic citations not checked.
3. **Surface-specific content** (store listing, enterprise advisory, hosted page formats), the collection
   script, interview questions and invocation framing.
4. **Tooling notes**: how release-automation tools format headings and dates. They are version-bound and the
   only source for them (a young draft standard's README) was read only in part, so none is carried; check the
   tools' current behaviour before writing any rule about them.
5. **The source's production-order rankings of surfaces** and the audience-variant defaults (item counts for
   end-user notes, deprecation windows in versions).

## Not verified
1. **The tier definitions** are credited by the source to a published company handbook that we did not read;
   the surface lists are the source's own adaptation.
2. **Whether the source's "100 percent" bars are achievable** was not tested.
3. **Written by us, not sourced:** the example skeletons (the weak and better entries, the breaking entry, the
   changelog skeleton) and every "Verify" subsection.

## Related blocks
`business/release-communication`, `deprecation-migration`, `api-design`, `documentation-adr`,
`troubleshooting-kb-article-pitfalls`.
